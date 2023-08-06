==============
DSClient-py
==============

A Python client for interacting with `debugserver-js <https://github.com/tiflash/debugserver-js>`__

Documentation can be found at

    https://dsclient-py.readthedocs.io/


Install
=======

From PyPi
---------

*Currently not available*

From Source
-----------

::

    pip install .

Development
===========

To setup your development environment, you'll need at least one device to run
tests on. Below are the devices supported out of the box that include resources
for testing (if you want to run tests on a device not listed below, you'll need
to provide similar resources for that device. See tests/resources/cc13x0 for an
example)

- cc13x0

Steps
-----

1. Edit the file tests/env.cfg

   a. Enter the full path to your ccs installation under `ccs_exe`
   b. Enter the serial number for the device you'd like to run tests on

2. Configure the test setup
   ::

       make configure

3. Run tests
   ::

       make test
