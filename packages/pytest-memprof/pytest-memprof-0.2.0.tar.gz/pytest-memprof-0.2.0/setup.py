#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-memprof',
    version='0.2.0',
    author='Uwe Schmitt',
    author_email='uwe.schmitt@id.ethz.ch',
    maintainer='Uwe Schmitt',
    maintainer_email='uwe.schmitt@id.ethz.ch',
    license='BSD-3',
    url='https://sissource.ethz.ch/schmittu/pytest-memprof',
    description='Estimates memory consumption of test functions',
    long_description=read('README.rst'),
    python_requires='>=3.5',
    py_modules=['pytest_memprof'],
    install_requires=['pytest>=3.1.1', 'psutil'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'memprof = pytest_memprof',
        ],
    },
    zip_safe=False,
)
