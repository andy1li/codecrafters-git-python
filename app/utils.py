import hashlib
import os
import zlib
from io import BytesIO
from os import path


def hash_bytes(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def read_until_zero(stream: BytesIO) -> bytes:
    result = b''
    while True:
        c = stream.read(1)
        if c == b'':
            raise EOFError
        if c == b'\0':
            return result
        result += c


def sha_to_path(sha: str) -> str:
    """
    Convert sha to path, and create directory if not exists
    """
    folder, file = split_sha(sha)
    folder_path = path.join('.git', 'objects', folder)
    os.makedirs(folder_path, exist_ok=True)
    return path.join(folder_path, file)


def sha_to_bytes(sha: str) -> bytes:
    file_path = sha_to_path(sha)
    with open(file_path, 'rb') as f:
        return zlib.decompress(f.read())


def split_sha(sha: str) -> tuple[str, str]:
    assert len(sha) == 40
    return sha[:2], sha[2:]
