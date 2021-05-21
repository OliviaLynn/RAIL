import sys
from rail.evaluation.plot_utils import *
import time as t

class Summary:
    """ Summary tables with all metrics available. """
    def __init__(self, pdfs, xvals, ztrue):
        """Class constructor."""
        # placeholders for metrics to be calculated
        self._pdfs = pdfs
        self._xvals = xvals
        self._ztrue = ztrue
        self._pit_out_rate = None
        self._ks = None
        self._cvm = None
        self._ad = None
        self._kld = None
        self._cde_loss = None

    def evaluate_all(self, pits=None):
        if pits is None:
            pits = PIT(self._pdfs, self._xvals, self._ztrue).evaluate()
        self._pit_out_rate = PitOutRate(self._pdfs, self._xvals, self._ztrue).evaluate(pits=pits)
        self._ks, _ = KS(self._pdfs, self._xvals, self._ztrue).evaluate(pits=pits)
        self._cvm, _ = CvM(self._pdfs, self._xvals, self._ztrue).evaluate(pits=pits)
        self._ad, _, _ = AD(self._pdfs, self._xvals, self._ztrue).evaluate(pits=pits)
        self._kld = KLD(self._pdfs, self._xvals, self._ztrue).evaluate(pits=pits)
        self._cde_loss = CDE(self._pdfs, self._xvals, self._ztrue).evaluate()

    def markdown_metrics_table(self, show_dc1=None, pits=None):
        self.evaluate_all(pits=pits)
        if show_dc1:
            dc1 = utils.DC1()
            if show_dc1 not in dc1.codes:
                raise ValueError(f"{show_dc1} not in the list of codes from DC1: {dc1.codes}" )
            table = str("Metric|Value|DC1 reference value \n ---|---:|---: \n ")
            table += f"PIT out rate | {self._pit_out_rate:11.4f} |{dc1.results['PIT out rate'][show_dc1]:11.4f} \n"
            table += f"KS           | {self._ks:11.4f}  |{dc1.results['KS'][show_dc1]:11.4f} \n"
            table += f"CvM          | {self._cvm:11.4f} |{dc1.results['CvM'][show_dc1]:11.4f} \n"
            table += f"AD           | {self._ad:11.4f}  |{dc1.results['AD'][show_dc1]:11.4f} \n"
            table += f"KLD          | {self._kld:11.4f}      |  N/A  \n"
            table += f"CDE loss     | {self._cde_loss:11.2f} |{dc1.results['CDE loss'][show_dc1]:11.2f} \n"
        else:
            table = "Metric|Value \n ---|---: \n "
            table += f"PIT out rate | {self._pit_out_rate:11.4f} \n"
            table += f"KS           | {self._ks:11.4f}  \n"
            table += f"CvM          | {self._cvm:11.4f} \n"
            table += f"AD           | {self._ad:11.4f}  \n"
            table += f"CDE loss     | {self._cde_loss:11.2f} \n"
            table += f"KLD          | {self._kld:11.4f}      \n"
        return Markdown(table)

    def print_metrics_table(self, pits=None):
        self.evaluate_all(pits=pits)
        table = str(
            "   Metric    |    Value \n" +
            "-------------|-------------\n" +
            f"PIT out rate | {self._pit_out_rate:11.4f}\n" +
            f"KS           | {self._ks:11.4f}\n" +
            f"CvM          | {self._cvm:11.4f}\n" +
            f"AD           | {self._ad:11.4f}\n" +
            f"KLD          | {self._kld:11.4f}\n" +
            f"CDE loss     | {self._cde_loss:11.4f}\n" )
        print(table)

def main(argv):
    """ RAIL Evaluation module - command line mode:
    * Compute all metrics available and display them in a table.
    * Make PIT-QQ plot and save it a PNG file.

    Parameters:
    -----------
    argv: `sys.argv`, `list`
        list of parameters inserted on command line

    Usage:
    ------
        python evaluator.py <code name> <PDFs file> <sample name> <z-spec file>

    Example:
        python evaluator.py FlexZBoost ./results/FZBoost/test_FZBoost.hdf5 toy_data ../tests/data/test_dc2_validation_9816.hdf5

    """
    t0 = t.time()
    print()
    print()
    print("        *** RAIL EVALUATION MODULE ***")
    print()
    if len(argv) != 5:
        print()
        print()
        print("Usage:")
        print("    python evaluator.py <code name> <PDFs file> <sample name> <z-spec file>")
        print()
        print("Example:")
        print("    python evaluator.py FlexZBoost ./results/FZBoost/test_FZBoost.hdf5 toy_data ../tests/data/test_dc2_validation_9816.hdf5")
        print()
        print()
        sys.exit()
    else:
        code, pdfs_file, name, ztrue_file = argv[1], argv[2], argv[3], argv[4]
        print()
        print()
        print(f"Photo-z results by: {code}")
        print(f"PDFs file: {pdfs_file}")
        print()
        print(f"Validation/test set: {name}")
        print(f"z-true file: {ztrue_file}")
        print()
        print()

    print("Reading data...")
    pdfs, zgrid, ztrue, photoz_mode = read_pz_output(pdfs_file, ztrue_file)
    print()
    print()

    print("Computing metrics...")
    pit = PIT(pdfs, zgrid, ztrue)
    pit.evaluate()
    pits = pit.metric
    summary = Summary(pdfs, zgrid, ztrue)
    summary.print_metrics_table(pits=pits)
    print()
    print()


    print("Making plots...")
    print()
    print()
    pit_out_rate = PitOutRate(pdfs, zgrid, ztrue).evaluate(pits=pits)

    fig_filename = pit.plot_pit_qq(pit_out_rate=pit_out_rate, code=code, savefig=True)
    print(f"PIT-QQ plot saved as:   {fig_filename}")
    print()
    print ()

    t1 = t.time()
    dt = t1 - t0
    print(f"Done! (total time: {int(dt)} seconds)")
    print()
    print()



if __name__ == "__main__":
    main(sys.argv)
