import os
from binascii import unhexlify
from io import BytesIO
from os import path
from typing import Iterable, NamedTuple

from app.utils import read_until_zero
from git.blob import Blob
from git.object import Object

TreeEntries = Iterable['TreeEntry']


class TreeEntry(NamedTuple):
    mode: bytes
    name: bytes
    sha: bytes

    @staticmethod
    def from_file(filename: str) -> 'TreeEntry':
        blob = Blob.from_file(filename)
        basename = path.basename(filename)
        return TreeEntry(b'100644', basename.encode(), unhexlify(blob.sha))

    @staticmethod
    def from_tree(tree: 'Tree', pathname: str) -> 'TreeEntry':
        basename = path.basename(pathname)
        return TreeEntry(b'40000', basename.encode(), unhexlify(tree.sha))

    @staticmethod
    def from_stream(stream: BytesIO) -> 'TreeEntry':
        mode, name = read_until_zero(stream).split(b' ')
        sha = stream.read(20)
        return TreeEntry(mode, name, sha)

    @staticmethod
    def many_from_stream(stream: BytesIO) -> TreeEntries:
        while True:
            try:
                yield TreeEntry.from_stream(stream)
            except EOFError:
                return

    @staticmethod
    def many_from_path(pathname) -> TreeEntries:
        for filename in os.listdir(pathname):
            filename = path.join(pathname, filename).removeprefix('./')

            if path.basename(filename) == '.git':
                continue

            if path.isdir(filename):
                tree = Tree.from_path(filename)
                yield TreeEntry.from_tree(tree, filename)

            if path.isfile(filename):
                yield TreeEntry.from_file(filename)

    def to_bytes(self):
        return self.mode + b' ' + self.name + b'\0' + self.sha


class Tree(Object):
    @staticmethod
    def from_entries(entries: TreeEntries) -> 'Tree':
        entries_sorted = sorted(entries, key=lambda e: e.name)
        content = b''.join(e.to_bytes() for e in entries_sorted)
        return Tree(b'tree', len(content), content)

    @staticmethod
    def from_path(pathname='.') -> 'Tree':
        entries = TreeEntry.many_from_path(pathname)
        return Tree.from_entries(entries)

    @staticmethod
    def from_sha(sha: str) -> 'Tree':
        object = Object.from_sha(sha)
        assert object.type == b'tree'
        return Tree(*object)

    @property
    def entries(self) -> TreeEntries:
        content_stream = BytesIO(self.content)
        return TreeEntry.many_from_stream(content_stream)

    def print_entry_names(self):
        for e in self.entries:
            print(e.name.decode())
