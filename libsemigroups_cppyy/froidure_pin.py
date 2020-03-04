"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__froidurepin.html

for further details.
"""

import cppyy
import libsemigroups_cppyy.detail as detail
import networkx

def install_froidure_pin_methods(froidure_pin_type):
    detail.unwrap(froidure_pin_type, froidure_pin_type.factorisation, lambda x:
            list(x))
    detail.unwrap_int(froidure_pin_type, froidure_pin_type.left)
    detail.unwrap_int(froidure_pin_type, froidure_pin_type.right)
    detail.unwrap_int(froidure_pin_type, froidure_pin_type.nr_generators)
    detail.unwrap(froidure_pin_type, froidure_pin_type.factorisation, lambda x: list(x))

def FroidurePin(*args):
    if len(args) == 1 and isinstance(args[0], list):
        gens = args[0]
    else:
        gens = [*args]

    types = {type(g) for g in gens}
    if len(types) > 1:
        raise ValueError("the generators are not all of the same type")
    froidure_pin_type = cppyy.gbl.libsemigroups.FroidurePin(types.pop())
    install_froidure_pin_methods(froidure_pin_type)
    return froidure_pin_type(gens)

def right_cayley(S):
    G=networkx.DiGraph()
    for i in range(S.size()):
        for j in range(S.nr_generators()):
            G.add_edge(str(S.factorisation(i)),str(S.factorisation(S.right(i,j))))
    return G

def left_cayley(S):
    G=networkx.DiGraph()
    for i in range(S.size()):
        for j in range(S.nr_generators()):
            G.add_edge(str(S.factorisation(i)),str(S.factorisation(S.left(i,j))))
    return G
