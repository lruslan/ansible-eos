#!/usr/bin/env python

import os
import sys


def install():
    if "install" in sys.argv:
        return True
    else:
        return False

# Use the following to build ansible-eos modules
if install() and os.environ.get('READTHEDOCS'):
    print 'This python install only builds the module documentation.'
    from subprocess import Popen
    proc = Popen(['make', 'modules'], cwd='docs/')
    (_, err) = proc.communicate()
    return_code = proc.wait()

    if return_code or err:
        raise ('Failed to make modules.(%s:%s)' % (return_code, err))
