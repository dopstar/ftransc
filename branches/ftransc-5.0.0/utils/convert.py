from subprocess import Popen, PIPE

def convert_to_mp3(filename, ext, stderr_out, outdir, preset=None):
    """
    converts input track to MPEG-1 Layer III format (aka MP3)
    """
    outdir = outdir or './'
    cmd1 = ["avconv", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("lame " + preset).split()
    cmd2.extend(["-", outdir + filename + ".mp3"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)

def convert_to_m4a(filename, ext, stderr_out, outdir, preset=None):
    """
    converts input track into MPEG-4 audio format (aka AAC/M4A/MP4)
    """
    outdir = outdir or './'
    cmd1 = ["avconv", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("faac " + preset).split()
    cmd2.extend(["-o", outdir + filename + ".m4a", "/dev/stdin"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)
   
def convert_to_wma(filename, ext, stderr_out, outdir, preset=None):
    """
    converts an input track into the Microsoft ASF format (aka WMA)
    """
    outdir = outdir or './'
    cmd1 = ["avconv", "-y", "-i", filename + ext]
    cmd2 =  preset.split()
    cmd1.extend(cmd2)
    cmd1.append(outdir + filename + ".wma")
    return convert(stderr_out, cmdline1=cmd1)

def convert_to_ogg(filename, ext, stderr_out, outdir, preset=None):
    """
    converts input track into Ogg Vorbis format
    """
    outdir = outdir or './'
    cmd1 = ["avconv", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("oggenc " + preset).split()
    cmd2.extend(["-o", outdir + filename + ".ogg", "/dev/stdin"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)
   
def convert_to_wav(filename, ext, stderr_out, outdir, preset=None):
    """
    decodes a track into WAVE format. This format has no metadata support.
    """
    outdir = outdir or './'
    cmd = ["avconv", "-y", "-i", filename + ext,
            "-f", "wav", outdir + filename + ".wav"]
    return convert(stderr_out, cmdline1=cmd)

def convert_to_flac(filename, ext, stderr_out, outdir, preset=None):
    """
    converts input track into Free Lossless Audio Codec format (aka FLAC).
    """
    outdir = outdir or './'
    status = convert_to_wav(filename, ext, stderr_out, outdir)
    if not status:
        return status
    cmd = ("flac " + preset).split()
    cmd.extend(["-f", "-o", outdir + filename + ".flac", filename + ".wav"])
    return convert(stderr_out, cmdline1=cmd)

def convert_to_mpc(filename, ext, stderr_out, preset=''):
    """
    converts input track into Musepack audio format
    """
    outdir = outdir or './'
    cmd1 = ["avconv", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("mppenc " + preset).split()
    cmd2.extend(["-", outdir + filename + ".mpc"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)

def convert(stderr_out, cmdline1=None, cmdline2=None):
    """
    executes audio conversion pipeline command
    """
    if cmdline1 is not None and cmdline2 is not None:
        p1 = Popen(cmdline1, stdout=PIPE, stderr=stderr_out)
        p2 = Popen(cmdline2, stdin=p1.stdout, stdout=PIPE, stderr=stderr_out)
        p2.communicate()
        return not p2.returncode
    elif cmdline1 is not None and cmdline2 is None:
        p1 = Popen(cmdline1, stdout=PIPE, stderr=stderr_out)
        p1.communicate()
        return not p1.returncode
    else:
        raise SystemExit("Error: unexpected arguments on: convert()")

