# # # # # # # # # # # # # # # # # # # # # # # # # #
# Sandbox class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import sys
import shutil
import errno

from ..io.format import plain

class Sandbox (object):
    """Class to construct safe environments (sandboxes) where to run independent instances of user model."""

    # constructor
    def __init__ (self, path='sandbox', target=None):

        self.target = target
        self.exists = 0

        if path is None and target is None:
            print (" :: ERROR: In sandbox, please specify a path to your shared working directory.")
            print ("  : -> Alternatively, please specify a name for the symlink as path and set target to the shared scratch directory.")
            print ("  : -> For clusters, please set path to None set target to the local (non-shared) scratch directory.")
            sys.exit ()

        # 'shared' mode: just path
        elif target is None:
            self.mode = 'shared'
            self.path = path
            self.tentative = 0
            self.make ()

        # 'symlink' mode: path as a symlink to a target directory
        elif path is not None and target is not None:
            self.mode = 'symlink'
            self.name = path
            self.path = target
            self.tentative = 0
            self.make ()

        # 'local' mode: path is None, only a local (non-shared) a target directory is specified
        elif path is None:
            self.mode = 'local'
            self.path = target
            self.tentative = 1

        # set cache directory to be in the root of the parent sandbox directory
        # notice, that this might mean no caching in the root sandbox
        try:
            parentpath, = os.path.split (self.path)
            self.cachepath = os.path.join (parentpath, '.cache')
        except:
            self.cachepath = None

    def make (self):
        """Make an actual sandbox directory."""

        if self.exists:
            return

        if not os.path.exists (self.path):
            os.makedirs (self.path, exist_ok = True)

        # 'symlink' mode: path as a symlink to a target directory
        if self.mode == 'symlink':
            try:
                os.symlink (self.target, self.name)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.remove (self.name)
                    os.symlink (self.target, self.name)
                else:
                    raise e

        self.exists = 1

    # get sandbox path (and create it, if necessary)
    def __call__ (self):
        """Get path to sandbox."""

        if not self.exists:
            self.make ()

        return self.path

    # get sandbox description
    def __str__ (self):
        """Get sandbox description."""

        return '%s%s' % (self.path, (' -> %s' % self.target) if self.target is not None else '')

    # spawn new sandbox
    def spawn (self, name):
        """Create new sandbox."""

        if not self.tentative:
            path = os.path.join (self.path, name)
            return Sandbox (path)

        else:
            path = None
            target = self.path + '_' + name
            return Sandbox (path, target)

    # copy all files from a given input directory to the sandbox
    def copyin (self, inputpath):
        """Copy all files from a given input directory to the sandbox."""

        # make sandbox if it does not exist yet
        if not self.exists:
            self.make ()

        # cache inputpath directory, if needed
        if self.cachepath is not None:
            sourcepath = self.cachepath + '-' + plain (inputpath)
            if not os.path.exists (sourcepath):
                shutil.copytree (inputpath, sourcepath)
        else:
            sourcepath = inputpath

        # remove directory
        shutil.rmtree (self.path)

        # copy all files
        shutil.copytree (sourcepath, self.path)

    # remove
    def remove (self):
        """Remove entire sandbox."""

        # remove entire sandbox
        if os.path.exists (self.path):
            shutil.rmtree (self.path)

        self.exists = 0

    # stash
    def stash (self, suffix='-stash'):
        """Stash (move) sandbox by appending the specified suffix."""

        path = self.path + suffix

        if os.path.exists (path):
            shutil.rmtree (path)

        if os.path.exists (self.path):
            os.rename (self.path, path)

        self.path = path

    # fetch
    def fetch (self, tail, suffix='-stash'):
        """Fetch (move) sandbox by removing the specified suffix and changing path end by a specified tail."""

        path = self.path [ : - (len (suffix) + len (tail))] + tail

        if os.path.exists (path):
            shutil.rmtree (path)

        if os.path.exists (self.path):
            os.rename (self.path, path)

        self.path = path
