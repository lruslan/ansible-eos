#!/usr/bin/env python

import os
import sys
import subprocess

# sys.path.insert(0, os.path.abspath('lib'))
VERSION = open('VERSION').read().split()[0].strip()

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def install():
    if "install" in sys.argv:
        return True
    else:
        return False


if install() and os.environ.get('READTHEDOCS'):
    print 'Customizing install for ReadTheDocs.org build servers...'
    from subprocess import Popen
    proc = Popen(['make', 'modules'], cwd='docs/')
    (_, err) = proc.communicate()
    return_code = proc.wait()

    if return_code or err:
        raise ('Failed to make modules.(%s:%s)' % (return_code, err))

# setup(name='ansible-eos',
#      version=VERSION,
#      description='Ansible role that provides modules for managing resources on Arista EOS nodes',
#      author='EOS+ Consulting Services',
#      author_email='eosplus-dev@arista.com',
#      url='https://github.com/arista-eosplus',
#      license='BSD-3',
#      install_requires=[],
#      package_dir={'': 'lib'},
#      data_files=[]
#      )
