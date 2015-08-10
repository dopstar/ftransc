#!/usr/bin/python
from subprocess import Popen, PIPE

def determine_ffmpeg_utility():
    for util in ["avconv", "ffmpeg"]:
        found = Popen(["which", util], stdout=PIPE).communicate()[0].strip()
        if found:
            return util
    raise SystemExit("ffmpeg/avconv not installed")



NO_TAGS             = False
SILENT              = False
VERSION             = open('/usr/share/doc/ftransc/version').read().strip()
LOGFILE             = '/dev/null'
SUPPORTED_FORMATS   = {'mp3', 'wma', 'wav', 'ogg', 'flac', 'm4a', 'mpc', 'wv', 'avi'}
EXTERNAL_FORMATS    = {"mpc", "wv"}
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
FFMPEG_AVCONV = determine_ffmpeg_utility()
DEPENDENCIES = {
    'cdparanoia' : [],
    FFMPEG_AVCONV: list(SUPPORTED_FORMATS),
}
for audio_format, encoder in EXTERNAL_ENCODERS.iteritems():
    DEPENDENCIES[encoder] = [audio_format]
