import hashlib
from os import path


def hash_bytes(data: bytes):
    return hashlib.sha1(data).hexdigest()


def split_sha(sha: str):
    assert len(sha) == 40
    return sha[:2], sha[2:]


def sha_to_path(sha: str):
    folder, file = split_sha(sha)
    return path.join('.git', 'objects', folder, file)


def pick_size(header: bytes) -> int:
    return int(header.split(b' ')[-1].decode())


def read_until_zero(stream) -> bytes:
    result = b''
    while True:
        c = stream.read(1)
        if c == b'':
            raise EOFError
        if c == b'\0':
            return result
        result += c
    raise ValueError
