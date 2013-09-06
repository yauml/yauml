#--------------------------------------------------------
# File: Makefile    Author(s): Alexandre Blondin Massé
#                              Simon Désaulniers
# Date: 2013-09-05
#--------------------------------------------------------

#VARIABLES
DOT_TEMPLATE_FILE='/usr/share/yauml/template.dot'

all: config install

config:
	#TODO: config has to
	# - edit bin/process.py to configure variables such as `template_filename`.
install:
	#TODO
	# - create directories:
	#   - /usr/share/yauml
	# - Place the files:
	#   - template/template.dot -> /usr/share/yauml/template.dot
	#   - bin/process.py -> /usr/bin/yauml
uninstall:
	#TODO
	# inverse the install process.
