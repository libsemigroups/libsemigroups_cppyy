"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__froidurepin.html

for further details.
"""

import cppyy


def FroidurePin(*args):
    if len(args) == 1 and isinstance(args[0], list):
        gens = args[0]
    else:
        gens = [*args]

    types = {type(g) for g in gens}
    if len(types) > 1:
        raise ValueError("the generators are not all of the same type")
    froidure_pin_type = cppyy.gbl.libsemigroups.FroidurePin(types.pop())
    return froidure_pin_type(gens)
