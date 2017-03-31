.. -*- coding: utf-8; mode: rst -*-
.. include:: refs.txt

.. _xref_dbxml2rst_install:

============================
Install dbxml2rst and Pandoc
============================

This is a python 3 project (no python 2 support). First install python3 on your
OS, e.g. on Debian/Ubuntu::

  sudo apt-get install python3 python3-pip3

Next step is to clone the repository from github and install it::

  git clone https://github.com/return42/dbxml2rst.git
  cd dbxml2rst
  make install

This installs dbxml2rst and the `pandoc-filters`_. The dbxml2rst library
requires an up-to-date pandoc installation. I recommend to use pandoc
version>=1.17.1 which is available e.g. on Ubuntu 16.04.::

  $ sudo apt-get install pandoc

If your distribution has no pandoc or an older version, you have to go the *hard
way* and install the developer version of haskell-stack, ghc and pandoc
(:ref:`pandoc_devel_inst`).


.. _pandoc_devel_inst:

pandoc developer installation
=============================

The developer installation of pandoc requires up-to-date installations of
haskell-stack, ghc and pandoc.

To install haskell-stack on your OS follow:

* https://docs.haskellstack.org/en/stable/README/

Alternative use the 'haskell-stack' target of dbxm2rst Makefile::

  $ make haskell-stack

To install pandoc and ghc follow:

* https://github.com/jgm/pandoc/wiki/Installing-the-development-version-of-pandoc

Alternative use the 'pandoc-build' target of dbxm2rst Makefile::

  $ make pandoc-build

.. caution::

   Remind, building the haskel compiler and compiling pandoc does massive time,
   memory and CPU consumption.
