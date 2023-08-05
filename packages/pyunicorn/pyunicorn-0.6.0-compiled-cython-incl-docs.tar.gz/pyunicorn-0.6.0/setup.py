#!/usr/bin/env python

# This file is part of pyunicorn.
# Copyright (C) 2008--2019 Jonathan F. Donges and pyunicorn authors
# URL: <http://www.pik-potsdam.de/members/donges/software>
# License: BSD (3-clause)


from setuptools import setup
from setuptools.extension import Extension

import numpy as np

try:
    from Cython.Build import cythonize
    CYTHON = True
except ImportError:
    CYTHON = False

extensions = [
    Extension(
        f'pyunicorn.{pkg}._ext.numerics',
        sources=[f"pyunicorn/{pkg}/_ext/{pre}numerics.{ext}" for pre, ext in
                 [('', 'pyx') if CYTHON else ('', 'c')]],
        include_dirs=[np.get_include()],
        extra_compile_args=['-O3', '-std=c99'])
    for pkg in ['climate', 'core', 'funcnet', 'timeseries']]

if CYTHON:
    extensions = cythonize(extensions, compiler_directives={
            'language_level': 3, 'embedsignature': True,
            'boundscheck': False, 'wraparound': False,
            'initializedcheck': False, 'nonecheck': False})

setup(
    name='pyunicorn',
    version='0.6.0',
    description="Unified complex network and recurrence analysis toolbox",
    long_description="Advanced statistical analysis and modeling of \
general and spatially embedded complex networks with applications to \
multivariate nonlinear time series analysis",
    license='BSD',
    author='Jonathan F. Donges',
    author_email='donges@pik-potsdam.de',
    url='http://www.pik-potsdam.de/~donges/pyunicorn/',
    keywords='complex networks statistics modeling time series analysis \
nonlinear climate recurrence plot surrogates spatial model',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research'],
    provides=['pyunicorn'],
    packages=['pyunicorn', 'pyunicorn.core', 'pyunicorn.core._ext',
              'pyunicorn.climate', 'pyunicorn.climate._ext',
              'pyunicorn.timeseries', 'pyunicorn.timeseries._ext',
              'pyunicorn.funcnet', 'pyunicorn.funcnet._ext',
              'pyunicorn.eventseries', 'pyunicorn.utils'],
    scripts=[],
    ext_modules=extensions,
    install_requires=open('requirements.txt', 'r').read().split('\n'),
    platforms=['all']
)
