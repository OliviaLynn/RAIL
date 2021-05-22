import inspect
import numpy as np
from scipy import stats
import qp
from rail.evaluation.evaluator import Evaluator
from rail.evaluation.utils import stat_and_pval, stat_crit_sig

default_quants = np.linspace(0, 1, 100)
_pitMetaMetrics = {}
def PITMetaMetric(cls):
    argspec = inspect.getargspec(cls.evaluate)
    if argspec.defaults is not None:
        num_defaults=len(argspec.defaults)
        kwargs = {var: val for var, val in zip(argspec.args[-num_defaults:], argspec.defaults)}
        _pitMetaMetrics.setdefault(cls, {})["default"] = kwargs
    return cls


class PIT(Evaluator):
    """ Probability Integral Transform """
    def __init__(self, qp_ens, ztrue):
        """Class constructor"""
        super().__init__(qp_ens)

        self._ztrue = ztrue
        self._pit_samps = np.array([self._qp_ens[i].cdf(self._ztrue[i])[0][0] for i in range(len(self._ztrue))])

    def evaluate(self, eval_grid=default_quants, meta_options=_pitMetaMetrics):
        """Compute PIT array using qp.Ensemble class
        Notes
        -----
        eval_grid shouldn't be necessary but new qp doesn't have a samples parameterization, only spline from KDE of samples
        """
        pit = qp.spline_from_samples(xvals=eval_grid,
                                     samples=np.atleast_2d(self._pit_samps))
        pit.samples = self._pit_samps

        if meta_options is not None:
            metamets = {}
            for cls, params in meta_options.items():
                meta = cls(pit)
                for name, kwargs in params.items():
                    metamets[(cls, name)] = meta.evaluate(**kwargs)

        # self.qq = _evaluate_qq(self._eval_grid)
        return pit, metamets


    # def _evaluate_qq(self):
    #     q_data = qp.convert(self._pit, 'quant', quants=self._eval_grid)
    #     return q_data
    #
    # def plot_all_pit(self):
    #     plot_utils.ks_plot(self)
    #
    #
    # def plot_pit_qq(self, bins=None, code=None, title=None, show_pit=True,
    #                 show_qq=True, pit_out_rate=None, savefig=False):
    #     """Make plot PIT-QQ as Figure 2 from Schmidt et al. 2020."""
    #     fig_filename = plot_utils.plot_pit_qq(self, bins=bins, code=code, title=title,
    #                                      show_pit=show_pit, show_qq=show_qq,
    #                                      pit_out_rate=pit_out_rate,
    #                                      savefig=savefig)
    #     return fig_filename

class PITMeta():
    """ A superclass for metrics of the PIT"""
    def __init__(self, pit):
        """Class constructor.
        Parameters
        ----------
        pit: qp.spline_from_samples object
            PIT values
        """
        self._pit = pit

    # they all seem to have a way to trim the ends, so maybe just bring those together here?
    # def _trim(self, pit_min=0., pit_max=1.):
    #


    def evaluate(self):
        """
        Evaluates the metric a function of the truth and prediction

        Returns
        -------
        metric: dictionary
            value of the metric and statistics thereof
        """
        raise NotImplementedError


@PITMetaMetric
class PITOutRate(PITMeta):
    """ Fraction of PIT outliers """
    def __init__(self, pit):
        super().__init__(pit)

    def evaluate(self, pit_min=0., pit_max=1.):
        """Compute fraction of PIT outliers"""
        out_area = self._pit.cdf(pit_min) + (1. - self._pit.cdf(pit_max))
        return out_area

@PITMetaMetric
class PITKS(PITMeta):
    """ Kolmogorov-Smirnov test statistic """

    def __init__(self, pit):
        super().__init__(pit)

    def evaluate(self):
        """ Use scipy.stats.kstest to compute the Kolmogorov-Smirnov test statistic for
        the PIT values by comparing with a uniform distribution between 0 and 1. """
        stat, pval = stats.kstest(self._pit.samples, 'uniform')
        return stat_and_pval(stat, pval)

@PITMetaMetric
class PITCvM(PITMeta):
    """ Cramer-von Mises statistic """

    def __init__(self, pit):
        super().__init__(pit)

    def evaluate(self):
        """ Use scipy.stats.cramervonmises to compute the Cramer-von Mises statistic for
        the PIT values by comparing with a uniform distribution between 0 and 1. """
        stat, pval = stats.cramervonmises(self._pit.samples, 'uniform')
        return stat_and_pval(stat, pval)

@PITMetaMetric
class PITAD(PITMeta):
    """ Anderson-Darling statistic """
    def __init__(self, pit):
        super().__init__(pit)

    def evaluate(self, pit_min=0., pit_max=1.):
        """ Use scipy.stats.anderson_ksamp to compute the Anderson-Darling statistic
        for the PIT values by comparing with a uniform distribution between 0 and 1.
        Up to the current version (1.6.2), scipy.stats.anderson does not support
        uniform distributions as reference for 1-sample test.

        Parameters
        ----------
        pit_min: float, optional
            PIT values below this are discarded
        pit_max: float, optional
            PIT values greater than this are discarded

        Returns
        -------

        """
        pits = self._pit.samples
        mask = (pits >= pit_min) & (pits <= pit_max)
        pits_clean = pits[mask]
        diff = len(pits) - len(pits_clean)
        if diff > 0:
            print(f"{diff} PITs removed from the sample.")
        uniform_yvals = np.linspace(pit_min, pit_max, len(pits_clean))
        ad_results = stats.anderson_ksamp([pits_clean, uniform_yvals])
        stat, crit_vals, sig_lev = ad_results

        return stat_crit_sig(stat, crit_vals, sig_lev)

# this KLD implementation is actually only valid for discrete distribution, won't work on a non-discrete grid
# @PITMetaMetric
# class PITKLD(PITMeta):
#     """ Kullback-Leibler Divergence """
#
#     def __init__(self, pit):
#         super().__init__(pit)
#
#     def evaluate(self, eval_grid=default_quants):
#         """ Use scipy.stats.entropy to compute the Kullback-Leibler
#         Divergence between the empirical PIT distribution and a
#         theoretical uniform distribution between 0 and 1."""
#         if pits is None:
#             pits = PIT(self._pdfs, self._xvals, self._ztrue).evaluate()
#         uniform_yvals = np.linspace(0., 1., len(pits))
#         pit_pdf, _ = np.histogram(pits, bins=len(self._xvals))
#         uniform_pdf, _ = np.histogram(uniform_yvals, bins=len(self._xvals))
#
#         self._metric = stats.entropy(pit_pdf, uniform_pdf)
#         return self._metric
