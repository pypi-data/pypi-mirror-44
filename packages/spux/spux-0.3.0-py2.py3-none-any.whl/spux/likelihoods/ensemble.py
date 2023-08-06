# # # # # # # # # # # # # # # # # # # # # # # # # #
# Ensemble class for processing of multiple models in likelihoods
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from copy import deepcopy as copy

from ..utils.setup import setup
from ..utils.seed import Seed
from ..io.format import compactify

class Ensemble (object):
    """Class of type ensemble operates set of particles (user models)."""

    @property
    def name (self):

        return type(self).__name__

    # constructor requires dynamical system 'model' including its 'input' and 'parameters', and the 'error' distribution for prediction validation
    def __init__(self, model, input, parameters, error, log=1):

        self.model = model
        self.input = input
        self.parameters = parameters
        self.error = error
        self.log = log

        self.sandboxing = model.sandboxing

        # label for sandboxes
        self.label = "P%04d"

        # seeds for iterations
        self.seeds = {}

        self.task = self.model

    # setup ensemble
    def setup (self, sandbox=None, verbosity=1, seed=Seed(), informative=0, trace=0):
        """Do a standardized setup."""

        # standardized setup
        setup (self, sandbox, verbosity, seed, informative, trace)

    # setup 'index' particle (including its sandbox and seed)
    def prepare (self, index):
        """Prepare particles sandboxes and seeds."""

        if not self.sandboxing:
            sandbox = None
        else:
            label = self.label % index
            sandbox = self.sandbox.spawn (label)
        seed = self.seeds [self.iteration] .spawn (index, name='PF index')
        self.particles [index] .setup (sandbox, self.verbosity - 2, seed, self.informative, self.trace)

    # stash 'index' particle
    def stash (self, index, suffix='-stash'):
        """ Stash (move) particle key and sandbox by appending the specified suffix."""

        if self.sandboxing:
            self.particles [index] .sandbox.stash ()

        key = str (index) + suffix

        self.particles [key] = self.particles [index]
        del self.particles [index]

        return key

    # fetch particle from 'key' stash and move it to a specified index
    def fetch (self, key, index, suffix='-stash'):
        """ Fetch (move) particle key and sandbox by removing the specified suffix and moving to a specified index."""

        self.particles [index] = self.particles [key]
        del self.particles [key]

        if self.sandboxing:
            label = self.label % index
            self.particles [index] .sandbox.fetch (tail = label)

    # remove 'index' particle (including its sandbox, if trace=0)
    def remove (self, index, trace=0):
        """Prepare particles sandboxes and seeds."""

        self.particles [index] .exit ()
        if self.sandboxing and not trace:
            self.particles [index] .sandbox.remove ()
        del self.particles [index]

    # initialize ensemble
    def init (self, indices):
        """Initializae ensemble."""

        if self.verbosity:
            print("Ensemble init with root", compactify (self.root))

        # set iteration
        self.iteration = 0

        # set iteration seed
        self.seeds [self.iteration] = self.seed.spawn (self.iteration, name='PF iteration')

        # construct particles and sandboxes
        self.particles = {}
        for index in indices:
            self.particles [index] = copy (self.model)
            self.prepare (index)

        # initialize particles with specified parameters
        for index, particle in self.particles.items ():
            particle.init (self.input, self.parameters)

    # advance ensemble state to next iteration
    def advance (self):
        """Advance ensemble state to next iteration."""

        if self.verbosity:
            print("Ensemble advance with root", compactify (self.root))

        # set iteration
        self.iteration += 1

        # set iteration seed
        self.seeds [self.iteration] = self.seed.spawn (self.iteration, name='PF iteration')

    # run all particles in ensemble up to the specified time
    def run (self, time):
        """Run all particles in ensemble up to the specified time."""

        self.time = time

        if self.verbosity:
            print("Ensemble run with root", compactify (self.root))

        self.predictions = {}
        for index, particle in self.particles.items ():
            self.predictions [index] = particle.run (time)

        return self.predictions

    # compute errors for all particles in ensemble
    def errors (self, data):
        """Compute errors for all particles in ensemble."""

        if self.verbosity:
            print("Ensemble errors with root", compactify (self.root))

        # transform data if error requires so
        if hasattr (self.error, 'transform'):
            if self.verbosity:
                print (' -> Data will be transformed before error computations.')
            data = self.error.transform (data, self.parameters)

        errors = {}
        for index, particle in self.particles.items():
            distribution = self.error.distribution (self.predictions [index], self.parameters)
            if self.verbosity >= 2:
                if hasattr (self.error, 'transform'):
                    predictions = self.error.transform (self.predictions [index], self.parameters)
                else:
                    predictions = self.predictions [index]
                print (' -> Predictions (particle %05d): ' % index, predictions)
                print (' -> Data (particle %05d): ' % index, data [distribution.labels])
            if self.log:
                errors [index] = distribution.logpdf (data [distribution.labels])
            else:
                errors [index] = distribution.pdf (data [distribution.labels])

        return errors

    # cleanup
    def exit (self):
        """Cleanup Ensemble object."""

        if self.verbosity:
            print("Ensemble exit with root", compactify (self.root))

        for index in list (self.particles.keys ()):
            self.remove (index, self.trace)

        # take out trash
        self.particles = None
