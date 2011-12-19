from subprocess import Popen, PIPE

def convert_to_mp3(filename, ext, stderr_out, preset=None):
    """
    converts input track to MPEG-1 Layer III format (aka MP3)
    """
    cmd1 = ["ffmpeg", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("lame " + preset).split()
    cmd2.extend(["-", "./" + filename + ".mp3"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)

def convert_to_m4a(filename, ext, stderr_out, preset=None):
    """
    converts input track into MPEG-4 audio format (aka AAC/M4A/MP4)
    """
    cmd1 = ["ffmpeg", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("faac " + preset).split()
    cmd2.extend(["-o", "./" + filename + ".m4a", "/dev/stdin"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)
   
def convert_to_wma(filename, ext, stderr_out, preset=None):
    """
    converts an input track into the Microsoft ASF format (aka WMA)
    """
    cmd1 = ["ffmpeg", "-y", "-i", filename + ext]
    cmd2 =  preset.split()
    cmd1.extend(cmd2)
    cmd1.append("./" + filename + ".wma")
    return convert(stderr_out, cmdline1=cmd1)

def convert_to_ogg(filename, ext, stderr_out, preset=None):
    """
    converts input track into Ogg Vorbis format
    """
    cmd1 = ["ffmpeg", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("oggenc " + preset).split()
    cmd2.extend(["-o", "./" + filename + ".ogg", "/dev/stdin"])
    return convert(stderr_out, cmdline1=cmd1, cmdline2=cmd2)
   
def convert_to_wav(filename, ext, stderr_out, preset=None):
    """
    decodes a track into WAVE format. This format has no metadata support.
    """
    cmd = ["ffmpeg", "-y", "-i", filename + ext, 
            "-f", "wav", "./" + filename + ".wav"]
    return convert(stderr_out, cmdline1=cmd)

def convert_to_flac(filename, ext, stderr_out, preset=None):
    """
    converts input track into Free Lossless Audio Codec format (aka FLAC).
    """
    status = convert_to_wav(filename, ext, stderr_out)
    if not status:
        return status
    cmd = ("flac " + preset).split()
    cmd.extend(["-f", "-o", "./" + filename + ".flac", filename + ".wav"])
    return convert(stderr_out, cmdline1=cmd)

def convert_to_mpc(filename, ext, stderr_out, preset=''):
    """
    converts input track into Musepack audio format
    """
    cmd1 = ["ffmpeg", "-y", "-i", filename + ext, "-f", "wav", "/dev/stdout"]
    cmd2 = ("mppenc " + preset).split()
    cmd2.extend(["-", "./" + filename + ".mpc"])
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

