#!/usr/bin/python
NO_TAGS             = False
SILENT              = False  
VERSION             = '5.0.8'
LOGFILE             = '/dev/null'
SUPPORTED_FORMATS   = set(['mp3', 'wma', 'wav', 'ogg', 'flac', 'm4a', 'mpc'])
EXTERNAL_FORMATS    = set(["mpc"])
EXTERNAL_ENCODERS   = {"mpc": "mppenc", "mp3": "lame", "ogg": "oggenc", "m4a": "faac", "flac": "flac"}
