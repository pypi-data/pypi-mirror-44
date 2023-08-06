python-json2yaml
=================

.. image:: https://travis-ci.org/appstore-zencore/python-json2yaml.svg?branch=master
    :target: https://travis-ci.org/appstore-zencore/python-json2yaml


A simple command that turn json data to yaml format and vice versa. It can be used in Linux, MacOS and Window.


Install
-------

::

    pip install python-json2yaml


Commands
--------

- json2yaml
- yaml2json


Command Helpers
---------------

::

    E:\code\zencore-json2yaml\test>json2yaml --help
    Usage: json2yaml [OPTIONS] [SRC] [DST]

    Options:
    --help  Show this message and exit.

    E:\code\zencore-json2yaml\test>yaml2json --help
    Usage: yaml2json [OPTIONS] [SRC] [DST]

    Options:
    --help  Show this message and exit.

Command Examples
----------------

1. Read json text from stdin and print yaml text to stdout

::

    cat a.json | json2yaml

1. Read json text from stdin and print yaml text to a file

::

    cat a.json | json2yaml - a.txt

1. Read json text from a file and print yaml text to another file

::

    json2yaml a.json a.txt
