"""
A minimal cppyy wrapper for the libsemigroups C++ library.

This module contains some minimal wrapping code to interact with the
libsemigroups C++ library:

    https://github.com/libsemigroups/libsemigroups

via cppyy:

    https://bitbucket.org/wlav/cppyy/

For this to work, libsemigroups must be installed on your computer (i.e. the
executables libsemigroups.0.dylib, libsemigroups.dylib, and libsemigroups.a
must be somewhere on your computer where cppyy can load it). libsemigroups
should have been compiled with HPCombi support disabled via the configuration
flag --disable-hpcombi.
"""

import cppyy
from cppyy.gbl import std

cppyy.add_include_path("/Users/jdm/libsemigroups/")
cppyy.add_include_path("/Users/jdm/libsemigroups/include")
cppyy.add_include_path("/Users/jdm/libsemigroups/extern/HPCombi/include")
cppyy.add_include_path("/Users/jdm/libsemigroups/extern/HPCombi/include/fallback")
cppyy.add_include_path("/Users/jdm/libsemigroups/extern/fmt-5.3.0/include")

cppyy.load_library("libsemigroups")

cppyy.cppdef("#define FMT_HEADER_ONLY")

cppyy.include("bmat8.hpp")
cppyy.include("element.hpp")
cppyy.include("element-helper.hpp")
cppyy.include("froidure-pin.hpp")

cppyy.gbl
cppyy.gbl.libsemigroups

# TODO
# 1. add operator** to BMat8
# 2. add operator<= to BMat8
# 3. add operator>= to BMat8

# Unwrappers
def __unwrap(type_nm, cpp_mem_fn, unwrap_fn):
    pass


# Adapters

from cppyy.gbl.libsemigroups import Degree
from cppyy.gbl.libsemigroups import One


def degree(x):
    """
    Returns the value of the libsemigroups adapter Degree for type(x) and x.
    """
    return Degree(type(x))()(x)


def one(x):
    """
    Returns the value of the libsemigroups adapter One for type(x) and x.
    """
    return One(type(x))()(x)


# Boolean matrices

from cppyy.gbl.libsemigroups import BMat8
from cppyy.gbl.libsemigroups import BMatHelper

BMat8.__repr__ = lambda x: cppyy.gbl.libsemigroups.detail.to_string(x)
BMat8._cpp_rows = BMat8.rows


def __BMat8_rows(x):
    return [bits(ord(y)) for y in x._cpp_rows()]


BMat8.rows = __BMat8_rows


def BooleanMat(mat):
    out = std.vector(std.vector("bool"))()
    for row in mat:
        v = std.vector("bool")()
        for x in row:
            v.push_back(x)
        out.push_back(v)
    return cppyy.gbl.libsemigroups.BMatHelper(len(mat)).type(out)


def bits(n):
    return [int(digit) for digit in format(n, "#010b")[2:]]


# Untested


def Transformation(images):
    out = cppyy.gbl.libsemigroups.Transf(len(images)).type(images)
    # out.__class__.__repr__ = lambda self: cppyy.gbl.std.to_string(self)
    return out


def PartialPerm(*args):
    if len(args) == 1:
        return cppyy.gbl.libsemigroups.PPerm(len(args[0])).type(args[0])
    elif len(args) == 3:
        return cppyy.gbl.libsemigroups.PPerm(args[2]).type(*args)


def Permutation(images):
    out = cppyy.gbl.libsemigroups.Perm(len(images)).type(images)
    # out.__class__.__repr__ = lambda self: cppyy.gbl.std.to_string(self)
    return out


def FroidurePin(gens):
    if gens:
        types = {type(g) for g in gens}
        if len(types) > 1:
            raise ValueError("the generators are not all of the same type")
        cls = types.pop()
        return cppyy.gbl.libsemigroups.FroidurePin(cls)(gens)


# from cppyy.gbl.libsemigroups import PBR, Bipartition, RWS
#
# def rules(rws):
#     if not isinstance(rws, cppyy.gbl.libsemigroups.RWS):
#         raise TypeError()
#     return [list(x) for x in rws.rules()]
