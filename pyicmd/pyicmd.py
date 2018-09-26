import argparse
from argparse import RawTextHelpFormatter
import glob
import posixpath

from irods.session import iRODSSession
from irods.test import helpers

description = '''
Python port of the irods icommands.

Supports irods_envirment.json file created by iinit. File can be at its
default location ('~/.irods/irods_environment.json') or set via the
IRODS_ENVIRONMENT_FILE variable.

If user is set via the commandline irods_enviorment.json is ingored
and given (or default) command line arguments are used to open the session.
'''

def ls(session,args):
    parser = argparse.ArgumentParser(
        prog='pyicmd ls',
        description='List the files and folders at the given path')
    parser.add_argument('path', type=str, help='Path on irods server to list')
    args = parser.parse_args(args)

    coll = session.collections.get(posixpath.join('/',args.path))
    print([obj.name for obj in coll.data_objects])
    print([obj.name for obj in coll.subcollections])

def put(session,args):
    parser = argparse.ArgumentParser(
        prog='pyicmd put',
        description='Copy file(s) from the local computer to [dir] on the server')
    parser.add_argument('loc', type=str, help='Location to put files')
    parser.add_argument('files', type=str, nargs='*', help='Path or pattern of files to upload')
    args = parser.parse_args(args)

    for file in args.files:
        obj = session.data_objects.create(posixpath.join(args.loc,file))
        with obj.open('r+') as dest, open(file,'rb') as f:
            dest.write(f.read())

def rm(session,args):
    parser = argparse.ArgumentParser(
        prog='pyicmd rm',
        description='Remove the files listed from the irods server')
    parser.add_argument('files', type=str, nargs='*', help='FULL Path or pattern of files to upload')
    args = parser.parse_args(args)

    for file in args.files:
        obj = session.data_objects.get(file)
        obj.unlink(force=True)

def main():
    help_str = """ The icommand to run:
    rm [file(s)]          Remove the files listed from the irods server
    ls [path]             List the files and folders at the given path
    put [dir] [file(s)]   Copy file(s) from the local computer to [dir] on the server

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
    parser.add_argument('--host', type=str, default='localhost', help="Address of irods server")
    parser.add_argument('--port', type=int, default=1247, help="irods server port")
    parser.add_argument('--user', type=str, help="irods username")
    parser.add_argument('--passwd',type=str, help="irods user password")
    parser.add_argument('--zone', type=str, default='tempZone', help="irods zone")
    args, unknownargs = parser.parse_known_args()

    if(args.cmd == "help"):
        parser.print_help()
        exit()

    if(args.user is not None):
        session = iRODSSession(host=args.host, port=args.port, user=args.user, password=args.passwd, zone=args.zone)
    else:
        try:
            session = helpers.make_session()
        except FileNotFoundError:
            print("ERROR: No irods_envirment.json file found. Type 'pyicmd help' for details")
            exit()

    if(args.cmd == "ls"):
        ls(session,unknownargs)
    elif(args.cmd == "put"):
        put(session,unknownargs)
    elif(args.cmd == "rm"):
        rm(session,unknownargs)

    session.cleanup()

if __name__ == "__main__":
    main()
