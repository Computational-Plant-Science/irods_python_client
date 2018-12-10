# Python port of the irods icommands.
---
## Install
```bash
pip3 install git+https://github.com/cottersci/irods_python_client.git#egg=pyicmd
```
sudo may be required to get pyicmd into the PATH.  

## Usage
```bash
usage: pyicmd [--host HOST] [--port PORT] [--user USER] [--passwd PASSWD]
              [--zone ZONE]
              [cmd]

Python port of the irods icommands.

Supports irods_environment.json file created by iinit. File can be at its
default location ('~/.irods/irods_environment.json') or set via the
IRODS_ENVIRONMENT_FILE variable.

If user is set via the commandline irods_enviorment.json is ingored
and given (or default) command line arguments are used to open the session.

positional arguments:
  cmd               The icommand to run:
                       rm [file(s)]          Remove the files listed from the irods server
                       ls [path]             List the files and folders at the given path
                       put [loc] [file(s)]   Copy file(s) and folder(s) from the local computer to [loc] on the server
                       get [files(s)] [loc]  Copy file(s) and folder(s) from the server to [loc] on the local computer
                       To learn more about a function, type pyicmd [cmd] -h


optional arguments:
  --host HOST      Address of irods server
  --port PORT      irods server port
  --user USER      irods username
  --passwd PASSWD  irods user password
  --zone ZONE      irods zone

```

## Speed Test
By default, icommands uses multi-threading for uploads greater than ~35MB. pyicmd does not currently support multiple threaded uploads, causing it to be slower for large files.
![Speed Test](assets/UploadTimes.png)

# Contributing
----
## Testing
Tests for the functional.py API are written in pytest format and can be run
with

```bash
make test
```

Tests require a valid iRODS server and configured irods_environment.json file created by iinit. [This iRODS docker container](https://github.com/mjstealey/irods-provider-postgres) Was used to run the tests.

## Code Standard
Code should follow [Python's PEP8 style guide](https://www.python.org/dev/peps/pep-0008/). All contributions should pass standard pylint tests. These can be run using:

```bash
make lint
```
