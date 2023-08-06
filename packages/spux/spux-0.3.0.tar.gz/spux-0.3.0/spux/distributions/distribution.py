# # # # # # # # # # # # # # # # # # # # # # # # # #
# Base class for distributions
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import pandas

class Distribution (object):

  # evaluate a joint PDF of the distribution
  # 'parameters' is assumed to be of a pandas.DataFrame type
  def pdf (self, parameters):
    """Base method to be overloaded to evaluate the (joint) prob. distr. function of parameters.

    'parameters' are assumed to be of a pandas.DataFrame type
    """

    return float ('nan')

  # evaluate a joint log-PDF of the distribution
  # 'parameters' is assumed to be of a pandas.DataFrame type
  def logpdf (self, parameters):
    """Base method to be overloaded to evaluate the logarithm of the
    (joint) prob. distr. function of parameters.

    'parameters' are assumed to be of a pandas.DataFrame type
    """

    return float ('nan')

  # return intervals (for each parameter) for the specified centered probability mass
  def intervals (self, alpha):
    """Return intervals for the specified centered probability mass.

    Intervals are returned for each parameter.
    """

    return { 'parameter' : [float ('nan'), float ('nan')] }

  # draw a random vector using the provided RNG engine
  # 'offset' is assumed to be of a pandas.DataFrame type
  def draw (self, rng, offset = None):
    """
    Draw a random vector using the provided RNG engineself.

    'offset' is assumed to be of a pandas.DataFrame type
    """
    parameters = { 'parameter' : float ('nan') }
    parameters = pandas.DataFrame (parameters, index=range(1))
    if offset is not None:
      parameters += offset
    return parameters
