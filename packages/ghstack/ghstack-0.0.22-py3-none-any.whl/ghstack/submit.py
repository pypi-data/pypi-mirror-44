#!/usr/bin/env python3

import re
import ghstack
import ghstack.git
import ghstack.shell
import ghstack.github
import ghstack.logging
from ghstack.typing import GitHubNumber, GitHubRepositoryId, GhNumber
from typing import List, Union, Optional, NamedTuple, Tuple, Set
from ghstack.git import GitCommitHash, GitTreeHash
from typing_extensions import Literal
import logging

BranchKind = Union[Literal['base'], Literal['head'], Literal['orig']]

DiffMeta = NamedTuple('DiffMeta', [
    ('title', str),
    ('number', GitHubNumber),
    ('body', str),
    ('ghnum', GhNumber),
    ('push_branches', Tuple[Tuple[GitCommitHash, BranchKind], ...]),
    ('what', str),
    ('closed', bool),
])


RE_STACK = re.compile(r'Stack.*:\n(\* [^\n]+\n)+')


RE_DIFF_REV = re.compile(r'^Differential Revision:.+?(D[0-9]+)', re.MULTILINE)


# repo layout:
#   - gh/username/23/base -- what we think GitHub's current tip for commit is
#   - gh/username/23/head -- what we think base commit for commit is
#   - gh/username/23/orig -- the "clean" commit history, i.e., what we're
#                      rebasing, what you'd like to cherry-pick (???)
#                      (Maybe this isn't necessary, because you can
#                      get the "whole" diff from GitHub?  What about
#                      commit description?)


def branch(username: str, ghnum: GhNumber, kind: BranchKind
           ) -> GitCommitHash:
    return GitCommitHash("gh/{}/{}/{}".format(username, ghnum, kind))


def branch_base(username: str, ghnum: GhNumber) -> GitCommitHash:
    return branch(username, ghnum, "base")


def branch_head(username: str, ghnum: GhNumber) -> GitCommitHash:
    return branch(username, ghnum, "head")


def branch_orig(username: str, ghnum: GhNumber) -> GitCommitHash:
    return branch(username, ghnum, "orig")


STACK_HEADER = "Stack from [ghstack](https://github.com/ezyang/ghstack)"


def main(msg: Optional[str],
         username: str,
         github: ghstack.github.GitHubEndpoint,
         update_fields: bool = False,
         sh: Optional[ghstack.shell.Shell] = None,
         stack_header: str = STACK_HEADER,
         repo_owner: Optional[str] = None,
         repo_name: Optional[str] = None,
         ) -> List[DiffMeta]:

    if sh is None:
        # Use CWD
        sh = ghstack.shell.Shell()

    if repo_owner is None or repo_name is None:
        # Grovel in remotes to figure it out
        origin_url = sh.git("remote", "get-url", "origin")
        while True:
            m = re.match(r'^git@github.com:([^/]+)/([^.]+)(?:\.git)?$', origin_url)
            if m:
                repo_owner_nonopt = m.group(1)
                repo_name_nonopt = m.group(2)
                break
            m = re.search(r'github.com/([^/]+)/([^.]+)', origin_url)
            if m:
                repo_owner_nonopt = m.group(1)
                repo_name_nonopt = m.group(2)
                break
            raise RuntimeError(
                "Couldn't determine repo owner and name from url: {}"
                .format(origin_url))
    else:
        repo_owner_nonopt = repo_owner
        repo_name_nonopt = repo_name

    # TODO: Cache this guy
    repo = github.graphql(
        """
        query ($owner: String!, $name: String!) {
            repository(name: $name, owner: $owner) {
                id
                isFork
            }
        }""",
        owner=repo_owner_nonopt,
        name=repo_name_nonopt)["data"]["repository"]

    if repo["isFork"]:
        raise RuntimeError(
            "Cowardly refusing to upload diffs to a repository that is a "
            "fork.  ghstack expects 'origin' of your Git checkout to point "
            "to the upstream repository in question.  If your checkout does "
            "not comply, please adjust your remotes (by editing .git/config) "
            "to make it so.  If this message is in error, please register "
            "your complaint on GitHub issues (or edit this line to delete "
            "the check above.")
    repo_id = repo["id"]

    sh.git("fetch", "origin")
    base = GitCommitHash(sh.git("merge-base", "origin/master", "HEAD"))

    # compute the stack of commits to process (reverse chronological order),
    # INCLUDING the base commit
    stack = ghstack.git.split_header(
        sh.git("rev-list", "--header", "^" + base + "^@", "HEAD"))

    assert len(stack) > 0

    ghstack.logging.record_status(
        "{} \"{}\"".format(stack[0].commit_id()[:9], stack[0].title()))

    # start with the earliest commit
    g = reversed(stack)
    base_obj = next(g)

    submitter = Submitter(github=github,
                          sh=sh,
                          username=username,
                          repo_owner=repo_owner_nonopt,
                          repo_name=repo_name_nonopt,
                          repo_id=repo_id,
                          base_commit=base,
                          base_tree=base_obj.tree(),
                          stack_header=stack_header,
                          update_fields=update_fields,
                          msg=msg)

    for s in g:
        submitter.process_commit(s)
    submitter.post_process()

    # NB: earliest first
    return submitter.stack_meta


