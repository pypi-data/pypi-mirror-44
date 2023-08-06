=====================
DSClient-py   |Build|
=====================

A Python client for interacting with `debugserver-js <https://github.com/tiflash/debugserver-js>`__

Documentation can be found at

    https://dsclient-py.readthedocs.io/


Install
=======

From PyPi
---------

::

    pip install dsclient

From Source
-----------

::

    cd dsclient-py/
    pip install .

Development
===========

To setup your development environment, you'll need at least one device to run
tests on. Below are the devices supported out of the box that include resources
for testing (if you want to run tests on a device not listed below, you'll need
to provide similar resources for that device. See `tests/resources/cc13x0 <tests/resources/cc13x0>`_ for an
example)

- cc13x0

Steps
-----

1. Edit the file `tests/env.cfg <tests/env.cfg>`_

   a. Enter the full path to your ccs installation under ``ccs``
   b. Enter the required device information (see `tests/resources/cc13x0/README.rst <tests/resources/cc13x0/README.rst>`_
      for what's required)

2. Configure the test setup
   ::

       make configure

3. Run tests
   ::

       make test

.. Badges:

.. |Build| image::    https://travis-ci.org/webbcam/dsclient-py.svg?branch=master
    :target:            https://travis-ci.org/webbcam/dsclient-py
    :alt:               Build
