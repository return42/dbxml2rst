# -*- coding: utf-8; mode: makefile-gmake -*-

# This is a python 3 project (no python 2 support!).
PYTHON   = python3
PIP      = pip3

include utils/makefile.include
include utils/makefile.python
include utils/makefile.sphinx

GIT_URL   = https://github.com/return42/dbxml2rst.git
PYOBJECTS = dbxml2rst

all: clean pylint pytest build docs

PHONY += help
help:
	@echo  '  docs		- build documentation'
	@echo  '  clean		- remove most generated files'
	@echo  '  rqmts		- info about build requirements'
	@echo  ''
	@$(MAKE) -s -f utils/makefile.include make-help
	@echo  ''
	@$(MAKE) -s -f utils/makefile.python python-help
	@echo  ''
	@$(MAKE) -s -f utils/makefile.sphinx docs-help

PHONY += docs
docs:  sphinx-doc
	$(call cmd,sphinx,html,docs,docs)

PHONY += clean
clean: pyclean docs-clean
	$(call cmd,common_clean)

PHONY += help-rqmts
rqmts: msg-sphinx-doc msg-pylint-exe msg-pip-exe

.PHONY: $(PHONY)

