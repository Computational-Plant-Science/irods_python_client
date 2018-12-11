from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyicmd',
    version='1.0.3',
    description='Python port of the iRODS icommands',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cottersci/irods_python_client',
    author='Chris Cotter',
    author_email="cotter@uga.edu",
    license='MIT License',
    packages=['pyicmd'],
    zip_safe=False,
    entry_points={
        'console_scripts':[
            'pyicmd = pyicmd.pyicmd:cli'
        ]
    },
    install_requires=['python-irodsclient>=0.8.1'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='irods'
)
