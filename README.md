# libsemigroups_cppyy

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/libsemigroups/libsemigroups_cppyy/master?filepath=demo.ipynb)
[![Build Status](https://travis-ci.org/libsemigroups/libsemigroups_cppyy.svg?branch=master)](https://travis-ci.org/libsemigroups/libsemigroups_cppyy)

libsemigroups_cppyy is an experimental package for using the C++ library
[libsemigroups](https://libsemigroups.readthedocs.io/en/latest/)
in python via [cppyy](https://cppyy.readthedocs.io/en/latest/).

## Installation

Install
[libsemigroups](https://github.com/libsemigroups/libsemigroups), via its sources or conda package.

By conda:
Add conda-forge to an installation of anaconda:

    conda config --add channels conda-forge
    
And then download libsemigroups, specifying the version (1.0.5)

    conda install libsemigroups=1.0.5

Then install cppyy and networkx via conda or pip:
    
    conda install cppyy
    conda install networkx

To use cppyy, note you will need gcc. 

Finally, for normal use, git clone this repository and then run:

    pip install .

Refer to demo.ipynb for more functionality. 


