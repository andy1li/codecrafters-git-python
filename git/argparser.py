from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(
        'init', help='Create an empty Git repository or reinitialize an existing one'
    )

    parser_cat_file = subparsers.add_parser(
        'cat-file',
        help='Provide content or type and size information for repository objects',
    )
    parser_cat_file.add_argument('-p', dest='pretty_print', action='store_true')
    parser_cat_file.add_argument('blob_sha')

    parser_hash_object = subparsers.add_parser(
        'hash-object',
        help='Compute object ID and optionally creates a blob from a file',
    )
    parser_hash_object.add_argument('-w', dest='write', action='store_true')
    parser_hash_object.add_argument('filename')

    parser_ls_tree = subparsers.add_parser(
        'ls-tree',
        help='List the contents of a tree object',
    )
    parser_ls_tree.add_argument('--name-only', action='store_true')
    parser_ls_tree.add_argument('tree_sha')

    subparsers.add_parser(
        'write-tree',
        help='Create a tree object from the current index',
    )

    parser_commit_tree = subparsers.add_parser(
        'commit-tree',
        help='Create a new commit object',
    )
    parser_commit_tree.add_argument('tree_sha')
    parser_commit_tree.add_argument('-p', dest='commit_sha')
    parser_commit_tree.add_argument('-m', dest='message')

    return parser.parse_args()
