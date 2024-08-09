from typing import NamedTuple

from app.utils import pick_size


class Blob(NamedTuple):
    size: int
    content: bytes

    @classmethod
    def parse(cls, blob_bytes: bytes) -> 'Blob':
        header, _, content = blob_bytes.partition(b'\0')
        size = pick_size(header)

        assert size == len(content)
        return cls(size, content)

    @staticmethod
    def serialize(content: bytes):
        size = len(content)
        return b'blob ' + str(size).encode() + b'\0' + content

    def print(self):
        print(self.content.decode(), end='')
