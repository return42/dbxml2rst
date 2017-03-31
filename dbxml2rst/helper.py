#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
# pylint: disable=C0103

u"""
    dbxml2rst.helpers
    ~~~~~~~~~~~~~~~~~

    Some helpers, used by the dbxml2rst library

    :copyright:  Copyright (C) 2017  Markus Heiser
    :license:    GPL V3.0, see LICENSE for details.
"""

# ==============================================================================
# imports
# ==============================================================================

import os
import sys
import json
import argparse

from fspath import FSPath, OS_ENV

# ==============================================================================
# constants
# ==============================================================================

mainFOOTER=""
rstHEADER=""".. -*- coding: utf-8; mode: rst -*-
"""
rstFOOTER=""

# ==============================================================================
class Container(dict):
# ==============================================================================

    u"""container class"""

    @property
    def __dict__(self):
        return self

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, val):
        self[attr] = val

# ==============================================================================
# Logging stuff
# ==============================================================================

STREAM = Container(
    # pipes used by the application & logger
    appl_out   = sys.__stdout__
    , log_out  = sys.__stderr__
    , )

VERBOSE = False
DEBUG   = False
QUIET   = False

class SimpleLog(object):

    LOG_FORMAT = "%(logclass)s: %(message)s\n"

    def error(self, message, **replace):
        message = message % replace
        replace.update(dict(message = message, logclass = "ERROR"))
        STREAM.log_out.write(self.LOG_FORMAT % replace)

    def warn(self, message, **replace):
        if QUIET:
            return
        message = message % replace
        replace.update(dict(message = message, logclass = "WARN"))
        STREAM.log_out.write(self.LOG_FORMAT % replace)

    def info(self, message, **replace):
        if QUIET or not VERBOSE:
            return
        message = message % replace
        replace.update(dict(message = message, logclass = "INFO"))
        STREAM.log_out.write(self.LOG_FORMAT % replace)

    def debug(self, message, **replace):
        if not DEBUG:
            return
        message = message % replace
        replace.update(dict(message = message, logclass = "DEBUG"))
        STREAM.log_out.write(self.LOG_FORMAT % replace)

    def msg(self, message, **replace):
        if QUIET:
            return
        message = message % replace
        STREAM.appl_out.write(message + "\n")

LOG = SimpleLog()

# ==============================================================================
class PContainer(Container):
# ==============================================================================

    u"""Persistent container class.

    The persistence is a json dump in the file given by constructor's argument
    ``fname``. It serialize only properties (objects) which are covered by the
    :py:mod:`json.dump`.
    """
    @property
    def __dict__(self):
        return self

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, val):
        self[attr] = val

    def __init__(self, fname, *args, **kwargs):
        dict.__setattr__(self, "pFile", FSPath(fname))
        self.updFromFile()
        super(PContainer, self).__init__(self, *args, **kwargs)

    def updFromFile(self):
        if not self.pFile.EXISTS:
            return
        with self.pFile.openTextFile(mode='r', encoding='utf-8') as jsonFile:
            self.update(json.load(jsonFile, encoding='utf-8'))

    def writeToFile(self):
        tmpFile = FSPath(self.pFile + "tmp")
        with tmpFile.openTextFile(mode='w', encoding='utf-8') as jsonFile:
            jsonFile.write(str(json.dumps(self, ensure_ascii=False)))
        tmpFile.move(self.pFile)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.writeToFile()

# ==============================================================================
class EntityContainer(PContainer):
# ==============================================================================

    u"""Variant of PContainer used by the dbxml2rst for xml-entities."""

    def addNew(self, attr, val):
        unset = object()
        exists = self.get(attr, unset)
        for k,v in self.items():
            if v == val:
                LOG.info("two entity names with identical value %s <--> %s (%s)" % (attr, k,v))

        if exists != unset:
            if exists == val:
                LOG.info("double entity entry %r -->  %r" % (attr, exists))
            else:
                raise KeyError("name collision %r -->  old: %r <--> new: %r"
                               % (attr, exists, val))
        else:
            self[attr] = val

