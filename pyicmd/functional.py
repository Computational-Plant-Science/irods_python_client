import posixpath
import os

"""
    Contains functional backends for commands
"""


def get(session, file_list, dest, recursive=False):
    """
        Args:
            session: irods session
            file: file or folder to get from the iRODS server
            dest: local folder to place the gotten files in
    """
    for file in file_list:
        print("Looking at obj: " + file)
        if(session.data_objects.exists(file)):
            to_file_path = os.path.join(dest,obj.name)
            session.data_objects.get(file, file=to_file_path)
        elif(session.collections.exists(file)):
            if(recursive):
                coll = session.collections.get(file)
                files = [os.path.join(file,f.path) for f in coll.data_objects]
                collections = [c.path for c in coll.subcollections]
                dest = os.path.join(dest,os.path.basename(file))

                os.mkdir(dest)
                get(session,files,dest,True)
                get(session,collections,dest,True)
            else:
                print("Skipping collection %s"%(file))
        else:
            print("Does not exist")


def put(session,file_list,dest,recursive = False):
    """
        Args:
            session: irods session
            file_list: list of file paths
            dest: irods colletion to put files in
            recursive: perform put recursively
    """
    for file in file_list:
        path = posixpath.join(dest,file)
        if(os.path.isfile(file)):
            session.data_objects.put(file,path)
        elif(os.path.isdir(file)):
            if(recursive):
                session.collections.create(path)
                files = [os.path.join(file,f) for f in os.listdir(file)]
                put(session,files,dest,True)
            else:
                print("Skipping directory %s"%(file))
        else:
            print("Does not exist")

def rm(session,file_list):
    """
        Args:
            session: irods session
            file_list: list of file paths
    """
    for file in file_list:
        obj = session.data_objects.get(file)
        obj.unlink(force=True)

def ls(session,path):
    """
        Args:
            session: irods session
            path: path on irods server to list
    """
    coll = session.collections.get(posixpath.join('/',path))
    print([obj.name for obj in coll.data_objects])
    print([obj.name for obj in coll.subcollections])
