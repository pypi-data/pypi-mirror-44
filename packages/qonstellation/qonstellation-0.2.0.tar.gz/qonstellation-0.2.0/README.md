# Qonstellation Client

The Qonstellation Client is a basic Python package that can work with the [Qonstellation API](https://www.qonstellation.co) 

## Installation

You can install the Qonstellation Client from [PyPI](https://pypi.org/project/qonstellation/):

    pip install qonstellation

The reader is supported on Python 2.7, as well as Python 3.4 and above.

## How to use

The Real Python Feed Reader is a command line application, named `realpython`. To see a list of the [latest Real Python tutorials](https://realpython.com/) simply call the program:

    >>> from qonstellation import api
    >>> success, error = api.login(token='xxx')
    (True, '')

