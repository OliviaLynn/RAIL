############
Installation
############

If you intend to use rail in exploratory mode with notebooks, see :ref:`RAIL 
Quickstart`.

If you intend to contribute to RAIL code or perform other development work, see 
:ref:`Installing RAIL from Source`.

If you're ready to run photo-z pipelines at scale, see :ref:`Custom Installation 
Instructions`.

RAIL Quickstart
***************

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

*Include a couple of lines about running notebooks*

Installing RAIL from Source
***************************

Create a new conda environment:

.. code-block:: bash

    conda create -y --name [your-env-name] pip python=3.10 h5py 
    conda activate [your-env-name]

If you are using a Mac with an M1+ chip, you will need to install healpy with
conda:

.. code-block:: bash

    conda install -c conda-forge healpy

Go to the directory you wish to work in, clone the repository, and install RAIL 
in editable mode:

.. code-block:: bash

    cd [whichever-directory]
    gh repo clone LSSTDESC/RAIL
    cd RAIL
    pip install -e .

Custom Installation Instructions
************************************

Custom installations include ``rail_ties``, plus any number of 
additional RAIL packages. 

Note: Running RAIL on a Mac M1+ will require installing healpy via conda.

RAIL Pipelines
==============

Running a RAIL pipeline from command line requires the ``rail_pipelines`` package, as well.

Individual RAIL Codes
=====================

RAIL codes may be installed individually by name.

Currently supported codes are:


Example: Golden Spike Custom Installation
=========================================

A user wishes to run the Golden Spike example pipeline. 

This pipeline uses the BPZ and Flexzboost codes. *(Any others?)*

The user will need ``rail_ties`` and ``rail_pipelines``, as well as 
``rail_bpz``, ``rail_flexzboost``, and (anything else?).

Such a user might run:

.. code-block:: bash

    conda create -y --name rail-env pip python=3.10 h5py 
    conda activate rail-env
    pip install pz-rail-ties pz-rail-pipelines pz-rail-bpz pz-rail-flexzboost

Then, they can run the pipeline by:

.. code-block:: bash

    cd [whichever-directory]
    ceci ---