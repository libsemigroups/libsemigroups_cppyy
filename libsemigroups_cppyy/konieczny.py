"""
This file contains the interface to the Konieczny class template in
libsemigroups; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__konieczny.html

for further details.
"""

import cppyy

from libsemigroups_cppyy.detail import RandomAccessRange


def Konieczny(*args):
    if len(args) == 1 and isinstance(args[0], list):
        gens = args[0]
    else:
        gens = [*args]

    types = {type(g) for g in gens}
    if len(types) > 1:
        raise ValueError("the generators are not all of the same type")
    # TODO the following can result in python seg faulting if it isn't possible
    # to create an object of this type. Fix this somehow?
    k_type = cppyy.gbl.libsemigroups.Konieczny(types.pop())

    def repr_method(self):
        try:
            element_type_str = "<%s>" % type(self).element_type.short_name
        except AttributeError:
            element_type_str = ""
        plural = "s" if self.number_of_generators() > 1 else ""
        return "<Konieczny{0} object with {1} generator{2} at {3}>".format(
            element_type_str, self.number_of_generators(), plural, hex(id(self))
        )

    k_type.__repr__ = repr_method

    k_type.D_classes = lambda self: RandomAccessRange(
        self.cbegin_D_classes(), self.cend_D_classes()
    )
    return k_type(gens)
