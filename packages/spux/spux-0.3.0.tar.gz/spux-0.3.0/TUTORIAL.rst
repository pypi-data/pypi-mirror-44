
.. _tutorial:

========
Tutorial
========

This section guides you through a tutorial for an example model and usage pattern of SPUX.
For peculiarities regarding the coupling your model with the SPUX framework, refer to :ref:`customization`.

Commands should be executed in Python terminal, or inside a Python script, or in a Jupyter notebook.
To learn how to write your own custom scripts and configure spux,
first read through the rest of this section and take a look at the
`examples <https://gitlab.com/siam-sc/spux/tree/master/examples>`_
suite.

Editor
------

Try one of the following cross-platform editors (you can also use Vim or Emacs, of course):

* Spyder - similar UI as R,
* PyCharm - proprietary,
* VS Code - works very well with GitLab integration extensions - give it a try!

Straightwalk (serial)
---------------------

This is an example of how to use spux with deterministic models, requiring a simple ``Direct`` likelihood.
As SPUX framework has a focus on the stochastic models,
this example is not discussed in detail in the current version of this tutorial.
However, this is simply a stripped down version (with the randomness eliminated) of the stochastic randomwalk example below.
Please refer to all example scripts in the dedicated example directory at:
`examples/straightwalk/ <https://gitlab.com/siam-sc/spux/tree/master/examples/straightwalk/>`_.

Work in progress.

Randomwalk (serial)
-------------------

Here we provide an elaborate description of the spux framework
setup and simulation execution for an example of a simple Randomwalk model.

