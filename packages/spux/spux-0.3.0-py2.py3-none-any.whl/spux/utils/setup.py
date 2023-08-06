# process setup
import numpy

from .sandbox import Sandbox
from ..io.report import report

def setup (instance, sandbox, verbosity, seed, informative, trace):
    """Do standardized setup on 'instance'."""

    # set verbosity
    instance.verbosity = verbosity if verbosity >= 0 else 0

    # standartized report
    report (instance, 'setup')

    # make a default sandbox if sandboxing is required
    if instance.sandboxing and sandbox is None:
        if instance.verbosity:
            print ('  : -> WARNING: No \'sandbox\' not specified in %s, but sandboxing is enabled.' % instance.name)
            print ('  : -> Setting sandbox to a default \'sandbox = Sandbox ()\' in %s.', instance.name)
        instance.sandbox = Sandbox ()
    else:
        instance.sandbox = sandbox

    # set seed and rng
    if seed is not None:
        instance.seed = seed
        instance.rng = numpy.random.RandomState (instance.seed ())

    # set informativity
    instance.informative = informative

    # set trace
    instance.trace = trace

    # report
    if instance.verbosity:
        print ("  : -> %s verbosity: %s" % (instance.name, instance.verbosity))
        if hasattr (instance, 'sandboxing') and instance.sandboxing:
            print ("  : -> %s sandbox: %s" % (instance.name, instance.sandbox))
        if hasattr (instance, 'seed') and instance.seed is not None:
            print ("  : -> %s seed: %s" % (instance.name, instance.seed))
        if hasattr (instance, 'infos'):
            print ("  : -> %s informative: %s" % (instance.name, instance.informative))
