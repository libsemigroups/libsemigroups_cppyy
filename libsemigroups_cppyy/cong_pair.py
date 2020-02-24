"""
This file contains the interface to libsemigroups adapters; see

    https://libsemigroups.readthedocs.io/en/latest/_generated/libsemigroups__congruencebypairs.html
for further details.
"""

import cppyy

# I'm not sure why this is necessary, but I couldn't get CongruenceByPairs to
# work without it. JDM
cppyy.cppdef("""
        template <typename T>
        libsemigroups::CongruenceByPairs<typename T::element_type> make(libsemigroups::congruence_type type, T const& fp) {
            return libsemigroups::CongruenceByPairs<typename T::element_type>(type, fp);
        }""")

def CongruenceByPairs(t, S):
    if t == "right":
        pj = cppyy.gbl.libsemigroups.congruence_type.right
    elif t == "left":
        pj = cppyy.gbl.libsemigroups.congruence_type.left
    elif t == "twosided":
        pj = cppyy.gbl.libsemigroups.congruence_type.twosided
    else:
        raise TypeError("Expected one of \"right\", \"left\", or \"twosided\"")
    cp_type = cppyy.gbl.libsemigroups.CongruenceByPairs(type(S).element_type)
    return cppyy.gbl.make[type(S)](pj, S)
