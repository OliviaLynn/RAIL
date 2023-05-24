############
Installation
############

RAIL supports multiple interaction modes to enable a variety of use cases.
We thus provide three quick-start guides to help you get set up with the one(s) that best meet your needs.

If you want to use RAIL to explore different estimators on a variety of mock or real data and assess the results in Jupyter notebooks, see :ref:`RAIL Quickstart for data exploration`.

If you're ready to run specific analysis pipelines at scale from the command line, see :ref:`RAIL Quickstart for at-scale pipeline execution`.

"Golden Spike" end-to-end demos are provided for both these usage modes.

If you intend to contribute to RAIL by adding new ways to generate mock data, estimate redshift information, or assess the quality for your use case, see :ref:`RAIL Quickstart for prospective developers`.

Quickstart for data exploration
*******************************

These instructions will equip you with the maximal set of features, including engines to generate mock data, degraders to introduce realistic imperfections to the mock data, algorithms to characterize photo-z uncertainties, and metrics to evaluate results.

Create a new conda environment:

.. code-block:: bash

    conda create -y --name [your-env-name] pip python=3.10 h5py 
    conda activate [your-env-name]

*Check: is h5py necessary? Do we include the python=3.10? when decision made
update this in following section as well.*

If you are using a Mac with an M1+ chip, you will need to install healpy with
conda:

.. code-block:: bash

    conda install -c conda-forge healpy

Now, you can install RAIL:

.. code-block:: bash

    pip install pz-rail
    
RAIL provides an extensive set of demonstrative Jupyter notebooks, including the Golden Spike end-to-end demo, that you can access here on ReadTheDocs, or you can install `pz-rail` from source to get them on your local machine:

.. code-block:: bash

    git clone git@github.com:LSSTDESC/RAIL.git
    cd RAIL
    pip install .
    
*This doesn't make use of the conditional install script stuff*

Quickstart for at-scale pipeline execution
******************************************

These instructions assume you are already familiar with the underlying algorithms to estimate photo-zs and their uncertainties and/or engines to create mock data and just want the minimal amount of code to run the one you want.

Create a new conda environment:

.. code-block:: bash

    conda create -y --name [your-env-name] pip python=3.10 h5py 
    conda activate [your-env-name]

If you are using a Mac with an M1+ chip and want to use degraders with spatial dependence, you will need to install healpy with conda:

.. code-block:: bash

    conda install -c conda-forge healpy

The following approaches are supported as standalone packages that you can install with pip, all of which include the barebones `rail_ties` package containing the basic infrastructure and class definitions:

* `pz-rail-bpz <https://github.com/LSSTDESC/rail_bpz>`_
* `pz-rail-delight <https://github.com/LSSTDESC/rail_delight>`_
* `pz-rail-flexzboost <https://github.com/LSSTDESC/rail_flexzboost>`_
* `pz-rail-fsps <https://github.com/LSSTDESC/rail_fsps>`_
* `pz-rail-gpz <https://github.com/LSSTDESC/rail_gpz_v1>`_

*check these names*

Then, install `pz-rail-pipelines <https://github.com/LSSTDESC/rail_pipelines>`_ to access a variety of demonstrative modules and config files upon which to build your pipeline.

.. code-block:: bash

    pip install pz-rail-pipelines
    
To contribute your own pipeline to the repository, install from source and make a pull request.

*why not just tell them to install from source from the start?*
    
Example: the Golden Spike end-to-end demo
=========================================

The Golden Spike pipeline uses the BPZ and Flexzboost estimation algorithms so those must be installed first:

.. code-block:: bash

    conda create -y --name rail-env pip python=3.10 h5py 
    conda activate rail-env
    pip install pz-rail-ties pz-rail-pipelines pz-rail-bpz pz-rail-flexzboost

*I don't think rail-ties would be necessary here because it's included in the others, no?*

Then, they can run the pipeline by:

.. code-block:: bash

    cd [whichever-directory]
    ceci ---
    
Quickstart for prospective developers
*************************************

These instructions will enable you to wrap your own methods for estimating photo-zs, characterizing their uncertainties, and summarizing their ensemble properties through the same API shared with other algorithms.

Create a new conda environment:

.. code-block:: bash

    conda create -y --name [your-env-name] pip python=3.10 h5py 
    conda activate [your-env-name]

Go to the directory you wish to work in, clone the repository, and install RAIL 
in editable mode:

.. code-block:: bash

    cd [whichever-directory]
    gh repo clone LSSTDESC/RAIL
    cd RAIL
    pip install -e .
    
*update to rail-ties when ready*

After familiarizing yourself with the wrapped methods in src/rail/estimation/algos, src/rail/creation/engines, src/rail/creation/degraders, and/or src/rail/evaluation/metrics, please refer to the Contributing page for details on next steps.
