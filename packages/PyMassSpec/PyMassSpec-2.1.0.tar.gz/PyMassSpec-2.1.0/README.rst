************
PyMassSpec
************

A Python toolkit for processing of chromatography--mass spectrometry data
===========================================================================

Originally by Andrew Isaac, Sean O'Callaghan and Vladimir Likić
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Forked from the original PyMS Repository: https://github.com/ma-bio21/pyms.

The project seems to have been abandoned as there have been no commits in 18 months.

|

Introduction
==============
PyMassSpec is a a Python_ package for processing chromatography-mass spectrometry data,
released under the `GNU Public License version 2 <GPL_>`__.

PyMassSpec provides a framework and a set of components for rapid development
and testing of methods for processing of chromatography--mass spectrometry data.
PyMassSpec can be used interactively through the Python shell, or the functions
can be collected into scripts and run non-interactively when it is preferable
to perform data processing in the batch mode.

PyMassSpec functionality consists of modules which are loaded when needed,
and different functionalities are completely decoupled from one another.
If desired, new functionality (such as a test or prototype of a new algorithm)
can be implemented efficiently and ensuring that this will not break any
existing functionality.

.. _Python: https://www.python.org/
.. _GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html


The original publication can be found here: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-13-115


The PyMS project
=================

The directory structure of PyMassSpec is as follows:

.. code-block:: text

    /
    ├── pyms:      The PyMassSpec code
    │
    ├── docs: The PyMassSpec User Guide and Documentation
    │
    ├── pyms-test: Examples of how to use PyMassSpec
    │
    └── UserGuide: Sphinx source for pyms-docs

