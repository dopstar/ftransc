install:
	install -m 755 code/ftransc /usr/local/bin
	install -m 755 code/fmetadata /usr/local/bin
	mkdir -m 755 /usr/share/doc/ftransc 2> /dev/null
	install -m 644 Changelog README AUTHORS Makefile /usr/share/doc/ftransc
	install -m 644 ftransc.1.gz /usr/share/man/man1
uninstall:
	rm -f -v /usr/local/bin/ftransc 
	rm -f -v /usr/local/bin/fmetadata
	rm -f -v /usr/share/man/man1/ftransc.1.gz
	rm -r -f -v /usr/share/doc/ftransc
