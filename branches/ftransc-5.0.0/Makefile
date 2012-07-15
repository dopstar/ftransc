MAJOR=`python --version 2> /dev/stdout | awk '{print $$2}' | cut -d+ -f1 | cut -d. -f1`
MINOR=`python --version 2> /dev/stdout | awk '{print $$2}' | cut -d+ -f1 | cut -d. -f2`
install:
	install -m 755 code/ftransc /usr/local/bin
	install -m 755 code/ftransc_qt /usr/local/bin
	mkdir -m 755 /usr/share/doc/ftransc 2> /dev/null || :
	install -m 644 Changelog README AUTHORS Makefile /usr/share/doc/ftransc
	install -m 644 ftransc.1.gz /usr/share/man/man1
	mkdir -m 775 ~/.gnome2/nautilus-scripts/ftransc 2> /dev/null || :
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ MP3
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ WMA
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ AAC
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ OGG
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ FLAC
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ WAV
	ln -s /usr/local/bin/ftransc ~/.gnome2/nautilus-scripts/ftransc/convert\ to\ MPC
	chown ${SUDO_USER}:${SUDO_USER} ~/.gnome2/nautilus-scripts/ftransc/
	mkdir -m 755 /etc/ftransc 2> /dev/null || :
	install -m 644 config/presets.conf /etc/ftransc
	mkdir -p -m 755 /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/utils 2> /dev/null || :
	install -m 644 utils/__init__.py /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/utils
	install -m 644 utils/tagmap.py /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/utils
	install -m 644 utils/convert.py /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/utils
	install -m 644 utils/constants.py /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/utils
	install -m 644 utils/metadata.py /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/utils
	touch /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc/__init__.py
	{ which rhythmbox && cp -r plugins/ftransc /usr/lib/rhythmbox/plugins; } || :

uninstall:
	rm -f /usr/local/bin/ftransc
	rm -f /usr/local/bin/ftransc_qt
	rm -f /usr/share/man/man1/ftransc.1.gz
	rm -r -f /usr/share/doc/ftransc
	rm -r -f ~/.gnome2/nautilus-scripts/ftransc
	rm -r -f /etc/ftransc
	rm -r -f /usr/lib/python$(MAJOR).$(MINOR)/dist-packages/ftransc
	rm -r -f /usr/lib/rhythmbox/plugins/ftransc
