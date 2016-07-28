# -*- coding: utf-8; mode: python -*-
u"""
Normally XML tools are used to convert DocBook XML, e.g. XSL Style-sheets
to convert DocBook XML into various formats (examples:
http://docbook.sourceforge.net/release/xsl/current).

I haven't found any XSL Template to convert DocBook to reST, and I'am not
interested in developing one. Thats why I compiled these small ``dbxml2rst``
toolbox, which uses existing tools and *hacked* a bit around them.  The
``dbxml2rst`` uses the pandoc converter and implements some XML-filters, where
pandoc fails, e.g. cross references in a multi-part DocBook document.

The migration of DocBook-XML is a working process and a task which is mostly
done by developers, not end users. This in mind, the ``dbxml2rst`` tools are not
*ready to go* for every one.  The ``dbxml2rst`` toolbox is useful for DocBook
to reST migration, it don't attempt to be a *converter* for a daily usage.

:copyright:  Copyright (C) 2016 Markus Heiser
:e-mail:     *markus.heiser*\ *@*\ *darmarIT.de*
:license:    GPL Version 2, June 1991 see linux/COPYING for details.
:docs:       http://return42.github.io/dbxml2rst
:reposetory: `github return42/fspath <https://github.com/return42/dbxml2rst>`_

"""

__version__     = "20160727"
__copyright__   = "2016 Markus Heiser"
__url__         = "https://github.com/return42/dbxm2rst"
__description__ = "Collection of *hackish* tools to migrate DocBook-XML to reST."
__license__     = "GPLv2"