# ==============================================================================
class CLI(object):
# ==============================================================================

    u"""A comfortable commandline."""

    _OUT = sys.__stdout__
    _ERR = sys.__stderr__

    def __init__(self, *args, **kwargs):

        kwargs["formatter_class"] = argparse.ArgumentDefaultsHelpFormatter

        self.cmdFunc       = kwargs.pop("cmdFunc", None)
        self.cliSubParsers = None

        if self.cmdFunc is not None:
            kwargs["epilog"] = kwargs.get("epilog", self.cmdFunc.__doc__)
            kwargs["description"] = kwargs.get(
                "description"
                , kwargs["epilog"].strip().split("\n")[0] if kwargs["epilog"] else None)

        self.parser        = argparse.ArgumentParser(*args, **kwargs)

        if self.cmdFunc is None:
            self.cliSubParsers = self.parser.add_subparsers(title='commands', dest='command')
            self.cliSubParsers.required = True

        self.add_argument  = self.parser.add_argument
        self.add_argument(
            '--debug'
            , action  = 'store_true'
            , help    = 'run in debug mode' )

        self.add_argument(
            '--verbose'
            , action  = 'store_true'
            , help    = 'run in verbose mode' )

        self.add_argument(
            '--quiet'
            , action  = 'store_true'
            , help    = 'run in quiet mode' )

    def addCMDParser(self, func, cmdName=None):

        if self.cliSubParsers is None:
            raise Exception("this command-line has no sub-commands!")

        subCmd = self.cliSubParsers.add_parser(
            cmdName or func.__name__
            , epilog          = func.__doc__
            , formatter_class = argparse.ArgumentDefaultsHelpFormatter
            , help            = ((func.__doc__ or "").strip().split("\n") + [ "sorry, no help available" ])[0]
        )
        subCmd.set_defaults(func=func)
        return subCmd

    def __call__(self):

        _exitCode  = 0
        _exception = None
        _retVal    = None

        self.autocomplete()

        cmd_args = self.parser.parse_args()
        cmd_args.CLI = self

        if OS_ENV.get("DEBUG", None):
            cmd_args.debug = True

        # pylint: disable=W0603
        global DEBUG, VERBOSE, QUIET
        DEBUG   = cmd_args.debug
        VERBOSE = cmd_args.verbose
        QUIET   = cmd_args.quiet

        LOG.debug(u"argparse --> %s\n" % cmd_args)
        try:
            if self.cmdFunc is None:
                _retVal = cmd_args.func(cmd_args)
            else:
                _retVal = self.cmdFunc(cmd_args)
            try:
                _exitCode = int(_retVal)
            except Exception as exc: # pylint: disable=W0703
                pass

        except Exception as exc: # pylint: disable=W0703
            if cmd_args.debug:
                raise
            _exitCode  = 42
            _exception = str(exc)
            sys.stderr.write(u"FATAL ERROR: %s\n" % _exception)
        sys.exit(_exitCode)

    def autocomplete(self):
        u"""bash completion

        To get in use of bash completion, install ``argcomplete``:

        .. code-block:: bash

           pip install argcomplete

        and add the following to your ~/.bashrc:

        .. code-block:: bash

           function _py_argcomplete() {
                   local IFS=$(echo -e '\\v')
                   COMPREPLY=( $(IFS="$IFS" \\
                           COMP_LINE="$COMP_LINE" \\
                           COMP_POINT="$COMP_POINT" \\
                           _ARGCOMPLETE_COMP_WORDBREAKS="$COMP_WORDBREAKS" \\
                           _ARGCOMPLETE=1 \\
                           "$1" 8>&1 9>&2 1>/dev/null) )
                   if [[ $? != 0 ]]; then
                           unset COMPREPLY
                   fi
           }
           complete -o nospace -o default -F _py_argcomplete myCommandName

        ..
        """

        # only complete when called from _py_argcomplete()
        if '_ARGCOMPLETE' not in os.environ:
            return
        try:
            import argcomplete
        except:   # pylint: disable=W0702
            LOG.error("TAB-completion, python-argcomplete not installed.")
            sys.exit(1)
        argcomplete.autocomplete(self.parser)

