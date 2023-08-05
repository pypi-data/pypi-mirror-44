****************
pip-install-test
****************
A stub package for testing if pip install is working.

Introduction
============

The intent of this package is to provide a simple module that can be easily installed and uninstalled.
This provides a straightforward mechanism for showing that an arbitrary environment is capable of installing third party modules via ``pip``.
It is not intended to exercise the full feature set of ``pip`` or ``setuptools``, but to provide a minimal existence proof of viability.

Usage
=====

Install::

  pip install pip-install-test

or::

  pip install --user pip-install-test

Import:: 
 
  >>> import pip_install_test

or::

  python -c 'import pip_install_test'

Uninstall::
 
  pip uninstall pip-install-test
