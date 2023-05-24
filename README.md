<div align="center">

[![DOI](https://zenodo.org/badge/223043497.svg)](https://zenodo.org/badge/latestdoi/223043497)
[![PyPI](https://img.shields.io/pypi/v/pz-rail?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/pz-rail/)
[![Read the Docs (version)](https://img.shields.io/readthedocs/lsstdescrail/stable?color=blue&logo=readthedocs&logoColor=white)](https://lsstdescrail.readthedocs.io/en/stable/#)

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/LSSTDESC/RAIL/rail?logo=Github)](https://github.com/LSSTDESC/RAIL/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/LSSTDESC/RAIL/branch/master/graph/badge.svg)](https://codecov.io/gh/LSSTDESC/RAIL)

</div>

# RAIL: Redshift Assessment Infrastructure Layers

RAIL is a flexible software library providing tools to produce at-scale photometric redshift data products, including uncertainties and summary statistics, and stress-test them under realistically complex systematics.
A detailed description of RAIL's modular structure is available in the [Overview Section](https://lsstdescrail.readthedocs.io/en/stable/source/overview.html) on ReadTheDocs.

RAIL serves as the infrastructure supporting many extragalactic applications of the Legacy Survey of Space and Time (LSST) on the Vera C. Rubin Observatory, including Rubin-wide commissioning activities. 
RAIL was initiated by the Photometric Redshifts (PZ) Working Group (WG) of the LSST Dark Energy Science Collaboration (DESC) as a result of the lessons learned from the [Data Challenge 1 (DC1) experiment](https://academic.oup.com/mnras/article/499/2/1587/5905416) to enable the PZ WG Deliverables in [the LSST-DESC Science Roadmap (see Sec. 5.18)](https://lsstdesc.org/assets/pdf/docs/DESC_SRM_latest.pdf), aiming to guide the selection and implementation of redshift estimators in DESC analysis pipelines.
RAIL is developed and maintained by a diverse team comprising of DESC Pipeline Scientists (PSs), international in-kind contributors, LSST Interdisciplinary Collaboration for Computing (LINCC) Frameworks software engineers, and other volunteers, but all are welcome to join the team regardless of LSST data rights. 

## Installation

Installation instructions are available in the [Installation section](https://lsstdescrail.readthedocs.io/en/stable/source/installation.html) on ReadTheDocs.

## Contributing

The greatest strength of RAIL is its extensibility; those interested in contributing to RAIL should start by consulting the [Contributing section](https://lsstdescrail.readthedocs.io/en/stable/source/contributing.html) on ReadTheDocs.

## Citing RAIL

This code, while publicly developed on GitHub and pip-installable, has not yet been released by DESC and is still under active development. 
Our release of v1.0 will be accompanied by a journal paper describing the development and validation of RAIL.
If you make use of the ideas or software here, you must cite this repository <https://github.com/LSSTDESC/RAIL> with the [Zenodo DOI](https://doi.org/10.5281/zenodo.7017551).
Please consider also inviting the authors of the code to join publications resulting from your use of RAIL by [making an issue](https://github.com/LSSTDESC/RAIL/issues/new/choose).
You are welcome to re-use the code, which is open source and available under terms consistent with our [LICENSE](https://github.com/LSSTDESC/RAIL/blob/main/LICENSE) [(BSD 3-Clause)](https://opensource.org/licenses/BSD-3-Clause).

### Citing specific codes accessed through RAIL

Several of the codes included within the RAIL ecosystem, e.g. BPZ, Delight, and FlexZBoost, are pre-existing codes that have been included in RAIL.
If you use those specific codes, you must also cite the appropriate papers for each code used, a convenient list of which may be found in the [Citing RAIL](https://lsstdescrail.readthedocs.io/en/stable/source/citing.html) section on ReadTheDocs.

## Future Plans

Potential extensions of the RAIL package are summarized in the [Future Plans section](https://lsstdescrail.readthedocs.io/en/stable/source/futureplans.html) on ReadTheDocs.
