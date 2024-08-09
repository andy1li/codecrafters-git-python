import os
import zlib
from os import path

from app.utils import hash_bytes
from git.blob import Blob


def git_hash_object(filename: str):
    with open(filename, 'rb') as f:
        raw_bytes = f.read()
        blob_bytes = Blob.serialize(raw_bytes)
        sha = hash_bytes(blob_bytes)

    folder, file = sha[:2], sha[2:]
    folderpath = path.join('.git', 'objects', folder)
    if not path.exists(folderpath):
        os.makedirs(folderpath)
    filepath = path.join(folderpath, file)
    with open(filepath, 'wb') as f:
        compressed_bytes = zlib.compress(blob_bytes)
        f.write(compressed_bytes)
    return sha
