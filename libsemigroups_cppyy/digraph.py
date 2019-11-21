"""
This file contains the interface to libsemigroups digraph; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__actiondigraph.html

for further details.
"""

import cppyy


def ActionDigraph(int_type):
    return cppyy.gbl.libsemigroups.ActionDigraph(int_type)()
