"""
This file contains the interface to libsemigroups actions; see

    https://libsemigroups.readthedocs.io/en/latest/action.html

for further details.
"""

import cppyy


def RightAction(element_type, point_type):
    ImageRightAction = cppyy.gbl.libsemigroups.ImageRightAction(
        element_type, point_type
    )
    return cppyy.gbl.libsemigroups.RightAction(
        element_type, point_type, ImageRightAction
    )()


def LeftAction(element_type, point_type):
    ImageLeftAction = cppyy.gbl.libsemigroups.ImageLeftAction(
        element_type, point_type
    )
    return cppyy.gbl.libsemigroups.LeftAction(
        element_type, point_type, ImageLeftAction
    )()
