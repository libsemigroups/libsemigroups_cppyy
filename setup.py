'''
A minimal cppyy wrapper for the libsemigroups C++ library.
'''
from setuptools import find_packages, setup

setup(name='libsemigroups_cppyy',
      version='0.0.0',
      description='A minimal cppyy wrapper for the libsemigroups C++ library',
      url='http://github.com/james-d-mitchell/libsemigroups_cppyy',
      author='James D. Mitchell',
      author_email='jdm3@st-andrews.ac.uk',
      license='GPL3',
      install_requires=['cppyy'],
      packages=find_packages(exclude=['tests']),
      zip_safe=False)
