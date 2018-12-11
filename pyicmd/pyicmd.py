"""
    Python port of the iRODS icommands.

    Supports irods_environment.json file created by iinit. File can be at its
    default location ('~/.irods/irods_environment.json') or set via the
    IRODS_ENVIRONMENT_FILE variable.

    If user is set via the command line irods_environment.json is ignored
    and given (or default) command line arguments are used to open the session.
"""
import sys
import argparse
from argparse import RawTextHelpFormatter

from irods.session import iRODSSession
from irods.test import helpers
from irods.exception import (CollectionDoesNotExist,
                             CAT_INVALID_USER,
                             CAT_INVALID_AUTHENTICATION,
                             CAT_INVALID_CLIENT_USER,
                             NetworkException)
import pyicmd.functional as F

def test(session):
    '''Test the connection to the server'''
    print("Connection Successful. iRODS server version: %s"%
          (session.server_version,))

def ls(session, args):# pylint: disable=invalid-name
    ''' List Files in collection '''
    parser = argparse.ArgumentParser(
        prog='pyicmd ls',
        description='List the files and folders at the given path')
    parser.add_argument('path', type=str, help='Path on iRODS server to list')
    args = parser.parse_args(args)

    try:
        files, collections = F.ls(session, args.path)
    except CollectionDoesNotExist:
        sys.exit("Collection \"" + args.path + "\" does not exist.")

    print(files)
    print(collections)

def get(session, args):
    ''' Get file or collection from the iRODS server'''
    parser = argparse.ArgumentParser(
        prog='pyicmd get',
        description='Copy file(s) and folder(s) from the server to [loc] on the local computer')
    parser.add_argument('files', type=str, nargs='+',
                        help='Path or pattern of files to download')
    parser.add_argument('loc', type=str, help='Location to put files')
    parser.add_argument('-R', action='store_true',
                        help="Put directories and their contents recursively")
    args = parser.parse_args(args)

    for file in args.files:
        try:
            F.get(session, file, args.loc, recursive=args.R)
        except FileNotFoundError as exception:
            sys.exit(str(exception))

def put(session, args):
    '''Put a file or folder onto the iRODS server'''
    parser = argparse.ArgumentParser(
        prog='pyicmd put',
        description='Copy file(s) and folder(s) from the local computer to [loc] on the server')
    parser.add_argument('loc', type=str, help='Location to put files')
    parser.add_argument('files', type=str, nargs='+',
                        help='Path or pattern of files to upload')
    parser.add_argument('-R', action='store_true',
                        help="Put directories and their contents recursively")
    args = parser.parse_args(args)

    for file_path in args.files:
        try:
            F.put(session, file_path, args.loc, recursive=args.R)
        except FileNotFoundError as exception:
            sys.exit(str(exception))

def rm(session, args):# pylint: disable=invalid-name
    '''Remove a file from the iRODS server'''
    parser = argparse.ArgumentParser(
        prog='pyicmd rm',
        description='Remove the files listed from the iRODS server')
    parser.add_argument('files', type=str, nargs='+',
                        help='FULL Path or pattern of files to upload')
    args = parser.parse_args(args)

    for file_path in args.files:
        try:
            F.rm(session, file_path)
        except FileNotFoundError as exception:
            sys.exit(str(exception))

def connect(args):
    '''Connect to the iRODS server'''
    if args.user is not None:
        if args.passwd is None:
            print("ERROR: --passwd required with --user")
            sys.exit()

        session = iRODSSession(host=args.host, port=args.port,
                               user=args.user, password=args.passwd,
                               zone=args.zone)
    else:
        try:
            session = helpers.make_session()
        except FileNotFoundError:
            sys.exit("ERROR: No irods_environment.json file found. Type 'pyicmd help' for details")

    #Test the connection
    try:
        session.server_version
    except CAT_INVALID_AUTHENTICATION:
        sys.exit("iRODS server authentication failed.")
    except CAT_INVALID_USER:
        sys.exit("Invalid iRODS user.")
    except CAT_INVALID_CLIENT_USER:
        sys.exit("Invalid client user. (Did you use the right zone?)")
    except NetworkException as exception:
        sys.exit(str(exception))

    return session

def main(args):
    ''' Main program function '''

    description = '''
    Python port of the iRODS icommands.

    Supports irods_environment.json file created by iinit. File can be at its
    default location ('~/.irods/irods_environment.json') or set via the
    IRODS_ENVIRONMENT_FILE variable.

    If user is set via the command line irods_environment.json is ignored
    and given (or default) command line arguments are used to open the session.
    '''

    version = "1.0.3"

    help_str = """ The icommand to run:
    rm [file(s)]          Remove the files listed from the iRODS server
    ls [path]             List the files and folders at the given path
    put [loc] [file(s)]   Copy file(s) and folder(s) from the local computer to [loc] on the server
    get [files(s)] [loc]  Copy file(s) and folder(s) from the server to [loc] on the local computer
    test                  Test the connection to the iRODS server.
    To learn more about a function, type pyicmd [cmd] -h
    """

    parser = argparse.ArgumentParser(
        description=description,
        add_help=False,
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('cmd', nargs='?',
                        default='help',
                        type=str,
                        help=help_str)
    parser.add_argument('--host', type=str, default='localhost', help="Address of iRODS server")
    parser.add_argument('--port', type=int, default=1247, help="iRODS server port")
    parser.add_argument('--user', type=str, help="iRODS username")
    parser.add_argument('--passwd', type=str, help="iRODS user password")
    parser.add_argument('--zone', type=str, default='tempZone', help="iRODS zone")
    parser.add_argument('--version', action='version', version='pyicmd ' + version)
    args, unknownargs = parser.parse_known_args(args)

    if args.cmd == "help":
        parser.print_help()
        sys.exit()

    session = connect(args)

    if args.cmd == "ls":
        ls(session, unknownargs)
    elif args.cmd == "put":
        put(session, unknownargs)
    elif args.cmd == "rm":
        rm(session, unknownargs)
    elif args.cmd == "get":
        get(session, unknownargs)
    elif args.cmd == "test":
        test(session)
    else:
        print("ERROR: \"" + args.cmd + "\" is not a valid command")
        parser.print_help()
        sys.exit()

    session.cleanup()

def cli():
    '''Entry point used by setup.'''
    main(sys.argv[1:])

if __name__ == "__main__":
    main(sys.argv[1:])
