# # # # # # # # # # # # # # # # # # # # # # # # # #
# Individual Based Model class
# Based on: Kattwinkel & Reichert, EMS 2017.
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

import os, re

import numpy

from spux.models.model import Model

from spux.drivers import java
from spux.io import parameters as txt
from spux.utils.seed import Seed
from spux.utils.annotate import annotate
from spux.io.loader import read_params_types

class IBM (Model): #(object)
    """Individual Based Model class with java interface."""

    # construct IBM for the specified 'config'
    def __init__(
        self,
        config,
        classpath=None,
        inputpath=None,
        jvmpath=None,
        jvmargs="-Xmx1G",
        paramtypefl=None
    ):
        """Construct IBM for the specified 'config'."""

        #kick-out
        if paramtypefl is None:
            raise ValueError("Fatal. Input file with parameters types is mandatory.")

        #find name of input files
        fullfile = os.path.join('input/input/',config)
        #
        keys = ["fNameInputUniParam","fNameInputTaxParam","fNameInputTaxNames"]
        self.infls = []
        with open (fullfile, 'r') as fl:
            for line in fl:
                if re.match(keys[0],line) or re.match(keys[1],line):
                    self.infls.append( ((line.split(':')[1]).strip('\n')).strip('\t') )
                elif re.match(keys[2],line):
                    specsfl = ( (line.split(':')[1]).strip('\n') ).strip('\t')

        #get name of species (labels)
        fullfile = os.path.join('input/input/',specsfl)
        with open(fullfile, 'r') as fl:
            next(fl)
            self.species = [ line.strip('\n') for line in fl ]

        #get parameters types
        self.paramtypefl = paramtypefl
        self.all_params = read_params_types(paramtypefl=paramtypefl)

        #check parameters names
        for i in range(len(self.infls)):
            fullfile = os.path.join('input/input/',self.infls[i])
            with open(fullfile) as fl:
                next(fl) #first line is not a paramter
                for line in fl:
                    (key, val) = line.split()
                    if key not in self.all_params:
                        raise ValueError("Fatal. Parameter {} is not in file {}.".format(key,paramtypefl))

        self.config = config

        # Java Virtual Machine arguments
        self.jvmpath = jvmpath
        self.classpath = classpath
        self.jvmargs = jvmargs

        self.inputpath = inputpath

        # initially neither interface nor model do exist
        self.interface = None
        self.model = None

        # sandboxing
        self.sandboxing = 1

        # serialization
        self.serialization = 'binary'

    # setup driver
    def driver (self):
        """Setup java driver (interface to user java code)."""

        # start Java Virtual Machine
        if self.verbosity:
            print("IBM %s: setup -> driver" % self.sandbox())

        driver = java.Java (jvmpath=self.jvmpath, classpath=self.classpath, jvmargs=self.jvmargs)

        # get model class
        if self.verbosity:
            print("IBM %s: setup -> model" % self.sandbox())
        self.Model = driver.get_class("mesoModel.TheModel")

        # construct ModelWriterReader object for later save/load
        if self.verbosity:
            print("IBM %s: setup -> interface" % self.sandbox())
        Interface = driver.get_class("mesoModel.ModelWriterReader")
        self.interface = Interface()

    def setup (self, sandbox=None, verbosity=1, seed=Seed(), informative=0, trace=0):
        """Setup IB Model."""

        # base class 'setup (...)' method
        Model.setup (self, sandbox, verbosity, seed, informative, trace)

        # if interface does not exist
        if self.interface is None:

            # setup driver
            self.driver ()

        # if model exists - the java model
        if self.model is not None:

            # set path
            if self.verbosity:
                print("IBM %s: setup -> setPaths ()" % self.sandbox())
            self.model.setPaths (self.sandbox())

            # set seed
            if self.verbosity:
                print("IBM %s: setup -> reinitiliazeModel ()" % self.sandbox())

            # pass array of seeds to Java source code
            self.model.reinitializeModel ( numpy.ndarray.tolist(self.seed()) )

    # initialize IBM using specified 'input' and 'parameters'
    def init (self, input, parameters):
        """Setup IBM using specified 'input' and 'parameters'."""

        # print("self: %s" %(self)) # ibm.IBM
        if self.verbosity:
            print("IBM %s: init parameters:" % self.sandbox())
            print(parameters)

        # base class 'init (...)' method
        Model.init (self, input, parameters)

        # copy all required input files
        self.sandbox.copyin (self.inputpath)

        path = os.path.join(self.sandbox(), "input")

        #update parameter values in model input filr
        for filename in self.infls:
            inputfile = os.path.join(path, filename)
            available = txt.load(inputfile)
            for label, value in parameters.items():
                if label in available:
                    if self.all_params[label].lower() == 'double' or self.all_params[label].lower() == 'float':
                        available [label] = float([value] [0])
                    elif self.all_params[label][0:3].lower() == 'int':
                        available [label] = round([value] [0])
                    elif self.all_params[label].lower() == 'binary':
                        if [value] [0] != 0 or [value] [0] != 1:
                            raise ValueError("Fatal. Wrong value for binary parameter.")
                        available [label] = round([value] [0])
                    else:
                        raise ValueError("Fatal. Wrong type for parameter.")
            txt.save(available, inputfile, delimiter="\t")

        # construct model object - set self.model to the java Model
        if self.verbosity:
            print("IBM %s: init -> model" % self.sandbox())
        self.model = self.Model (numpy.ndarray.tolist(self.seed()))

        # set path
        if self.verbosity:
            print("IBM %s: init -> setPaths ()" % self.sandbox())
        self.model.setPaths (self.sandbox())

        # run model initialization for the specified 'config'
        if self.verbosity:
            print("IBM %s: init -> initModel ()" % self.sandbox())
        self.config

        try:
            self.model.initModel ([self.config])
        except:
            raise ValueError("Caught the runtime exception on java.")

        # simulation initialization
        if self.verbosity:
            print("IBM %s: init -> initSimulation ()" % self.sandbox())

        self.model.initSimulation()

        if self.verbosity:
            print("IBM %s: init -> runSimulationInitExtPartFiltering ()" % self.sandbox())
        self.model.runSimulationInitExtPartFiltering()

    # run IBM up to specified time and return the prediction
    def run (self, time):
        """Run IBM up to specified time and return the prediction."""

        # base class 'init ()' method
        Model.run (self, time)

        # run model up to specified time
        self.model.runModelExtPartFiltering(int(time))

        # get model output
        observation = self.model.observe()
        observation = numpy.array (observation)
        sums = numpy.sum (observation, axis=0)

        labels = self.species

        return annotate(sums,labels,time)

    # save current model state
    def save (self):
        """Save current model state (the whole java program instance is saved)."""

        if self.serialization == "binary":
            buff = self.interface.writeModelByteArray (self.model)
            state = java.Java.save(buff)

        if self.verbosity:
            print("IBM: save", self.sandbox())

        return state

    # load specified model state
    def load (self, state):
        """Load model state (the whole java program instance) previously saved with save()."""

        if self.verbosity:
            print("IBM: load", state, self.sandbox())

        # copy all required input files
        self.sandbox.copyin (self.inputpath)

        # - binary array representing serialize model state (fast)
        if self.serialization == "binary":
            buff = java.Java.load(state)
            self.model = self.interface.loadModelByteArray(buff)

    # construct a data container for model state with a specified size
    def state (self, size):
        """Construct a data container for model state with a specified size."""

        return numpy.empty (size, dtype="uint8")