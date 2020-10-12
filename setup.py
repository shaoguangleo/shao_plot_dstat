#! /usr/bin/env python3
"""
Setup for shao_plot_dstat
"""
import os
import sys
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    """Read a file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    """Get the version number of shao_plot_dstat"""
    import plotdstat
    return plotdstat.__version__


reqs = ['scipy>=0.16',
        'healpy >=1.10',
        'six>=1.11']

if sys.version_info < (3,0):
    reqs.append('numpy>=1.16,<1.18')
    reqs.append('astropy>=2.0, <3')
    reqs.append('lmfit>=0.9.2, <1')
else:
    reqs.append('numpy>=1.16')
    reqs.append('astropy>=2.0')
    reqs.append('lmfit>=0.9.2')

data_dir = 'test'

setup(
    name="shao_plot_dstat",
    version=get_version(),
    author="Shaoguang Guo",
    author_email="sgguo@shao.ac.cn",
    description="A tiny program used to plot dstat output.",
    url="https://github.com/shaoguangleo/shao_plot_dstat",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['shao_plot_dstat'],
    install_requires=reqs,
    #scripts=['scripts/aegean', 'scripts/BANE', 'scripts/SR6', 'scripts/AeRes', 'scripts/MIMAS'],
    #data_files=[('AegeanTools', [os.path.join(data_dir, 'MOC.fits')]) ],
    python_requires='>=3.7',
    #setup_requires=['pytest-runner'],
    #tests_require=['pytest', 'nose']
)
