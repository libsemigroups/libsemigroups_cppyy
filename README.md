# libsemigroups_cppyy

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/libsemigroups/libsemigroups_cppyy/master?filepath=demo.ipynb)
[![Build Status](https://travis-ci.org/libsemigroups/libsemigroups_cppyy.svg?branch=master)](https://travis-ci.org/libsemigroups/libsemigroups_cppyy)

libsemigroups_cppyy is an experimental package for using the C++ library
[libsemigroups](https://github.com/james-d-mitche)
in python via [cppyy](https://cppyy.readthedocs.io/en/latest/).

## Installation

Install
[libsemigroups](https://github.com/james-d-mitchell/libsemigroups/),
e.g. via its sources or conda package.

Then, for a normal install, run:

    pip install .

For a developer install, run instead:

    pip install .

This will install cppyy, etc. Not that it includes llvm, cling, etcm
and thus takes quite some time to compile.

## Setup

Somehow cppyy currently has trouble libsemigroups dynamic library. On
my system I need to do:

    export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

before running python.

