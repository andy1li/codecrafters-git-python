from argparse import ArgumentParser

from git.git import *
from git.git_hash_object import git_hash_object


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_init = subparsers.add_parser(
        'init', help='Create an empty Git repository or reinitialize an existing one'
    )

    parser_cat_file = subparsers.add_parser(
        'cat-file',
        help='Provide content or type and size information for repository objects',
    )
    parser_cat_file.add_argument('-p', dest='object')

    parser_hash_object = subparsers.add_parser(
        'hash-object',
        help='Compute object ID and optionally creates a blob from a file',
    )
    parser_hash_object.add_argument('-w', dest='filename')

    parser_ls_tree = subparsers.add_parser(
        'ls-tree',
        help='List the contents of a tree object',
    )
    parser_ls_tree.add_argument('--name-only', dest='tree_sha')

    parser_write_tree = subparsers.add_parser(
        'write-tree',
        help='Create a tree object from the current index',
    )

    args = parser.parse_args()

    match args.command:
        case 'init':
            git_init()
        case 'cat-file':
            git_cat_file(args.object)
        case 'hash-object':
            sha = git_hash_object(args.filename)
            print(sha, end='')
        case 'ls-tree':
            git_ls_tree(args.tree_sha)
        case 'write-tree':
            git_write_tree()
        case _:
            raise RuntimeError(f'Unknown command #{args.command}')


if __name__ == '__main__':
    main()
