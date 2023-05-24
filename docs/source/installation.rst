############
Installation
############

If you intend to use RAIL in exploratory mode with notebooks, see :ref:`RAIL 
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

Note: Running RAIL on a Mac M1+ will require installing healpy via conda.

Custom installations include:

* ``rail_ties``
* optionally: ``rail_pipelines``, if running a pipeline from command line
* optionally: any number of individual RAIL codes

Currently supported codes are:

* `rail_bpz <https://github.com/LSSTDESC/rail_bpz>`_
* `rail_flexzboost <https://github.com/LSSTDESC/rail_flexzboost>`_
* `rail_delight <https://github.com/LSSTDESC/rail_delight>`_
* And?


Example: Golden Spike custom installation
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