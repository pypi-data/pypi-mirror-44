# # # # # # # # # # # # # # # # # # # # # # # # # #
# Connector class for subdivision of MPI.COMM_WORLD into manager and workers
# using mpi4py bindings and MPI backend for distributed memory paralellization
# Legacy version of the 'Split' connector, avoiding the use of Accept/Connect
#
# Marco Bacci
# Eawag, Switzerland
# marco.bacci@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from mpi4py import MPI
from .split import Split

def universe_address ():
    """Return rank in MPI COMM_WORLD"""

    address = MPI.COMM_WORLD.Get_rank ()
    return address


class Legacy (Split):
    """Class to establish workers MPI processes when dealing with legacy MPI implementations."""

    def __init__ (self, verbosity=0):

        self.verbosity = verbosity

    # connect manager with the number of requested workers by returning a port needed to connect to an inter-communicator
    @staticmethod
    def bootup (contract, task, resource, root, verbosity):

        # use self.split () analogously as in split.py
        # overwrite any needed changes in self.barrier () and self.init () as well

        # def Create_intercomm(self,
        #                          int local_leader,
        #                          Intracomm peer_comm,
        #                          int remote_leader,
        #                          int tag=0):

        # here, most probably we return the rank of a remote_leader needed above (and maybe a list of local ranks to form the peers intra-communicator)
        return None
