# # # # # # # # # # # # # # # # # # # # # # # # # #
# Particle Filter likelihood class for a stochastic model
# Particle filtering based on
# Kattwinkel & Reichert, EMS 2017.
# Implementation described in
# Sukys & Kattwinkel, Proceedings of ParCo 2017,
# Advanced Parallel Computing, IOS Press, 2018.
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import scipy
import numpy

from ..utils.timing import Timing
from ..utils import transforms
from .likelihood import Likelihood
from .ensemble import Ensemble

numpy.seterr (divide = 'ignore')

class PF (Likelihood):
    """Particle Filter likelihood class for a stochastic model.

    Operates ensemble of particles.
    """

    # constructor
    def __init__ (self, particles=100, log=1, noresample=0):

        self.particles = particles
        self.log = log
        self.noresample = noresample

    @property
    def evaluations (self):

        if hasattr (self, 'task'):
            return self.particles * self.task.evaluations
        else:
            return self.particles

    # attach an executor
    def attach (self, executor):
        """Attach an executor."""

        self.executor = executor
        self.executor.setup (self)
        methods = ['connect', 'call', 'resample', 'disconnect']
        self.executor.capabilities (methods)

    # redraw particles based on errors
    def redraw (self, indices, logerrors, logscaling):
        """Redraw particles based on errors."""

        # compute probabilities for discrete distribution
        nans = numpy.isnan (logerrors)
        if logscaling == float ('-inf'):
            if self.verbosity:
                print(" :: WARNING: The sum of all particle errors is 0 (i.e., exp (-inf)).")
                print("  : -> This issue should have been mitigated already earlier.")
                print("  : -> Assigning equal probabilities to all particles.")
            probabilities = numpy.where (nans, 0, 1.0 / numpy.sum (~nans))
        else:
            probabilities = numpy.where (nans, 0, numpy.exp (logerrors - logscaling))

        # sample from discrete distribution
        choice = self.rng.choice (indices, size=self.particles, p=probabilities)

        # compute redraw rate
        redraw = len(set(choice)) / float(len(indices))

        return choice, redraw

    # evaluate/approximate likelihood of the specified parameters
    def __call__ (self, parameters):
        """Evaluate estimate of the likelihood for the specified parameters."""

        # verbose output
        if self.verbosity >= 2:
            print ("PF likelihood parameters:")
            print (parameters)

        # report a warning if resampling is disabled
        if self.noresample:
            print (" :: WARNING: \'noresample\' is specified in PF - use ONLY FOR DEVELOPMENT.")

        # start global timer
        timing = Timing ()
        timing.start ('evaluate')

        # construct ensemble task
        ensemble = Ensemble (self.model, self.input, parameters, self.error)

        # setup ensemble
        ensemble.setup (self.sandbox, self.verbosity - 2, self.seed, self.informative, self.trace)

        # initialize task ensemble in executor
        self.executor.connect (ensemble, indices = numpy.arange (self.particles))

        # initialize indices container
        indices = { 'prior' : {}, 'posterior' : {} }

        # initialize predictions container
        predictions = { 'prior' : {}, 'posterior' : {}, 'unique' : {} }

        # initialize weights container
        weights = {}

        # initialize errors containter
        errors = { 'prior' : {}, 'posterior' : {} }

        # initialize estimates container
        estimates = {}

        # initialize quality control container
        variances = {}

        # initialize container for source indices
        sources = {}

        # initialize traffic measurements container
        traffic = {}

        # initialize particle redraw rate measurements container
        redraw = {}

        # iterate over all data snapshots (times)
        for snapshot in self.data.index:

            if self.verbosity:
                print("Snapshot", snapshot)

            # reset indices
            indices ['prior'] [snapshot] = numpy.arange (self.particles)

            # run particles (models)
            if self.verbosity >= 2:
                print("Running particles (%s models)..." % self.task.name)

            predictions ['prior'] [snapshot] = transforms.pandify (self.executor.call ('run', args = [snapshot], flatten=1))
            if self.verbosity >= 2:
                print ("Prior (non-resampled) predictions:")
                print (predictions ['prior'] [snapshot])

            # compute errors
            if self.verbosity >= 2:
                print("Computing errors...")
            errors ['prior'] [snapshot] = transforms.numpify (self.executor.call ('errors', args = [self.data.loc [snapshot]], flatten=1))

            if self.verbosity >= 2:
                print("Prior (non-resampled) errors", errors ['prior'] [snapshot])

            # if all errors are NaNs - no further filtering is possible
            if all (numpy.isnan (errors ['prior'] [snapshot])):
                estimates [snapshot] = float ('nan')
                variances [snapshot] = float ('nan')
                if self.verbosity:
                    print (" :: WARNING: NaN estimate in the PF likelihood.")
                    print ("  : -> All error model distribution densities are NaN.")
                    print ("  : -> Stopping here and returning the infos as they are.")
                successful = False
                break

            # if all errors are '-inf's - no further filtering is possible
            if all (errors ['prior'] [snapshot] == float ('-inf')):
                estimates [snapshot] = float ('-inf') if self.log else 0
                variances [snapshot] = float ('nan')
                if self.verbosity:
                    print (" :: WARNING: '-inf' (i.e., log (0)) estimate in the PF likelihood.")
                    print ("  : -> All error model distribution densities are '-inf' (i.e., log (0)).")
                    print ("  : -> Stopping here and returning the infos as they are.")
                successful = False
                break

            # compute (log-)error estimates for the current snapshot
            nonnan = errors ['prior'] [snapshot] [~ numpy.isnan (errors ['prior'] [snapshot])]
            M = len (nonnan)
            logmean = scipy.special.logsumexp (nonnan) - numpy.log (M)
            mean = numpy.exp (logmean)
            estimates [snapshot] = logmean if self.log else mean
            if self.verbosity:
                print ("Estimated %slikelihood at snapshot %s: %1.1e" % ('log-' if self.log else '', str (snapshot), estimates [snapshot]))

            # if estimate is '-inf' (or 0 for self.log = 0) - no further filtering is possible
            if (self.log and estimates [snapshot] == float ('-inf')) or (not self.log and estimates [snapshot] == 0):
                variances [snapshot] = float ('nan')
                if self.verbosity:
                    print (" :: WARNING: '-inf' (i.e., log (0)) estimate in the PF likelihood.")
                    print ("  : -> Stopping here and returning the infos as they are.")
                successful = False
                break

            # estimate variance of the log-likelihood estimate for the current snapshot,
            # using 1st order Taylor approximation for the log-likelihood case:
            # https://stats.stackexchange.com/questions/57715/expected-value-and-variance-of-loga#57766
            if M == 1 or mean == 0:
                variances [snapshot] = float ('nan')
            else:
                logscaling = numpy.max (nonnan)
                if not numpy.isfinite (logscaling):
                    logscaling = 0
                variance = numpy.var (numpy.exp (nonnan - logscaling), ddof=1)
                deviation = numpy.exp (0.5 * (numpy.log (variance) + 2 * logscaling - numpy.log (M)))
                variances [snapshot] = (deviation / mean) ** 2
            if self.verbosity:
                print ("Estimated variance of log-likelihood at snapshot %s: %1.1e" % (str (snapshot), variances [snapshot]))

            # redraw particles based on errors
            if self.noresample:
                indices ['posterior'] [snapshot] = indices ['prior'] [snapshot]
                redraw [snapshot] = {}
            else:
                indices ['posterior'] [snapshot], redraw [snapshot] = self.redraw (indices ['prior'] [snapshot], errors ['prior'] [snapshot], logscaling = logmean + numpy.log (M))
            if self.verbosity >= 2:
                print ("Posterior (resampled) indices:")
                print (indices ['posterior'] [snapshot])

            # redraw predictions as well
            if self.noresample:
                predictions ['posterior'] [snapshot] = predictions ['prior'] [snapshot]
            else:
                predictions ['posterior'] [snapshot] = predictions ['prior'] [snapshot] .iloc [indices ['posterior'] [snapshot]]

            # unique indices and counts for redrawn predictions (compression to reduce 'info' size)
            predictions ['unique'] [snapshot] = predictions ['posterior'] [snapshot] .drop_duplicates ()
            counts = [ len (predictions ['posterior'] [snapshot] .loc [i]) for i in predictions ['unique'] [snapshot] .index ]
            weights [snapshot] = numpy.array (counts)

            if self.verbosity >= 2:
                print ("Posterior (resampled) predictions:")
                print (predictions ['posterior'] [snapshot])

            # redraw errors as well
            errors ['posterior'] [snapshot] = errors ['prior'] [snapshot] [indices ['posterior'] [snapshot]]
            if self.verbosity >= 2:
                print("Posterior (resampled) errors", errors ['posterior'] [snapshot])

            # advance ensemble state to next iteration (do not gather results)
            self.executor.call ('advance', results=0)

            # resample (delete and replicate) particles and balance ensembles in the executor and record resulting traffic
            if self.noresample:
                sources [snapshot] = indices ['posterior'] [snapshot]
                traffic [snapshot] = {}
            else:
                traffic [snapshot], sources [snapshot] = self.executor.resample (indices ['posterior'] [snapshot])
            if self.verbosity >= 2:
                print ("Posterior (resampled) particles sources:")
                print (sources [snapshot])
                print ("Traffic:")
                print (traffic [snapshot])

            # all steps were successful
            successful = True

        # finalize task ensemble in executor
        timings = self.executor.disconnect ()

        # append executor timing
        timing += self.executor.report ()

        # compute estimated (log-)likelihood as the product of estimates from all snapshots
        if self.log:
            estimate = numpy.sum (list (estimates.values()))
        else:
            estimate = numpy.prod (list (estimates.values()))

        # compute estimated variance of the estimated log-likelihood
        variance = numpy.sum (list (variances.values()))

        if self.verbosity:
            print ("Estimated %slikelihood: %1.1e" % ('log-' if self.log else '', estimate))
            print ("Estimated variance of log-likelihood: %1.1e" % variance)

        # compute MAP estimate
        if not successful:
            MAP = None
        else:
            cumulative = errors ['posterior'] [self.data.index [0]] [:]
            for snapshot in self.data.index [1:]:
                if self.verbosity >= 2:
                    print ('Cumulative posterior errors (tracked by sources) for snapshot %s:' % str (snapshot))
                    print (cumulative [sources [snapshot]])
                cumulative = errors ['posterior'] [snapshot] + cumulative [sources [snapshot]]
            MAP_indices = {}
            MAP_predictions = {}
            last = self.data.index [-1]
            MAP_indices [last] = numpy.argmax (cumulative)
            MAP_predictions [last] = predictions ['posterior'] [last] .iloc [MAP_indices [last]]
            for snapshot in reversed (self.data.index [:-1]):
                MAP_indices [snapshot] = sources [snapshot] [MAP_indices [last]]
                MAP_predictions [snapshot] = predictions ['posterior'] [snapshot] .iloc [MAP_indices [snapshot]]
                last = snapshot
            MAP = { 'indices' : MAP_indices, 'predictions' : MAP_predictions, 'error' : cumulative [MAP_indices [last]] }

        # measure evaluation runtime and timestamp
        timing.time ('evaluate')

        # information includes predictions, errors, estimates and their variances, MAP trajectory
        # resampling sources, redraw rate, used up communication traffic, and timings
        info = {}
        info ["predictions"] = predictions ['unique']
        info ["weights"] = weights
        info ["MAP"] = MAP
        info ["variance"] = variance
        info ["redraw"] = redraw
        info ["successful"] = successful
        if self.informative:
            info ["errors"] = errors
            info ["estimates"] = estimates
            info ["variances"] = variances
            info ["indices"] = indices ['posterior']
            info ["sources"] = sources
            info ["infos"] = None
            info ["traffic"] = traffic
            info ["timing"] = timing
            info ["timings"] = timings

        # return estimated likelihood and its info
        return estimate, info
