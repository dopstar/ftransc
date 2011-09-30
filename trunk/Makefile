install:
	install -m 755 code/ftransc /usr/local/bin
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
	chown ${SUDO_USER}:${SUDO_USER} ~/.gnome2/nautilus-scripts/ftransc/
uninstall:
	rm -f /usr/local/bin/ftransc 
	rm -f /usr/share/man/man1/ftransc.1.gz
	rm -r -f /usr/share/doc/ftransc
	rm -r -f ~/.gnome2/nautilus-scripts/ftransc
