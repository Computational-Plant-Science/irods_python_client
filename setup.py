from setuptools import setup

setup(
    name='pyicmd',
    version='0.3',
    description='Python port of the irods icommands',
    url='http://github.com/cottersci/',
    author='Chris Cotter',
    license='The Unlicense',
    packages=['pyicmd'],
    zip_safe=False,
    scripts=['bin/pyicmd'],
    install_requires=['python-irodsclient']
)
