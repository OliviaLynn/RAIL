<div align="center">

[![DOI](https://zenodo.org/badge/223043497.svg)](https://zenodo.org/badge/latestdoi/223043497)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/LSSTDESC/RAIL/rail?logo=Github)](https://github.com/LSSTDESC/RAIL/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/LSSTDESC/RAIL/branch/master/graph/badge.svg)](https://codecov.io/gh/LSSTDESC/RAIL)
[![PyPI](https://img.shields.io/pypi/v/pz-rail?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/pz-rail/)
[![Read the Docs (version)](https://img.shields.io/readthedocs/lsstdescrail/stable?color=blue&logo=readthedocs&logoColor=white)](https://lsstdescrail.readthedocs.io/en/stable/#)

</div>

# RAIL: Redshift Assessment Infrastructure Layers

RAIL is a flexible software library providing tools to produce at-scale photometric redshift data products, including uncertainties and summary statistics, and stress-test them under realistically complex systematics.
RAIL was purpose is to be the infrastructure enabling the PZ WG Deliverables in [the LSST-DESC Science Roadmap (see Sec. 5.18)](https://lsstdesc.org/assets/pdf/docs/DESC_SRM_latest.pdf), aiming to guide the selection and implementation of redshift estimators in DESC pipelines.
RAIL differs from previous plans for PZ pipeline infrastructure in that it is broken into stages, each corresponding to a manageable unit of infrastructure advancement, a specific question to answer with that code, and a guaranteed publication opportunity.
RAIL uses [qp](https://github.com/LSSTDESC/qp) as a back-end for handling univariate probability density functions (PDFs) such as photo-z posteriors or n(z) samples.

A more detailed overview is available in the [Overview Section](https://lsstdescrail.readthedocs.io/en/stable/source/overview.html) of the RAIL Read The Docs page.

## Installation

Installation instructions are available on the [Installation section](https://lsstdescrail.readthedocs.io/en/stable/source/installation.html) of the [RAIL Read The Docs page](https://lsstdescrail.readthedocs.io/en/stable/)

## Contributing

If interested in contributing to `RAIL` see the [Contributing section](https://lsstdescrail.readthedocs.io/en/stable/source/contributing.html) of the RAIL Read The Docs page.

## Future Plans

Potential extensions of the RAIL package are summarized in the [Future Plans section](https://lsstdescrail.readthedocs.io/en/stable/source/futureplans.html) of the RAIL Read The Docs page.

## Citing RAIL

This code, while publicly developed on GitHub and pip-installable, has not yet been released by DESC and is still under active development. 
Our release of v1.0 will be accompanied by a journal paper describing the development and validation of RAIL.
If you make use of the ideas or software here, you must cite this repository <https://github.com/LSSTDESC/RAIL> with the [Zenodo DOI](https://doi.org/10.5281/zenodo.7017551).
Please consider also inviting the authors of the code to join publications resulting from your use of RAIL by [making an issue](https://github.com/LSSTDESC/RAIL/issues/new/choose).
You are welcome to re-use the code, which is open source and available under terms consistent with our [LICENSE](https://github.com/LSSTDESC/RAIL/blob/main/LICENSE) [(BSD 3-Clause)](https://opensource.org/licenses/BSD-3-Clause).

### Citing specific codes accessed through RAIL

Several of the codes included within the RAIL ecosystem, e.g. BPZ, Delight, and FlexZBoost, are pre-existing codes that have been included in RAIL.
If you use those specific codes, you must also cite the appropriate papers for each code used, a convenient list of which may be found in the [Citing RAIL](https://lsstdescrail.readthedocs.io/en/stable/source/citing.html) section on ReadTheDocs.
