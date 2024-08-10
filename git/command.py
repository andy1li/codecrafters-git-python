import os

from git.argparser import parse_arguments
from git.blob import Blob
from git.object import Object
from git.tree import Tree


def git_init():
    os.mkdir('.git')
    os.mkdir('.git/objects')
    os.mkdir('.git/refs')
    with open('.git/HEAD', 'w') as f:
        f.write('ref: refs/heads/main\n')
    print('Initialized git directory')


def execute_command():
    args = parse_arguments()

    match args.command:
        case 'init':
            git_init()
        case 'cat-file':
            blob = Object.from_sha(args.blob_sha)
            if args.pretty_print:
                print(blob.content.decode(), end='')
        case 'hash-object':
            blob = Blob.from_file(args.filename)
            if args.write:
                blob.write()
            print(blob.sha, end='')
        case 'ls-tree':
            tree = Tree.from_sha(args.tree_sha)
            if args.name_only:
                tree.print_entry_names()
        case 'write-tree':
            tree = Tree.from_path('.')
            print(tree.sha, end='')
        case _:
            raise RuntimeError(f'Unknown command #{args.command}')
