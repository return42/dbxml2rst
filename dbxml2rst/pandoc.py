#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
# pylint: disable=C0103,R0912,R0914,R0915

u"""
    dbxml2rst.pandoc
    ~~~~~~~~~~~~~~~~

    Pandoc stuff used by the dbxml2rst library

    :copyright:  Copyright (C) 2016  Markus Heiser
    :license:    GPL V3.0, see LICENSE for details.
"""


# ==============================================================================
# imports
# ==============================================================================

import re
import sys
import functools
import json

from fspath import which

from .nodes import Table
from . import helper
from .helper import LOG

# ==============================================================================
# constants
# ==============================================================================

PANDOC_EXE = None

def init():
    global PANDOC_EXE # pylint: disable=W0603
    PANDOC_EXE = which('pandoc', False)


# ==============================================================================
def xml2json(src, dst, **kwargs):
# ==============================================================================

    u"""convert xml file to json file with pandoc"""

    if not PANDOC_EXE:
        LOG.error("pandoc is not installed")
        sys.exit(42)

    proc = PANDOC_EXE.Popen(
        "--smart"
        # , "-s" # standalone document
        , "--from", "docbook"
        , "--to", "json"
        , "--output" , dst
        , src
        , **kwargs )
    proc.communicate()


# ==============================================================================
def toJSONFilters(input_stream, output_stream, *actions):
# ==============================================================================

    """Modified version of pandoc filter.

    This version of pandoc filter is able to read from any input stream (not only
    from stdin) and writes to any output stream (not only stdout).
    """
    import pandocfilters
    doc = json.loads(input_stream.read())
    fmt = "json"
    altered = functools.reduce(
        lambda x, action: pandocfilters.walk(x, action, fmt, doc[0]['unMeta'])
        , actions, doc )
    json.dump(altered, output_stream)


# ==============================================================================
def jsonFilter(src, dst, *filters):
# ==============================================================================

    u"""apply ``*filters`` on a pandoc json file"""

    with src.openTextFile() as inFile, dst.openTextFile("w") as outFile:
        toJSONFilters(inFile, outFile, *filters)


# ==============================================================================
def json2rst(src, dst, **kwargs):
# ==============================================================================

    u"""convert a json file with pandoc to reST markup"""

    proc = PANDOC_EXE.Popen(
        "--reference-links"
        , "--from", "json"
        , "--to", "rst"
        , "--output" , dst
        # activate this for the large ASCII tables
        #, "--columns" , "180"
        , src
        , **kwargs )
    proc.communicate()

# ==============================================================================
def fixPandocRST(src, dst):
# ==============================================================================

    u"""Fix common reST markup bugs from the pandoc reST writer.  """

    # fix malicious pandoc quoting
    # https://github.com/jgm/pandoc/blob/master/src/Text/Pandoc/Writers/RST.hs#L162
    # --> """escapeStringUsing (backslashEscapes "`\\|*_")"""
    backslashEscapes = re.compile(r"\\[`\|\||\*|_]")

    indent = ""
    with src.openTextFile() as src, dst.openTextFile("w") as dst:

        dst.write(helper.rstHEADER)

        for line in src:
            line = line.replace(u"⋆", "*")
            striped = line.strip()
            if not striped:
                dst.write("\n")
                continue
            if striped == Table.tableStartMark:
                indent += Table.rstBlock
                continue
            if striped == Table.tableEndMark:
                indent = indent[:-len(Table.rstBlock)]
                continue

            line = indent + line

            if backslashEscapes.search(line):
                spaces = ""
                if line.strip()[0] == "|":
                    # this is a table markup
                    buf  = ""
                    for c in line:
                        if c == "\\":
                            spaces += " "
                        elif spaces and c in ["\t", " ", "\n"]:
                            buf += spaces + c
                            spaces = ""
                        else:
                            buf += c
                    line = buf.rstrip() + "\n"
                else:
                    line = line.replace("\\", "")
            dst.write(line)

        dst.write(helper.rstFOOTER)

# ==============================================================================
# init
# ==============================================================================

init()

