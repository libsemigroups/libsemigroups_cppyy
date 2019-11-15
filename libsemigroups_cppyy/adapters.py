"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/adapters.html

for further details.
"""

import cppyy


def Degree(x):
    """
    Returns the value of the libsemigroups adapter Degree for type(x) and x.
    """
    return cppyy.gbl.libsemigroups.Degree(type(x))()(x)


def One(x):
    """
    Returns the value of the libsemigroups adapter One for type(x) and x.
    """
    return cppyy.gbl.libsemigroups.One(type(x))()(x)


def Product(x, y):
    """
    Returns the value of the libsemigroups adapter Product for type(x), x, and
    y.
    """
    xy = One(x)
    cppyy.gbl.libsemigroups.Product(type(x))()(xy, x, y)
    return xy
