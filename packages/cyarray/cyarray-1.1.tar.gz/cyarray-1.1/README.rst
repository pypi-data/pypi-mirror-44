cyarray: a typed, re-sizable Cython array
------------------------------------------

|Travis Status| |Appveyor Status| |Documentation Status|


.. |Travis Status| image:: https://travis-ci.org/pypr/cyarray.svg?branch=master
    :target: https://travis-ci.org/pypr/cyarray
.. |Appveyor Status| image:: https://ci.appveyor.com/api/projects/status/rbl358nj2876dap1?svg=true
    :target: https://ci.appveyor.com/project/prabhuramachandran/cyarray
.. |Documentation Status| image:: https://readthedocs.org/projects/cyarray/badge/?version=latest
    :target: https://cyarray.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


The cyarray package provides a fast, typed, re-sizable, Cython array.

It currently provides the following arrays: ``IntArray, UIntArray, LongArray,
FloatArray, DoubleArray``.

All arrays provide for the following operations:

- access by indexing.
- access through get/set function.
- resizing the array.
- appending values at the end of the array.
- reserving space for future appends.
- access to internal data through a numpy array.

If you are writing Cython code this is a convenient array to use as it exposes
the raw underlying pointer to the data. For example if you use a ``FloatArray``
and access its ``data`` attribute it will be a ``float*``.

Each array also provides an interface to its data through a numpy array.
This is done through the ``get_npy_array`` function. The returned numpy
array can be used just like any other numpy array but for the following
restrictions:

- the array may not be resized.
- references of this array should not be kept.
- slices of this array may not be made.

The numpy array may however be copied and used in any manner.

Installation
------------

cyarray can be installed using pip_::

  $ pip install cyarray

The package requires ``Cython``, ``numpy``, and ``mako`` to be installed and
also requires a suitably configured C/C++ compiler.

.. _pip: http://www.pip-installer.org

Usage
-----

In Python one may import and use the package as::

  from cyarray.api import IntArray
  a = IntArray(10)

Here ``a`` is an array of 10 integers.
