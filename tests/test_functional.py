from os import path
import pytest
import pyicmd.functional as F
from irods.session import iRODSSession
from irods.test import helpers

IRODS_TEST_DIR = "/tempZone/home/rods/pytest"

@pytest.fixture()
def session():
    try:
        session = helpers.make_session()
    except FileNotFoundError:
        session = iRODSSession(host="localhost",
                           port=1247,
                           user="rods",
                           password="rods",
                           zone="tempZone")

    if(session.collections.exists(IRODS_TEST_DIR)):
        coll = session.collections.get(IRODS_TEST_DIR)
        coll.remove(recursive=True,force=True)

    session.collections.create(IRODS_TEST_DIR)

    return session

def test_ls(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    TMP_COLL_NAME = 'col1'
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")
    session.collections.create(path.join(IRODS_TEST_DIR,TMP_COLL_NAME))
    session.data_objects.put(str(file),
                             path.join(IRODS_TEST_DIR,TMP_FILE_NAME))

    files, collections = F.ls(session,IRODS_TEST_DIR)

    assert files == [TMP_FILE_NAME]
    assert collections == [TMP_COLL_NAME]

def test_rm(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    irods_file_path = path.join(IRODS_TEST_DIR,TMP_FILE_NAME)
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")
    session.data_objects.put(str(file),
                             irods_file_path)
    assert session.data_objects.exists(irods_file_path)

    F.rm(session,irods_file_path)

    assert not session.data_objects.exists(irods_file_path)

def test_put_file(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")

    F.put(session,str(file),IRODS_TEST_DIR)

    assert session.data_objects.exists(path.join(IRODS_TEST_DIR,TMP_FILE_NAME))

def test_put_recursive(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    TMP_DIR_NAME = "test"
    dir = tmpdir.mkdir(TMP_DIR_NAME)
    file = dir.join(TMP_FILE_NAME)
    file.write("hello")

    F.put(session,str(dir),IRODS_TEST_DIR,recursive=True)

    assert session.collections.exists(path.join(IRODS_TEST_DIR,TMP_DIR_NAME))
    assert session.data_objects.exists(path.join(IRODS_TEST_DIR,TMP_DIR_NAME,TMP_FILE_NAME))

def test_get(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    irods_file_path = path.join(IRODS_TEST_DIR,TMP_FILE_NAME)
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")
    session.data_objects.put(str(file),
                             irods_file_path)
    todir = tmpdir.mkdir("to")
    F.get(session,irods_file_path,str(todir))

    assert path.isfile(path.join(todir,TMP_FILE_NAME))

def test_get_recursive(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    TMP_DIR_NAME = "test"
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")
    irods_dir_path = path.join(IRODS_TEST_DIR,TMP_DIR_NAME)
    session.collections.create(irods_dir_path)
    irods_file_path = path.join(irods_dir_path,TMP_FILE_NAME)
    session.data_objects.put(str(file),
                             irods_file_path)
    todir = tmpdir.mkdir("to")

    F.get(session,irods_dir_path,str(todir),recursive=True)

    assert path.isdir(path.join(todir,TMP_DIR_NAME))
    assert path.isfile(path.join(todir,TMP_DIR_NAME,TMP_FILE_NAME))
