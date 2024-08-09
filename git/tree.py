import os
from binascii import unhexlify
from io import BytesIO
from os import path
from typing import NamedTuple

from app.utils import pick_size, read_until_zero
from git.git_hash_object import git_hash_object


def traverse(current_path):
    return tuple(
        Entry.parse_from_path(current_path, filename)
        for filename in os.listdir(current_path)
        if filename != '.git'
    )


class Entry(NamedTuple):
    mode: bytes
    name: bytes
    sha: bytes

    @classmethod
    def parse(cls, stream: BytesIO) -> 'Entry':
        mode, name = read_until_zero(stream).split(b' ')
        sha = stream.read(20)
        return cls(mode, name, sha)

    @staticmethod
    def parse_entries(stream: BytesIO) -> tuple['Entry', ...]:
        entires = []
        while True:
            try:
                entry = Entry.parse(stream)
                entires.append(entry)
            except EOFError:
                return tuple(entires)

    @classmethod
    def parse_from_path(cls, current_path: str, filename: str) -> 'Entry':
        filename = path.join(current_path, filename)

        if path.isdir(filename):
            tree = Tree.parse_from_path(filename)
            return tree.to_entry()

        if path.isfile(filename):
            filename = filename.lstrip('./')
            sha_40 = git_hash_object(filename)
            sha_20 = unhexlify(sha_40)
            return Entry(b'100644', filename.encode(), sha_20)

        print(filename, path.isdir(filename), path.isfile(filename))

        raise ValueError

    def serialize(self):
        return self.mode + b' ' + self.name + b'\0' + self.sha


class Tree(NamedTuple):
    name: bytes
    entries: tuple[Entry, ...]

    @classmethod
    def parse_from_bytes(cls, tree_bytes: bytes) -> 'Tree':
        header, _, content = tree_bytes.partition(b'\0')
        size = pick_size(header)
        assert size == len(content)

        content_stream = BytesIO(content)
        entries = Entry.parse_entries(content_stream)

        # TODO: Need to fix
        return cls(b'', entries)

    @staticmethod
    def parse_from_path(current_path='.') -> 'Tree':
        return Tree(current_path, traverse(current_path))

    def to_entry(self):
        self.serialize()
        return Entry(b'040000', self.name.encode(), b'tree')

    def serialize(self):
        print('serialize show entries:')
        for e in self.entries:
            print('e:', type(e), e)

        content = b''.join(e.serialize() for e in self.entries)
        print('content:', content)
