# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base likelihood class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from ..utils.setup import setup
from ..utils.seed import Seed
from ..executors.serial import Serial

class Likelihood (object):
    """Base class for objects that can be classified as likelihoods in a mathematical perspective."""

    @property
    def name (self):

        return type(self).__name__

    # assign required components to likelihood
    def assign (self, model, error=None, data=None, input=None):
        """Assign required components to likelihood."""

        self.model = model
        self.error = error
        self.data = data
        self.input = input

        self.sandboxing = self.model.sandboxing
        self.task = self.model

        if hasattr (self, 'executor'):
            self.executor.setup (self)
        else:
            self.attach (Serial ())

    # attach an executor
    def attach (self, executor):
        """Attach an executor to likelihood."""

        self.executor = executor
        self.executor.setup (self)
        self.executor.capabilities (['map', 'report'])

    # setup likelihood
    def setup (self, sandbox=None, verbosity=1, seed=Seed(), informative=0, trace=0):
        """Do standardized setup."""

        # standardized setup
        setup (self, sandbox, verbosity, seed, informative, trace)
