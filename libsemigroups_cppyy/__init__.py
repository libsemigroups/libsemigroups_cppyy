"""
A minimal cppyy wrapper for the libsemigroups C++ library.

This module contains some minimal wrapping code to interact with the
libsemigroups C++ library:

    https://github.com/libsemigroups/libsemigroups

via cppyy:

    https://bitbucket.org/wlav/cppyy/

For this to work, libsemigroups must be installed on your computer (i.e. the
executables libsemigroups.1.dylib, libsemigroups.dylib, and libsemigroups.a
must be somewhere on your computer where cppyy can load it).
"""

import os
import pkgconfig

__LIBSEMIGROUPS_VERSION = "1.0.7"

if "PKG_CONFIG_PATH" not in os.environ:
    os.environ["PKG_CONFIG_PATH"] = ""

pkg_config_path = os.environ["PKG_CONFIG_PATH"].split(":")

if "/usr/local/lib/pkgconfig" not in pkg_config_path:
    os.environ["PKG_CONFIG_PATH"] += ":/usr/local/lib/pkgconfig"

if not pkgconfig.exists("libsemigroups"):
    raise ImportError("cannot locate libsemigroups library")
elif pkgconfig.installed("libsemigroups", "< " + __LIBSEMIGROUPS_VERSION):
    raise ImportError(
        "libsemigroups version {0} is required, found {1}".format(
            __LIBSEMIGROUPS_VERSION, pkgconfig.modversion("libsemigroups")
        )
    )

import cppyy
import sys

cppyy.gbl

path = os.environ["PATH"].split(":")
for d in path:
    if d.find("include") != -1:
        try:
            cppyy.add_include_path(d)
        except:
            pass

stderr, sys.stderr = sys.stderr, open(os.devnull, "w")
stdout, sys.stdout = sys.stdout, open(os.devnull, "w")
try:
    cppyy.load_library("libsemigroups.1")
except Exception:
    cppyy.load_library("libsemigroups")
sys.stderr = stderr
sys.stdout = stdout

cppyy.cppdef("#define FMT_HEADER_ONLY")
cppyy.cppdef("#define HPCOMBI_CONSTEXPR_FUN_ARGS")

cppyy.include("libsemigroups/action.hpp")
cppyy.include("libsemigroups/bmat8.hpp")
cppyy.include("libsemigroups/cong-pair.hpp")
cppyy.include("libsemigroups/element.hpp")
cppyy.include("libsemigroups/element-helper.hpp")
cppyy.include("libsemigroups/froidure-pin.hpp")
cppyy.include("libsemigroups/fpsemi.hpp")
cppyy.include("libsemigroups/kbe.hpp")
cppyy.include("libsemigroups/knuth-bendix.hpp")
cppyy.include("libsemigroups/schreier-sims.hpp")
cppyy.include("libsemigroups/report.hpp")

cppyy.gbl.libsemigroups

from cppyy.gbl.libsemigroups import ReportGuard

from libsemigroups_cppyy.action import LeftAction, RightAction
from libsemigroups_cppyy.bmat import *
from libsemigroups_cppyy.cong_pair import CongruenceByPairs
from libsemigroups_cppyy.digraph import ActionDigraph
from libsemigroups_cppyy.fpsemi import FpSemigroup
from libsemigroups_cppyy.froidure_pin import FroidurePin, right_cayley, left_cayley
from libsemigroups_cppyy.knuth_bendix import KnuthBendix
from libsemigroups_cppyy.perm import *
from libsemigroups_cppyy.pperm import *
from libsemigroups_cppyy.schreier_sims import SchreierSims
from libsemigroups_cppyy.transf import *

cppyy.add_include_path(__file__[: __file__.rfind(os.path.sep)])
cppyy.include("include/python_element.h")
from cppyy.gbl import PythonElement
