#!/usr/bin/make -f
## -*- makefile -*- 
##
SHELL:=/bin/sh
PYTHON:=python2.7

clean:
	find ./ -type f -name "*.py[co]" | xargs rm -f -
	find ./ -type d -name __pycache__ -delete
build: clean
	$(PYTHON) setup.py build
all: build

