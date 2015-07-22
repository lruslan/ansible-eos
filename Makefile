#!/usr/bin/make
# WARN: gmake syntax
########################################################
# Makefile for ansible-eos
#
# useful targets:
#	make flake8 -- flake8 checkes
#	make tests -- run all of the tests
#	make clean -- clean distutils
#
########################################################
# variable section

NAME = "ansible-eos"

PYTHON=python
BUILDER=scripts/build_modules.py
COPYCMD=scripts/copy_modules.py

VERSION := $(shell cat VERSION)

########################################################

all: clean flake8 build tests

flake8:
	flake8 --ignore=E265,E302,E303,F401,F403 library/ test/ common/

clean:
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete

tests: clean
	nosetests -v 

build: copy
	$(PYTHON) $(BUILDER)

copy:
	$(PYTHON) $(COPYCMD)


