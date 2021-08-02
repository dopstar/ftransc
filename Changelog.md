#### 7.0.2 - 30 Dec 2020
 - added --force-root option to force running as root

#### 7.0.0 - XX XXX 20XX
- dropped python 2 support. only supporting python 3.6 and higher

#### 6.0.9 - 07 April 2017
 - Performance improvements when transcoding files from youtube playlists

#### 6.0.6 - 05 Apr 2017
 - Adding youtube playlist support
 
#### 6.0.0 - 01 Aug 2016
 - New reworked version. Not backward compatible.
 
#### 5.1.7 - 26 Aug 2015
 - fixed rhythmbox plugin

#### 5.1.6 - 10 Aug 2015
 - installing dependencies via make install

#### 5.1.5 - 10 Aug 2015
 - added title and artist columns on ftransc_qt

#### 5.1.4 - 10 Aug 2015
 - code cleanup.

#### 5.1.3 - 09 Aug 2015
 - fixed working out ffmpeg/avconv utility

#### 5.1.1 - 19 Nov 2013
 - fixed broken nautilus scripts
 - added convert to avi video (experimental)

#### 5.1.0 - 17 Feb 2013
 - added the -x option to be able to use external encoder if it is
	available (eg using FFmpeg to decode and pipe to lame to encode instead of
	using ffmpeg to decode and encode via libmp3lame)

#### 5.0.9 - 02 Feb 2013
 - added WavPack support

#### 5.0.8 - 13 Jan 2013
 - using FFmpeg to encode any supported format where possible

#### 5.0.7 - 04 Nov 2012
 - Added cover art insertion support to flac files

#### 5.0.6 - 03 Nov 2012
 - Fixed bug when disk number is present in the metadata which caused all
	metadata to be dropped
 - Added support for extraction of metadata from .3gp files

#### 5.0.5 - 28 Oct 2012
 - Merged the CoverTag class into MetaTag class
 - Fixed bug when the default 'normal' preset is not in the presets file
 - Generating fewer consumer processes when there are fewer files than CPU
	count

#### 5.0.4 - 19 Aug 2012
 - added --list-formats option
 - added --processes/-p option

#### 5.0.3 - 23 Jul 2012
 - moved away from ffmpeg to avconv

#### 5.0.2 - 15 Jul 2012
 - added rhythmbox plugin
 - added CD ripping via cdparanoia

#### 5.0.1 - 15 Jul 2012
 - added multithreading.

#### 4.3.3 - 25 Mar 2012
 - fixed fatal KeyError when converting .aac and .mp4 files

#### 4.3.2 - 10 Mar 2012
 - added album artist, disk number, and comment metadata tags to some
	formats
 - added output folder feature to fransc GUI, ftransc_qt

#### 4.3.1 - 20 Feb 2012
 - added lyrics support for mp3, m4a and wma formats

#### 4.3.0 - 20 Feb 2012
 - added the -o/--outdir option
 - fixed potential bug with --upgrade
 - refined parsing of playlist files

#### 4.2.9 - 13 Jan 2012
 - added ability to convert audio files specified in PLS playlist file and
	XSPF playlist file via the --pls option and the --xspf option, resp.

#### 4.2.8 - 10 Jan 2012
 - added ability to convert audio files specified in the M3U playlist file
	via the --m3u option

#### 4.2.7 - 06 Jan 2012
 - added album art support when converting FROM ogg/flac TO mp3/m4a

#### 4.2.6 - 05 Jan 2012
 - code cleanup
 - added album art support when converting from mp3 to m4a and vice versa

#### 4.2.5 - 19 Dec 2011
 - code cleanup
 - proper message when --upgrade option is used while offline

#### 4.2.4 - 19 Dec 2011
 - dropping checking mutagen version against version 1.17 since easy=True
	option of File() has been dropped.
 - fixed fatal errors when mutagen is not installed. instead, metadata
	support is dropped.

#### 4.2.3 - 19 Dec 2011
 - code cleanup

