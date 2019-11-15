"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__schreiersims.html

for further details.
"""

import cppyy

# TODO needs some changes in libsemigroups to actually work
def SchreierSims(*args):
    return cppyy.gbl.libsemigroups.SchreierSims(*args)()
