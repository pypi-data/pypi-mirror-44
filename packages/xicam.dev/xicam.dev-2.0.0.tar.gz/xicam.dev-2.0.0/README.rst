==================================
Xi-cam 2 Developer Quick-Installer
==================================

A quick-installer for Xi-cam 2 developers. Python and Git experience required. The default install location is **~/Xi-cam**.

Attention
---------

Xi-cam 2 has not yet reached a release state. Expect some changes to API design as we continue development.

Requirements
------------

- Python 3.6+
- PyQt5
- GitPython
- (...and the Xi-cam 2 platform requirements)

Installation
------------

To run the quick-installer::

    pip install -v xicam.dev

This quick-installer performs the following operations:

- Clone essential Xi-cam 2 packages to the installation directory
- Install Xi-cam 2 dependencies
- Install Xi-cam 2 essential packages as editable source

Note: The `-v` allows you to see installation progress.

Configuration
-------------