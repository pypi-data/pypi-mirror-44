# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base model class
# All class methods can be extended by inheriting and overwriting
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import cloudpickle

from ..utils.setup import setup
from ..utils.seed import Seed
from ..io.report import report

# List of Model class variables (identical for all instances)
# that could be modified in the custom constructor of the this inherited base class
# self.sandboxing - enable (set to 1), the default option, or disable (set to 0) sandboxing (see below for self.sandbox () usage)

# List of Model instance varialbles (different for each instance) set by 'setup ()' and available in all other methods:
# self.sandbox () - path to an isolated sandbox directory (if self.sandboxing == 1)
# self.verbosity - a integer indicating verbosity level for 'print ()' intensity management
# self.seed () - a list containing all hierarchical seeds
# self.seed.cumulative () - a (large) integer seed obtained by combining all hierarchical seeds
# self.rng - numpy.random.RandomState (self.seed ()) object for use as 'random_state' in the scipy.stats distributions

class Model (object):
    """Template class for users' Models."""

    # sandboxing enabled by default
    sandboxing = 1

    @property
    def name (self):

        return type(self).__name__

    @property
    def evaluations (self):

        return 1

    # attach an executor
    def attach (self, executor):
        """Attach an executor."""

        report (self, 'attach')

        self.executor = executor
        self.executor.setup (self)
        methods = ['connect', 'call', 'resample', 'disconnect']
        self.executor.capabilities (methods)

    # setup model using specified 'sandbox', 'verbosity' and 'seed'
    # setup is called before 'init (...)' and before/after (i.e. two identical calls to allow flexibility in models) 'load (...)'
    def setup (self, sandbox=None, verbosity=1, seed=Seed(), informative=0, trace=0):
        """Setup model using specified 'sandbox', 'verbosity' and 'seed'; also propage 'informative' and 'trace' flags."""

        setup (self, sandbox, verbosity, seed, informative, trace)

        # OPTIONAL: inherit this base class and write a custom 'setup (...)' method
        # where you MUST additionally execute base method by calling:
        # 'Model.setup (self, sandbox, verbosity, seed, informative, trace)'

        # ADVICE: create here all needed dynamical links to your model (loaded DLLs, Java Virtual Machine, etc.)
        # RATIONALE: 'model.load (...)' could be called immediately after 'model.setup (...)',
        # i.e. without calling model.init (...) or model.run (...) beforehand
        # NOTE: immediately after 'model.load (...)', an ADDITIONAL 'model.setup (...)' is called

    # initialize model using specified 'input' and 'parameters'
    def init (self, input, parameters):
        """Initialize model using specified 'input' and 'parameters'."""

        report (self, 'init', extras = { 'input' : input, 'parameters' : parameters })

        # inherit this base class and write a custom 'init (...)' method
        # you can additionally execute base method by
        # 'Model.init (self, input, parameters)'

        # if sandboxing is enabled, one could copy in all needed files
        # from a specified self.inputpath (to be set in constructor) using
        # 'self.sandbox.copyin (self.inputpath)'

    # run model up to specified 'time' and return the prediction
    def run (self, time):
        """Run model up to specified 'time' and return the prediction."""

        report (self, 'run')

        # inherit this base class and write a custom 'run (...)' method
        # you can additionally execute base method by 'Model.run (self, time)'

        # to return annotated results, use 'annotate' from spux.utils.annotate, e.g.
        # (here you can also return additional auxiliary (not present in the datasets) prediction variables,
        # such as system energy, latent (hidden) stochastic parameters, etc.)
        # return annotate (y, ['y'], time)

    # finalize model
    def exit (self):
        """Finalize model."""

        report (self, 'exit')

        # OPTIONAL: inherit this base class and write a custom 'exit (...)' method
        # you can additionally execute base method by 'Model.exit (self)'

    # save current model into its state
    # this is a fully functional method for pure Python models
    # OPTIONAL: inherit this base class and write a custon 'save (...)' method for other models
    # you can use helper routines in spux/drivers/ - check their sample usage in examples/
    def save (self):
        """Save the whole model into 'state'."""

        report (self, 'save')

        state = cloudpickle.dumps (self.__dict__)
        return state

    # load specified model from its state
    # this is a fully functional method for pure Python models
    # OPTIONAL: inherit this base class and write a custon 'load (...)' method for other models
    # you can use helper routines in spux/drivers/ - check their sample usage in examples/
    def load (self, state):
        """Load the whole model previously saved in 'state'."""

        report (self, 'load')

        self.__dict__ = cloudpickle.loads (state)

        # if sandboxing is enabled, one could copy in all needed files
        # from a specified self.inputpath (to be set in constructor) using
        # 'self.sandbox.copyin (self.inputpath)'

    # construct a data container for model state with a specified size
    # this is a functional method for pure Python models
    # OPTIONAL: inherit this base class and write a custon 'state (...)' method for other models
    # you can use helper routines in spux/drivers/ - check their sample usage in examples/
    def state (self, size):
        """Construct a data container for model state with a specified size."""

        return bytearray (size)
