"""This is the subclass of Creator that wraps a PZFlow Flow so that it can
be used to generate synthetic data and calculate posteriors."""

from ast import Param
import numpy as np
import qp
from pzflow import Flow
from rail.core.data import FlowHandle, PqHandle, QPHandle
from rail.creation.creator import Modeler, Creator, PosteriorCalculator


class FlowModeler(Modeler):
    """Modeler wrapper for a PZFlow Flow object.
    
    This class trains the flow.
    """

    name = 'FlowModeler'
    inputs = [('catalog', SomeHandle)] # move this to the base class!!!!!!
    outputs = [('flow', FlowHandle)]

    config_options = CatInformer.config_options.copy()
    config_options.update(
        color_transform=Param(bool, True, msg="Whether to internally convert magnitudes to colors."),
    )


    def __init__(self, args, comm=None):
        """Constructor
        
        Does standard Modeler initialization.
        """

        if self.config.color_transform:
            # tell it which column to use as the reference magnitude
            ref_idx = train_set.columns.get_loc("i")
            # and which columns correspond to the magnitudes we want colors for
            mag_idx = [train_set.columns.get_loc(band) for band in "ugrizy"]

        # the next bijector is shift bounds
        # we need to set the mins and maxes
        # I am setting strict limits on redshift, but am adding some padding to
        # the magnitudes and colors so that the flow can sample a little
        colors = -np.diff(train_set[list("ugrizy")].to_numpy())
        mins = np.concatenate(([0, train_set["i"].min()], colors.min(axis=0)))
        maxs = np.concatenate(([3, train_set["i"].max()], colors.max(axis=0)))

        # I will add 10% buffers to the mins and maxs in case that the train set
        # doesn't cover the full range of the test set
        ranges = maxs - mins
        buffer = ranges / 10 / 2
        buffer[0] = 0  # except no buffer for redshift!
        mins -= buffer
        maxs += buffer

        # finally, the settings for the RQ-RSC
        nlayers = train_set.shape[1]  # layers = number of dimensions
        K = 16  # number of spline knots
        transformed_dim = 1  # only transform one dimension at a time

        # chain all the bijectors together
        bijector = Chain(
            ColorTransform(ref_idx, mag_idx),
            ShiftBounds(mins, maxs),
            RollingSplineCoupling(nlayers, K=K, transformed_dim=transformed_dim),
        )

        # build the flow
        flow = Flow(train_set.columns, bijector=bijector)


class FlowCreator(Creator):
    """Creator wrapper for a PZFlow Flow object."""

    name = 'FlowCreator'
    inputs = [('flow', FlowHandle)]
    outputs = [('output', PqHandle)]

    def __init__(self, args, comm=None):
        """Constructor

        Does standard Creator initialization and also gets the `Flow` object
        """
        Creator.__init__(self, args, comm=comm)
        if not isinstance(args, dict):
            args = vars(args)
        self.set_flow(**args)

    def set_flow(self, **kwargs):
        """Set the `Flow`, either from an object or by loading from a file."""
        flow = kwargs.get('flow')
        if flow is None:  #pragma: no cover
            return None
        from pzflow import Flow
        if isinstance(flow, Flow):
            return self.set_data('flow', flow)
        return self.set_data('flow', data=None, path=flow)

    def run(self):
        """Run method

        Calls `Flow.sample` to use the `Flow` object to generate photometric data

        Notes
        -----
        Puts the data into the data store under this stages 'output' tag
        """
        flow = self.get_data('flow')
        if flow is None:  #pragma: no cover
            raise ValueError("Tried to run a FlowCreator before the `Flow` model is loaded")
        self.add_data('output', flow.sample(self.config.n_samples, self.config.seed))

class FlowPosterior(PosteriorCalculator):
    """PosteriorCalculator wrapper for a PZFlow Flow object

    Parameters
    ----------
    data : pd.DataFrame
        Pandas dataframe of the data on which the posteriors are conditioned.
        Must have all columns in self.flow.data_columns, *except*
        for the column specified for the posterior (see below).
    column : str
        Name of the column for which the posterior is calculated.
        Must be one of the columns in self.flow.data_columns. However,
        whether or not this column is present in `data` is irrelevant.
    grid : np.ndarray
        Grid over which the posterior is calculated.
    err_samples : int, optional
        Number of samples from the error distribution to average over for
        the posterior calculation. If provided, Gaussian errors are assumed,
        and method will look for error columns in `inputs`. Error columns
        must end in `_err`. E.g. the error column for the variable `u` must
        be `u_err`. Zero error assumed for any missing error columns.
    seed: int, optional
        Random seed for drawing samples from the error distribution.
    marg_rules : dict, optional
        Dictionary with rules for marginalizing over missing variables.
        The dictionary must contain the key "flag", which gives the flag
        that indicates a missing value. E.g. if missing values are given
        the value 99, the dictionary should contain {"flag": 99}.
        The dictionary must also contain {"name": callable} for any
        variables that will need to be marginalized over, where name is
        the name of the variable, and callable is a callable that takes
        the row of variables and returns a grid over which to marginalize
        the variable. E.g. {"y": lambda row: np.linspace(0, row["x"], 10)}.
        Note: the callable for a given name must *always* return an array
        of the same length, regardless of the input row.
        DEFAULT: the default marg_rules dict is
        {
        "flag": np.nan,
        "u": np.linspace(25, 31, 10),
        }
    batch_size: int, default=None
        Size of batches in which to calculate posteriors. If None, all
        posteriors are calculated simultaneously. This is faster, but
        requires more memory.
    nan_to_zero : bool, default=True
        Whether to convert NaN's to zero probability in the final pdfs.

    """

    name = 'FlowPosterior'
    config_options = PosteriorCalculator.config_options.copy()
    config_options.update(
        grid=list,
        err_samples=10,
        seed=12345,
        marg_rules={"flag": np.nan, "mag_u_lsst": lambda row: np.linspace(25, 31, 10)},
        batch_size=10000,
        nan_to_zero=True,
    )

    inputs = [('flow', FlowHandle),
              ('input', PqHandle)]
    outputs = [('output', QPHandle)]

    def __init__(self, args, comm=None):
        """ Constructor

        Does standard PosteriorCalculator initialization
        """
        PosteriorCalculator.__init__(self, args, comm=comm)

    def run(self):
        """Run method

        Calls `Flow.posterior` to use the `Flow` object to get the posterior distribution

        Notes
        -----
        Get the input data from the data store under this stages 'input' tag
        Puts the data into the data store under this stages 'output' tag
        """

        data = self.get_data('input')
        flow = self.get_data('flow')
        if self.config.marg_rules is None:  #pragma: no cover
            marg_rules = {"flag": np.nan, "mag_u_lsst": lambda row: np.linspace(25, 31, 10)}
        else:
            marg_rules = self.config.marg_rules

        pdfs = flow.posterior(
            inputs=data,
            column=self.config.column,
            grid=np.array(self.config.grid),
            err_samples=self.config.err_samples,
            seed=self.config.seed,
            marg_rules=marg_rules,
            batch_size=self.config.batch_size,
            nan_to_zero=self.config.nan_to_zero,
        )

        ensemble = qp.Ensemble(qp.interp, data={"xvals": self.config.grid, "yvals": pdfs})
        self.add_data('output', ensemble)
