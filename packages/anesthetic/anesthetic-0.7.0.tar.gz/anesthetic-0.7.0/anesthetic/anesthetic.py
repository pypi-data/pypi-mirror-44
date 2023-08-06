import numpy
import pandas
from scipy.special import logsumexp
from anesthetic.plot import make_1D_axes, make_2D_axes, plot_1d, scatter_plot_2d, contour_plot_2d
from anesthetic.read import read_chains, read_birth, read_limits, read_paramnames
from anesthetic.information_theory import compress_weights


class MCMCSamples(pandas.DataFrame):
    """Storage and plotting tools for MCMC samples

    We extend the pandas.DataFrame by providing plotting methods and standardising
    sample storage.

    Note that because of the design of pandas this does not override the
    __init__ constructor. You should build the samples with either:

    * `mcmc = MCMCSamples.read('your/file/root')`
    * `mcmc = MCMCSamples.build(params=params, other_keyword_arguments)`

    Example plotting commands include

    * `mcmc.plot_1d()`
    * `mcmc.plot_2d(['paramA', 'paramB'])`
    * `mcmc.plot_2d(['paramA', 'paramB'],['paramC', 'paramD'])`

    """
    _metadata = pandas.DataFrame._metadata + ['paramnames', 'tex', 'limits', 'root']

    @classmethod
    def read(cls, root):
        """Read in data from file root."""
        # Read in data
        w, logL, params = read_chains(root)
        paramnames, tex = read_paramnames(root)
        limits = read_limits(root)

        # Build class
        data = cls.build(params=params, w=w, logL=logL, paramnames=paramnames,
                         tex=tex, limits=limits)

        # Record root
        data.root = root
        return data

    @classmethod
    def build(cls, **kwargs):
        """Build an augmented pandas array for MCMC samples.

        Parameters
        ----------
        params: numpy.array
            Coordinates of samples. shape = (nsamples, ndims).

        logL: numpy.array
            loglikelihoods of samples.

        w: numpy.array
            weights of samples.

        paramnames: list(str)
            reference names of parameters

        tex: dict
            mapping from paramnames to tex labels for plotting

        limits: dict
            mapping from paramnames to prior limits
        """
        params = kwargs.pop('params', None)
        logL = kwargs.pop('logL', None) 
        if params is None and logL is None:
            raise ValueError("You must provide either params or logL")
        elif params is None:
            params = numpy.empty((len(logL),0))

        nsamps, nparams = numpy.atleast_2d(params).shape

        w = kwargs.pop('w', None)
        paramnames = kwargs.pop('paramnames', ['x%i' % i for i in range(nparams)])

        tex = kwargs.pop('tex', {})
        limits = kwargs.pop('limits', {})

        data = cls(data=params, columns=paramnames)
        if w is not None:
            data['w'] = w 
            tex['w'] = r'MCMC weight'
        if logL is not None:
            data['logL'] = logL
            tex['logL'] = r'$\log\mathcal{L}$'

        data['u'] = numpy.random.rand(len(data))

        data.tex = tex
        data.paramnames = paramnames
        data.limits = limits
        data.root = None
        return data

    def plot(self, ax, paramname_x, paramname_y=None, *args, **kwargs):
        """Generic plotting interface. 
        
        Produces a single 1D or 2D plot on an axis.

        Parameters
        ----------
        ax: matplotlib.axes.Axes
            Axes to plot on 

        paramname_x: str
            Choice of parameter to plot on x-coordinate from self.columns.

        paramname_y: str
            Choice of parameter to plot on y-coordinate from self.columns.
            If not provided, or the same as paramname_x, then 1D plot produced.

        plot_type: str
            Optional. must be in {'contour','scatter'}

        beta: float
            Temperature to plot at. beta=0 corresponds to the prior, beta=1
            corresponds to the posterior.
        """

        plot_type = kwargs.pop('plot_type', 'contour')
        beta = kwargs.pop('beta', 1)

        if beta != 1 and isinstance(self, MCMCSamples):
            raise ValueError("You cannot adjust the temperature of MCMCSamples")

        if paramname_y is None or paramname_x == paramname_y:
            xmin, xmax = self._limits(paramname_x)
            return plot_1d(ax, numpy.repeat(self[paramname_x], self._weights(beta)),
                           xmin=xmin, xmax=xmax, *args, **kwargs)

        xmin, xmax = self._limits(paramname_x)
        ymin, ymax = self._limits(paramname_y)

        if plot_type == 'contour':
            weights = self._weights(beta)
            plot = contour_plot_2d
        elif plot_type == 'scatter':
            weights = self._weights(beta, nsamples=500)
            plot = scatter_plot_2d
        else:
            raise ValueError("plot_type must be in {'contour', 'scatter'}")

        return plot(ax, numpy.repeat(self[paramname_x], weights),
                    numpy.repeat(self[paramname_y], weights),
                    xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, 
                    *args, **kwargs)

    def plot_1d(self, paramnames=None, *args, **kwargs):
        """Create an array of 1D plots

        Parameters
        ----------
        paramnames: list(str) or str
            list of parameter names, or single parameter name to plot from
            self.columns. Optional, defaults to all parameters.

        axes: numpy.array(matplotlib.axes.Axes)
            Existing array of axes to plot on. If not provided, one is created.

        beta: float
            Temperature to plot at. beta=0 corresponds to the prior, beta=1
            corresponds to the posterior.

        Returns
        -------
        fig: matplotlib.figure.Figure
            New or original (if supplied) figure object

        axes: pandas.Series(matplotlib.axes.Axes)
            Pandas array of axes objects 
        """
        if paramnames is None:
            paramnames = self.paramnames
        else:
            paramnames = numpy.atleast_1d(paramnames)

        axes = kwargs.pop('axes', None)
        beta = kwargs.pop('beta', 1)
        if axes is None:
            fig, axes = make_1D_axes(paramnames, tex=self.tex)
        else:
            fig = numpy.atleast_2d(axes)[0,0].figure

        for p in paramnames:
            self.plot(axes[p], p, beta=beta, *args, **kwargs)

        return fig, axes

    def plot_2d(self, paramnames_x=None, paramnames_y=None, *args, **kwargs):
        """Create an array of 2D plots

        Parameters
        ----------
        paramnames_x: list(str) or str
            list of parameter names, or single parameter name to plot from
            self.columns. If paramnames_y is not provided, produce triangle plot

        paramnames_y: list(str) or str
            list of parameter names, or single parameter name to plot on y
            coordinate from self.columns. If not provided, then a triangle plot
            is produced from paramnames_x

        axes: numpy.array(matplotlib.axes.Axes)
            Existing array of axes to plot on. If not provided, one is created.

        beta: float
            Temperature to plot at. beta=0 corresponds to the prior, beta=1
            corresponds to the posterior.

        Returns
        -------
        fig: matplotlib.figure.Figure
            New or original (if supplied) figure object

        axes: pandas.DataFrame(matplotlib.axes.Axes)
            Pandas array of axes objects 
        """
        if paramnames_x is None:
            paramnames_x = self.paramnames
        paramnames_x = numpy.atleast_1d(paramnames_x)
        if paramnames_y is None:
            paramnames_y = paramnames_x
        paramnames_y = numpy.atleast_1d(paramnames_y)
        all_paramnames = list(paramnames_y) +list(paramnames_x)

        axes = kwargs.pop('axes', None)
        beta = kwargs.pop('beta', 1)
        if axes is None:
            fig, axes = make_2D_axes(paramnames_x, paramnames_y, tex=self.tex)
        else:
            axes = pandas.DataFrame(axes, index=paramnames_y, columns=paramnames_x)
            fig = axes.iloc[0,0].figure

        for py in paramnames_y:
            for px in paramnames_x:
                if px in paramnames_y and py in paramnames_x and all_paramnames.index(px) > all_paramnames.index(py):
                    plot_type='scatter'
                else:
                    plot_type='contour'
                self.plot(axes[px][py], px, py, plot_type=plot_type, beta=beta, *args, **kwargs)
        return fig, axes

    def _weights(self, beta, nsamples=None):
        """ Return the posterior weights for plotting. """
        try:
            return compress_weights(self.w, self.u, nsamples=nsamples)
        except AttributeError:
            return numpy.ones(len(self), dtype=int, unit_weights=unit_weights)

    def _limits(self, paramname):
        return self.limits.get(paramname, (None, None))

    def _reload_data(self):
        self = type(self).read(self.root)


