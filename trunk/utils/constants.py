#!/usr/bin/python
NO_TAGS             = False
SILENT              = False  
VERSION             = '5.1.0'
LOGFILE             = '/dev/null'
SUPPORTED_FORMATS   = set(['mp3', 'wma', 'wav', 'ogg', 'flac', 'm4a', 'mpc', 'wv', 'avi'])
EXTERNAL_FORMATS    = set(["mpc", "wv"])
INTERNAL_FORMATS    = SUPPORTED_FORMATS - EXTERNAL_FORMATS
EXTERNAL_ENCODERS   = {
    "mpc"   : "mppenc",
    "wv"    : "wavpack",
    "mp3"   : "lame",
    "ogg"   : "oggenc",
    "m4a"   : "faac",
    "flac"  : "flac",
}
EXTERNAL_ENCODER_OUTPUT_OPT = {
    'mppenc'    : '',
    'lame'      : '',
    'faac'      : '-o',
    'flac'      : '-o',
    'oggenc'    : '-o',
    'wavpack'   : '-o',
}

DEPENDENCIES = {
    'cdparanoia'        : [],
    'ffmpeg'            : list(SUPPORTED_FORMATS),
    }
for audio_format, encoder in EXTERNAL_ENCODERS.iteritems():
    DEPENDENCIES[encoder] = [audio_format]
