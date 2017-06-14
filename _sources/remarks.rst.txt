.. -*- coding: utf-8; mode: rst -*-
.. include:: refs.txt

===========================
Remarks on Pandoc & DocBook
===========================

remarks on pandoc
=================

There are plenty docbook converter out. Most of them have common, that they
implement there own (less XML) parsers and they always implement only a subset
of the DocBook markup.

The coverage of the pandoc DocBook reader is the most advanced, but it is merely
a subset of the DocBook markup.  If the pandoc reader does not implement a
markup, it will not be in the AST. This is, why it can't be handled in a pandoc
filter. The coverage of the pandoc DocBook reader is documented in the sources:

* https://github.com/jgm/pandoc/blob/master/src/Text/Pandoc/Readers/DocBook.hs#L23

The pandoc reStructuredText writer is also incomplete and has several bugs, for
details take a look at the sources:

* https://github.com/jgm/pandoc/blob/master/src/Text/Pandoc/Writers/RST.hs

On my Ubuntu 15.10 sandbox is the pandoc version 1.13.2 via package manager
available. In this version, the DocBook reader missed some common used markups
like ``<xref>``. Therefore the development version of pandoc is needed (see
:ref:`pandoc_devel_inst`).  Remind, building the Haskell compiler and compiling
pandoc does massive time, memory and CPU consumption.

The pandoc DocBook reader does not *understand* XML nor SGML, therefore it will
not do all these XML stuff, like reading external entities (this is where the
dbxml2rst library comes into account).

DocBook remarks
===============

DocBook documentation is available from:

* http://docbook.org/tdg/en/html/docbook.html