#### 4.2.2 - 19 Dec 2011
 - code cleanup

#### 4.2.1 - 18 Dec 2011
 - removed the easy=True dependency on mutagen's File
 - fixed missing 'normal' ogg vorbis preset on configuration file

#### 4.2.0 - 03 Dec 2011
 - removed quality presets from code and placed them in a separate file
	/etc/ftransc/presets.
 - added new option to specify a custom preset file: --presets

#### 4.1.9 - 03 Dec 2011
 - reverted back metadata extraction method to earlier revision.

#### 4.1.8 - 24 Nov 2011
 - Adding logging for executing as nautilus script

#### 4.1.7 - 20 Nov 2011
 - Adding the options: -s/--silent, -l/--log, --debug, --notify
 - Fixed metadata issue with the year tag when converting from FLAC format.

#### 4.1.6 - 20 Nov 2011
 - Adding mpc format support on ftransc nautilus scripts.

#### 4.1.5 - 20 Nov 2011
 - extracting .wmv video metadata when extracting audio conntent from .wmv
	video.

#### 4.1.4 - 20 Nov 2011
 - fixed issue of not dropping support to encode to some format when
	the necessary dependency is not installed.

#### 4.1.3 - 13 Nov 2011
 - minor changes.

#### 4.1.1 - 16 Oct 2011
 - added musepack audio format support.
 - added the -n / --no-tags option.

#### 4.1.0 - 16 Oct 2011
 - added ftransc GUI, 'ftransc_qt'.
 - Explicitly drop support for python-mutagen versions older than 1.17.

#### 4.0.6 - 30 Sep 2011
 - now using os.path.splitext() instead of a custom built function.
 - printing summary statistics of time taken to encode all files and
	average time taken per file.
 - added 'nautilus scripts' functionality.

#### 4.0.5 - 25 Sep 2011
 - added the --upgrade option.

#### 4.0.4 - 25 Sep 2011
 - added notify-send summary notification
 - fixed the issue with left over temporary .wav files when converting to
	FLAC format.

#### 4.0.3 - 17 Apr 2011
 - no need to 'cd' to folder first before running ftransc.
 - /tmp/ftransc.log is not created anymore.
 - order of input files is sorted
 - prints out duration of conversion in seconds

#### 4.0.1 - 05 Apr 2011
 - disable support of functionality when its dependency is not installed.
	this prevents crashes like trying to convert with an unavailable encoder.

#### 4.0.0 - 22 Mar 2011
 - Written in python, thus, 'ftransc' & 'fmetadata' merged.
 - added the 'extreme' quality preset.
 - added directory walking.
 - transcode via wav option removed.
 - added a feature to unlock prelocked files.

#### 3.2.3 - 03 Jan 2011 # unreleased
 - FLAC support: encode + decode + extract metadata + add metadata
 - polished logging.
 - polished code style
 - added the 'tiny' quality preset.

#### 3.2.2 - 24 Dec 2010 # now available at code.google.com/p/ftransc
 - fmetadata python script.
 - decode to wav
 - trascode via wav and direct transcode
 - extract audio content from video files
 - added uninstallation option.
 - removed asftags, asfedit and aactags
 - removed dependency on mid3v2, id3 and vorbiscomment

#### 3.2.1 - 22 Aug 2010
 - Support for non-ASCII Unicode characters via UTF-8.
 - Installation via a Makefile.
 - Option to check dependencies.
 - Overwriting disabled by default, with option to enable.
 - If source and destination files are the same, do not proceed.

#### 3.2 - 16 Feb 2010
 - corrected man page installation path.

#### 3.1 - 15 Jan 2010
 - log file not created when usage is displayed.
 - usage modified.
 - print usage when no args are present.
 - progress status message modified to highlight file being encoded.

#### 3.0 - 24 Oct 2009
 - using FFmpeg to decode any type of input audio file.

#### 2.5 - 20 Oct 2009
 - Removed decoding to WAV format first because temporarily consumes
	a lot of space and is slower.
