"""
    Defines a functional API for working with an irods server using file path
    strings.
"""

import posixpath
import os


def get(session, file_path, dest, recursive=False):
    """
        Download files from an iRODS server.

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            file_path (String): File or folder path to get
                from the iRODS server. Must be absolute path.
            dest (String): local folder to place the downloaded files in
            recursive (boolean): recursively get folders.
    """
    if session.data_objects.exists(file_path):
        to_file_path = os.path.join(dest, os.path.basename(file_path))
        session.data_objects.get(file_path, file=to_file_path)
    elif session.collections.exists(file_path):
        if recursive:
            coll = session.collections.get(file_path)
            dest = os.path.join(dest, os.path.basename(file_path))
            os.mkdir(dest)

            for file_object in coll.data_objects:
                get(session, os.path.join(file_path, file_object.path), dest, True)
            for collection in coll.subcollections:
                get(session, collection.path, dest, True)
        else:
            raise FileNotFoundError("Skipping directory " + file_path)
    else:
        raise FileNotFoundError(file_path + " Does not exist")


def put(session, file_path, dest, recursive=False):
    """
        Upload files to an iRODS server.

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            file_path (String): path of file or folder to upload
                to the iRODS server.
            dest (String): Path to collection iRODS server to put the files.
                Must be an absolute path.
            recursive (boolean): perform put recursively
    """

    if not session.collections.exists(dest.rstrip('/')):
        raise FileNotFoundError(dest + " Does not exist")

    irods_path = posixpath.join(dest, os.path.basename(file_path))
    if os.path.isfile(file_path):
        session.data_objects.put(file_path, irods_path)
    elif os.path.isdir(file_path):
        if recursive:
            session.collections.create(irods_path)
            for obj in [os.path.join(file_path, f) for f in os.listdir(file_path)]:
                put(session, obj, irods_path, True)
        else:
            raise FileNotFoundError("Skipping directory " + file_path)
    else:
        raise FileNotFoundError(file_path + " Does not exist")

def rm(session, file_path):# pylint: disable=invalid-name
    """
        Remove file from an iRODS server

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            file_path: Path of file on the iRODS server to remove
    """
    if session.data_objects.exists(file_path):
        obj = session.data_objects.get(file_path)
        obj.unlink(force=True)
    elif session.collections.exists(file_path):
        raise NotImplementedError("We don't do collections yet")
    else:
        raise FileNotFoundError(file_path + " Does not exist")


def ls(session, path):# pylint: disable=invalid-name
    """
        List files on an iRODS server.

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            path (String): path on iRODS server to list. Must be absolute.
    """
    coll = session.collections.get(posixpath.join('/', path))

    return([obj.name for obj in coll.data_objects],
           [obj.name for obj in coll.subcollections])
