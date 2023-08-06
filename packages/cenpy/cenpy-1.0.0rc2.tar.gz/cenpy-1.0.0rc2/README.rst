CenPy
=====
.. image:: https://travis-ci.org/ljwolf/cenpy.svg?branch=master
    :target: https://travis-ci.org/ljwolf/cenpy
.. image:: https://img.shields.io/pypi/dm/cenpy.svg
    :target: https://pypi.org/project/cenpy/
.. image:: https://zenodo.org/badge/36956226.svg
    :target: https://zenodo.org/badge/latestdoi/36956226

An interface to explore and query the US Census API and return Pandas
Dataframes. Ideally, this package is intended for exploratory data
analysis and draws inspiration from sqlalchemy-like interfaces and
``acs.R``.

An `intro notebook is
available <http://nbviewer.ipython.org/github/ljwolf/cenpy/blob/master/demo.ipynb>`__.

Also, a great example on how to grab work with cenpy, moving from nothing to
data to map, `is here <https://gist.github.com/dfolch/2440ba28c2ddf5192ad7>`__, 
by `@dfolch <https://github.com/dfolch>`__. 

Installation
------------

This package depends on `Pandas <https://pandas.pydata.org>`__ and
`requests <https://docs.python-requests.org/en/latest>`__. You can
install ``cenpy`` and other dependencies using ``pip``:

``pip install cenpy``

If you do not have ``pip``, simply copy the module somewhere in your
python path.

Usage
-----

Once done, importing ``cenpy`` will provide the ``explorer`` and
``base`` modules. To create a connection:

::

    cxn = cenpy.base.Connection('DECENNIALSF12010')

Check the variables required and geographies supported:

::

    cxn.variables #is a pandas dataframe containing query-able vbls
    cxn.geographies #is a pandas dataframe containing query-able geographies

Note that some geographies (like tract) have higher-level requirements
that you'll have to specify for the query to work.

The structure of the query function maps to the Census API's use of
``get``, ``for``, and ``in``. The main arguments for the query function
are ``cols``, ``geo_unit`` and ``geo_filter``, and map back to those predicates, respectively. If more predicates are required for the
search, they can be added as keyword arguments at the end of the query.

The ``cols`` argument must be a list of columns to retrieve from the
dataset. Then, you must specify the ``geo_unit`` and ``geo_filter``,
which provide *what* the unit of aggregation should be and *where* the
units should be. ``geo_unit`` must be a string containing the unit of
analysis and an identifier. For instance, if you want all counties in
Arizona, you specify ``geo_unit = 'county:*'`` and ``geo_filter =
{'state':'04'}``.

ToDo:
-----

- Recursively search for incompletely-specified hierarchies (partially implemented in `cenpy.tools`)
- Write dedicated wrappers for commonly-used data products, such as
    - ACS
    - Decennial censuses (2010,2000,1990)
    - County Business Statistics
