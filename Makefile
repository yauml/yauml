#--------------------------------------------------------
# File: Makefile    Author(s): Alexandre Blondin Massé
#                              Simon Désaulniers
# Date: 2013-09-05
#--------------------------------------------------------

# USER CONFIGURATION -------------------------------
PROGRAM=yauml
INSTALL_DIR=/usr/share/$(PROGRAM)
DOT_TEMPLATE_FILE=$(INSTALL_DIR)/template.dot
BIN=/usr/bin/$(PROGRAM)
DOCDIR=/usr/share/man/man1
BASH_COMPLETION_DIR=/usr/share/bash-completion/completions
# --------------------------------------------------

config: clean
	sed -e "s,template_filename.*=.*'.*',template_filename = '$(DOT_TEMPLATE_FILE)'," bin/process.py \
		>bin/$(PROGRAM)
clean:
	@rm -f bin/$(PROGRAM)

install: ./bin/$(PROGRAM) ./template/template.dot ./doc/$(PROGRAM).1
	@#you don't want to overwrite an existing installation.. Use reinstall
	@if test -d "$(INSTALL_DIR)"; then echo "$(INSTALL_DIR) already exists. Use 'make reinstall'" >&2; \
		exit 1; fi
	@echo "Installing yauml..."
	mkdir -p $(INSTALL_DIR)
	cp template/template.dot $(DOT_TEMPLATE_FILE)
	cp bin/$(PROGRAM) $(BIN)
	chmod 755 $(BIN)
	@echo "Installing documentation..."
	cp doc/$(PROGRAM).1 $(DOCDIR)
	gzip $(DOCDIR)/$(PROGRAM).1
	@echo "Configuring bash completion..."
	@cp ./bin/yauml_completion $(BASH_COMPLETION_DIR)/$(PROGRAM) \
		|| echo "Cannot configure BASH_COMPLETION. See BASH_COMPLETION_DIR variable..." >&2

uninstall:
	@echo "Uninstalling yauml..."
	rm -rf $(BIN) $(INSTALL_DIR) $(DOCDIR)/$(PROGRAM).1.gz $(BASH_COMPLETION_DIR)/$(PROGRAM)

reinstall: uninstall install
