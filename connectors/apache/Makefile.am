ACLOCAL_AMFLAGS = -I build

MAINTAINERCLEANFILES = \
	config.log \
        Makefile.in \
        aclocal.m4 \
        compile \
        configure \
        install-sh \
        missing \
        modsec-shared-collections \
        modsec-shared-collections-lock

CLEANFILES = \
	src/*.lo \
	src/*.slo \
	src/*.o \
	src/*.so \
	src/.libs/*.so


CLEANDIRECTORIES = \
	src/.libs


# The wrapper appends the Common SDK sources required by Apache adoption.
all:
	chmod +x build/apxs-wrapper
	build/apxs-wrapper

install-exec-hook: $(pkglib_LTLIBRARIES)
	@APXS@ -i -n mod_security3 ./src/.libs/mod_security3.so


.PHONY: all
