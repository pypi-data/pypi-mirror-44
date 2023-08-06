# # # # # # # # # # # # # # # # # # # # # # # # # #
# Cloudpickle-based loader class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import cloudpickle
import os
import glob
import numpy

def load (name="samples-*.dat", directory="output", verbosity=1, interactive=True, last=False):
    """Load SPUX binary output file."""

    path = os.path.join (directory, name)
    paths = sorted (glob.glob (path))
    if last:
        paths = [paths [-1]]
    sizes = [ os.path.getsize (p) / (1024 ** 3) for p in paths ]
    size = numpy.sum (sizes)
    print ('  : -> Size of all \'%s\' files to be loaded (minimum requirement for RAM): %.1f GB' % (path, size))

    if size > 4 and interactive:
        print ('  : -> Proceed? [press ENTER if yes, and enter \'n\' if not]')
        reply = input ('  : -> ')
        if reply == 'n':
            print ('  : -> Canceling.' % size)
            yield None
        else:
            print ('  : -> Proceeding.' % size)

    for index, path in enumerate (paths):
        with open (path, "rb") as f:
            result = cloudpickle.load (f)
            if verbosity:
                print ('  : -> Loaded %s with length %d and size: %.1f GB' % (path, len (result), sizes [index]))
            yield result

def last (name="samples-*.dat", directory="output", verbosity=1, interactive=True):
    """Load the last sample batch from the SPUX binary output files."""

    return [info for info in load (name, directory, verbosity, interactive, last=1)] [0] [-1]

def read_params_types (paramtypefl=None):
    """Read file with parameter types"""

    if paramtypefl is None or not os.path.exists (paramtypefl):
        return None

    if paramtypefl is not None:
        all_params = {}
        with open(paramtypefl) as fl:
            for line in fl:
                (key, val) = line.split()
                all_params[key] = val

    return all_params
