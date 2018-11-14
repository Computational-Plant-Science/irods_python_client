import posixpath
import os

"""
    Contains functional backends for commands
"""

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
            obj = session.data_objects.create(path)
            with obj.open('r+') as dest_obj, open(file,'rb') as f:
                dest_obj.write(f.read())
        elif(os.path.isdir(file)):
            if(recursive):
                session.collections.create(path)
                files = [os.path.join(file,f) for f in os.listdir(file)]
                put(session,files,dest,True)
            else:
                print("Skipping directory %s"%(file))

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