class NestedSamples(MCMCSamples):
    """Storage and plotting tools for Nested Sampling samples

    We extend the MCMCSamples class with the additional methods:
    
    * ns_output

    Note that because of the design of pandas this does not override the
    __init__ constructor. You should build the samples with either:

    * NestedSamples.read('your/file/root')
    * NestedSamples.build(params=params, other_keyword_arguments)
    """

    @classmethod
    def read(cls, root):
        """Read in data from file root."""
        # Read in data
        paramnames, tex = read_paramnames(root)
        limits = read_limits(root)
        params, logL, logL_birth = read_birth(root)

        # Build class
        data = cls.build(params=params, logL=logL, paramnames=paramnames, tex=tex, limits=limits, logL_birth=logL_birth)

        # Record root
        data.root = root
        return data

    @classmethod
    def build(cls, **kwargs):
        """Build an augmented pandas array for Nested samples.

        Parameters
        ----------
        params: numpy.array
            Coordinates of samples. shape = (nsamples, ndims).

        logL: numpy.array
            loglikelihoods of samples.

        logL_birth: numpy.array
            birth loglikelihoods of samples.

        w: numpy.array
            weights of samples.

        paramnames: list(str)
            reference names of parameters

        tex: dict
            mapping from paramnames to tex labels for plotting

        limits: dict
            mapping from paramnames to prior limits
        """
        # Build pandas DataFrame
        logL_birth = kwargs.pop('logL_birth', None)
        data = super(NestedSamples, cls).build(**kwargs)
        data['logL_birth'] = logL_birth

        # Compute nlive
        index = data.logL.searchsorted(data.logL_birth)-1
        births = pandas.Series(+1, index=index).sort_index()
        deaths = pandas.Series(-1, index=data.index)
        nlive = pandas.concat([births, deaths]).sort_index().cumsum()
        nlive = (nlive[~nlive.index.duplicated(keep='first')]+1)[1:]
        data['nlive'] = nlive
        data['logw'] = data._dlogX()
        return data

    def ns_output(self, nsamples=100):
        """ Compute Bayesian global quantities

        Using nested sampling we can compute the evidence (logZ),
        Kullback-Leibler divergence (D) and Bayesian model dimensionality (d).
        More precisely, we can infer these quantities via their probability
        distribution.

        Parameters
        ----------
        nsamples: int
            number of samples to generate
            optional, default 100
        
        Returns
        -------
        pandas.DataFrame
            Samples from the P(logZ, D, d) distribution
        
        """
        columns = ['logZ', 'D', 'd']
        dlogX = self._dlogX(nsamples)

        logZ = logsumexp(self.logL.values + dlogX, axis=1)
        logw = ((self.logL.values + dlogX).T - logZ).T
        S = ((self.logL.values + numpy.zeros_like(dlogX)).T
             - logZ).T

        D = numpy.exp(logsumexp(logw, b=S, axis=1))
        d = numpy.exp(logsumexp(logw, b=(S.T-D).T**2, axis=1))*2

        params = numpy.vstack((logZ, D, d)).T
        paramnames = ['logZ', 'D', 'd']
        tex = {'logZ':r'$\log\mathcal{Z}$', 'D':r'$\mathcal{D}$', 'd':r'$d$'}
        return MCMCSamples.build(params=params, paramnames=paramnames, tex=tex)

    def live_points(self, logL):
        """ Get the live points within logL """
        return self[(self.logL > logL) & (self.logL_birth <= logL)]

    def posterior_points(self, beta):
        """ Get the posterior points at temperature beta """
        return self[self._weights(beta, nsamples=-1)>0]

    def _weights(self, beta, nsamples=None):
        """ Return the posterior weights for plotting. """
        logw = self.logw + beta*self.logL
        w = numpy.exp(logw - logw.max())
        return compress_weights(w, self.u, nsamples=nsamples)

    def _dlogX(self, nsamples=None):
        """ Compute volume of shell of loglikelihood

        Parameters
        ----------
        nsamples: int
            Number of samples to generate. optional. If None (default), then
            compute the statistical average. If integer, generate samples from
            the distribution
        """
        if nsamples is None:
            t = numpy.atleast_2d(numpy.log(self.nlive/(self.nlive+1)))
            nsamples=1
        else:
            t = numpy.log(numpy.random.rand(nsamples, len(self))
                          )/self.nlive.values
        logX = numpy.concatenate((numpy.zeros((nsamples, 1)),
                                  t.cumsum(axis=1),
                                  -numpy.inf*numpy.ones((nsamples, 1))
                                  ), axis=1)
        dlogX = logsumexp([logX[:, :-2], logX[:, 2:]],
                          b=[numpy.ones_like(t), -numpy.ones_like(t)], axis=0)
        dlogX -= numpy.log(2)
        return numpy.squeeze(dlogX)

