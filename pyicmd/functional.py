"""
    Defines a functional API for working with an iRODS server using file path
    strings.
"""

import posixpath
import os


def get(session, irods_path, local_path, recursive=False):
    """
        Download files from an iRODS server.

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            irods_path (String): File or folder path to get
                from the iRODS server. Must be absolute path.
            local_path (String): local folder to place the downloaded files in
            recursive (Boolean): recursively get folders.
    """
    if session.data_objects.exists(irods_path):
        to_file_path = os.path.join(local_path, os.path.basename(irods_path))
        session.data_objects.get(irods_path, file=to_file_path)
    elif session.collections.exists(irods_path):
        if recursive:
            coll = session.collections.get(irods_path)
            local_path = os.path.join(local_path, os.path.basename(irods_path))
            os.mkdir(local_path)

            for file_object in coll.data_objects:
                get(session, os.path.join(irods_path, file_object.path), local_path, True)
            for collection in coll.subcollections:
                get(session, collection.path, local_path, True)
        else:
            raise FileNotFoundError("Skipping directory " + irods_path)
    else:
        raise FileNotFoundError(irods_path + " Does not exist")


def put(session, local_path, irods_path, recursive=False):
    """
        Upload files to an iRODS server.

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            local_path (String): path of file or folder to upload
                to the iRODS server.
            irods_path (String): Path to collection iRODS server to put the files.
                Must be an absolute path.
            recursive (Boolean): perform put recursively
    """

    if not session.collections.exists(irods_path.rstrip('/')):
        raise FileNotFoundError(irods_path + " Does not exist")

    irods_path = posixpath.join(irods_path, os.path.basename(local_path))
    if os.path.isfile(local_path):
        session.data_objects.put(local_path, irods_path)
    elif os.path.isdir(local_path):
        if recursive:
            session.collections.create(irods_path)
            for obj in [os.path.join(local_path, f) for f in os.listdir(local_path)]:
                put(session, obj, irods_path, True)
        else:
            raise FileNotFoundError("Skipping directory " + local_path)
    else:
        raise FileNotFoundError(local_path + " Does not exist")

def rm(session, irods_path):# pylint: disable=invalid-name
    """
        Remove file from an iRODS server

        Args:
            session (iRODS.session.iRODSSession): iRODS session
            irods_path (String): Path of file on the iRODS server to remove
    """
    if session.data_objects.exists(irods_path):
        obj = session.data_objects.get(irods_path)
        obj.unlink(force=True)
    elif session.collections.exists(irods_path):
        raise NotImplementedError("We don't do collections yet")
    else:
        raise FileNotFoundError(irods_path + " Does not exist")


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
