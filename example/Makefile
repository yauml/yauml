#--------------------------------------------------------
# File: Makefile    Author(s): Alexandre Blondin-Massé
# Date: 2013-09-09	       Simon Désaulniers
#--------------------------------------------------------
# Makefile exemple for yauml
#--------------------------------------------------------

PROCESS=../bin/process.py  # if yauml is installed, simply write PROCESS=yauml 
FORMAT=pdf

all: diagram

diagram: diagram.yaml
	python $(PROCESS) diagram.yaml | dot -T$(FORMAT) -o diagram.$(FORMAT)
