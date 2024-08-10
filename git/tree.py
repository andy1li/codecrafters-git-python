import os
from binascii import unhexlify
from io import BytesIO
from os import path
from typing import Iterable, NamedTuple

from app.utils import read_until_zero
from git.blob import Blob
from git.object import Object


class TreeEntry(NamedTuple):
    mode: bytes
    name: bytes
    sha: bytes

    @staticmethod
    def from_file(filename: str) -> 'TreeEntry':
        blob = Blob.from_file(filename)
        basename = path.basename(path.normpath(filename))
        return TreeEntry(b'100644', basename.encode(), unhexlify(blob.sha))

    @staticmethod
    def from_tree(tree: 'Tree', pathname: str) -> 'TreeEntry':
        basename = path.basename(path.normpath(pathname))
        return TreeEntry(b'40000', basename.encode(), unhexlify(tree.sha))

    @staticmethod
    def parse_one(stream: BytesIO) -> 'TreeEntry':
        mode, name = read_until_zero(stream).split(b' ')
        sha = stream.read(20)
        return TreeEntry(mode, name, sha)

    @staticmethod
    def parse_many(stream: BytesIO) -> tuple['TreeEntry', ...]:
        entires = []
        while True:
            try:
                entry = TreeEntry.parse_one(stream)
                entires.append(entry)
            except EOFError:
                return tuple(entires)

    def to_bytes(self):
        return self.mode + b' ' + self.name + b'\0' + self.sha


TreeEntries = Iterable[TreeEntry]


class Tree(Object):
    @staticmethod
    def from_entries(entries: TreeEntries) -> 'Tree':
        entries_sorted = sorted(entries, key=lambda e: e.name)
        content = b''.join(e.to_bytes() for e in entries_sorted)
        return Tree(b'tree', len(content), content)

    @staticmethod
    def from_sha(sha: str) -> 'Tree':
        object = Object.from_sha(sha)
        assert object.type == b'tree'
        return Tree(*object)

    @staticmethod
    def from_path(pathname='.') -> 'Tree':
        entries = []
        for filename in os.listdir(pathname):
            filename = path.join(pathname, filename).removeprefix('./')

            if filename == '.git':
                continue

            if path.isdir(filename):
                tree = Tree.from_path(filename)
                entry = TreeEntry.from_tree(tree, filename)

            if path.isfile(filename):
                entry = TreeEntry.from_file(filename)

            entries.append(entry)

        tree = Tree.from_entries(entries)
        tree.write()
        return tree

    @property
    def entries(self) -> TreeEntries:
        content_stream = BytesIO(self.content)
        return TreeEntry.parse_many(content_stream)

    def print_entry_names(self):
        for e in self.entries:
            print(e.name.decode())
