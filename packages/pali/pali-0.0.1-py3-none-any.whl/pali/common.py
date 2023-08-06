#!/usr/bin/env python
'''
Some general purpose utilities.
'''

from platform import python_version
import sys

PYTHON_VER = python_version()

PYTHON_2 = PYTHON_VER.startswith('2')
PYTHON_3 = PYTHON_VER.startswith('3')


if PYTHON_2:
    import Queue as queue
elif PYTHON_3:
    import queue as queue


queue = queue
