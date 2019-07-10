# Copyright 2019 Gradient Health Inc. All Rights Reserved.
# Author: Marcelo Lerendegui <marcelo@gradienthealth.io>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Setup for pip package."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.dist import Distribution

import os
import sysconfig
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

import tensorflow as tf

tf_L = tf.sysconfig.get_link_flags()[0][2::]
tf_l = tf.sysconfig.get_link_flags()[1][2::]

tf_I = tf.sysconfig.get_compile_flags()[0][2::]
tf_D = tf.sysconfig.get_compile_flags()[1][2::]

tf_decode_dicom_ext = Extension(
    'gradient_decode_dicom.python.ops._decode_dicom_ops',
    define_macros=[
        ('HAVE_CONFIG_H', None),
        ('USE_STD_CXX_INCLUDES', None),
        ('HAVE_CXX11', None),
        (tf_D, None),
    ],
    include_dirs=['/usr/local/include', tf_I],
    libraries=[
        tf_l,
        'dcmjpeg',
        'dcmjpls',
        'dcmdata',
        'dcmimgle',
        'dcmimage',
        'oflog',
        'ofstd',
        'z',
        'm',
        'rt',
        'pthread',
    ],
    library_dirs=['/usr/local/lib', tf_L, ],
    extra_compile_args=['-fPIC', '-w', '-O2'],
    language='c++11',
    sources=[
        'gradient_decode_dicom/cc/kernels/decode_dicom_data.cc',
        'gradient_decode_dicom/cc/ops/decode_dicom_data_op.cc',
        'gradient_decode_dicom/cc/kernels/decode_dicom_image.cc',
        'gradient_decode_dicom/cc/ops/decode_dicom_image_op.cc'
    ]
)

deps_dcmtk = [
    '-ldcmjpeg',
    '-ldcmjpls',
    '-ldcmdata',
    '-ldcmimgle',
    '-ldcmimage',
    '-loflog',
    '-lofstd',
]

deps_other = [
    '-lz',
    '-lm',
    '-lrt',
    '-lpthread',
]


def get_ext_filename_without_platform_suffix(filename):
    print(filename)
    name, ext = os.path.splitext(filename)
    ext_suffix = sysconfig.get_config_var('SO')

    if ext_suffix == ext:
        return filename

    ext_suffix = ext_suffix.replace(ext, '')
    idx = name.find(ext_suffix)

    if idx == -1:
        return filename
    else:
        return name[:idx] + ext


class BuildExtWithoutPlatformSuffix(build_ext, object):
    def get_ext_filename(self, ext_name):
        filename = super(BuildExtWithoutPlatformSuffix,
                         self).get_ext_filename(ext_name)
        return get_ext_filename_without_platform_suffix(filename)


def CheckDeps():
    with open(os.devnull, 'w') as devnull:
        print("Checking OS Compatibility")
        print("{} ........".format(platform.system()), end=" ")
        if platform.system() == "Windows":
            raise RuntimeError("ERROR: Windows not supported")
        print(" OK")

        print("Checking Library Dependencies")
        print("Checking DCMTK")
        for lib in deps_dcmtk:
            print("Library lib{} installed ........".format(lib[2::]), end=" ")
            try:
                s = subprocess.check_output(
                    ['g++ test.cc {}'.format(lib)],
                    stderr=devnull,
                    shell=True
                )
            except OSError:
                print(
                    "ERROR: Missing required library: {}\n TO FIX THIS, INSTALL DCMTK-DEV".format(
                        lib)
                )
                raise RuntimeError(
                    "ERROR: Missing required library: {}\n TO FIX THIS, INSTALL DCMTK-DEV".format(
                        lib)
                )
            print("OK")

        print("Checking other libs")
        for lib in deps_other:
            print("Library lib{} installed ........".format(lib[2::]), end=" ")
            try:
                s = subprocess.check_output(
                    ['g++ test.cc {}'.format(lib)],
                    stderr=devnull,
                    shell=True
                )
            except OSError:
                print(
                    "ERROR: Missing required library: {}".format(
                        lib)
                )
                raise RuntimeError(
                    "ERROR: Missing required library: {}".format(
                        lib)
                )
            print("OK")


class BinaryDistribution(Distribution):
    """This class is needed in order to create OS specific wheels."""

    def has_ext_modules(self):
        return True


CheckDeps()

setup(
    name='gradient_decode_dicom',
    version='0.0.4',
    description=(
        'Gradient Decode DICOM is a dicom image and tag reader op for TensorFlow'),
    author='Marcelo Lerendegui',
    author_email='marcelo@gradienthealth.io',
    # Contained modules and scripts.
    packages=find_packages(),
    install_requires=[
        'tensorflow >= 1.12.0',
    ],
    # Add in any packaged data.
    include_package_data=True,
    zip_safe=False,
    distclass=BinaryDistribution,
    # PyPI package information.
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    license='Apache 2.0',
    keywords='tensorflow dicom custom op machine learning',
    cmdclass={'build_ext': BuildExtWithoutPlatformSuffix},
    ext_modules=[tf_decode_dicom_ext],
)
