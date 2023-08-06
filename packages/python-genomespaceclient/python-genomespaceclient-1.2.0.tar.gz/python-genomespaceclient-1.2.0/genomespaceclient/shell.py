import argparse
import logging
import sys

from genomespaceclient import GenomeSpaceClient
from genomespaceclient import util


log = logging.getLogger(__name__)


def get_client(args):
    return GenomeSpaceClient(username=args.user, password=args.password,
                             token=args.token)


def genomespace_copy_files(args):
    client = get_client(args)
    client.copy(args.source, args.destination, recurse=args.recurse)


def genomespace_move_files(args):
    client = get_client(args)
    client.move(args.source, args.destination)


def genomespace_delete_files(args):
    client = get_client(args)
    client.delete(args.file_url, recurse=args.recurse)


def genomespace_create_folder(args):
    client = get_client(args)
    client.mkdir(args.folder_url, create_path=args.path)


def genomespace_list_files(args):
    client = get_client(args)
    folder_contents = client.list(args.folder_url)

    for folder in folder_contents.contents:
        print("{isdir:<3s} {owner:<10s} {size:>10s} {last_modified:>26s}"
              " {name:s}".format(
                  isdir="d" if folder.is_directory else "_",
                  owner=folder.owner["name"] or "",
                  size=util.format_file_size(folder.size),
                  last_modified=folder.last_modified or "",
                  name=folder.name))


def process_args(args):
    parser = argparse.ArgumentParser()

    # authentication settings
    grp_auth_userpass = parser.add_argument_group(
        'user_pass_auth', 'username/password based authentication')
    grp_auth_userpass.add_argument('-u', '--user', type=str,
                                   help="GenomeSpace username", required=False)
    grp_auth_userpass.add_argument('-p', '--password', type=str,
                                   help="GenomeSpace password", required=False)
    grp_auth_token = parser.add_argument_group(
        'token_auth',
        'token based authentication  (instead of username/password)')
    grp_auth_token.add_argument(
        '-t', '--token', type=str,
        help="GenomeSpace auth token.",
        required=False)

    # debugging and logging settings
    parser.add_argument("-v", "--verbose", action="count",
                        dest="verbosity_count", default=0,
                        help="increases log verbosity for each occurrence.")
    subparsers = parser.add_subparsers(metavar='<subcommand>')

    # File copy commands
    file_copy_parser = subparsers.add_parser(
        'cp',
        formatter_class=argparse.RawTextHelpFormatter,
        help='Copy a file from/to/within GenomeSpace',
        description="Examples:\n\n"
        "1. Copy a local file to GenomeSpace dir\n"
        "{0} cp /tmp/myfile.txt https://dmdev.genomespace.org/datamanager/v1.0"
        "/file/Home/s3:test/\n\n"
        "2. Copy a remote file from GenomeSpace to a local file\n"
        "{0} cp https://dmdev.genomespace.org/datamanager/v1.0/file/Home/"
        "s3:test/hello.txt /tmp/myfile.txt\n\n"
        "3. Copy a file within GenomeSpace\n"
        "{0} cp https://dmdev.genomespace.org/datamanager/v1.0/file/Home/"
        "s3:test/hello.txt https://dmdev.genomespace.org/datamanager/v1.0/"
        "file/Home/s3:test/hello2.txt".format(parser.prog))
    file_copy_parser.add_argument(
        '-R', '--recurse', action='store_true',
        help="Copy files recursively.",
        required=False, default=False)
    file_copy_parser.add_argument(
        'source', type=str,
        help="Local path or GenomeSpace URI of source file.")
    file_copy_parser.add_argument(
        'destination', type=str,
        help="Local path or GenomeSpace URI of destination file.")
    file_copy_parser.set_defaults(func=genomespace_copy_files)

    # file move commands
    file_move_parser = subparsers.add_parser(
        'mv',
        formatter_class=argparse.RawTextHelpFormatter,
        help='Move a file within GenomeSpace',
        description="Examples:\n\n"
        "{0} mv https://dmdev.genomespace.org/datamanager/v1.0/file/Home/"
        "s3:test/folder1/hello.txt https://dmdev.genomespace.org/"
        "datamanager/v1.0/file/Home/s3:test/folder2/"
        "world.txt".format(parser.prog))
    file_move_parser.add_argument('source', type=str,
                                  help="GenomeSpace URI of source file.")
    file_move_parser.add_argument('destination', type=str,
                                  help="GenomeSpace URI of destination file.")
    file_move_parser.set_defaults(func=genomespace_move_files)

    # download commands
    gs_list_parser = subparsers.add_parser(
        'ls',
        help='List contents of a GenomeSpace folder')
    gs_list_parser.add_argument('folder_url', type=str,
                                help="GenomeSpace URI of folder to list.")
    gs_list_parser.set_defaults(func=genomespace_list_files)

    # delete commands
    gs_rm_parser = subparsers.add_parser(
        'rm',
        help="Delete a GenomeSpace file or folder.")
    gs_rm_parser.add_argument(
        '-R', '--recurse', action='store_true',
        help="Delete files recursively.",
        required=False, default=False)
    gs_rm_parser.add_argument(
        'file_url', type=str,
        help="GenomeSpace URI of file/folder to delete.")
    gs_rm_parser.set_defaults(func=genomespace_delete_files)

    # mkdir commands
    gs_mkdir_parser = subparsers.add_parser(
        'mkdir',
        help="Creates a remote GenomeSpace folder.")
    gs_mkdir_parser.add_argument(
        '-p', '--path', action='store_true',
        help="Creates intermediate directories as required.",
        required=False, default=False)
    gs_mkdir_parser.add_argument(
        'folder_url', type=str,
        help="GenomeSpace URI of folder to create.")
    gs_mkdir_parser.set_defaults(func=genomespace_create_folder)

    args = parser.parse_args(args[1:])
    return args


def configure_logging(verbosity_count):
    if verbosity_count < 3:
        logging.getLogger('requests').setLevel(logging.ERROR)
    # set global logging level
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if verbosity_count > 3 else logging.ERROR,
        format='%(levelname)-5s: %(name)s: %(message)s')
    # Set client log level
    if verbosity_count:
        log.setLevel(max(4 - verbosity_count, 1) * 10)
    else:
        log.setLevel(logging.INFO)


def main():
    try:
        args = process_args(sys.argv)
        configure_logging(args.verbosity_count)
        # invoke subcommand
        args.func(args)
    finally:
        logging.shutdown()


if __name__ == "__main__":
    sys.exit(main())
