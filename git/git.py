import os
import zlib
from os import path

from app.utils import sha_to_path
from git.blob import Blob
from git.tree import Tree


def git_init():
    os.mkdir('.git')
    os.mkdir('.git/objects')
    os.mkdir('.git/refs')
    with open('.git/HEAD', 'w') as f:
        f.write('ref: refs/heads/main\n')
    print('Initialized git directory')


def git_cat_file(sha: str):
    filepath = sha_to_path(sha)
    if path.exists(filepath):
        with open(filepath, 'rb') as blob_file:
            blob_bytes = zlib.decompress(blob_file.read())
            blob = Blob.parse(blob_bytes)
            blob.print()


def git_ls_tree(tree_sha: str):
    filepath = sha_to_path(tree_sha)
    with open(filepath, 'rb') as f:
        tree_bytes = zlib.decompress(f.read())
        tree = Tree.parse_from_bytes(tree_bytes)

    for e in tree.entries:
        print(e.name.decode())


def git_write_tree():
    tree = Tree.parse_from_path()
    print(*tree.entries, sep='\n\n')
