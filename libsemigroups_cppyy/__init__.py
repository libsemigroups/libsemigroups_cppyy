'''
A minimal cppyy wrapper for the libsemigroups C++ library.

This module contains some minimal wrapping code to interact with the
libsemigroups C++ library:

    https://github.com/james-d-mitchell/libsemigroups

via cppyy:

    https://bitbucket.org/wlav/cppyy/
'''

import cppyy
from cppyy.gbl import std
# This assumes that the header files are in the standard include path,
# and that the libsemigroups dynamic library is in LD_LIBRARY_PATH
cppyy.load_library('libsemigroups')
cppyy.include('libsemigroups/libsemigroups.h')
cppyy.include("python3.6m/Python.h")
cppyy.include(__file__[:-31]+"python_element.h")

# Variants:
# cppyy.include('/usr/local/include/libsemigroups/libsemigroups.h')
# cppyy.include('~/anaconda/include/libsemigroups/libsemigroups.h')
# cppyy.include('/Users/jdm/libsemigroups/src/libsemigroups.h')

CPPInstance = cppyy.gbl.libsemigroups.Element.__base__

from cppyy.gbl.libsemigroups import PBR, Bipartition, PythonElement


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


def BooleanMat(mat):
    if isinstance(mat, list) and all(isinstance(row, list) for row in mat):
        out = std.vector(std.vector("bool"))()
        for row in mat:
            v = std.vector("bool")()
            for x in row:
                assert isinstance(x, int)
                v.push_back(x)
            out.push_back(v)
    else:
        raise ValueError("mat must be a list of lists")

    out = cppyy.gbl.libsemigroups.BMat(len(mat)).type(out)
    return out

def Semigroup(gens):
    if gens:
       types =  { type(g) for g in gens }
       if len(types) > 1:
           raise ValueError("the generators are not all of the same type")
       cls = types.pop()
       if not issubclass(cls, CPPInstance):
           cls = cppyy.gbl.libsemigroups.PythonElement
           gens = tuple( cls(g) for g in gens )
    else:
        cls = "int"
    return cppyy.gbl.libsemigroups.Semigroup(cls)(gens)
