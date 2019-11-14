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
    actual = "__" + type_nm.__name__ + "_" + cpp_mem_fn.__name__
    setattr(type_nm, actual, cpp_mem_fn)
    actual = getattr(type_nm, actual)
    setattr(type_nm, cpp_mem_fn.__name__, lambda *args: unwrap_fn(actual(*args)))


def __generic_pow(self, n):
    message = "the argument (power) must be a non-negative integer"
    if not isinstance(n, int):
        raise TypeError(message)
    elif n < 0:
        raise ValueError(message)

    if n == 0:
        return One(self)
    g = self
    if n % 2 == 1:
        x = self  # x = x * g
    else:
        x = One(self)
    while n > 1:
        g *= g
        n //= 2
        if n % 2 == 1:
            x *= g
    return x


# Adapters


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


# Boolean matrices

from cppyy.gbl.libsemigroups import BMat8
from cppyy.gbl.libsemigroups import BMatHelper


def __bits(n):
    return [int(digit) for digit in format(n, "#010b")[2:]]


BMat8.__repr__ = lambda x: cppyy.gbl.libsemigroups.detail.to_string(x)
__unwrap(BMat8, BMat8.rows, lambda x: [__bits(ord(y)) for y in x])


def BooleanMat(mat):
    out = std.vector(std.vector("bool"))()
    for row in mat:
        v = std.vector("bool")()
        for x in row:
            v.push_back(x)
        out.push_back(v)
    bmat_type = cppyy.gbl.libsemigroups.BMatHelper(len(mat)).type
    bmat_type.__pow__ = __generic_pow
    return bmat_type(out)


# Partial perms


def PartialPerm(*args):
    if len(args) == 1:
        pperm_type = cppyy.gbl.libsemigroups.PPermHelper(len(args[0])).type
        ret = pperm_type(args[0])
    elif len(args) == 3:
        if not isinstance(args[2], int):
            raise TypeError("the third parameter must be an integer")
        pperm_type = cppyy.gbl.libsemigroups.PPermHelper(args[2]).type
        ret = pperm_type(*args)
    pperm_type.__pow__ = __generic_pow
    pperm_type.__mul__ = lambda self, other: Product(self, other)
    pperm_type.dom = lambda x: [y for y in range(Degree(x)) if ord(x[y]) != 255]
    pperm_type.ran = lambda x: [ord(x[y]) for y in range(Degree(x)) if ord(x[y]) != 255]
    pperm_type.__repr__ = lambda x: "PartialPerm(%s, %s, %d)" % (
        x.dom(),
        x.ran(),
        Degree(x),
    )
    pperm_type.rank = pperm_type.crank
    return ret


# Untested


def Transformation(images):
    out = cppyy.gbl.libsemigroups.Transf(len(images)).type(images)
    # out.__class__.__repr__ = lambda self: cppyy.gbl.std.to_string(self)
    return out


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
