# # # # # # # # # # # # # # # # # # # # # # # # # #
# Cloudpickle-based dumper class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import cloudpickle
import shutil

def mkdir (directory, fresh=0):
    if fresh and os.path.exists (directory):
        shutil.rmtree (directory)
    if not os.path.exists (directory):
        os.mkdir (directory)

def dump (obj, name="dump.dat", directory="output", verbose=0):
    """
    Writes *obj* as Python cloudpickle to given file with name *name* and directory *directory*.
    Creates target directory if this does not exist yet.
    If the file already exists, it is deleted before writing to prevent any corruption.

    returns: None
    """

    mkdir (directory)
    path = os.path.join (directory, name)
    if os.path.exists (path):
        shutil.rmtree (path)
    if verbose:
        print ('DUMP:', path)
    with open (path, "wb") as f:
        cloudpickle.dump (obj, f)

    return '%.1f GB' % (os.path.getsize (path) / (1024 ** 3))
