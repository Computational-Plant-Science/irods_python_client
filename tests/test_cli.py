from os import path
import pytest
import pkg_resources  # part of setuptools

from test_functional import session, IRODS_TEST_DIR
from pyicmd.pyicmd import main

def test_help(capfd):
    with pytest.raises(SystemExit):
        args = []
        main(args)

    captured = capfd.readouterr()
    assert captured.out.startswith("usage: pytest")

def test_version(capfd):
    with pytest.raises(SystemExit):
        args = ['--version']
        main(args)

    captured = capfd.readouterr()
    assert captured.out == "pyicmd " + pkg_resources.require("pyicmd")[0].version + "\n"


def test_put(tmpdir,session):
    TMP_FILE_NAME = "hello.txt"
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")

    args = ["put", IRODS_TEST_DIR, str(file)]
    main(args)

    assert session.data_objects.exists(path.join(IRODS_TEST_DIR,TMP_FILE_NAME))

def test_put_recursive(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    TMP_DIR_NAME = "test"
    dir = tmpdir.mkdir(TMP_DIR_NAME)
    file = dir.join(TMP_FILE_NAME)
    file.write("hello")

    args = ["put", "-R", IRODS_TEST_DIR, str(dir)]
    main(args)

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

    args = ["get", irods_file_path, str(todir)]
    main(args)

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

    args = ["get", "-R", irods_dir_path, str(todir)]
    main(args)

    assert path.isdir(path.join(todir,TMP_DIR_NAME))
    assert path.isfile(path.join(todir,TMP_DIR_NAME,TMP_FILE_NAME))

def test_ls(session,tmpdir,capfd):
    TMP_FILE_NAME = "hello.txt"
    TMP_COLL_NAME = 'col1'
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")
    session.collections.create(path.join(IRODS_TEST_DIR,TMP_COLL_NAME))
    session.data_objects.put(str(file),
                             path.join(IRODS_TEST_DIR,TMP_FILE_NAME))

    args = ["ls", IRODS_TEST_DIR]
    main(args)
    captured = capfd.readouterr()

    str_output = str([TMP_FILE_NAME]) + "\n" + str([TMP_COLL_NAME]) + "\n"
    assert captured.out == str_output

def test_rm(session,tmpdir):
    TMP_FILE_NAME = "hello.txt"
    irods_file_path = path.join(IRODS_TEST_DIR,TMP_FILE_NAME)
    file = tmpdir.join(TMP_FILE_NAME)
    file.write("hello")
    session.data_objects.put(str(file),
                             irods_file_path)
    assert session.data_objects.exists(irods_file_path)

    args = ["rm", irods_file_path]
    main(args)

    assert not session.data_objects.exists(irods_file_path)

def test_test(capfd):
    args = ["test"]
    main(args)
    captured = capfd.readouterr()
    assert captured.out.startswith("Connection Successful.")

def test_test(session,capfd):
    args = ["test"]
    main(args)
    captured = capfd.readouterr()
    assert captured.out.startswith("Connection Successful.")

def test_cmdline_irods_env(session,capfd):
    args = ["--host", session.host,
            "--user", session.username,
            "--port", str(session.port),
            "--passwd", "rods",
            "--zone", session.zone,
            "test"]
    main(args)
    captured = capfd.readouterr()
    assert captured.out.startswith("Connection Successful.")
