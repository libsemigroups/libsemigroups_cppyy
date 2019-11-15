"""
This file contains the interface to the implementation of the
Schreier-Sims algorithm for permutation groups in libsemigroups; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__schreiersims.html

for further details.
"""

import cppyy

# TODO needs some changes in libsemigroups to actually work
def SchreierSims(*args):
    return cppyy.gbl.libsemigroups.SchreierSims(*args)()
