import os
from subprocess import Popen, PIPE
from ftransc.utils.constants import EXTERNAL_FORMATS, EXTERNAL_ENCODERS

def convert(infilename, audioformat, outputfolder=None, audiopresets=None, logfile=None):
    if outputfolder in (None, ''):
        outputfolder = "./"
    if logfile is None:
        logfile = open("/dev/null", 'w')

    audioformat = audioformat.lower()
    basefilename, ext = os.path.splitext(infilename)
    outfilename = outputfolder + '/' + basefilename + '.' + audioformat
    utility = _get_external_encoder(audioformat)

    encoder = _determine_ffmpeg_utility()
    cmdline = [encoder, '-y', '-i']
    cmdline += [infilename]

    if utility not in (None, ''):
        cmdline += "-f wav /dev/stdout".split()
        cmdline2 = [utility] + audiopresets.split() + ["-", outfilename]
        pipeline1 = Popen(cmdline, stdout=PIPE, stderr=logfile)
        pipeline = Popen(cmdline2, stdin=pipeline1.stdout,stdout=PIPE, stderr=logfile)
    else:
        if audiopresets is not None:
            cmdline += audiopresets.split()
        cmdline += [outfilename]
        pipeline = Popen(cmdline, stdout=PIPE, stderr=logfile)

    pipeline.communicate()
    return pipeline.returncode == 0

def _get_external_encoder(audioformat):
    if audioformat in EXTERNAL_FORMATS:
        return EXTERNAL_ENCODERS.get(audioformat)

def _determine_ffmpeg_utility():
    for util in ["avconv", "ffmpeg"]:
        found = Popen(["which", util], stdout=PIPE).communicate()[0].strip()
        if found:
            return util

    raise SystemExit("ffmpeg/avconv not installed")