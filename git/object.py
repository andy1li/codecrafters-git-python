import zlib
from typing import NamedTuple

from app.utils import hash_bytes, sha_to_bytes, sha_to_path


class Object(NamedTuple):
    type: bytes
    size: int
    content: bytes

    @staticmethod
    def from_bytes(object_bytes: bytes) -> 'Object':
        header, _, content = object_bytes.partition(b'\0')
        type, size_bytes = header.split(b' ')
        size = int(size_bytes.decode())
        assert size == len(content)
        return Object(type, size, content)

    @staticmethod
    def from_sha(sha: str) -> 'Object':
        object_bytes = sha_to_bytes(sha)
        return Object.from_bytes(object_bytes)

    @property
    def sha(self) -> str:
        object_bytes = self.to_bytes()
        return hash_bytes(object_bytes)

    def print_sha(self):
        print(self.sha, end='')

    def to_bytes(self) -> bytes:
        assert self.size == len(self.content)
        size_bytes = str(self.size).encode()
        return self.type + b' ' + size_bytes + b'\0' + self.content

    def write(self):
        file_path = sha_to_path(self.sha)
        with open(file_path, 'wb') as f:
            object_bytes = self.to_bytes()
            compressed_bytes = zlib.compress(object_bytes)
            f.write(compressed_bytes)
