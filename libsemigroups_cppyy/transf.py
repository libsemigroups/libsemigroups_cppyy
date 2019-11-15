"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/transf.html

for further details.
"""

import cppyy

import libsemigroups_cppyy.detail as detail
from libsemigroups_cppyy.adapters import Degree, Product


def Transformation(images):
    transf_type = cppyy.gbl.libsemigroups.TransfHelper(len(images)).type
    transf_type.__pow__ = detail.generic_pow
    transf_type.__mul__ = Product
    transf_type.__repr__ = lambda x: "Transformation(%s)" % (x.ran())
    transf_type.ran = lambda x: images
    return transf_type(images)