The model describes a stochastic one-dimensional walk on integers,
with a prescribed (let's say, genetically) :code:`stepsize`.
Starting at the location given by the :code:`origin` parameter,
a randomwalk takes a random step of size :code:`stepsize` either to the left or to the right,
with direction distribution depending on the :code:`drift` parameter.
Inaccurate observations at several times of the randomwalk's position are available,
with unknown observational error distribution,
assumed to be Gaussian with zero mean and standard deviation given by the paramameter :code:`$\sigma$`.
In this particular example, multiple replicates of observations are available,
with each replicate corresponding to the same (assumed to be unknown) model parameter values,
but different stochastic evolution path (e.g. seed).

All files required throughout this example (and some more) could be found in
`examples/randomwalk/ <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/>`_,
which we assume is the current working directory where commands are executed.
This means that all :code:`import module` statements will import the corresponding :code:`module.py` script from this directory (or an already installed external Python module).
All imports starting with :code:`from spux import ...` import modules that are built-in in the spux module,
and we use relative links starting with `spux/ <https://gitlab.com/siam-sc/spux/tree/master/spux/>`_ for a corresponding file in the GitLab repository.

The randomwalk model is a built-in module in spux and can be found at
`spux/models/randomwalk.py <https://gitlab.com/siam-sc/spux/tree/master/spux/models/randomwalk.py>`_:

.. literalinclude:: ../spux/models/randomwalk.py
   :language: python
   :linenos:
   :lines: 10-
   :lineno-start: 10

In the source code above, :code:`Randomwalk` class has a constructor (note the underscores!) :code:`__init__ (self, ...)`,
which is called when constructing model by :code:`model = Randomwalk (stepsize=1)`.
The argument :code:`self` is a pointer to the object itself, analogous to :code:`this` in C/C++.
Additional methods include:

* :code:`init (self, input, parameters)` - to initialize the model with the specified :code:`input` and :code:`parameters`,
* :code:`run (self, time)` - run the model from the current time up to the specified :code:`time`.

Note, that the "current time" in the above is set in :code:`init (...)` or the previous call of :code:`run (...)`
and is handled differently in different models (in this example: simply saving it to :code:`self.time`).

The :code:`annotate (values, labels, time)` method packages model predictions stored in :code:`values` to a :code:`pandas.DataFrame`
with the specified list of :code:`labels` for the elements if the :code:`values` and with the requested :code:`time`.

Apart from the actual model, we also need to specify several auxiliary configuration files for observational datasets,
statistical error model (i.e. a probabilistic distribution of the observations conditional on the specified model prediction), and prior distribution of the parameters.
Actual datasets files are located in the input directory
`examples/randomwalk/input/ <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/input/>`_.

The script to load these datasets into :code:`pandas` DataFrames (a default container for dataset management in SPUX, see https://pandas.pydata.org) is located in
`examples/randomwalk/datasets.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/datasets.py>`_:

.. literalinclude:: ../examples/randomwalk/datasets.py
   :language: python
   :linenos:
   :lines: 2-
   :lineno-start: 2

Error model is defined in
`examples/randomwalk/error.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/error.py>`_
as an object with a method :code:`distribution (prediction, parameters)`
which returns a distribution of the model observations (data):

.. literalinclude:: ../examples/randomwalk/error.py
   :language: python
   :linenos:
   :lines: 2-
   :lineno-start: 2

Prior distribution is defined in `examples/randomwalk/prior.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/prior.py>`_:

.. literalinclude:: ../examples/randomwalk/prior.py
   :language: python
   :linenos:
   :lines: 2-
   :lineno-start: 2

Within the context if this illustrative Randomwalk example, we also make use of the (optional) exact parameter values ("the truth") available at
`examples/randomwalk/exact.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/exact.py>`_:

.. literalinclude:: ../examples/randomwalk/exact.py
   :language: python
   :linenos:
   :lines: 2-
   :lineno-start: 2

We would also like to emphasize, that in the above scripts we generously use LaTeX syntax
within labels for parameters, predictions, and observations.
The benefit of such scrupulous naming will become evident from the generated plots
within this tutorial, where all axes labels are LaTeX-formatted mathematical symbols.
Notice, that for a LaTeX syntax to be supported in Python,
one must preprend the string with the :code:`r` letter (as in "raw").

In order to give you a better overview of the datasets, the error model, the prior distribution,
and (optional) exact parameters values for a reference, consider running a preparation script
`examples/randomwalk/plot_config.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/plot_config.py>`_:

.. literalinclude:: ../examples/randomwalk/plot_config.py
   :language: python
   :linenos:
   :lines: 2-
   :lineno-start: 2

The above script plots model observations (datasets),
marginal prior distributions of model parameters,
and marginal error model distributions for specified model prediction and parameters:

.. figure:: _static/randomwalk/randomwalk_datasets-position.png
   :align: center
   :scale: 20 %

   Plot of the observational datasets (three independent replicates).

.. figure:: _static/randomwalk/randomwalk_distributions-prior.png
   :align: center

   Plots of the prior marginal distributions of model parameters.
   Red dashed line represents the exact parameter values.

.. figure:: _static/randomwalk/randomwalk_errors-dataset-0.png
   :align: center
   :scale: 20 %

   Plot of the error model distribution treating each dataset point as a model prediction
   and using exact parameters (for :code:`$\sigma$`) for dataset :code:`0`.

The main script
`examples/randomwalk/script.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/script.py>`_,
using the above auxiliary scripts, configures SPUX:

.. literalinclude:: ../examples/randomwalk/script.py
   :language: python
   :linenos:
   :lines: 1-
   :lineno-start: 1

In this script, different additional components, such as model, likelihood, joint likelihood for dataset replicates (datasets), and sampler, are created.
Afterwards, all these components are merged together by assigning according to the logical dependencies.
In the future, SPUX will provide a :code:`spux.utils.assign` module containing a :code:`assign` function,
which takes a list of components (in any order) as an argument, tries to "automagically" perform all needed assignments and returns the resulting top-level component
(in this example, the :code:`sampler`):

.. code-block:: python

    from spux.utils.assign import assign

    components = [model, error, datasets, likelihood, replicates, prior]
    sampler = assign (sampler, components)

It is a good idea to keep this main :code:`script.py` separate from the scripts that will actually run SPUX,
in order to have flexibility for the later customization of output location, sampling duration, and the targetted hardware resources.

To achieve this, we import the main configuration script and initiate the execution of the framework
in a separate script named (you will see later why such name)
`examples/randomwalk/script_serial.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/script_serial.py>`_:

.. literalinclude:: ../examples/randomwalk/script_serial.py
   :language: python
   :linenos:
   :lines: 1-
   :lineno-start: 1

The :code:`verbosity` value is an integer,
with higher values corresponding to additional reporting from components deeper in the assignment hierarchy.
Regarding the auxilliary calls :code:`sampler.executor.init ()` and :code:`sampler.executor.exit ()`,
you must have them, and in this particular order, i.e. wrapping every other call of the SPUX framework
(apart from the calls in the main configurations script).

The ``sandbox`` in this example script is configured to use the fast virtual node-local RAM-based linux filesystem called ``tmpfs``.
Note, that the exact path to the local ``tmpfs`` might differ depending on the linux distribution.
For local testing, a user might prefer to temporarily switch to a conventional filesystem and set a different desired sandbox ``path``, leaving ``target=None``.
For production runs on high performance computing clusters, we recommend either to use the default ``tmpfs``,
or, if the amount of system memory is a limiting factor, to set ``target`` to the scratch file system of the cluster.
Node-local (not shared) scratch filesystems are referrable, due to their better performance and the lack of restrictions regarding any storage quotas.
If target is a shared (hence not a node-local) filesystem (the worst case scenario, for development only), you can also set ``path``, where a corresponding symlink pointing to the specified ``target`` will be created.

The main script then generates an :code:`output/` directory
(can be changed by setting :code:`outputdir` in :code:`sampler.setup (...)`)
with files containing posterior samples and supporting information;
multiple files of each type will be generated for each checkpoint,
with the default period being 10 minutes:

* :code:`samples-*.csv` - a CSV file containing a list of comma-separated posterior samples of parameters
* :code:`samples-*.dat` - a binary file (:code:`cloudpickle`) containing posterior samples of parameters
* :code:`infos-*.dat` - a binary file (:code:`cloudpickle`) containing a :code:`list` of supporting information

The supporting files :code:`infos-*.dat` contain detailed information about
each component in the hierarchical assignment structure specified by the main configuration script.
In the particular example, when loaded (see following paragraphs) will contain a list of dictionaries for each draw of the posterior parameters from the sampler.
For samplers supporting multiple MCMC chains, each draw provides as many samples as there are chains,
and hence the list in the :code:`infos-*.dat` will be shorter than the list of all posterior parameters by a factor of the number of chains.
The structure of each element in the list of loaded :code:`infos-*.dat` can be infered from the corresponding info generation routines for each SPUX component (look for :code:`info = {...}`).
In particular, the :code:`predictions` field of the PF likelihood :code:`infos` contains the :code:`'prior'` (pre-filtering) and :code:`'posterior'` (post-filtering) model predictions for each particle.

EMCEE sampler: `spux/samplers/emcee.py <https://gitlab.com/siam-sc/spux/tree/master/spux/samplers/emcee.py>`_:

.. literalinclude:: ../spux/samplers/emcee.py
   :language: python
   :linenos:
   :lines: 130-141
   :lineno-start: 130

Replicates likelihood: `spux/likelihoods/replicates.py <https://gitlab.com/siam-sc/spux/tree/master/spux/likelihoods/replicates.py>`_:

.. literalinclude:: ../spux/likelihoods/replicates.py
   :language: python
   :linenos:
   :lines: 128-134
   :lineno-start: 128

Direct likelihood: `spux/likelihoods/direct.py <https://gitlab.com/siam-sc/spux/tree/master/spux/likelihoods/direct.py>`_:

.. literalinclude:: ../spux/likelihoods/direct.py
   :language: python
   :linenos:
   :lines: 127-134
   :lineno-start: 127

PF likelihood: `spux/likelihoods/pf.py <https://gitlab.com/siam-sc/spux/tree/master/spux/likelihoods/pf.py>`_:

.. literalinclude:: ../spux/likelihoods/pf.py
   :language: python
   :linenos:
   :lines: 305-321
   :lineno-start: 305

If :code:`self.sandboxing == 1` is set for the model,
a :code:`sandbox` directory is created (or a custom name, if custom sandbox is specified).
This directory is populated with nested sandboxes for each sample, chain, replicate, likelihood, and model.
For sandboxes in the ``local`` mode (for non-shared filesystems), nested directories are replaced by a single directory with a long name indicating the underlying hierarchy.
Please also note, that sandboxes in ``local`` mode are tentative, meaning that they are only created once ``self.sandbox ()`` is executed for the first time.
If :code:`trace=True` is additionally specified in the :code:`sampler.setup (...)`,
this directory contains the stored sandboxes of all samplers,
likelihoods and models, including all the generated results. However, these results would be easily accessible only if sanboxes are placed in a shared filesystem and a non-local mode is used.

Before we proceed to the results, please note,
that all following plots were generated with the production settings,
which are more computationally demanding compared to the example scripts above.
In particular, 16 particles were used in the PF likelihood, and 16 chains were used in the EMCEE sampler.
We used in total 129 cores, with 8 workers for the ``EMCEE`` sampler, 3 workers for the ``Relicates`` likelihood, and 4 workers for the ``PF`` likelihood.
In total, 50'000 samples were requested.

An example analysis script to load and vizualize results from the :code:`output/` directory is available at
`examples/randomwalk/plot_results.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/plot_results.py>`_:

.. literalinclude:: ../examples/randomwalk/plot_results.py
   :language: python
   :linenos:
   :lines: 1-
   :lineno-start: 1

This script uses some built-in plotting routines available in `spux/plot/mpl.py <https://gitlab.com/siam-sc/spux/tree/master/spux/plot/mpl.py>`_ module.
However, the use is free to use only the loading parts and choose how to visualize the results using other established data visualization libraries,
including the built-in visualization module :code:`pandas.plotting` in :code:`pandas` for the visualization of the :code:`pandas.DataFrame` objects.
Also check out `NumFOCUS <https://numfocus.org/sponsored-projects?_sft_project_category=python-interface+visualization>`_.

The above analysis script generates multiple plots of the results, but firslty it is most useful to look at the ``unsuccessfuls`` and ``parameters`` plots.

However, since all likelihood evaluations were successful (none were skipped due to zero prior or failed due to PF or model problems), this (empty) plot is not included here.
This is usually not the case in complex realistic models, often having a less restrictive parameters prior distributions.
Note, that skipped likelihoods are not scheduled in the executor and might result in a temporary (for that particular paramter proposal)
parallelization imbalances due to the lack of tasks to process.

.. .. figure:: _static/randomwalk/randomwalk_unsuccessfuls.png
..    :align: center
..    :scale: 20 %

..    Plots unsuccessful evaluations (either skipped due to zero prior or failed due to PF or model problems) of the likelihood in the Markov chains.
..    In this particular synthetic example there are no unsuccessful likelihood evaluations.
..    This is usually not the case in complex realistic models, often having a less restrictive parameters prior distributions.
..    Note, that skipped likelihoods are not scheduled in the executor and might result in a temporary (for that particular paramter proposal)
..    parallelization imbalances due to the lack of tasks to process.

.. figure:: _static/randomwalk/randomwalk_parameters.png
   :align: center
   :scale: 15 %

   Plots of the Markov chain parameters samples. Note the initial burnin period.

From the diagnostic plots above, we determinte that the inference was (tentatively) successful (not many failed (NaN) or skipped (zero prior) likelihood evaluations)
and that the burnin period lasts for approximately 300 batches of EMCEE samples from multiple chains.
We use this information to generate all subsequent plots with the initial bias already removed
by setting ``burnin=300`` in the constructor of the ``MatPlotLib`` in the ``plot_results.py`` script above.
The resulting inference plots provide a detailed insight into posterior parameters and model predictions distributions,
as well as the performance of the overall Bayesian inference and the specifics within the PF likelihood.

.. figure:: _static/randomwalk/randomwalk_posteriors-unbiased.png
   :align: center

   Plots of the marginal posterior distributions of model parameters.
   Brown dotted line is the approximated maximum likelihood estimate for parameters,
   and dashed red line denotes the exact parameters.

.. figure:: _static/randomwalk/randomwalk_posteriors2d-unbiased.png
   :align: center
   :scale: 15 %

   Joint pairwise marginal posterior distributions of all model parameters,
   including the corresponding Markov chains from the EMCEE sampler.
   Legend:
   blue "+" - initial parameters,
   brown "o" - approximate maximum a posteriori (MAP) estimate for parameters,
   red "x" - the exact parameters.

.. figure:: _static/randomwalk/randomwalk_likelihoods-unbiased.png
   :align: center
   :scale: 20 %

   Plots of the (scaled) log-posterior and (scaled) log-likelihood estimates
   for the sampled model posterior parameters.
   For log-likelihood, the estimates from the rejected proposed parameters are also taken into account,
   resulting in a significantly large estimate variations for each batch of EMCEE samples from multiple chains.
   Legend:
   red - (scaled) posterior estimates,
   purple - (scaled) likelihood estimates,
   brown "o" - approximate maximum a posteriori (MAP) estimate for parameters.

.. figure:: _static/randomwalk/randomwalk_redraw-unbiased.png
   :align: center
   :scale: 20 %

   Plots of the particle redraw rates if the PF likelihood.

.. figure:: _static/randomwalk/randomwalk_deviations-unbiased.png
   :align: center
   :scale: 20 %

   Plots of the standard deviations for the estimated marginal parameters log-likelihood using the PF.
   These standard deviations should be of the order of O(1) to ensure the efficient performance of the MCMC sampler.
   If the advised O(1) is exceeded, consider increasing the number of particles used in the PF.

.. figure:: _static/randomwalk/randomwalk_acceptances-unbiased.png
   :align: center
   :scale: 20 %

   Plots of the cumulative acceptances for the proposed paramters samples.

.. figure:: _static/randomwalk/randomwalk_predictions-posterior-dataset-0-unbiased.png
   :align: center
   :scale: 20 %

   Plot of the posterior distribution of model predictions for an observational dataset.

.. figure:: _static/randomwalk/randomwalk_qq-unbiased.png
   :align: center
   :scale: 20 %

   Plots of the quantile-quantile distribution comparison between the prediction residuals and the specified error model.

Continue sampling
-----------------

It is possible to continue the sampling process where it finished without any additional re-evaluation of the likelihoods,
since all the needed information is already availble.
One simply needs to customize the ``sampler.setup (...)`` method by providing the ``index`` from which to continue,
and the loaded last parameter samples for each sampler chain as ``initial`` together with the associated posteriors.

An example continuation script is available at
`examples/randomwalk/script_serial_continue.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/script_serial_continue.py>`_:

.. literalinclude:: ../examples/randomwalk/script_serial_continue.py
   :language: python
   :linenos:
   :lines: 1-
   :lineno-start: 1

Informative flag
----------------

You can incorporate computational performance information
and the :code:`infos` from the models by setting
:code:`informative=1` flag in the :code:`sampler.setup (...)` routine.
Note, however, that this results in an overhead for your inference,
and is only advised for the non-production runs during the development stages.
You can then use the sample script
`examples/randomwalk/plot_performance.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/plot_performance.py>`_
to generate plots for timings and scaling.

Performance plotting is work in progress.

Profiling
---------

If you would like to have more detailed information about the execution process,
you can enable the profiling by setting :code:`profile=1` in :code:`sampler.sample (...)`.
The profiling information after the execution of the framework will be saved in :code:`output/profile.pstats`.
You can then use the sample script
`examples/randomwalk/plot_profiler.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/plot_profiler.py>`_
to generate a report and a callgraph plot, which will be saved under the :code:`fig/` directory.

Parallel runs (spawn)
---------------------

With minimal effort, the above example configuration could be parallelized
either on a local machine or on high performance computing clusters.

Note, that NO MODIFICATIONS are needed for this particular model class in :code:`randomwalk.py`.
For a more detailed discussion for other user-specific models written not in pure Python, refer to :ref:`customization`.

To enable parallel execution, each SPUX component in the main configuration script :code:`script.py`
can be assigned a parallel executor, specifying the number of parallel workers (for that particular SPUX conmponent).
In this example, we use a separate script
`examples/randomwalk/script_spawn.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/script_spawn.py>`_:

.. literalinclude:: ../examples/randomwalk/script_spawn.py
   :language: python
   :linenos:
   :lines: 1-
   :lineno-start: 1

The additional lines regarding the :code:`resources` estimate the needed resources,
which are determined by the number of workers requested in each executor.
Note, that a separate core is used for the manager process of each executor.
An example output of such table (for this particular configuration) is provided below,
where the total of 31 cores are needed (scroll horizontally to see everything).
This table is also written into the ``resources.dat`` file.

.. code-block:: console

     :: Required resources:
    ========================
          class |           owner |            task |        executor |    manager |    workers |  resources | cumulative
    ----------- + --------------- + --------------- + --------------- + ---------- + ---------- + ---------- + ----------
          Model |      Randomwalk |               - |               - |          0 |          1 |          1 |          1
     Likelihood |              PF |      Randomwalk |  Mpi4pyEnsemble |          1 |          2 |          1 |          3
     Likelihood |      Replicates |              PF |      Mpi4pyPool |          1 |          3 |          3 |         10
        Sampler |           EMCEE |      Replicates |      Mpi4pyPool |          1 |          2 |         10 |         21

Assuming you have MPI installed (see :ref:`installation`),
the above script can be executed using MPI with:

.. code-block:: console

    $ mpirun -n 1 python -m mpi4py script_spawn.py

Note, that any needed additionally required MPI processes will be spawned automatically according to :code:`resources`,
hence for this configuration always use :code:`-n 1`, independently of the workers in executors.

Remark on MPI libraries
~~~~~~~~~~~~~~~~~~~~~~~

Note, that different MPI libraries provide different implementations,
which have different configuration capabilities and might not completely follow the MPI standard.

Here we try to provide a list of useful advices to address any issues that you could encounter:

* For ``OpenMPI``:
    * You might need to specify ``--mca mpi_warn_on_fork 0`` for ``mpirun`` to avoid annoying warnings.
    * For large runs, you might need to specify ``--mca pmix_server_max_wait 3600`` and ``--mca pmix_base_exchange_timeout 3600`` for ``mpirun`` to avoid connection failures.
    * For local testing, you might need to specify ``--oversubscribe`` for ``mpirun`` to use more MPI ranks than you have cores.

Remark on executors
~~~~~~~~~~~~~~~~~~~

Note, that multiple different kinds of serial and parallel executors (``Serial``, ``Pool``, ``Ensemble``)
can be freely mixed and matched for every SPUX component (``Model``, ``Likelihood``, ``Sampler``, etc.).

This freedom to use individual parallel executors of arbitrary size for every SPUX component provides lots of flexibility,
but also leaves lots of space for computationally inefficient parallel configurations.
Hence, for large production runs, we strongly advice to take the following guidelines into consideration, decreasing in priority:

* Allocate most workers to the executors of the outer-most SPUX component(s) (e.g. ``sampler``).
* Avoid parallel executors with few workers (less than 4) - replace them with ``Serial`` executors.

SPUX will report the percentage of the number of manager cores w.r.t. the total number of all (manager and worker) cores.
If the above guidelines are not properly implemented, this fraction could be larger than 20%,
in which case SPUX will display an explicit inefficiency warning.
Such warning will be skipped for jobs that requested not more than 8 cores in total,
to filter out local debug and development runs, where parallelization efficiency is not of the highest importance.

Remark on replicates
~~~~~~~~~~~~~~~~~~~~

For parallel runs, the :code:`Replicates` likelihood performs guided load balancing
by evaluating the lengths of the associated datasets and sorting likelihood evaluations.
Higher priorities are assigned to the likelihoods with longer datasets,
and lower priorities are assigned to the likelihoods with shorter datasets.
If needed, one can disable such behavior by setting :code:`sort=0`
in the constructor :code:`Replicates (...)`.
We warn, however, that depending on the executor configuration,
disabling sorting (and hence reverting to non-guided load balancing)
might lead to inefficient parallelization.

Parallel models
---------------

Most probably you have already noticed, that in the example above,
the no parallel executor is attached to the model object.
This is because our implementation Randomwalk model does not support parallelization.
However, a custom user model might be very computationally expensive and need further parallelization.

Provided that the content of the pure Python model :code:`init (...)` and/or :code:`run (...)` methods
can be split into a list of independent computationally intensive tasks,
one could attach a :code:`spux.executors.mpi4py.map` executor to the model.
To make use of the executor, you will need
either to provide a function and a list of its arguments for which the function needs to be evaluated,
or a list of callable objects (with an optional list of fixed arguments).

For more information, take a look at the corresponding documentation files in :ref:`documentation`.

However, a custom user model might be either already parallelized, or the model might be written in another programming language rather than Python.
SPUX framework does support such models too, provided that they use MPI for parallelization.
In particular, one can attach the built-in parallel MPI wrapper executor from
`spux/executors/mpi4py/wrapper.py <https://gitlab.com/siam-sc/spux/tree/master/spux/executors/mpi4py/wrapper.py>`_:

.. code-block:: python

    from spux.executors.mpi4py.wrapper import Wrapper

With the :code:`wrapper = Wrapper (...)` executor attached to the model,
in the model :code:`init (...)` and :code:`run (...)` methods,
the call :code:`self.executor.connect (command)` returns an MPI inter-communicator
connected to the parallel workers, each executing the provided shell command :code:`command` in parallel.
You can use this manager-side inter-communicator to workers for simulation control,
parameters specification, predictions retrieval, and saving/loading of the model state.

The connection procedure from the parallel workers (model) to the manager depends on the connector used in :code:`wrapper = Wrapper (...)`, as described below.
In all cases, in each parallel worker you will have an access to a corresponding inter-communicator with the manager.
You can use this worker-side inter-communicator to manager for simulation control,
parameters acquisition, predictions reporting, and saving/loading of the model state.

For more information, take a look at the corresponding documentation files in :ref:`documentation`.

Spawn connector
~~~~~~~~~~~~~~~

For :code:`connector = Spawn ()`, on the workers (model) side,
you have access to an inter-communicator with the manager returned by calling :code:`MPI_Comm_get_parent ()`.

Split connector
~~~~~~~~~~~~~~~

For :code:`connector = Split (...)`, on the workers (model) side,
you have access to an inter-communicator with the manager returned by calling :code:`MPI_Comm_connect (...)`
with the :code:`port` provided by :code:`self.executor.port`.
You must also pass the value of the :code:`self.executor.port` to the application,
either within the :code:`command` or by writing it out to file that will be read by the application.

Legacy connector
~~~~~~~~~~~~~~~~

Work in progess.
For :code:`connector = Legacy (...)`, on the workers (model) side,
you have access to an inter-communicator with the manager returned by calling :code:`?? TODO :) ??`.

Parallel runs (split)
---------------------

Some HPC systems do not allow dynamically spawning new MPI processes.
In this case, you will need to use a :code:`Split` connector for each executor.
In this example, we use a separate script
`examples/randomwalk/script_split.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/script_split.py>`_:

.. literalinclude:: ../examples/randomwalk/script_split.py
   :language: python
   :linenos:
   :lines: 1-
   :lineno-start: 1

Note the additional connector specification at the to of the script,
the passing of this connector to each executor,
and the initialization of the connector inbetween the SPUX components specification and the sampler execution parts of the script.
We emphasize, that such ordering of the connector and remaining SPUX components is mandatory.

To run SPUX in parallel on 21 cores with MPI using this script, simply execute:

.. code-block:: console

    $ mpiexec -n 21 python -m mpi4py script_split.py

Note, that :code:`-n 21` MUST match the total amount of required resources reported by

.. code-block:: console

    $ sampler.executor.table (resources)

in the script above.

Initially, consider inserting :code:`import sys` and then :code:`sys.exit ()` directly after this line to stop the script,
and run the script only with one core to have the resource table printed:

.. code-block:: console

    $ mpiexec -n 1 ...

Do not forget to remove :code:`sys.exit ()` once you have determined the total amount of cores for MPI.

Parallel runs (legacy)
----------------------

Some HPC systems not only disallow dynamically spawning new MPI processes,
but also do not support modern dynamical MPI process management features such as inter-communicator creation
between two existing MPI intra-communicators using :code:`MPI_Comm_accept ()` and :code:`MPI_Comm_connect ()` methods.
In this case, you will simply need to use a legacy :code:`Legacy` connector
instead of the :code:`Split` connector for each executor in the :code:`script_split.py`.
For your convenience, such example script is also provided in
`examples/randomwalk/script_legacy.py <https://gitlab.com/siam-sc/spux/tree/master/examples/randomwalk/script_legacy.py>`_ (work in progress).

Parallel profiling
------------------

Currently no special scripts for parallel profiling are packaged with SPUX.