# -*- coding: utf-8; mode: makefile-gmake -*-

# This is a python 3 project (no python 2 support!).
PYTHON   = python3
PIP      = pip3
PYLINT   = pylint3

include utils/makefile.include
include utils/makefile.python
include utils/makefile.sphinx

GIT_URL   = https://github.com/return42/dbxml2rst.git
PYOBJECTS = dbxml2rst

all: clean pylint pytest build docs

PHONY += help
help:
	@echo  '  docs		- build documentation'
	@echo  '  [un]install	- developer un-/install'
	@echo  '  haskell-stack	- up-to-date install of haskell stack (needs sudo privileges)'
	@echo  '  pandoc-build	- developer install of pandoc'
	@echo  '  clean		- remove most generated files'
	@echo  '  rqmts		- info about build requirements'
	@echo  ''
	@$(MAKE) -s -f utils/makefile.include make-help
	@echo  ''
	@$(MAKE) -s -f utils/makefile.python python-help
	@echo  ''
	@$(MAKE) -s -f utils/makefile.sphinx docs-help

PHONY += haskell-stack
haskell-stack:
	curl -sSL https://get.haskellstack.org/ | sh

PHONY += pandoc-build
pandoc-build:
	mkdir -p pandoc-build
	cd pandoc-build ; [ -d "pandoc-types" ]    || git clone https://github.com/jgm/pandoc-types
	cd pandoc-build ; [ -d "texmath" ]         || git clone https://github.com/jgm/texmath
	cd pandoc-build ; [ -d "pandoc-citeproc" ] || git clone https://github.com/jgm/pandoc-citeproc
	cd pandoc-build ; [ -d "pandoc" ]          || git clone https://github.com/jgm/pandoc
	cd pandoc-build ; [ -d "cmark-hs" ]        || git clone https://github.com/jgm/cmark-hs
	cd pandoc-build ; [ -d "zip-archive" ]     || git clone https://github.com/jgm/zip-archive
	cd pandoc-build/pandoc ; git submodule update --init
	cd pandoc-build/pandoc ; stack install --install-ghc --stack-yaml stack.full.yaml

PHONY += install
install: pyinstall

PHONY += uninstall
uninstall: pyuninstall

PHONY += docs
docs:  sphinx-doc
	$(call cmd,sphinx,html,docs,docs)


quiet_cmd_clean = CLEAN     $@
      cmd_clean = \
	rm -rf cache ;\

PHONY += clean clean-cache
clean: pyclean docs-clean clean-cache
	$(call cmd,common_clean)

clean-cache:
	$(call cmd,clean)

PHONY += help-rqmts
rqmts: msg-sphinx-doc msg-pylint-exe msg-pip-exe

.PHONY: $(PHONY)

