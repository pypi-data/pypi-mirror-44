# # # # # # # # # # # # # # # # # # # # # # # # # #
# Straightwalk Model class
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from spux.models.model import Model
from spux.utils.annotate import annotate

class Straightwalk (Model):
    """Class for Straightwalk model."""

    # no need for sandboxing
    sandboxing = 0

    # construct model
    def __init__ (self, stepsize=1):

        self.stepsize = stepsize

    # initialize model using specified 'input' and 'parameters'
    def init (self, input, parameters):
        """Initialize model using specified 'input' and 'parameters'."""

        # base class 'init (...)' method - OPTIONAL
        Model.init (self, input, parameters)

        self.position = parameters ["origin"]
        self.drift = parameters ["drift"]

        self.time = 0

    # run model up to specified 'time' and return the prediction
    def run (self, time):
        """Run model up to specified 'time' and return the prediction."""

        # base class 'run (...)' method - OPTIONAL
        Model.run (self, time)

        # update position (e.g., perform walk)
        self.position += self.stepsize * self.drift * (time - self.time)

        # update time
        self.time = time

        # return results
        return annotate ([self.position], ['position'], time)
