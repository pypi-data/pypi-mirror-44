COnstrained Geometries simulate External Force
==============================================

COGEF is an ASE module which contains tools for simulating force-induced
bond-breaking reactions based on the COnstrained Geometries simulate External
Force (COGEF) method (Beyer, M. K. J. Chem. Phys. 2000, 112, 7307).

Webpage: https://gitedit.gitlab.io/cogef


Requirements
------------

* Python_ 2.7, 3.4-
* ASE_ (atomic simulation environment)
* NumPy_ (base N-dimensional array package)


Installation
------------

* Installation with pip::

  $ sudo pip install --upgrade pip
  $ python -m pip install ase-cogef

* Developer installation with git (no merge requests needed)

Clone the repository::

  $ git clone git@gitlab.com:GitEdit/cogef.git

Add ``cogef`` folder to the $PYTHONPATH environment variable.
Add ``cogef/bin`` folder to the $PATH environment variable.

* Developer installation with git (merge requests needed)

Go to https://gitlab.com/GitEdit/cogef and fork the project, then clone it
with your gitlab account name::

  $ git clone git@gitlab.com:your-user-name/cogef.git

Add ``cogef`` folder to the $PYTHONPATH environment variable.
Add ``cogef/bin`` folder to the $PATH environment variable.

Testing
-------

Please run the tests::

  $ cogef test


Contact
-------

* Functional Nanosystems group::

  https://www.functional-nanosystems.uni-freiburg.de/People/PDWalter

* Oliver Brügner::

  oliver.bruegner@fit.uni-freiburg.de


Example
-------

See https://gitedit.gitlab.io/cogef/tutorials/cogef.


.. _Python: http://www.python.org/
.. _ASE: http://wiki.fysik.dtu.dk/ase
.. _NumPy: http://docs.scipy.org/doc/numpy/reference/
