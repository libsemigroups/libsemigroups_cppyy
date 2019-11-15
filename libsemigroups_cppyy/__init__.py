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

import libsemigroups_cppyy.detail
from libsemigroups_cppyy.adapters import *

cppyy.add_include_path("/Users/jdm/libsemigroups/")
cppyy.add_include_path("/Users/jdm/libsemigroups/include")
cppyy.add_include_path("/Users/jdm/libsemigroups/extern/fmt-5.3.0/include")

cppyy.load_library("libsemigroups")

cppyy.cppdef("#define FMT_HEADER_ONLY")

cppyy.include("bmat8.hpp")
cppyy.include("element.hpp")
cppyy.include("element-helper.hpp")
cppyy.include("froidure-pin.hpp")

from libsemigroups_cppyy.bmat import *
from libsemigroups_cppyy.pperm import *
from libsemigroups_cppyy.transf import *

# Untested


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
