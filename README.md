# Installation Instructions and Usage Tutorial

## What is ftransc

ftransc is a script written in python for the Linux-based operating systems 
for converting audio files across various formats.

## ftransc Dependencies

The dependencies for ftransc include:
 * mutagen, ffmpeg, lame, flac, vorbis-tools, faac, mppenc, PyQt4, cdparanoia, wavpack
 

## Installing ftransc

Install dependencies, including subversion, on Terminal using apt-get as follows.
`sudo apt-get install ffmpeg lame flac faac vorbis-tools`
`sudo apt-get install python-mutagen mppenc subversion`
`sudo apt-get install python-qt4 cdparanoia wavpack`

Installing ftransc from Github:
`git clone https://github.com/dopstar/ftransc.git`
`cd ftransc`
`sudo make uninstall`
`sudo make install`

## Upgrading ftransc
`sudo ftransc --upgrade`

Now you should be able to run ftransc from terminal. You use ftransc to check if the dependencies it needs are installed or not as follows:
`
    ftransc --check
`

For further ftransc help:
`
    man ftransc
`


## How ftransc Works 

ftransc should be invoked/run on Terminal, typically in a syntax like 
*ftransc options files*. ftransc will convert one file at a time and 
followed by the next one, until all input files are converted.
(EDIT: ftransc version 5.0.0 and up supports multiprocessing so ftransc first put all the files to be converted on one single pool (queue). Then processes up to the number of available CPU cores are generated. Each process take a file from the queue and convert it. When it finishes it takes another file from the queue or terminates if the queue is empty.)

Conversion steps:

 - A lockfile corresponding to the input file is created, if it exists already, then the file is skipped because its already locked.
 - Then, the metadata tags are copied from the input file. See [#ftransc_Metadata_Tags this] or a list of supported tags.
 - The input file is converted to the the desired audio format. The input file is not changed in any way. 
 - When the second step, above, has finised successfully, the metadata tags that were copied, if any, are then inserted into the newly created file.
 - A lockfile corresponding to the input file is deleted.
 - If an option to remove the original file is specified and if the conversion process has finished successfully, the original file is deleted.
 - Note: If step any of steps 2 to 4 has caused ftransc to terminate before reaching step 5, a lockfile will still exist. Further attempts to encode a file with a lockfile existing will cause that file to be skipped. To remove the lockfile use the '-u' option.

## ftransc Examples

Example 1 - converting from MP3 to OGG:
`
    ftransc -f ogg filename.mp3
`
The output file name for the above example will be 'filename.ogg'

Example 2 - converting from MP3 to AAC, removing original file on success, using high quality preset:
`
    ftransc -r -q extreme -f aac filename.mp3
`

Example 3 - extract audio content from a video files into the MP3 format, use best quality preset:
`
    ftransc -q insane -f mp3 filename1.flv filename2.avi filename3.mpg filename4.vob ...
`

Example 4 - convert all audio files inside a given folder into WMA format. (This option is not recursive to child-folders)
`
    ftransc -f wma --directory /path/to/folder_name
`

Example 5 - convert all audio audio files (and extract all audio content from video files) inside a given folder recursively including all sub-/child-folders, ftransc should be used with the 'find' command in the pipeline as follows:
`
    find /path/to/folder_name -type f -print0 | xargs -0 ftransc -f aac -q high
`

## ftransc Quality Presets 

ftransc uses quality presets called 'insane', 'extreme', 'high', 'normal', 'low', and 'tiny'. These presets are specified by the '-q' or '--quality' option of ftransc and are defined in the '/etc/ftransc/presets.conf' configuration file. 

The '/etc/ftransc/presets.conf' presets file can be overriden by use of the --presets option and specify the custom presets file to use or, if you know what you are doing, make changes directly on the it.
