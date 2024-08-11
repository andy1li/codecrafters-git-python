from argparse import Namespace
from textwrap import dedent

from git.object import Object

AUTHOR = 'author Andy Li <1450947+andy1li@users.noreply.github.com> 1723305607 +0800'
COMMITER = (
    'committer Andy Li <1450947+andy1li@users.noreply.github.com> 1723305607 +0800'
)


class Commit(Object):
    @staticmethod
    def from_args(args: Namespace):
        content = f"""\
            tree {args.tree_sha}'
            parent {args.commit_sha}
            {AUTHOR}
            {COMMITER}

            {args.message}
            """
        content_bytes = dedent(content).encode()
        return Commit(b'commit', len(content_bytes), content_bytes)
