DEST_DIR=`python -c "import sysconfig; print sysconfig.get_path('platlib')"`
install:
	sudo apt-get install libav-tools lame flac faac vorbis-tools python-mutagen mppenc git python-qt4 cdparanoia wavpack libglib2.0-dev libglib2.0-0 gir1.2-gconf-2.0 
	install -m 755 src/ftransc.py /usr/local/bin/ftransc
	install -m 755 src/ftransc_qt.py /usr/local/bin/ftransc_qt
	mkdir -p -m 755 /usr/share/doc/ftransc 2> /dev/null || :
	install -m 644 Changelog README.md AUTHORS Makefile src/version /usr/share/doc/ftransc
	install -m 644 ftransc.1.gz /usr/share/man/man1
	mkdir -p -m 775 ~/.local/share/nautilus/scripts/ftransc 2> /dev/null || :
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ MP3
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ WMA
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ AAC
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ OGG
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ FLAC
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ WAV
	ln -s /usr/local/bin/ftransc ~/.local/share/nautilus/scripts/ftransc/convert\ to\ MPC
	chown ${SUDO_USER}:${SUDO_USER} ~/.local/share/nautilus/scripts/ftransc/
	mkdir -m 755 /etc/ftransc 2> /dev/null || :
	install -m 644 src/conf/presets.conf /etc/ftransc
	mkdir -p -m 755 $(DEST_DIR)/ftransc/utils 2> /dev/null || :
	install -m 644 src/lib/utils/__init__.py  $(DEST_DIR)/ftransc/utils
	install -m 644 src/lib/utils/tagmap.py    $(DEST_DIR)/ftransc/utils
	install -m 644 src/lib/utils/convert.py   $(DEST_DIR)/ftransc/utils
	install -m 644 src/lib/utils/constants.py $(DEST_DIR)/ftransc/utils
	install -m 644 src/lib/utils/metadata.py  $(DEST_DIR)/ftransc/utils
	touch $(DEST_DIR)/ftransc/__init__.py
	{ which rhythmbox && cp -r src/lib/plugins/ftransc /usr/lib/rhythmbox/plugins; } || :

uninstall:
	rm -f /usr/local/bin/ftransc
	rm -f /usr/local/bin/ftransc_qt
	rm -f /usr/share/man/man1/ftransc.1.gz
	rm -r -f /usr/share/doc/ftransc
	rm -r -f ~/.local/share/nautilus/scripts/ftransc
	rm -r -f /etc/ftransc
	rm -r -f $(DEST_DIR)/ftransc
	rm -r -f /usr/lib/rhythmbox/plugins/ftransc
