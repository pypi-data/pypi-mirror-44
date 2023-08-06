# # # # # # # # # # # # # # # # # # # # # # # # # #
# Markov chain Monter Carlo (plain Metropolis-Hastings MCMC) sampler class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import numpy
import pandas

from .sampler import Sampler

class MCMC (Sampler):
    """Markov chain Monter Carlo (plain Metropolis-Hastings MCMC) sampler class."""

    def __init__(self, proposal, log=1):

        self.proposal = proposal
        self.log = log

    # init chain
    def init (self, initial):
        """Init chain."""

        # set 'initial' parameters
        self.parameters = pandas.DataFrame (initial, index=range(1))

        if self.verbosity:
            print("Initial samples:")
            print(self.parameters)

        # reset status
        self.initialized = 0

    # evaluate likelihood and prior of the specified 'parameters'
    def evaluate (self, parameters):
        """Evaluate likelihood and prior of the specified 'parameters'."""

        # evaluate prior
        p = self.prior.pdf (parameters) if self.prior else 1.0

        # if prior is zero and chain is already initialized - skip likelihood evaluation
        if p == 0 and self.initialized:
            return None, 0, 0, None

        # evaluate likelihood
        results, timings = self.executor.map (self.likelihood, [self.parameters])
        L, info = results [0]

        # get executor timing
        timing = self.executor.report ()

        # transform likelihood, if needed
        if self.likelihood.log:
          L = numpy.exp (L)

        # compute L * p
        Lp = L * p

        return L, p, Lp, info, timing, timings

    # returned packed results
    def results(self):
        """Returned packed results."""

        info = {}
        info ["index"] = self.index
        info ["parameters"] = [self.parameters]
        info ["proposes"] = [self.proposed]
        info ["priors"] = [self.p]
        info ["likelihoods"] = [self.L]
        info ["posteriors"] = [self.Lp]
        info ["accepts"] = [self.accept]
        info ["infos"] = [self.info]
        if self.informative:
            info ["timing"] = self.timing
            info ["timings"] = self.timings

        return self.parameters, info

    # draw samples from posterior distribution
    def draw (self, sandbox, seed):
        """Draw samples from posterior distribution."""

        # setup likelihood
        # chain = 0
        # label = 'C%05d' % chain
        # chain_sandbox = sandbox.spawn (label) if self.sandboxing else None
        # chain_seed = seed.spawn (chain, name=label)
        # self.likelihood.setup (chain_sandbox, self.verbosity - 2, chain_seed, self.informative, self.trace)
        self.likelihood.setup (sandbox, self.verbosity - 2, seed, self.informative, self.trace)

        # treat 'initial' parameters as the first sample
        if not self.initialized:

            if self.verbosity >= 3:
                print ('MCMC: draw (initialize)')

            # evaluate likelihood and prior of 'initial' parameters
            self.L, self.p, self.Lp, self.info, self.timing, self.timings = self.evaluate (self.likelihood, self.parameters)

            # 'initial' sample is neither accepted nor rejected
            self.accept = None

            # 'initial' sample is proposed
            self.proposed = self.parameters

            # update status
            self.initialized = 1

            return self.results()

        if self.verbosity >= 3:
            print ('MCMC: draw (sample)')

        # generate new parameters based on proposal distribution given previous sample
        self.proposed = self.proposal.draw (self.rng, offset = self.parameters)

        # store previous Lp
        self.Lp_prev = self.Lp

        # evaluate likelihood and prior of the proposed parameters
        self.L, self.p, self.Lp, self.info, self.timing, self.timings = self.evaluate (self.likelihood, self.proposed)

        # compute acceptance probability
        a = min(1, self.Lp / self.Lp_prev) if self.Lp_prev != 0 else 1

        # draw a uniform random number in [0, 1)
        u = self.rng.uniform(0, 1)

        # accept or reject the proposed parameters
        self.accept = 1 if u < a else 0

        # update chain state, if accepted
        if self.accept:
            self.parameters = self.proposed

        return self.results()
