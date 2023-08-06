# -*- coding: utf-8 -*-

"""That is shim pure-python module that detects and loads the original selinux package
from outside the current virtualenv, avoiding a very common error of 'missing selinux'
module inside virtualenvs.
"""

__author__ = """Sorin Sbarnea"""
__email__ = 'sorin.sbarnea@gmail.com'
__version__ = '0.1.0'

import sys

if sys.platform == 'linux2':
    # TODO: write code for py34+ where imp was retired

    import imp

    # TODO: add real path detection
    sys.modules['selinux'] = \
        imp.load_source('selinux', '/usr/lib64/python2.7/site-packages/selinux')
