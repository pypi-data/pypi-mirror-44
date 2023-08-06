# # # # # # # # # # # # # # # # # # # # # # # # # #
# Plotting class based on MatPlotLib (PyLab)
#
# Jonas Sukys
# Eawag, Switzerland
# jonas.sukys@eawag.ch
# All rights reserved.
# # # # # # # # # # # # # # # # # # # # # # # # # #

from .mpl_utils import matplotlib, brighten, figname
from .mpl_palette_pf import palette
from ..io.format import plain
from ..io.loader import read_params_types

import numpy
import scipy
import pylab
import pandas

# register additional palette colors
for name, color in palette ['colors'] .items ():
    matplotlib.colors.ColorConverter.colors [name] = color

class MatPlotLib (object):
    """Plotting class based on MatPlotLib (PyLab)."""

    # constructor
    def __init__ (self, samples=None, infos=None,
                  prior=None, exact=None,
                  burnin=0, chains=None, replicates=False, names=None, deterministic=False,
                  typesfiles={'parameters' : 'parameters.types', 'predictions' : 'predictions.types'},
                  title=False, legend=True, autosave=True, verbosity=0):

        print (' :: Initializing MatPlotLib plotter...')

        self.samples = samples
        self.infos = infos
        self.prior = prior
        self.exact = exact
        self.burnin = burnin
        self.replicates = replicates
        self.names = names
        self.deterministic = deterministic
        self.types = {}
        for key, typesfile in typesfiles.items ():
            self.types [key] = read_params_types (typesfile) if typesfile is not None else None
        self.title = title
        self.legend = legend
        self.autosave = autosave
        self.verbosity = verbosity
        self.chains = chains if chains is not None else len (infos [0] ['infos']) if infos is not None else None
        if prior is not None or self.samples is not None:
            self.labels = list (prior.labels if prior is not None else self.samples.columns.values)
        else:
            self.labels = None
        if self.infos is not None:
            self.batches = len (self.infos)
        elif self.chains is not None:
            self.batches = len (samples) // self.chains
        else:
            self.batches = None
        self.indices = numpy.arange (self.batches) if self.batches is not None else None
        self._MAP = None

        print ('  : -> Samples:', len (self.samples) if self.samples is not None else 'none')
        print ('  : -> Chains:', self.chains)
        print ('  : -> Infos:', len (self.infos) if self.infos is not None else 'none')
        print ('  : -> Batches:', self.batches)
        print ('  : -> Burn-in:', self.burnin)

    # plot line and range and return handles for legend
    def line_and_range (self, xs, lower, middle, upper, color="k", alpha=0.6, middlealpha=1, style="-", linewidth=1, marker=None, logx=0, logy=0, merged=1, fill=True):
        """Plot line and range and return handles for legend."""

        if fill:
            pylab.fill_between (xs, lower, upper, facecolor=brighten(color), edgecolor=brighten(color), alpha=alpha, linewidth=0)
        edgewidth = 0.3 * linewidth
        area, = pylab.plot (xs, lower, color=color, alpha=alpha, linewidth=edgewidth)
        pylab.plot (xs, upper, color=color, alpha=alpha, linewidth=edgewidth)
        if fill:
            area, = pylab.plot ([], [], color=brighten(color), alpha=alpha, linewidth=10)

        line, = pylab.plot (xs, middle, style, color=color, linewidth=linewidth, marker=marker, markersize=10, alpha=middlealpha, markeredgewidth=linewidth)

        if logx:
            pylab.xscale ("log")
        if logy:
            pylab.yscale ("log")

        if merged:
            handles = (area, line)
        else:
            handles = (line, area)

        return handles

    # custom legend handles (only, no plotting) for line and range plots
    def line_and_range_handles (self, color="k", alpha=0.6, style="-", linewidth=1, marker=None, merged=1):
        """Plot line and range and return handles for legend."""

        area, = pylab.plot ([], [], color=brighten(color), alpha=alpha, linewidth=10)
        line, = pylab.plot ([], [], style, color=color, linewidth=linewidth, marker=marker, markersize=10, markeredgewidth=linewidth)

        if merged:
            handles = (area, line)
        else:
            handles = (line, area)

        return handles

    # save figure
    def save (self, save, formats=["eps", "png", "pdf", "svg"]):
        """Save figure."""

        if isinstance (formats, list):
            base_name = save[:-4]
            if self.burnin > 0:
                base_name += '-unbiased'
            print ('  : -> Saving to:', base_name + '.{' + ','.join (formats) + '}')
            for format in formats:
                pylab.savefig (base_name + "." + format, bbox_inches="tight")
        else:
            print ('  : -> Saving to:', save)
            pylab.savefig (save, bbox_inches="tight")

    # show figures
    def show (self):
        """Show figures."""

        pylab.show()

    # compute extents
    def extents (self, x, y, alpha=0.99):
        """Compute extents."""

        xv = self.samples [x]
        yv = self.samples [y]

        # get prior support intervals, if available
        intervals = self.prior.intervals (alpha) if self.prior is not None else None

        # compute plotting extents
        xvmin = xv.min ()
        xvmax = xv.max ()
        yvmin = yv.min ()
        yvmax = yv.max ()
        xpmin = intervals [x] [0] if intervals is not None else xvmin
        xpmax = intervals [x] [1] if intervals is not None else xvmax
        ypmin = intervals [y] [0] if intervals is not None else yvmin
        ypmax = intervals [y] [1] if intervals is not None else yvmax
        xmin = min (xpmin, xvmin)
        xmax = max (xpmax, xvmax)
        ymin = min (ypmin, yvmin)
        ymax = max (ypmax, yvmax)

        return xmin, xmax, ymin, ymax

    # plot dataset
    def datasets (self, datasets, legend=True, save=None, suffix='', color=None, scientific=True, frame=0):
        """Plot dataset."""

        for label in list (datasets.values ()) [0] .columns.values:

            if not frame:
                print (' :: Plotting datasets for %s' % label)
                pylab.figure()
            names = sorted (list (datasets.keys ()))
            for index, name in enumerate (names):
                data = datasets [name] [label] .dropna ()
                ylabel = label
                xlabel = data.index.name
                if color is None:
                    datacolor = palette ['spaghetti'] [index]
                else:
                    datacolor = color
                if len (data) <= 50:
                    marker = "o"
                    markeredgecolor = datacolor
                    markerfacecolor = 'none'
                    markersize = 6
                    markeredgewidth = 2
                else:
                    marker = "."
                    markeredgecolor = 'none'
                    markerfacecolor = datacolor
                    markersize = 6
                    markeredgewidth = 0
                observations, = pylab.plot (
                    data.index, data,
                    marker=marker,
                    markeredgecolor=markeredgecolor, markerfacecolor=markerfacecolor,
                    markersize=markersize, markeredgewidth=markeredgewidth, linewidth=0,
                    label="observation " + str (name)
                    )
            if not frame:
                pylab.ylabel (ylabel)
                pylab.xlabel (xlabel)
            if self.title:
                pylab.title ("obseravations (data)")
            if self.legend and legend:
                pylab.legend (loc='best')

            if scientific:
                pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

            if not frame:
                pylab.draw ()
                self.save (figname (save, suffix="datasets-%s%s" % (plain (ylabel), suffix)))
            else:
                return observations

    # plot marginal distributions of all parameters
    def distributions (self, distribution, color='spux_blue', alpha=0.99, columns=3, scientific=True, samples=None, exact=False, title=False, save=None, suffix=''):
        """Plot marginal distributions of all parameters."""

        print (' :: Plotting distributions...')
        if len (self.types) > 0:
            print ('  : -> Using the specified types.')
        else:
            print ('  : -> Assuming all types are float.')

        plots = len (distribution.labels)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))

        intervals = distribution.intervals (alpha)
        for index, label in enumerate (sorted (distribution.labels)):
            print ('  : -> For %s...' % label)
            pylab.subplot (rows, columns, index + 1)
            interval = list (intervals [label])
            extent = interval [1] - interval [0]
            interval [0] -= 0.2 * extent
            interval [1] += 0.2 * extent
            if self.types is not None:
                if self.types ['parameters'] is not None and label in self.types ['parameters']:
                    group = 'parameters'
                elif self.types ['predictions'] is not None and label in self.types ['predictions']:
                    group = 'predictions'
                else:
                    group = None
            if self.types is not None and group is not None and self.types [group] [label] == 'int':
                x = numpy.arange (numpy.floor (interval [0]), numpy.ceil (interval [1]) + 1)
                pylab.plot (x, distribution.mpdf (label, x), marker=".", color=color, markersize=10, linewidth=0)
            else:
                x = numpy.linspace (interval [0], interval [1], 1000)
                pylab.plot (x, distribution.mpdf (label, x), color=color, linestyle='-', lw=5)
            ylim = list (pylab.ylim ())
            ylim [0] = 0
            ylim [1] *= 1.05
            pylab.ylim (ylim)
            if samples is not None:
                for name, sample in samples.items ():
                    pylab.axvline (sample [label], color='k', linestyle='-', lw=5, alpha=0.5, label=name)
            if exact and self.exact is not None:
                pylab.axvline (self.exact [label], color='r', linestyle='--', lw=5, alpha=0.5, label='exact')
            pylab.ylim (ylim)
            pylab.xlabel (label)
            pylab.ylabel ('pdf of %s' % label)
            if scientific:
                pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
            if self.title:
                pylab.title ("prior")
            pylab.draw ()
        self.save (figname (save, suffix="distributions%s" % suffix))

    # plot histogram
    def histogram (self, label, indices, densities, interval, color, scale=None, centered=False, log=False, logextent=1e3, interpolation='none'):
        """Plot histogram instead of the provided densities for each index in indices."""

        vs = densities

        if log:
            if centered:
                vs = numpy.abs (vs)
            vs = numpy.where (vs == 0.0, 1e-16, vs)

        gap = (indices [-1] - indices [0]) / (len (indices) - 1)
        extent = ( indices [0] - 0.5 * gap, indices [-1] + 0.5 * gap, interval [0], interval [1] )

        if centered and not log:
            if scale is not None:
                vmax = scale
                vmin = - scale
            else:
                vmax = numpy.max ( numpy.abs (vs) )
                vmin = - numpy.max ( numpy.abs (vs) )
            cmap = 'seismic'
        else:
            vmax = scale if scale is not None else numpy.max (vs)
            vmin = 0.0
            colors = [ brighten (color, factor=1.0 ), color ]
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list ('gradient', colors)

        if log:
            from matplotlib.colors import LogNorm
            vmin = vmax / logextent
            norm = LogNorm (vmin=vmin, vmax=vmax)
        else:
            norm = None

        pylab.imshow (numpy.transpose (vs), cmap=cmap, origin='lower', aspect='auto', norm=norm, extent=extent, interpolation=interpolation, vmin=vmin, vmax=vmax)
        pylab.colorbar ()
        # colorbar = pylab.colorbar ()
        # colorbar.set_label ('probability density')

    # plot marginal distributions over the prediction values in the datasets
    def errors (self, error, datasets, parameters, bins=200, percentiles=5, color='spux_green', columns=3, scientific=True, title=False, save=None, suffix=''):
        """Plot marginal distributions over the prediction values in the datasets."""

        print (" :: Plotting errors...")

        for name, dataset in datasets.items ():

            print ("  : -> For dataset", name)

            data_labels = list (dataset.columns.values)
            error_labels = list (percentiles.keys ())
            plots = len (data_labels)
            rows = numpy.ceil (plots / columns)
            pylab.figure (figsize = (8 * columns, 5 * rows))

            for plot, label in enumerate (data_labels):

                pylab.subplot (rows, columns, plot + 1)

                predictions = dataset.copy (deep=1) [label] .dropna ()

                upper = numpy.empty (len (predictions.index))
                middle = numpy.empty (len (predictions.index))
                lower = numpy.empty (len (predictions.index))

                interval = [float ('inf'), float ('-inf')]

                for index, time in enumerate (predictions.index):

                    distribution = error.distribution (dataset.loc [time], parameters)

                    lower [index], upper [index] = distribution.intervals (1 - 2 * percentiles [error_labels [plot]] / 100.0) [error_labels [plot]]
                    if hasattr (error, 'transform'):
                        middle [index] = error.transform (dataset.loc [time], parameters) [error_labels [plot]]
                    else:
                        middle [index] = predictions.loc [time]

                    lowest, highest = distribution.intervals (0.999) [error_labels [plot]]
                    if lowest < interval [0]:
                        interval [0] = lowest
                    if highest > interval [1]:
                        interval [1] = highest

                extent = interval [1] - interval [0]
                interval [0] -= 0.1 * extent
                interval [1] += 0.1 * extent

                if self.types ['predictions'] is not None and self.types ['predictions'] [label] == 'int':
                    locations = numpy.arange (numpy.floor (interval [0]), numpy.ceil (interval [1]) + 1)
                else:
                    locations = numpy.linspace (interval [0], interval [1], bins)
                densities = numpy.empty ((len (predictions.index), len (locations)))

                for index, time in enumerate (predictions.index):
                    distribution = error.distribution (dataset.loc [time], parameters)
                    densities [index] [:] = distribution.mpdf (error_labels [plot], locations)

                self.histogram (error_labels [plot], predictions.index, densities, interval, color)
                percentiles_handles = self.line_and_range (predictions.index, lower, middle, upper, linewidth=2, color='dimgray', alpha=0.5, middlealpha=0.5, merged=False, fill=False)
                single_dataset = { name : pandas.DataFrame (middle, columns=[error_labels [plot]], index=predictions.index) }
                observations_handle = self.datasets (single_dataset, save, suffix, color='dimgray', frame=1)
                pylab.ylabel (error_labels [plot])
                pylab.xlabel (dataset.index.name)
                pylab.ylim (interval)
                handles = percentiles_handles + (observations_handle,)
                labels = ["error median", "error percentiles (%s - %s)" % (str(percentiles [error_labels [plot]]), str(100 - percentiles [error_labels [plot]])), "observations"]
                if scientific:
                    pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
                if self.legend:
                    pylab.legend (handles, labels, loc="best")

            if self.title:
                pylab.title ("errors")
            pylab.draw ()
            self.save (figname (save, suffix="errors-dataset-%s%s" % (name, suffix)))

    # return maximum a posteriori (MAP) estimate of parameters and the associated posterior estimate
    def MAP (self):
        """Return maximum a posteriori (MAP) estimate of parameters and the associated posterior estimate."""

        print (' :: Computing MAP...')

        sample = None if not self.replicates else {}
        Lp = float ('-inf')

        # look through each batch and chain
        for batch in self.indices [self.burnin:]:
            info = self.infos [batch]
            for chain in range (len (info ['posteriors'])):

                # check if chain 'infos' is not None
                if info ['infos'] [chain] is None:
                    continue

                # no replicates - all straight forward
                if not self.replicates:

                    # check if likelihood was successful
                    if not info ['infos'] [chain] ['successful']:
                        continue

                    # get the MAP likelihood of the the PF MAP, if available
                    if 'MAP' in info ['infos'] [chain]:
                        #particles = True
                        predictions = info ['infos'] [chain] ['MAP'] ['predictions']
                        error = info ['infos'] [chain] ['MAP'] ['error']
                    else:
                        #particles = False
                        predictions = info ['infos'] [chain] ['predictions']

                    # compute the joint posterior of parameter posterior and PF MAP error
                    posterior = info ['posteriors'] [chain]
                    # posterior = (error if particles else 0) + info ['priors'] [chain]

                # replicates - need predictions for each dataset
                else:

                    predictions = {}
                    error = {}

                    # check if replicate likelihood was successful
                    if not info ['infos'] [chain] ['successful']:
                        continue

                    successful = True
                    for name in info ['infos'] [chain] ['infos'] .keys ():

                        # check if likelihood was successful
                        if not info ['infos'] [chain] ['infos'] [name] ['successful']:
                            successful = False
                            break

                        if 'MAP' in info ['infos'] [chain] ['infos'] [name]:
                            #particles = True
                            predictions [name] = info ['infos'] [chain] ['infos'] [name] ['MAP'] ['predictions']
                            error [name] = info ['infos'] [chain] ['infos'] [name] ['MAP'] ['error']
                        else:
                            #particles = False
                            predictions [name] = info ['infos'] [chain] ['infos'] [name] ['predictions']

                    if not successful:
                        continue

                    # compute the joint posterior of parameter posterior and PF MAP error
                    posterior = info ['posteriors'] [chain]
                    # posterior = (numpy.sum (list (error.values ())) if particles else 0) + info ['priors'] [chain]

                # check if the joint posterior is larger than current Lp
                if posterior > Lp:
                    Lp = posterior
                    sample = {}
                    sample ['parameters'] = info ['parameters'] .loc [chain]
                    sample ['predictions'] = predictions
                    sample ['posterior'] = posterior
                    sample ['batch'] = batch
                    sample ['chain'] = chain

        print (' :: Estimated marginal MAP parameters:')
        print (sample ['parameters'])
        # print (' :: -> Joint (parameters and realizations, if available) MAP log-posterior: %1.1e' % Lp)
        # Lp = self.infos [sample ['batch']] ['posteriors'] [sample ['chain']]
        print (' :: -> Estimated marginal MAP parameters log-posterior: %1.1e' % Lp)
        # L = self.infos [sample ['batch']] ['likelihoods'] [sample ['chain']]
        # print (' :: -> Parameters MAP log-likelihood: %1.1e' % L)
        # p = self.infos [sample ['batch']] ['priors'] [sample ['chain']]
        # print (' :: -> Parameters MAP log-prior: %1.1e' % p)

        self._MAP = sample

    # plot evolution of all parameters samples
    def parameters (self, MAP=True, alpha=0.99, columns=3, merged=True, percentile=5, exact=True, legend=False, scientific=True, save=None, suffix=''):
        """Plot evolution of all parameters samples."""

        print (' :: Plotting parameters...')

        plots = len (self.prior.labels)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))

        linewidth = 2 if plots <= columns else 4

        intervals = self.prior.intervals (alpha)

        for index, label in enumerate (sorted (self.prior.labels)):
            pylab.subplot (rows, columns, index + 1)
            support = list (intervals [label])
            interval = support [:]
            if not merged:
                for chain in range (self.chains):
                    samples = self.samples [label] .iloc [chain::self.chains] .iloc [self.burnin:]
                    pylab.plot (self.indices [self.burnin:], samples, color=palette ['spaghetti'][chain], linestyle='-', lw=linewidth)
                    interval [0] = min (interval [0], numpy.min (samples))
                    interval [1] = max (interval [1], numpy.max (samples))
            else:
                median = numpy.empty (self.batches - self.burnin)
                upper = numpy.empty (self.batches - self.burnin)
                lower = numpy.empty (self.batches - self.burnin)
                for i in range (len (self.indices [self.burnin:])):
                    parameters = self.samples [label] .iloc [(i + self.burnin) * self.chains : (i + self.burnin + 1) * self.chains]
                    median [i] = numpy.median (parameters)
                    lower [i] = numpy.percentile (parameters, percentile)
                    upper [i] = numpy.percentile (parameters, 100 - percentile)
                self.line_and_range (self.indices [self.burnin:], lower, median, upper, color='spux_orange', linewidth=linewidth, alpha=0.9)
                interval [0] = min (interval [0], numpy.min (lower))
                interval [1] = max (interval [1], numpy.max (upper))
            extent = interval [1] - interval [0]
            interval [0] -= 0.2 * extent
            interval [1] += 0.2 * extent
            pylab.ylim (interval)
            pylab.axhline (support [0], color='gray', linestyle='-', alpha=0.5, lw=5)
            pylab.axhline (support [1], color='gray', linestyle='-', alpha=0.5, lw=5)
            if MAP and self._MAP is not None:
                if not merged:
                    location = self._MAP ['batch']
                    value = self.samples [label] .iloc [self._MAP ['batch'] * self.chains + self._MAP ['chain']]
                    pylab.plot (location, value, marker="o", color="brown", markerfacecolor='none', markersize=10, markeredgewidth=2, linewidth=0, label="MAP")
                else:
                    pylab.axhline (self._MAP ['parameters'] [label], color='brown', linestyle=':', alpha=0.5, lw=5)
            if exact and self.exact is not None:
                pylab.axhline (self.exact [label], color='r', linestyle='--', alpha=0.5, lw=5)
            if scientific:
                pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
            pylab.ylabel (label)
            pylab.xlabel ('sample')
            if self.title:
                pylab.title("parameters")
            pylab.draw()
        self.save (figname (save, suffix="parameters%s" % suffix))

    # evaluate 1D kde estimator
    def kde (self, samples, x):
        """Evaluate 1D kde estimator."""

        # density = suftware.DensityEstimator (samples)
        # return density.evaluate (x)

        density = scipy.stats.gaussian_kde (samples)
        return density (x)

    # plot marginal posterior distributions of all parameters
    def posteriors (self, initial=True, MAP=True, alpha=0.99, columns=3, exact=True, prior=True, legend=False, scientific=True, save=None, suffix=''):
        """Plot marginal posterior distributions of all parameters."""

        print (' :: Plotting posteriors...')
        if self.types ['parameters'] is not None:
            print ('  : -> Using the specified types.')
        else:
            print ('  : -> Assuming all types are float.')

        plots = len (self.prior.labels)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))

        percentile = (1 - alpha) / 2 * 100
        intervals = self.prior.intervals (alpha)

        for plot, label in enumerate (sorted (self.prior.labels)):
            pylab.subplot (rows, columns, plot + 1)
            interval = list (intervals [label])
            samples = self.samples [label] .values [self.burnin * self.chains:]
            interval [0] = min (interval [0], numpy.percentile (samples, percentile))
            interval [1] = max (interval [1], numpy.percentile (samples, 100 - percentile))
            extent = interval [1] - interval [0]
            interval [0] -= 0.2 * extent
            interval [1] += 0.2 * extent
            if self.types ['parameters'] is not None and self.types ['parameters'] [label] == 'int':
                x = numpy.arange (numpy.floor (interval [0]), numpy.ceil (interval [1]) + 1)
                if prior:
                    pylab.plot (x, self.prior.mpdf (label, x), color='spux_blue', marker=".", markersize=10, linewidth=0)
                pylab.plot (x, self.kde (samples, x), color='spux_orange', marker=".", markersize=10, linewidth=0)
            else:
                x = numpy.linspace (interval [0], interval [1], 1000)
                if prior:
                    pylab.plot (x, self.prior.mpdf (label, x), color='spux_blue', linestyle='-', lw=5)
                pylab.plot (x, self.kde (samples, x), color='spux_orange', linestyle='-', lw=5)
            ylim = list (pylab.ylim ())
            ylim [0] = 0
            ylim [1] *= 1.05
            pylab.ylim (ylim)
            if MAP and self._MAP is not None:
                pylab.axvline (self._MAP ['parameters'] [label], color='brown', linestyle=':', alpha=0.5, lw=5)
            if exact and self.exact is not None:
                pylab.axvline (self.exact [label], color='r', linestyle='--', alpha=0.5, lw=5)
            if scientific:
                pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
            pylab.ylim (ylim)
            pylab.xlabel (label)
            pylab.ylabel ('pdf of %s' % label)
            if self.title:
                pylab.title("posterior")
            pylab.draw()
        self.save(figname(save, suffix="posteriors%s" % suffix))

    # # compute pairwise joint kde
    # def kde2d (self, xv, yv, xmin, xmax, ymin, ymax, points=100j):
    #     """Compute pairwise joint kde."""

    #     # estimate posterior PDF with a KDE
    #     xsg, ysg = numpy.mgrid[xmin:xmax:points, ymin:ymax:points]
    #     positions = numpy.vstack([xsg.ravel(), ysg.ravel()])
    #     values = numpy.vstack([xv, yv])
    #     kernel = scipy.stats.gaussian_kde(values)
    #     Z = numpy.reshape(kernel(positions).T, xsg.shape)
    #     return Z

    # plot pairwise joint posterior distributions of all parameters
    # with chains in subdiagonals and histograms in superdiagonals
    def posteriors2d (self, color="spux_orange", bins=30, initial=True, MAP=True, exact=True, legend=False, scientific=True, save=None, suffix=''):
        """Plot pairwise joint posterior distributions of all parameters."""

        print (' :: Plotting all pairwise joint posteriors..')

        plots = len (self.labels)
        canvas = pylab.figure (figsize = (6 * plots, 6 * plots))
        canvas.subplots_adjust (hspace = 0, wspace = 0)

        for i, label_i in enumerate (sorted (self.labels)):
            for j, label_j in enumerate (sorted (self.labels)):
                pylab.subplot (plots, plots, j * plots + i + 1)
                if i == j:
                    xmin, xmax, ymin, ymax = self.extents (label_i, label_j)
                    pylab.xlim ([xmin, xmax])
                    pylab.ylim ([ymin, ymax])
                    pylab.gca().text (0.5, 0.5, label_i, fontsize=60, verticalalignment='center', horizontalalignment='center', transform=pylab.gca().transAxes)
                    if scientific:
                        pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
                else:
                    kde = (i < j)
                    chains = (i > j)
                    self.posterior2d (label_i, label_j, color, kde, chains, initial, MAP, exact, legend, scientific, bins, save, suffix, frame=True)
                pylab.xlabel (None)
                pylab.ylabel (None)
                if j != (plots - 1):
                    pylab.gca().set_xticklabels ([])
                if i != 0:
                    pylab.gca().set_yticklabels ([])
                pylab.gca().axis ('equal')

        self.save (figname (save, suffix="posteriors2d" + suffix))

    # plot pairwise joint posterior
    def posterior2d (self, x, y, color="spux_orange", kde=True, chains=True, initial=True, MAP=True, exact=True, legend=False, scientific=True, bins=30, save=None, suffix="", frame=False):
        """Plot pairwise joint posterior."""

        print ('  : -> For %s and %s (%d chains)' % (x, y, self.chains))

        xv = self.samples [x] .iloc [self.burnin * self.chains:]
        yv = self.samples [y] .iloc [self.burnin * self.chains:]

        xmin, xmax, ymin, ymax = self.extents (x, y)

        if not frame:
            pylab.figure ()

        # plot 2d KDE for posterior PDF
        if kde:

            samples = self.samples.iloc [self.burnin * self.chains:]
            colors = [brighten (color, factor=1.0 ), color]
            cmap = matplotlib.colors.LinearSegmentedColormap.from_list ('gradient', colors)
            samples.plot.hexbin (x, y, gridsize=(bins, bins), colormap=cmap, xlim=(xmin, xmax), ylim=(ymin, ymax), colorbar=(not frame), ax=pylab.gca())
            # kde2d = self.kde2d (xv, yv, xmin, xmax, ymin, ymax)
            # pylab.imshow (numpy.transpose (kde2d), origin="lower", aspect="auto", extent=[xmin, xmax, ymin, ymax], cmap="YlOrBr")
            # if not frame:
            #     colorbar = pylab.colorbar()
            #     colorbar.set_label("probability density")

        # plot all posterior samples and paths of each chain
        if chains:
            for chain in range (self.chains):
                xs = xv.iloc [chain::self.chains]
                ys = yv.iloc [chain::self.chains]
                color = 'dimgray'
                pylab.plot (xs, ys, color=color, marker=".", markersize=10, markeredgewidth=0, alpha=0.2, label="chain %d" % chain)

        # plot initial parameter set
        if initial and chains:
            x0 = self.samples [x] [self.burnin * self.chains:] [0:self.chains]
            y0 = self.samples [y] [self.burnin * self.chains:] [0:self.chains]
            pylab.plot (x0, y0, marker="+", color="spux_blue", markersize=10, markeredgewidth=2, linewidth=0, label="initial")

        # plot MAP
        if MAP and self._MAP is not None:
            pylab.plot (self._MAP ['parameters'] [x], self._MAP ['parameters'] [y], marker="o", color="brown", markerfacecolor='none', markersize=10, markeredgewidth=2, linewidth=0, label="MAP")

        # plot exact parameter set
        if exact and self.exact is not None:
            pylab.plot (self.exact [x], self.exact [y], marker="x", color="r", markersize=10, markeredgewidth=3, linewidth=0, label="exact")

        # set axes extents
        pylab.xlim ([xmin, xmax])
        pylab.ylim ([ymin, ymax])

        # use scientific format for axes tick labels
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

        # add legend
        if self.legend and legend:
            pylab.legend (loc="best", numpoints=1)

        if self.title:
            pylab.title("joint posterior")

        # add axes labels
        pylab.xlabel (x)
        pylab.ylabel (y)

        pylab.draw ()

        if not frame:
            self.save (figname (save, suffix="posterior2d-%s-%s%s" % (plain (x), plain (y), suffix)))

    # plot likelihoods (and acceptances, if requested)
    def likelihoods (self, MAP=True, acceptances=False, unsuccessfuls=False, merged=True, percentile=5, palette=palette['likelihoods'], scientific=True, save=None, suffix=""):
        """Plot likelihoods (and acceptances or unsuccessfuls, if requested)."""

        print (' :: Plotting likelihoods%s...' % (' and acceptances' if acceptances else ' and unsuccessfuls' if unsuccessfuls else ''))

        pylab.figure ()

        # likelihoods
        if merged:

            L_means = numpy.empty (len (self.indices) - self.burnin)
            L_lower = numpy.empty (len (self.indices) - self.burnin)
            L_upper = numpy.empty (len (self.indices) - self.burnin)
            Lp_means = numpy.empty (len (self.indices) - self.burnin)
            Lp_lower = numpy.empty (len (self.indices) - self.burnin)
            Lp_upper = numpy.empty (len (self.indices) - self.burnin)

            for index, batch in enumerate (self.indices [self.burnin:]):
                likelihood = [ self.infos [batch] ['likelihoods'] [chain] for chain in range (self.chains) ]
                posterior = [ self.infos [batch] ['posteriors'] [chain] for chain in range (self.chains) ]
                L_means [index] = numpy.nanmedian (likelihood)
                L_lower [index] = numpy.nanpercentile (likelihood, percentile)
                L_upper [index] = numpy.nanpercentile (likelihood, 100 - percentile)
                Lp_means [index] = numpy.nanmedian (posterior)
                Lp_lower [index] = numpy.nanpercentile (posterior, percentile)
                Lp_upper [index] = numpy.nanpercentile (posterior, 100 - percentile)

            handles_likelihood = self.line_and_range (self.indices [self.burnin:], L_lower, L_means, L_upper, linewidth=2, color=palette ['likelihood'], alpha=0.6)
            handles_likelihood = (handles_likelihood,)
            handle_posterior = self.line_and_range (self.indices [self.burnin:], Lp_lower, Lp_means, Lp_upper, linewidth=2, color=palette ['posterior'], alpha=0.6)

        else:

            for chain in range (self.chains):
                likelihood = [ info ['likelihoods'] [chain] for info in self.infos [self.burnin:] ]
                posterior = [ info ['posteriors'] [chain] for info in self.infos [self.burnin:] ]
                if self.deterministic:
                    pylab.plot (self.indices [self.burnin:], likelihood, lw=1, color=palette ['spaghetti'][chain], linestyle='-')
                else:
                    variance = numpy.empty (len (self.infos) - self.burnin)
                    if not self.replicates:
                        for index, info in enumerate (self.infos [self.burnin:]):
                            if info ['infos'] [chain] is not None:
                                variance [index] = info ['infos'] [chain] ['variance']
                            else:
                                variance [index] = float ('nan')
                    else:
                        for index, info in enumerate (self.infos [self.burnin:]):
                            if info ['infos'] [chain] is not None:
                                variances = [ replicate ['variance'] for replicate in info ['infos'] [chain] ['infos'] .values () ]
                                variance [index] = numpy.sum (variances)
                            else:
                                if self.verbosity:
                                    print (' :: WARNING: NaN variance at', chain, index)
                                variance [index] = float ('nan')
                    lower = likelihood - numpy.sqrt (variance)
                    upper = likelihood + numpy.sqrt (variance)
                    self.line_and_range (self.indices [self.burnin:], lower, likelihood, upper, merged=0, linewidth=1, color=palette ['spaghetti'][chain])
                pylab.plot (self.indices [self.burnin:], posterior, lw=1, color=palette ['spaghetti'][chain], linestyle=':')
            if self.deterministic:
                handles_likelihood, = pylab.plot ([], [], lw=1, color='dimgray', linestyle='-')
            else:
                handles_likelihood = self.line_and_range_handles (merged=0, linewidth=2, color='dimgray')
            handle_posterior, = pylab.plot ([], [], lw=2, color='dimgray', linestyle=':')

        if MAP and self._MAP is not None:
            location = self._MAP ['batch']
            value = self.infos [self._MAP ['batch']] ['posteriors'] [self._MAP ['chain']]
            handle_map, = pylab.plot (location, value, marker="o", color="brown", markerfacecolor='none', markersize=10, markeredgewidth=2, linewidth=0)

        pylab.xlabel("sample")
        pylab.ylabel("log-probability")
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

        # unsuccessfuls
        if unsuccessfuls:
            fail = numpy.empty (self.batches - self.burnin)
            skip = numpy.empty (self.batches - self.burnin)
            for batch, info in enumerate (self.infos [self.burnin:]):
                successful = [ info ['infos'] [chain] ['successful'] if info ['infos'] [chain] is not None else None for chain in range (self.chains) ]
                fail [batch] = len ( [ state for state in successful if state is False ] )
                skip [batch] = len ( [ state for state in successful if state is None ] )
            fail = numpy.where (fail != 0, fail, float ('nan'))
            skip = numpy.where (skip != 0, skip, float ('nan'))
            pylab.sca (pylab.twinx())
            handle_fail, = pylab.plot (self.indices [self.burnin:], fail, marker="x", color="r", markerfacecolor='none', markersize=5, markeredgewidth=1, linewidth=0)
            handle_skip, = pylab.plot (self.indices [self.burnin:], skip, marker="o", color="r", markerfacecolor='none', markersize=5, markeredgewidth=1, linewidth=0)
            pylab.ylabel("counts")
            pylab.ylim ((0, 1.05 * self.chains))

        # acceptances
        if acceptances and not unsuccessfuls:
            pylab.sca (pylab.twinx())
            handle_accept = self.acceptances (merged=merged, frame=True)

        handles = handles_likelihood
        if merged or self.deterministic:
            labels = ["log-likelihood estimate (scaled)"]
        else:
            labels = ["log-likelihood estimate (scaled)", "log-likelihood deviation (scaled)"]
        handles += (handle_posterior,)
        labels += ["log-posterior estimate (scaled)"]
        if unsuccessfuls:
            handles += (handle_fail, handle_skip)
            labels += ["NaN posterior", "zero prior"]
        if MAP and self._MAP is not None:
            handles += (handle_map,)
            labels += ["MAP"]
        if acceptances and not unsuccessfuls:
            handles += (handle_accept,)
            labels += ["acceptance rate"]
        if self.legend:
            pylab.legend (handles, labels, loc="best")

        if self.title:
            pylab.title ("log-likelihood and log-posterior" + (" and acceptance rate" if acceptances else " and unsuccessfulls" if unsuccessfuls else ""))
        pylab.draw()
        self.save (figname (save, suffix="likelihoods" + suffix))

    # plot report for unsuccessful posteriors
    def unsuccessfuls (self, scientific=True, save=None, suffix=""):
        """Plot report for unsuccessful posteriors."""

        print (' :: Plotting unsuccessful posteriors...')

        pylab.figure()

        fail = numpy.empty (self.batches - self.burnin)
        skip = numpy.empty (self.batches - self.burnin)
        for batch, info in enumerate (self.infos [self.burnin:]):
            successful = [ info ['infos'] [chain] ['successful'] if info ['infos'] [chain] is not None else None for chain in range (self.chains) ]
            fail [batch] = len ( [ state for state in successful if state is False ] )
            skip [batch] = len ( [ state for state in successful if state is None ] )
        fail = numpy.where (fail != 0, fail, float ('nan'))
        skip = numpy.where (skip != 0, skip, float ('nan'))
        handle_fail = pylab.bar (self.indices [self.burnin:], fail, color="firebrick")
        handle_skip = pylab.bar (self.indices [self.burnin:], skip, bottom=fail, color="lightgray")
        pylab.ylabel("counts")
        pylab.ylim ((0, 1.05 * self.chains))
        pylab.xlabel("sample")
        pylab.axhline (self.chains, color='gray', linestyle='-', alpha=0.5, lw=5)
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

        handles = (handle_fail, handle_skip)
        labels = ["NaN posterior", "zero prior"]
        if self.legend:
            pylab.legend (handles, labels, loc="best")

        if self.title:
            pylab.title ("unsuccessful posteriors")
        pylab.draw()
        self.save (figname (save, suffix="unsuccessfuls" + suffix))

    # plot redraw rate
    def redraw (self, MAP=True, percentile=5, scientific=True, save=None, suffix=""):
        """Plot redraw rate."""

        print (' :: Plotting redraw...')

        pylab.figure()

        means = numpy.empty (len (self.infos) - self.burnin)
        lower = numpy.empty (len (self.infos) - self.burnin)
        upper = numpy.empty (len (self.infos) - self.burnin)

        for batch, info in enumerate (self.infos [self.burnin:]):
            available = [ chain for chain in info ['infos'] if chain is not None ]
            values = [ redraw for chain in available for replicate in chain ['infos'] .values () for redraw in replicate ["redraw"] .values() ]
            means [batch] = numpy.mean (values) if values != [] else float ('nan')
            lower [batch] = numpy.percentile (values, percentile) if values != [] else float ('nan')
            upper [batch] = numpy.percentile (values, 100 - percentile) if values != [] else float ('nan')

        handles = self.line_and_range (self.indices [self.burnin:], lower, means, upper, merged=0, linewidth=2, color="olivedrab")

        if MAP and self._MAP is not None:
            pylab.axvline (self._MAP ['batch'], color="brown", linestyle=':', lw=2, alpha=0.5, label="MAP")
        if self.legend:
            pylab.legend (handles, ["mean", "range"], loc="best")

        if self.title:
            pylab.title("particle redraw rate")
        pylab.xlabel("sample")
        pylab.xlim((self.indices [self.burnin], self.indices [-1]))
        pylab.ylabel("redraw rate")
        pylab.ylim([-0.05, 1.05])
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
        pylab.draw()
        self.save(figname(save, suffix="redraw" + suffix))

    def deviations (self, merged=True, percentile=5, palette=palette['deviations'], scientific=True, save=None, suffix=""):
        """Plot standard deviations of the marginal likelihood estimates."""

        if self.deterministic:
            print (' :: ERROR: Deviations for log-likelihood are not available for deterministic models.')
            return

        print (' :: Plotting deviations...')

        pylab.figure()

        if merged:

            means = numpy.empty (len (self.indices) - self.burnin)
            lower = numpy.empty (len (self.indices) - self.burnin)
            upper = numpy.empty (len (self.indices) - self.burnin)

            for index, batch in enumerate (self.indices [self.burnin:]):
                variance = numpy.empty (self.chains)
                if not self.replicates:
                    for chain in range (self.chains):
                        if self.infos [batch] ['infos'] [chain] is not None:
                            variance [chain] = self.infos [batch] ['infos'] [chain] ['variance']
                        else:
                            variance [chain] = float ('nan')
                else:
                    for chain in range (self.chains):
                        if self.infos [batch] ['infos'] [chain] is not None:
                            variances = [ replicate ['variance'] for replicate in self.infos [batch] ['infos'] [chain] ['infos'] .values () ]
                            variance [chain] = numpy.sum (variances)
                        else:
                            if self.verbosity:
                                print (' :: WARNING: NaN deviation at', chain, index)
                            variance [chain] = float ('nan')
                deviation = numpy.sqrt (variance)
                means [index] = numpy.nanmedian (deviation)
                lower [index] = numpy.nanpercentile (deviation, percentile)
                upper [index] = numpy.nanpercentile (deviation, 100 - percentile)

            self.line_and_range (self.indices [self.burnin:], lower, means, upper, linewidth=2, color=palette)

        else:

            for chain in range (self.chains):
                variance = numpy.empty (len (self.infos) - self.burnin)
                if not self.replicates:
                    for index, info in enumerate (self.infos [self.burnin:]):
                        if info ['infos'] [chain] is not None:
                            variance [index] = info ['infos'] [chain] ['variance']
                        else:
                            variance [index] = float ('nan')
                else:
                    for index, info in enumerate (self.infos [self.burnin:]):
                        if info ['infos'] [chain] is not None:
                            variances = [ replicate ['variance'] for replicate in info ['infos'] [chain] ['infos'] .values () ]
                            variance [index] = numpy.sum (variances)
                        else:
                            if self.verbosity:
                                print (' :: WARNING: NaN deviation at', chain, index)
                            variance [index] = float ('nan')
                pylab.plot (self.indices [self.burnin:], numpy.sqrt (variance), lw=2, color=palette ['spaghetti'] [chain])

        pylab.xlabel("sample")
        pylab.ylabel("std. deviation of log-likelihood")
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
        pylab.xlim((self.indices[self.burnin], self.indices[-1]))
        pylab.ylim ((0, pylab.ylim()[1]))
        if self.title:
            pylab.title ("std. deviation of log-likelihood")
        pylab.draw()
        self.save (figname (save, suffix="deviations" + suffix))

    # plot acceptances
    def acceptances (self, MAP=True, merged=True, palette=palette['acceptances'], scientific=True, save=None, suffix="", start=1, frame=False):
        """Plot acceptancess."""

        print (' :: Plotting acceptances...')

        # check if available
        acceptances = 'accepts' in self.infos [0]
        if not acceptances:
            print ('  -> Acceptances not available')
            return None

        if not frame:
            pylab.figure()

        # plot acceptances

        rolling = {}
        for chain in range (self.chains):
            accept = [ info ['accepts'] [chain] for info in self.infos [self.burnin:] ]
            rolling [chain] = numpy.cumsum (accept [start:]) / numpy.arange (1, len (accept) + 1 - start, dtype=float)

        if merged:

            means = numpy.empty (len (self.indices) - self.burnin - start)
            lower = numpy.empty (len (self.indices) - self.burnin - start)
            upper = numpy.empty (len (self.indices) - self.burnin - start)

            for index, batch in enumerate (self.indices [self.burnin:] [start:]):
                accept = [ rolling [chain] [index] for chain in range (self.chains) ]
                means [index] = numpy.nanmedian (accept)
                lower [index] = numpy.nanmin (accept)
                upper [index] = numpy.nanmax (accept)

            handles = self.line_and_range (self.indices [self.burnin:] [start:], lower, means, upper, linewidth=2, color=palette)

        else:

            rolling = {}
            for chain in range (self.chains):
                handles, = pylab.plot (self.indices [self.burnin:] [start:], rolling [chain], color=palette ['spaghetti'][chain], linewidth=2)
            if MAP and self._MAP is not None:
                location = self._MAP ['batch']
                value = rolling [self._MAP ['chain']] [self._MAP ['batch'] - start]
                pylab.plot (location, value, marker="o", color="brown", markerfacecolor='none', markersize=10, markeredgewidth=2, linewidth=0, label="MAP")

        pylab.ylabel("acceptance rate")
        pylab.xlabel ("sample")
        pylab.ylim((-0.05, 1.05))
        pylab.xlim((self.indices [self.burnin], self.indices [-1]))
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
        if not frame:
            if self.title:
                pylab.title ("acceptance rate")
            pylab.draw ()
            self.save (figname (save, suffix="acceptances" + suffix))

        return handles

    # plot autocorrelations
    def autocorrelations (self, columns=3, save=None, suffix='', split=1, merge=True):
        """Plot autocorrelations."""

        print (' :: Plotting autocorrelations...')

        plots = len (self.samples.columns)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))

        for plot, (label, series) in enumerate (self.samples.iteritems ()):
            print ('  : -> For %s...' % label)
            pylab.subplot (rows, columns, plot + 1)
            if split:
                if merge:
                    length = (len (series) // self.chains - self.burnin) // 2
                    lags = length - 1
                    upper = numpy.empty (lags, dtype=float)
                    means = numpy.empty (lags, dtype=float)
                    lower = numpy.empty (lags, dtype=float)
                    for lag in range (lags):
                        acors = [ series [chain::self.chains] [self.burnin:] .autocorr (lag = lag) for chain in range (self.chains) ]
                        upper [lag] = numpy.max (acors)
                        means [lag] = numpy.mean (acors)
                        lower [lag] = numpy.min (acors)
                    self.line_and_range (range (lags), lower, means, upper, color='r', linewidth = 2)
                    pylab.xlabel ('lag')
                    pylab.ylabel ('autocorrelation of %s' % label)
                    pylab.ylim ((-1, 1))
                else:
                    for chain in range (self.chains):
                        pandas.plotting.autocorrelation_plot (series [chain::self.chains] [self.burnin:], lw=2, color=palette ['spaghetti'] [chain])
            else:
                pandas.plotting.autocorrelation_plot (series [self.burnin * self.chains:], lw=5, color='r')
        pylab.draw ()
        self.save(figname(save, suffix="autocorrelations" + suffix))

    # plot posterior model predictions including observations
    def predictions (self, datasets, labels=None, MAP=True, bins=200, log=True, percentile=5, scientific=True, columns=3, save=None, suffix=""):
        """Plot posterior model predictions including observations."""

        print (' :: Plotting predictions for each dataset...')

        if labels is None:
            labels = list (list (datasets.values ()) [0] .columns.values)

        plots = len (labels)
        rows = numpy.ceil (plots / columns)

        for plot, (name, dataset) in enumerate (datasets.items ()):

            print (' : -> For dataset', name)
            pylab.figure (figsize = (8 * columns, 5 * rows))

            for plot, label in enumerate (labels):

                times = dataset.index

                lower = numpy.empty (len (times))
                upper = numpy.empty (len (times))

                interval = [float ('inf'), float ('-inf')]
                values = {}
                weights = {}
                last = [ None for chain in range (self.chains) ]

                for index, time in enumerate (times):
                    values [time] = []
                    weights [time] = []
                    for sample, info in enumerate (self.infos [self.burnin:]):
                        if not self.replicates:
                            available = [ (chain, chaininfo) for chain, chaininfo in enumerate (info ['infos']) if chaininfo is not None and chaininfo ['successful'] ]
                            for chain, chaininfo in available:
                                if info ['accepts'] [chain]:
                                    last [chain] = []
                                    for i, value in enumerate (chaininfo ['predictions'] [time] [label] .values):
                                        weight = chaininfo ['weights'] [time] [i]
                                        values [time] += [value]
                                        weights [time] += [weight]
                                        last [chain] += [(weight, value)]
                                else:
                                    if last [chain] is None:
                                        source = sample
                                        for source in range (self.burnin + sample - 1, -1, -1):
                                            lastinfo = self.infos [source] ['infos'] [chain]
                                            if lastinfo is not None and lastinfo ['successful'] and self.infos [source] ['accepts'] [chain]:
                                                last [chain] = []
                                                for i, value in enumerate (lastinfo ['predictions'] [time] [label] .values):
                                                    weight = lastinfo ['weights'] [time] [i]
                                                    values [time] += [value]
                                                    weights [time] += [weight]
                                                    last [chain] += [(weight, value)]
                                                break
                                    for weight, value in last [chain]:
                                        values [time] += [value]
                                        weights [time] += [weight]

                        else:
                            available = [ (chain, chaininfo) for chain, chaininfo in enumerate (info ['infos']) if chaininfo is not None and chaininfo ['infos'] [name] ['successful'] ]
                            for chain, chaininfo in available:
                                if info ['accepts'] [chain]:
                                    last [chain] = []
                                    for i, value in enumerate (chaininfo ['infos'] [name] ['predictions'] [time] [label] .values):
                                        weight = chaininfo ['infos'] [name] ['weights'] [time] [i]
                                        values [time] += [value]
                                        weights [time] += [weight]
                                        last [chain] += [(weight, value)]
                                else:
                                    if last [chain] is None:
                                        source = sample
                                        for source in range (self.burnin + sample - 1, -1, -1):
                                            lastinfo = self.infos [source] ['infos'] [chain]
                                            if lastinfo is not None and lastinfo ['infos'] [name] ['successful'] and self.infos [source] ['accepts'] [chain]:
                                                last [chain] = []
                                                for i, value in enumerate (lastinfo ['infos'] [name] ['predictions'] [time] [label] .values):
                                                    weight = lastinfo ['infos'] [name] ['weights'] [time] [i]
                                                    values [time] += [value]
                                                    weights [time] += [weight]
                                                    last [chain] += [(weight, value)]
                                                break
                                    for weight, value in last [chain]:
                                        values [time] += [value]
                                        weights [time] += [weight]

                    replicated = [ value for i, value in enumerate (values [time]) for copy in range (weights [time] [i]) ]
                    try:
                        lower [index] = numpy.percentile (replicated, percentile)
                        upper [index] = numpy.percentile (replicated, 100 - percentile)
                    except:
                        if self.verbosity:
                            print (' :: WARNING: percentiles failed for', label, name, time)
                        lower [index] = float ('nan')
                        upper [index] = float ('nan')
                    lowest = numpy.percentile (values [time], 0.05)
                    highest = numpy.percentile (values [time], 99.95)
                    if lowest < interval [0]:
                        interval [0] = lowest
                    if highest > interval [1]:
                        interval [1] = highest

                extent = interval [1] - interval [0]
                interval [0] -= 0.1 * extent
                interval [1] += 0.1 * extent

                if self.types ['predictions'] is not None and self.types ['predictions'] [label] == 'int':
                    start = numpy.floor (interval [0])
                    end = numpy.ceil (interval [1])
                    count = end + 1 - start
                    densities = numpy.empty ((len (times), count))
                    for index, time in enumerate (times):
                        densities [index] [:] = numpy.bincount (values [time] - start, weights = weights [time], bins=count)

                else:
                    densities = numpy.empty ((len (times), bins))
                    for index, time in enumerate (times):
                        densities [index] [:], edges = numpy.histogram (values [time], weights=weights [time], bins=bins, range=interval, density=True)

                pylab.subplot (rows, columns, plot + 1)

                self.histogram (label, times, densities, interval, "spux_orange", log=log)

                # get MAP estimate
                if not MAP or self._MAP is None:
                    MAP_values = None
                else:
                    MAP_values = [ self._MAP ['predictions'] [name] [time] [label] for time in times ]

                predictions = self.line_and_range (times, lower, MAP_values, upper, linewidth=2, color='dimgray', alpha=0.5, middlealpha=0.5, merged=False, fill=False)
                handles = list (predictions)
                legend = ["MAP", "posterior percentiles (%s - %s)" % (str(percentile), str(100-percentile))]
                if label in list (dataset.columns.values):
                    observations = self.datasets ({ name : dataset [[label]] }, save, suffix, color='dimgray', frame=1)
                    handles += [observations]
                    legend += ["observations"]
                pylab.ylabel (label)
                pylab.xlabel (dataset.index.name)
                pylab.ylim (interval)
                if self.title:
                    pylab.title ("posterior predictions for dataset " + name)
                if self.legend:
                    pylab.legend (handles, legend, loc="best")
                if scientific:
                    pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

            pylab.draw()
            self.save (figname (save, suffix="predictions-posterior-dataset-%s%s" % (name, suffix)))

    # plot quantile-quantile comparison of the error and residual distributions
    def QQ (self, datasets, error, columns=3, seed=1, scientific=True, save=None, suffix=""):
        """ Plot quantile-quantile comparison of the error and residual distributions."""

        print (' :: Plotting QQ for each observed quantity...')

        data_labels = list (datasets.values ()) [0] .columns.values

        plots = len (data_labels)
        rows = numpy.ceil (plots / columns)
        pylab.figure (figsize = (8 * columns, 5 * rows))

        rng = numpy.random.RandomState (seed=seed)

        parameters = self._MAP ['parameters']
        name = list (datasets.keys ()) [0]
        predictions = list (self._MAP ['predictions'] [name] .values ()) [0]
        if hasattr (error, 'transform'):
            error_labels = list (error.transform (list (datasets.values ()) [0] .iloc [0], parameters) .index)
        else:
            error_labels = data_labels

        # compute residuals and draw theoretical random error samples
        residuals = {}
        errors = {}
        for plot, data_label in enumerate (data_labels):
            error_label = error_labels [plot]
            print (' : -> For', error_label)
            residuals [data_label] = numpy.array ([], dtype=float)
            errors [data_label] = numpy.array ([], dtype=float)
            for name, data in datasets.items ():
                predictions = self._MAP ['predictions'] [name]
                index = data [data_label] .dropna () .index
                if hasattr (error, 'transform'):
                    dt = lambda i : error.transform (data.loc [i], parameters) [error_label]
                    pt = lambda i : error.transform (self._MAP ['predictions'] [name] [i], parameters) [error_label]
                    r = [ dt (i) - pt (i) for i in index ]
                else:
                    r = [ data.loc [i] [data_label] - self._MAP ['predictions'] [name] [i] [data_label] for i in index ]
                residuals [data_label] = numpy.hstack ([residuals [data_label], r])
                if hasattr (error, 'transform'):
                    e = [ error.distribution (predictions [i], parameters).draw (rng=rng) [error_label] - error.transform (predictions [i], parameters) [error_label] for i in index ]
                else:
                    e = [ error.distribution (predictions [i], parameters).draw (rng=rng) [error_label] - predictions [i] [error_label] for i in index ]
                errors [data_label] = numpy.hstack ([errors [data_label], e])
            pylab.subplot (rows, columns, plot + 1)
            pylab.plot (sorted (errors [data_label]), sorted (residuals [data_label]), marker='.', color='spux_orange', linewidth=0, markersize=10)
            xlim = [ numpy.min (errors [data_label]), numpy.max (errors [data_label]) ]
            pylab.plot (xlim, xlim, linestyle='--', color='gray', linewidth=2)
            pylab.xlabel ('theoretical error quantiles for ' + error_label)
            pylab.ylabel ('posterior residual quantiles for ' + error_label)
            pylab.gca().set_aspect ('equal')
            if scientific:
                pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

        pylab.draw ()
        self.save (figname (save, suffix="qq%s" % suffix))

    # # plot predictive quantile-quantile comparison of the data and posterior model predictions distributions
    # def PQQ (self, datasets, error, columns=3, seed=1, scientific=True, save=None, suffix=""):
    #     """ Plot quantile-quantile comparison of the error and residual distributions."""

    #     print (' :: Plotting PQQ for each observed quantity and each dataset...')

    # make plots in log-quantities, if possible - this will allow to easily see scaling factor as well

    # compute Nash-Sutcliffe model efficinecy
    def NSE (self, datasets, label):
        """Nash-Sutcliffe model efficiency."""

        print (' :: Computing Nash-Sutcliffe efficiency (NSE) for the model...')

        NSE = {}
        for name, data in datasets.items ():
            data_values = numpy.array (data [label] .values)
            mean = numpy.nanmean (data_values)
            prediction_values = numpy.array ([ self._MAP ['predictions'] [name] [time] [label] for time in data.index ])
            differences = data_values - prediction_values
            upper = numpy.nansum (differences ** 2)
            lower = numpy.nansum ((data_values - mean) ** 2)
            NSE [name] = 1 - (upper / lower)

        print ('  : -> NSE:', NSE)

        return NSE

    # plot traffic
    def traffic (self, keys=["move", "copy", "kill"], palette=palette['traffic'], scientific=True, save=None, suffix=""):
        """Plot traffic."""

        print (' :: Plotting traffic...')

        if keys is None:
            keys = palette ['keys']
        colors = palette ['colors']
        present = set ()

        pylab.figure ()
        handles = []

        for key in keys:

            means = numpy.empty (len (self.infos) - self.burnin)
            lower = numpy.empty (len (self.infos) - self.burnin)
            upper = numpy.empty (len (self.infos) - self.burnin)

            for batch, info in enumerate (self.infos [self.burnin:]):
                available = [ chain for chain in info ['infos'] if chain is not None ]
                values = [ traffic [key] for chain in available for replicate in chain ['infos'] .values () for traffic in replicate ["traffic"] .values() if key in traffic ]
                if values != []:
                    present = present | {key}
                means [batch] = numpy.nanmedian (values) if values != [] else float ('nan')
                lower [batch] = numpy.nanmin (values) if values != [] else float ('nan')
                upper [batch] = numpy.nanmax (values) if values != [] else float ('nan')

            if key in present:
                handles.append (self.line_and_range (self.indices [self.burnin:], lower, means, upper, linewidth=2, color=colors [key]))

        if self.legend:
            pylab.legend (handles, present, loc="best")
        if self.title:
            pylab.title ("traffic fractions")
        pylab.xlabel ("sample")
        pylab.xlim ((self.indices[self.burnin], self.indices[-1]))
        pylab.ylabel ("traffic [fraction]")
        if scientific:
            pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))
        pylab.ylim ([-0.05, 1.05])
        pylab.draw ()
        self.save (figname (save, suffix="traffic" + suffix))

    # plot runtimes
    def runtimes (self, keys=None, palette=palette['runtimes'], percentile=0, columns=3, legendpos="", scientific=True, save=None, suffix=""):
        """Plot runtimes."""

        print (' :: Plotting runtimes...')

        if not self.replicates or self.deterministic:
            print (' :: ERROR: runtimes plots are not yet implemented for non-replicates likelihood or non-stochatic model.')
            return

        if keys is None:
            keys = list (palette ['colors'])

        indices = numpy.arange ((len (self.infos) - self.burnin) * self.chains)

        if self.replicates:

            plots = len (self.names)
            rows = numpy.ceil (plots / columns)

            pylab.figure (figsize = (8 * columns, 5 * rows))

            for plot, name in enumerate (self.names):

                pylab.subplot (rows, columns, plot + 1)
                handles = {}
                present = []

                for key in keys:

                    timing = numpy.empty (len (indices))
                    # mean = numpy.empty (len (indices))
                    # lower = numpy.empty (len (indices))
                    # upper = numpy.empty (len (indices))

                    means = numpy.empty (len (indices))
                    lowers = numpy.empty (len (indices))
                    uppers = numpy.empty (len (indices))

                    scalar = False

                    for batch, infos in enumerate (self.infos [self.burnin:]):
                        for chain, info in enumerate (infos ['infos']):

                            timings = []

                            if info is not None and info ['infos'] [name] is not None:
                                replicate = info ['infos'] [name]
                                if key in replicate ['timing'] .runtimes.keys ():
                                    if key not in present:
                                        present += [key]
                                    scalar = True
                                    timing [batch * self.chains + chain] = replicate ['timing'] .runtimes [key]
                                else:
                                    for worker in replicate ['timings']:
                                        if key in worker.runtimes.keys ():
                                            if key not in present:
                                                present += [key]
                                            timings += [ worker.runtimes [key] ]
                            else:
                                timing [batch * self.chains + chain] = float ('nan')

                            # mean [batch * self.chains + chain] = numpy.nanmedian (timing) if timing != [] else float ('nan')
                            # lower [batch * self.chains + chain] = numpy.nanpercentile (timing, percentile) if timing != [] else float ('nan')
                            # upper [batch * self.chains + chain] = numpy.nanpercentile (timing, 100 - percentile) if timing != [] else float ('nan')

                            means  [batch * self.chains + chain] = numpy.nanmedian (timings) if timings != [] else float ('nan')
                            lowers [batch * self.chains + chain] = numpy.nanpercentile (timings, percentile) if timings != [] else float ('nan')
                            uppers [batch * self.chains + chain] = numpy.nanpercentile (timings, 100 - percentile) if timings != [] else float ('nan')

                    color = palette ['colors'] [key]
                    style = ":" if any ([comm in key for comm in ["wait", "scatter", "sync", "gather"]]) else "-"

                    if scalar:
                        handles [key], = pylab.plot (indices, timing, style, color=color)
                    else:
                        handles [key] = self.line_and_range (indices, lowers, means, uppers, color=color, linewidth=2, style=style)

                legend_keys = [key for key in palette ['order'] if key in present]
                legend_handles = [handles [key] for key in legend_keys]

                pylab.legend (legend_handles, legend_keys, loc="best")
                # if len (legend_keys) <= 7:
                #     pylab.legend (legend_handles, legend_keys, loc="best")
                # else:
                #     pylab.legend (legend_handles, legend_keys, loc="center left", bbox_to_anchor=(1, 0.5))
                if self.title:
                    pylab.title ("runtimes")
                pylab.xlabel ("sample")
                pylab.xlim ((indices[0], indices[-1]))
                pylab.ylabel ("runtime [s]")
                if scientific:
                    pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

        pylab.draw ()
        self.save (figname (save, suffix="runtimes" + suffix))

    # plot efficiency: (init + run + errors + kill + replicate) / evaluate
    def efficiency (self, palette=palette['efficiency'], percentile=0, columns=3, scientific=True, save=None, suffix=""):
        """Plot efficiency."""

        print (' :: Plotting efficiency...')

        if not self.replicates or self.deterministic:
            print (' :: ERROR: efficiency plots are not yet implemented for non-replicates likelihood or non-stochatic model.')
            return

        keys = ['init', 'run', 'errors', 'kill', 'replicate']

        indices = numpy.arange ((len (self.infos) - self.burnin) * self.chains)

        if self.replicates:

            plots = len (self.names)
            rows = numpy.ceil (plots / columns)

            pylab.figure (figsize = (8 * columns, 5 * rows))

            for plot, name in enumerate (self.names):

                pylab.subplot (rows, columns, plot + 1)

                means = {}
                # upper = {}
                # lower = {}

                for key in keys:

                    means [key] = numpy.empty (len (indices))
                    # lower [key] = numpy.empty (len (indices))
                    # upper [key] = numpy.empty (len (indices))

                    for batch, infos in enumerate (self.infos [self.burnin:]):
                        for chain, info in enumerate (infos ['infos']):

                            timings = []

                            if info is not None and info ['infos'] [name] is not None:
                                for worker in info ['infos'] [name] ['timings']:
                                    if key in worker.runtimes.keys ():
                                        timings += [ worker.runtimes [key] ]

                            means [key] [batch * self.chains + chain] = numpy.nanmean (timings) if timings != [] else 0
                            # lower [key] [batch * self.chains + chain] = numpy.nanpercentile (timings, percentile) if timings != [] else 0
                            # upper [key] [batch * self.chains + chain] = numpy.nanpercentile (timings, 100 - percentile) if timings != [] else 0

                evaluate = numpy.empty (len (indices))
                for batch, infos in enumerate (self.infos [self.burnin:]):
                    for chain, info in enumerate (infos ['infos']):
                        if info is not None:
                            replicate = info ['infos'] [name]
                            evaluate [batch * self.chains + chain] = replicate ['timing'] .runtimes ['evaluate']
                        else:
                            evaluate [batch * self.chains + chain] = float ('nan')

                efficiencies = numpy.zeros (len (indices))
                for key in keys:
                    efficiencies += means [key]
                efficiencies /= evaluate

                pylab.plot (indices, efficiencies, color = palette, lw=2)

                if self.title:
                    pylab.title ("parallelization efficiency")
                pylab.xlabel ("sample")
                pylab.xlim ((indices[0], indices[-1]))
                pylab.ylabel ("parallelization efficiency")
                pylab.ylim ([-0.05, 1.05])
                if scientific:
                    pylab.gca().ticklabel_format (axis='both', style='sci', scilimits=(-2, 2))

        pylab.draw ()
        self.save (figname (save, suffix="efficiency" + suffix))

    # plot timestamps
    def timestamps (self, keys=None, sample=0, name=None, limit=10, palette=palette["runtimes"], scientific=True, save=None, suffix=""):

        print (' :: Plotting timestamps...')

        batch = sample // self.chains
        chain = sample - batch * self.chains

        if self.replicates and name is None:
            name = self.names [0]

        reference = self.infos [batch] ['infos'] [chain]
        if self.replicates:
            reference = reference ['infos'] [name]
        start = reference ["timing"] .timestamps ["evaluate"] [0] [0]
        final = reference ["timing"] .timestamps ["evaluate"] [0] [1]

        if keys is None:
            keys = list (reference ['timing'] .timestamps.keys()) + list (reference ['timings'] [0] .timestamps.keys())

        keys = [key for key in palette ['order'] if key in keys]

        present = []

        offset = lambda timestamp: (timestamp [0] - start, timestamp [1] - start)
        linewidth = 0.6
        patch = lambda timestamp, level: (
            (timestamp [0], level - 0.5 * linewidth),
            timestamp [1] - timestamp [0],
            linewidth,
        )

        pylab.figure ()
        handles = {}
        total = 1

        for key in keys:

            color = palette ['colors'] [key]
            alpha = 0.5 if any ([comm in key for comm in ["wait", "scatter", "sync", "gather"]]) else 1.0

            info = self.infos [batch] ['infos'] [chain]
            if self.replicates:
                info = info ['infos'] [name]

            if key in info ['timing'] .runtimes.keys ():
                if key not in present:
                    present += [key]
                timestamps = info ['timing'] .timestamps [key]
                for timestamp in timestamps:
                    xy, w, h = patch (offset (timestamp), 0)
                    pylab.gca().add_patch (pylab.Rectangle (xy, w, h, color=color, alpha=alpha, linewidth=0))
                    handles [key], = pylab.plot ([], [], color=color, alpha=alpha, linewidth=10)

            else:
                total = min (limit, len (info ['timings']))
                for worker, timing in enumerate (info ['timings']):
                    if limit is not None and worker == limit:
                        break
                    if key in timing.timestamps.keys ():
                        if key not in present:
                            present += [key]
                        timestamps = timing.timestamps [key]
                        for timestamp in timestamps:
                            xy, w, h = patch (offset (timestamp), worker + 1)
                            pylab.gca().add_patch (pylab.Rectangle (xy, w, h, color=color, alpha=alpha, linewidth=0))
                            handles[key], = pylab.plot ([], [], color=color, alpha=alpha, linewidth=10)

        legend_keys = [key for key in palette ['order'] if key in present]
        legend_handles = [handles [key] for key in legend_keys]

        if self.legend:
            pylab.legend (legend_handles, legend_keys, loc = "center left", bbox_to_anchor = (1, 0.5))
        if self.title:
            pylab.title ("timestamps")
        pylab.xlabel ("time [s]")
        pylab.ylabel ("worker")
        pylab.xlim ((0, final - start))
        pylab.ylim ((-0.5, total + 0.5))
        if total <= 20:
            pylab.yticks (range (total + 1), ["M "] + ["%3d " % worker for worker in range (total)])
        pylab.gca().invert_yaxis ()
        pylab.setp (pylab.gca().get_yticklines(), visible = False)
        if scientific:
            pylab.gca().ticklabel_format (axis='x', style='sci', scilimits=(-2, 2))
        pylab.draw ()
        replicate = ('-R-%s' % str (name)) if self.replicates else ''
        self.save (figname (save, suffix = ("timestamps-S%05d%s" % (sample, replicate) + suffix)))

    # plot scaling and average efficiencies from multiple simulations
    def scaling (self, infosdict, factors={}, palette=palette['scaling'], save=None, suffix=""):
        """Plot scaling and average efficiencies from multiple simulations."""

        print (' :: Plotting scaling...')

        workerslist = list (infosdict.keys ())

        evaluate = {}
        efficiency = {}

        keys = ['init', 'run', 'errors', 'kill', 'replicate']
        indices = numpy.arange ((len (self.infos) - self.burnin) * self.chains)

        for workers, infos in infosdict.items ():

            means = {}

            for key in keys:

                means [key] = numpy.empty (len (indices))

                for batch, infos in enumerate (self.infos [self.burnin:]):
                    for chain, info in enumerate (infos ['infos']):

                        timings = []

                        if info is not None and info ['infos'] [name] is not None:
                            for worker in info ['infos'] [name] ['timings']:
                                if key in worker.runtimes.keys ():
                                    timings += [ worker.runtimes [key] ]

                        means [key] [batch * self.chains + chain] = numpy.nanmean (timings) if timings != [] else 0

            evaluates = numpy.empty (len (indices))
            for batch, infos in enumerate (self.infos [self.burnin:]):
                for chain, info in enumerate (infos ['infos']):
                    if info is not None:
                        replicate = info ['infos'] [name]
                        evaluates [batch * self.chains + chain] = replicate ['timing'] .runtimes ['evaluate']
                    else:
                        evaluates [batch * self.chains + chain] = float ('nan')

            efficiencies = numpy.zeros (len (indices))
            for key in keys:
                efficiencies += means [key]
            efficiencies /= evaluates

            efficiency [workers] = numpy.nanmean (efficiencies)
            evaluate [workers] = numpy.nanmean (evaluates)

        # apply scaling factors if needed
        if factors != {}:
            for workers, runtime in evaluate.items():
                runtime *= factors [workers]

        pylab.figure ()

        # scaling
        means = [numpy.mean (evaluate [workers]) for workers in workerslist]
        lower = [numpy.percentile (evaluate [workers], 10) for workers in workerslist]
        upper = [numpy.percentile (evaluate [workers], 90) for workers in workerslist]
        linear, = pylab.plot (workerslist, [means[0] * workerslist[0] / workers for workers in workerslist], "--", color=palette ['linear'], linewidth=3, alpha=0.5)
        runtime = self.line_and_range (workerslist, lower, means, upper, color=palette ['runtime'], marker="+", linewidth=3, logx=1, logy=1)
        pylab.ylabel ("runtime [s]")
        pylab.ylim (0.5 * pylab.ylim()[0], 2 * pylab.ylim()[1])
        pylab.xlabel ("number of workers")

        # efficiencies
        pylab.sca (pylab.twinx ())
        means = [numpy.mean (efficiencies [workers]) for workers in workerslist]
        lower = [numpy.percentile (efficiencies [workers], 10) for workers in workerslist]
        upper = [numpy.percentile (efficiencies [workers], 90) for workers in workerslist]
        efficiency = self.line_and_range (workerslist, lower, means, upper, color=palette ['efficiency'], marker="+", linewidth=3, logx=1)
        pylab.ylabel ("efficiency")
        pylab.ylim ([-0.05, 1.05])

        pylab.xlim (0.5 * pylab.xlim()[0], 2 * pylab.xlim()[1])
        if self.title:
            pylab.title ("parallel scaling and efficiency")
        if self.legend:
            pylab.legend ([runtime, linear, efficiency], ["runtime", "linear scaling", "efficiency"], loc="best")
        pylab.draw ()
        self.save (figname (save, suffix="scaling" + suffix))
