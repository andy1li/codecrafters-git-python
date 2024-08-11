import os

from git.argparser import parse_arguments
from git.blob import Blob
from git.commit import Commit
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
            blob = Blob.from_sha(args.blob_sha)
            if args.pretty_print:
                print(blob.content.decode(), end='')

        case 'hash-object':
            blob = Blob.from_file(args.filename)
            if args.write:
                blob.write()
            blob.print_sha()

        case 'ls-tree':
            tree = Tree.from_sha(args.tree_sha)
            if args.name_only:
                tree.print_entry_names()

        case 'write-tree':
            tree = Tree.from_path('.')
            tree.write()
            tree.print_sha()

        case 'commit-tree':
            commit = Commit.from_args(args)
            commit.write()
            commit.print_sha()

        case 'clone':
            print(args)