def all_branches(username: str, ghnum: GhNumber) -> Tuple[str, str, str]:
    return (branch_base(username, ghnum),
            branch_head(username, ghnum),
            branch_orig(username, ghnum))


def push_spec(commit: GitCommitHash, branch: str) -> str:
    return "{}:refs/heads/{}".format(commit, branch)


class Submitter(object):
    # Endpoint to access GitHub
    github: ghstack.github.GitHubEndpoint

    # Shell inside git checkout that we are submitting
    sh: ghstack.shell.Shell

    # GitHub username who is doing the submitting
    username: str

    # Owner of the repository we are submitting to.  Usually 'pytorch'
    repo_owner: str

    # Name of the repository we are submitting to.  Usually 'pytorch'
    repo_name: str

    # GraphQL ID of the repository
    repo_id: GitHubRepositoryId

    # The base commit of the next diff we are submitting
    base_commit: GitCommitHash

    # The base tree of the next diff we are submitting
    base_tree: GitTreeHash

    # Message describing the update to the stack that was done
    msg: Optional[str]

    # Description of all the diffs we submitted; to be populated
    # by Submitter.
    stack_meta: List[DiffMeta]

    # Set of seen ghnums
    seen_ghnums: Set[GhNumber]

    # String used to describe the stack in question
    stack_header: str

    # Clobber existing PR description with local commit message
    update_fields: bool

    def __init__(
            self,
            github: ghstack.github.GitHubEndpoint,
            sh: ghstack.shell.Shell,
            username: str,
            repo_owner: str,
            repo_name: str,
            repo_id: GitHubRepositoryId,
            base_commit: GitCommitHash,
            base_tree: GitTreeHash,
            stack_header: str,
            update_fields: bool,
            msg: Optional[str]):
        self.github = github
        self.sh = sh
        self.username = username
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_id = repo_id
        self.base_commit = base_commit
        self.base_orig = base_commit
        self.base_tree = base_tree
        self.update_fields = update_fields
        self.stack_header = stack_header
        self.stack_meta = []
        self.seen_ghnums = set()
        self.msg = msg

    def _default_title_and_body(self, commit: ghstack.git.CommitHeader,
                                old_pr_body: Optional[str]
                                ) -> Tuple[str, str]:
        title = commit.title()
        extra = ''
        if old_pr_body is not None:
            # Look for tags we should preserve, and keep them
            m = RE_DIFF_REV.search(old_pr_body)
            if m:
                extra = (
                    "\n\nDifferential Revision: "
                    "[{phabdiff}]"
                    "(https://our.internmc.facebook.com/intern/diff/{phabdiff})"
                ).format(phabdiff=m.group(1))
        pr_body = (
            "{}:\n* (to be filled)\n\n{}{}"
            .format(self.stack_header,
                    ''.join(commit.commit_msg().splitlines(True)[1:]).lstrip(),
                    extra)
        )
        return title, pr_body

    def process_commit(self, commit: ghstack.git.CommitHeader) -> None:
        title, pr_body = self._default_title_and_body(commit, None)
        commit_id = commit.commit_id()
        tree = commit.tree()
        parents = commit.parents()
        new_orig = commit_id
        author = commit.author()

        logging.info("# Processing {} {}".format(commit_id[:9], title))
        logging.info("Authored by {}".format(author))
        logging.info("Base is {}".format(self.base_commit))

        if len(parents) != 1:
            raise RuntimeError(
                "The commit {} has {} parents, which makes my head explode.  "
                "`git rebase -i` your diffs into a stack, then try again."
                .format(commit_id, len(parents)))
        parent = parents[0]

        # TODO: check if we authored the commit.  We don't touch shit we didn't
        # create.

        commit_msg = commit.commit_msg()

        # check if the commit message says what pull request it's associated
        # with
        #   If NONE:
        #       - If possible, allocate ourselves a pull request number and
        #         then fix the branch afterwards.
        #       - Otherwise, generate a unique branch name, and attach it to
        #         the commit message

        m_metadata = commit.match_metadata()
        if m_metadata is None:
            # Determine the next available UUID.  We do this by
            # iterating through known branches and keeping track
            # of the max.  The next available UUID is the next number.
            # This is technically subject to a race, but we assume
            # end user is not running this script concurrently on
            # multiple machines (you bad bad)
            refs = self.sh.git(
                "for-each-ref",
                "refs/remotes/origin/gh/{}".format(self.username),
                "--format=%(refname)").split()
            max_ref_num = max(int(ref.split('/')[-2]) for ref in refs) \
                if refs else 0
            ghnum = GhNumber(str(max_ref_num + 1))
            assert ghnum not in self.seen_ghnums
            self.seen_ghnums.add(ghnum)

            # Create the incremental pull request diff
            new_pull = GitCommitHash(
                self.sh.git("commit-tree", tree,
                            "-p", self.base_commit,
                            input=commit_msg))

            # Push the branches, so that we can create a PR for them
            new_branches = (
                push_spec(new_pull, branch_head(self.username, ghnum)),
                push_spec(self.base_commit, branch_base(self.username, ghnum))
            )
            self.sh.git(
                "push",
                "origin",
                *new_branches,
            )
            self.github.push_hook(new_branches)

            # Time to open the PR
            # NB: GraphQL API does not support opening PRs
            r = self.github.post(
                "repos/{owner}/{repo}/pulls"
                .format(owner=self.repo_owner, repo=self.repo_name),
                title=title,
                head=branch_head(self.username, ghnum),
                base=branch_base(self.username, ghnum),
                body=pr_body,
                maintainer_can_modify=True,
            )
            number = r['number']

            logging.info("Opened PR #{}".format(number))

            # Update the commit message of the local diff with metadata
            # so we can correlate these later
            commit_msg = ("{commit_msg}\n\n"
                          "gh-metadata: "
                          "{owner} {repo} {number} {branch_head}"
                          .format(commit_msg=commit_msg.rstrip(),
                                  owner=self.repo_owner,
                                  repo=self.repo_name,
                                  number=number,
                                  branch_head=branch_head(self.username,
                                                          ghnum)))

            # TODO: Try harder to preserve the old author/commit
            # information (is it really necessary? Check what
            # --amend does...)
            new_orig = GitCommitHash(self.sh.git(
                "commit-tree",
                tree,
                "-p", self.base_orig,
                input=commit_msg))

            self.stack_meta.append(DiffMeta(
                title=title,
                number=number,
                body=pr_body,
                ghnum=ghnum,
                push_branches=((new_orig, 'orig'), ),
                what='Created',
                closed=False,
            ))

        else:
            if m_metadata.group("username") != self.username:
                # This is someone else's diff
                raise RuntimeError(
                    "cannot handle stack from diffs of other people yet")

            ghnum = GhNumber(m_metadata.group("ghnum"))
            number = int(m_metadata.group("number"))

            if ghnum in self.seen_ghnums:
                raise RuntimeError(
                    "Something very strange has happened: a commit for "
                    "the pull request #{} occurs twice in your local "
                    "commit stack.  This is usually because of a botched "
                    "rebase.  Please take a look at your git log and seek "
                    "help from your local Git expert.".format(number))
            self.seen_ghnums.add(ghnum)

            # TODO: There is no reason to do a node query here; we can
            # just look up the repo the old fashioned way
            r = self.github.graphql("""
              query ($repo_id: ID!, $number: Int!) {
                node(id: $repo_id) {
                  ... on Repository {
                    pullRequest(number: $number) {
                      id
                      body
                      title
                      closed
                    }
                  }
                }
              }
            """, repo_id=self.repo_id, number=number)["data"]["node"]["pullRequest"]
            pr_body = r["body"]
            # NB: Technically, we don't need to pull this information at
            # all, but it's more convenient to unconditionally edit
            # title in the code below
            # NB: This overrides setting of title previously, from the
            # commit message.
            title = r["title"]
            closed = r["closed"]

            if self.update_fields:
                title, pr_body = self._default_title_and_body(commit, pr_body)

            # Check if updating is needed
            clean_commit_id = GitCommitHash(self.sh.git(
                "rev-parse",
                GitCommitHash("origin/" + branch_orig(self.username, ghnum))
            ))
            push_branches: Tuple[Tuple[GitCommitHash, BranchKind], ...]
            if clean_commit_id == commit_id:
                logging.info("Nothing to do")
                # NB: NOT commit_id, that's the orig commit!
                new_pull = GitCommitHash("origin/" + branch_head(self.username, ghnum))
                push_branches = ()
            else:
                logging.info("Pushing to #{}".format(number))

                # We've got an update to do!  But what exactly should we
                # do?
                #
                # Here are a number of situations which may have
                # occurred.
                #
                #   1. None of the parent commits changed, and this is
                #      the first change we need to push an update to.
                #
                #   2. A parent commit changed, so we need to restack
                #      this commit too.  (You can't easily tell distinguish
                #      between rebase versus rebase+amend)
                #
                #   3. The parent is now master (any prior parent
                #      commits were absorbed into master.)
                #
                #   4. The parent is totally disconnected, the history
                #      is bogus but at least the merge-base on master
                #      is the same or later.  (You cherry-picked a
                #      commit out of an old stack and want to make it
                #      independent.)
                #
                # In cases 1-3, we can maintain a clean merge history
                # if we do a little extra book-keeping, so we do
                # precisely this.
                #
                #   - In cases 1 and 2, we'd like to use the newly
                #     created gh/ezyang/$PARENT/head which is recorded
                #     in self.base_commit, because it's exactly the
                #     correct base commit to base our diff off of.
                #

                # First, check if gh/ezyang/1/head is equal
                # to gh/ezyang/2/base.
                # We don't need to update base, nor do we need an extra
                # merge base.  (--is-ancestor check here is acceptable,
                # because the base_commit in our stack could not have
                # gone backwards)
                base_args: Tuple[str, ...]
                if self.sh.git(
                        "merge-base",
                        "--is-ancestor", self.base_commit,
                        "origin/" + branch_base(self.username, ghnum), exitcode=True):

                    new_base = self.base_commit
                    base_args = ()

                else:
                    # Second, check if gh/ezyang/2/base is an ancestor
                    # of gh/ezyang/1/head.  If it is, we'll do a merge,
                    # but we don't need to create a synthetic base
                    # commit.
                    is_ancestor = self.sh.git(
                        "merge-base",
                        "--is-ancestor", "origin/" + branch_base(self.username, ghnum),
                        self.base_commit, exitcode=True)
                    if is_ancestor:

                        new_base = self.base_commit

                    else:
                        # Our base changed in a strange way, and we are
                        # now obligated to create a synthetic base
                        # commit.
                        new_base = GitCommitHash(self.sh.git(
                            "commit-tree", self.base_tree,
                            "-p", "origin/" + branch_base(self.username, ghnum),
                            "-p", self.base_commit,
                            input='Update base for {} on "{}"\n\n{}'
                                  .format(self.msg, title, commit_msg)))
                    base_args = ("-p", new_base)

                #   - Directly blast our current tree as the newest entry of
                #   pull, merging against the previous pull entry, and the
                #   newest base.

                tree = commit.tree()
                new_pull = GitCommitHash(self.sh.git(
                    "commit-tree", tree,
                    "-p", "origin/" + branch_head(self.username, ghnum),
                    *base_args,
                    input='{} on "{}"\n\n{}'.format(self.msg, title, commit_msg)))

                # History reedit!  Commit message changes only
                if parent != self.base_orig:
                    logging.info("Restacking commit on {}".format(self.base_orig))
                    new_orig = GitCommitHash(self.sh.git(
                        "commit-tree", tree,
                        "-p", self.base_orig, input=commit_msg))

                push_branches = (
                    (new_base, "base"),
                    (new_pull, "head"),
                    (new_orig, "orig"),
                )

            if closed:
                what = 'Skipped closed'
            elif push_branches:
                what = 'Updated'
            else:
                what = 'Skipped'

            self.stack_meta.append(DiffMeta(
                title=title,
                number=number,
                # NB: Ignore the commit message, and just reuse the old commit
                # message.  This is consistent with 'jf submit' default
                # behavior.  The idea is that people may have edited the
                # PR description on GitHub and you don't want to clobber
                # it.
                body=pr_body,
                ghnum=ghnum,
                push_branches=push_branches,
                what=what,
                closed=closed,
            ))

        # The current pull request head commit, is the new base commit
        self.base_commit = new_pull
        self.base_orig = new_orig
        self.base_tree = tree
        logging.debug("base_commit = {}".format(self.base_commit))
        logging.debug("base_orig = {}".format(self.base_orig))
        logging.debug("base_tree = {}".format(self.base_tree))

    def _format_stack(self, index: int) -> str:
        rows = []
        for i, s in reversed(list(enumerate(self.stack_meta))):
            if index == i:
                rows.append('* **#{} {}**'.format(s.number, s.title.strip()))
            else:
                rows.append('* #{} {}'.format(s.number, s.title.strip()))
        return self.stack_header + ':\n' + '\n'.join(rows) + '\n'

    def post_process(self) -> None:
        # fix the HEAD pointer
        self.sh.git("reset", "--soft", self.base_orig)

        # update pull request information, update bases as necessary
        #   preferably do this in one network call
        # push your commits (be sure to do this AFTER you update bases)
        base_push_branches: List[str] = []
        push_branches: List[str] = []
        force_push_branches: List[str] = []
        for i, s in enumerate(self.stack_meta):
            # NB: GraphQL API does not support modifying PRs
            if not s.closed:
                logging.info(
                    "# Updating https://github.com/{owner}/{repo}/pull/{number}"
                    .format(owner=self.repo_owner,
                            repo=self.repo_name,
                            number=s.number))
                self.github.patch(
                    "repos/{owner}/{repo}/pulls/{number}"
                    .format(owner=self.repo_owner, repo=self.repo_name,
                            number=s.number),
                    body=RE_STACK.sub(self._format_stack(i), s.body),
                    title=s.title)
            else:
                logging.info(
                    "# Skipping closed https://github.com/{owner}/{repo}/pull/{number}"
                    .format(owner=self.repo_owner,
                            repo=self.repo_name,
                            number=s.number))

            # It is VERY important that we do base updates BEFORE real
            # head updates, otherwise GitHub will spuriously think that
            # the user pushed a number of patches as part of the PR,
            # when actually they were just from the (new) upstream
            # branch

            for commit, b in s.push_branches:
                if b == 'orig':
                    q = force_push_branches
                elif b == 'base':
                    q = base_push_branches
                else:
                    q = push_branches
                q.append(push_spec(commit, branch(self.username, s.ghnum, b)))
        # Careful!  Don't push master.
        # TODO: These pushes need to be atomic (somehow)
        if base_push_branches:
            self.sh.git("push", "origin", *base_push_branches)
            self.github.push_hook(base_push_branches)
        if push_branches:
            self.sh.git("push", "origin", *push_branches)
            self.github.push_hook(push_branches)
        if force_push_branches:
            self.sh.git("push", "origin", "--force", *force_push_branches)
            self.github.push_hook(force_push_branches)

        # Report what happened
        print()
        print('# Summary of changes (ghstack {})'.format(ghstack.__version__))
        print()
        for s in self.stack_meta:
            url = ("https://github.com/{owner}/{repo}/pull/{number}"
                   .format(owner=self.repo_owner,
                           repo=self.repo_name,
                           number=s.number))
            print(" - {} {}".format(s.what, url))
        print()
        print("Facebook employees can import your changes by running ")
        print("(on a Facebook machine):")
        print()
        print("    ghimport -s {}".format(url))
        print()
        print("If you want to work on this diff stack on another machine,")
        print("run these commands inside a valid Git checkout:")
        print()
        print("     git fetch origin")
        print("     git checkout {}"
              .format(branch_orig(self.username, s.ghnum)))
        print("")
