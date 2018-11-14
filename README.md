# Python port of the irods icommands.

## Install
```bash
pip3 install git+https://github.com/cottersci/irods_python_client.git#egg=pyicmd
```
sudo may be required to get pyicmd into the PATH.  

## Configuration
pyicmd supports either iinit configuration or command line options. To use an iinit configuration setup on a computer that does not have iinit, copy
```bash
~/.irods/irods_environment.json
~/.irods/.irodsA
```
to the ~/.irods on the computer without iinit.
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
                       put [dir] [file(s)]   Copy file(s) and folder(s) from the local computer to [dir] on the server

                       To learn more about a function, type pyicmd [cmd] -h


optional arguments:
  --host HOST      Address of irods server
  --port PORT      irods server port
  --user USER      irods username
  --passwd PASSWD  irods user password
  --zone ZONE      irods zone
```
