==============
Transport Maps
==============

This package provides basic functionalities for the construction of monotonic transport maps.

Supported systems
-----------------

* \*nix like OS (Linux, Unix, ...)
* Mac OS

Other operating systems have not been tested and they likely require a more complex procedure for the installation (this includes the Microsoft Windows family..).

We reccommend to work in a virtual environment using `virtualenv <https://virtualenv.readthedocs.io/en/latest/>`_ or `Anaconda <https://www.continuum.io/why-anaconda>`_.

Installation requirements
-------------------------

* `gcc <https://gcc.gnu.org/>`_ (or an alternative C/C++ compiler)
* `gfortran <https://gcc.gnu.org/fortran/>`_ (or an alternative Fortran compiler)

Automatic installation
----------------------

First of all make sure to have the latest version of `pip <https://pypi.python.org/pypi/pip>`_ installed

 $ pip install --upgrade pip

The package and its python dependencies can be installed running the command:

 $ pip install --upgrade numpy
 $ pip install --upgrade TransportMaps

If one whish to enable some of the optional dependencies:

 $ MPI=True SPHINX=True PLOT=True H5PY=True pip install --upgrade TransportMaps

These options will install the following modules:

* MPI -- parallelization routines (see the `tutorial <mpi-usage.html>`_). It requires the separate installation of an MPI backend (`openMPI <https://www.open-mpi.org/>`_, `mpich <https://www.mpich.org/>`_, etc.). The following Python modules will be installed:
  * `mpi4py <https://pypi.python.org/pypi/mpi4py>`_
  * `mpi_map <https://pypi.python.org/pypi/mpi_map>`_

* PLOT -- plotting capabilities:

  * `MatPlotLib <https://pypi.python.org/pypi/matplotlib/>`_

* SPHINX -- documentation generation routines:

  * `sphinx <https://pypi.python.org/pypi/Sphinx>`_
  * `sphinxcontrib-bibtex <https://pypi.python.org/pypi/sphinxcontrib-bibtex/>`_
  * `ipython <https://pypi.python.org/pypi/ipython>`_
  * `nbsphinx <https://pypi.python.org/pypi/nbsphinx>`_

* H5PY -- routines for the storage of big data-set. It requires the separate installation of the `hdf5 <https://www.hdfgroup.org/>`_ backend.

  * `mpi4py <https://pypi.python.org/pypi/mpi4py>`_
  * `h5py <http://www.h5py.org/>`_

* PYHMC -- routines for Hamiltonian Markov Chain Monte Carlo

  * `pyhmc <http://pythonhosted.org/pyhmc/>`_

Manual installation
-------------------

If anything goes wrong with the automatic installation you can try to install manually the following packages.

Mandatory Back-end packages (usually installed with `numpy <https://pypi.python.org/pypi/numpy>`_):

* `BLAS <http://www.netlib.org/blas/>`_ (with development/header files)
* `LAPACK <http://www.netlib.org/lapack/>`_ (with development/header files)

Mandatory Python packages:

* `pip <https://pypi.python.org/pypi/pip>`_
* `numpy <https://pypi.python.org/pypi/numpy>`_ >= 1.10
* `scipy <https://pypi.python.org/pypi/scipy>`_
* `orthpol_light <https://pypi.python.org/pypi/orthpol-light>`_
* `SpectralToolbox <https://pypi.python.org/pypi/SpectralToolbox>`_
* `dill <https://pypi.python.org/pypi/dill>`_

Finally install TransportMaps:

 $ pip install TransportMaps

Running the Unit Tests
----------------------

Unit tests are available and can be run through the command:

   >>> import TransportMaps as TM
   >>> TM.tests.run_all()

There are >3500 unit tests, and it will take some time to run all of them.

Status
------

+--------+----------------------------------------------------------------------------------+------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
|        | `Binary (PyPi) <https://pypi.python.org/pypi/TransportMaps>`_                    | `Public source (Bitbucket) <https://bitbucket.org/dabi86/transportmaps>`_          | `Private master (Bitbucket) <https://bitbucket.org/dabi86/transportmaps-private>`_         | `Private develop (Bitbucket) <https://bitbucket.org/dabi86/transportmaps-private>`_         | `Private hotfixes (Bitbucket) <https://bitbucket.org/dabi86/transportmaps-private>`_         |
+--------+----------------------------------------------------------------------------------+------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| Serial | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-pypi      | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-public      | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-master      | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-develop      | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-hotfixes      |
|        |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-pypi     |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-public     |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-master     |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-develop     |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-hotfixes     |
+--------+----------------------------------------------------------------------------------+------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+
| MPI    | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-pypi-mpi  | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-public-mpi  | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-master-mpi  | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-develop-mpi  | .. image:: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-hotfixes-mpi  |
|        |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-pypi-mpi |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-public-mpi |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-master-mpi |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-develop-mpi |    :target: https://acdl.mit.edu/csi/buildStatus/icon?job=TransportMaps-private-hotfixes-mpi |
+--------+----------------------------------------------------------------------------------+------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+

Credits
-------

This sofware has been developed and is being maintained by the `Uncertainty Quantification Group <http//uqgroup.mit.edu>`_ at MIT, under the guidance of Prof. Youssef Marzouk.

**Developing team**

| Daniele Bigoni – [`www <http://limitcycle.it/dabi/>`_]
| Alessio Spantini
| Rebecca Morrison
| Ricardo M. Baptista
|
