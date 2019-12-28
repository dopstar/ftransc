import os
import logging
import subprocess

import pafy
import blessings

from ftransc.constants import (
    EXTERNAL_FORMATS,
    EXTERNAL_ENCODERS,
    EXTERNAL_ENCODER_OUTPUT_OPT,
    FFMPEG_AVCONV,
)

import ftransc.utils


term = blessings.Terminal()
logger = logging.getLogger(__name__)


def transcode(
    input_file_name,
    output_audio_format,
    output_folder="./",
    audio_preset=None,
    external_encoder=False,
):
    output_folder = output_folder or "./"
    audio_preset = audio_preset or ""
    output_audio_format = output_audio_format.lower()
    base_input_file_name, input_ext = os.path.splitext(input_file_name)
    output_file_name = (
        output_folder
        + "/"
        + os.path.basename(base_input_file_name)
        + "."
        + output_audio_format
    )

    encoder = _get_external_encoder(output_audio_format)
    cmdline = [FFMPEG_AVCONV, "-y", "-i", input_file_name]

    if encoder and (external_encoder or output_audio_format in EXTERNAL_FORMATS):
        output_opt = EXTERNAL_ENCODER_OUTPUT_OPT.get(encoder, "")
        cmdline += ["-f", "wav", "/dev/stdout"]
        cmdline2 = [encoder] + audio_preset.split() + ["-"]
        if output_opt:
            cmdline2 += [output_opt]
        cmdline2 += [output_file_name]

        logger.debug(
            "Command-Line: `{term.green}{0} | {1}{term.normal}`".format(
                " ".join(cmdline), " ".join(cmdline2), term=term
            )
        )
        pipeline1 = subprocess.Popen(
            cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pipeline = subprocess.Popen(
            cmdline2,
            stdin=pipeline1.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    else:
        cmdline += audio_preset.split() + [output_file_name]
        logger.debug(
            "Command-Line: `{term.green}{0}{term.normal}`".format(
                " ".join(cmdline), term=term
            )
        )
        pipeline = subprocess.Popen(
            cmdline, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

    std_out, std_err = pipeline.communicate()
    if std_out:
        logger.debug(std_out)
    if std_err:
        logger.debug(std_err)
    return pipeline.returncode == 0


def _get_external_encoder(audio_format):
    return EXTERNAL_ENCODERS.get(audio_format)


def download_from_youtube(url):
    logger.debug("Fetching audio from [{0}]".format(url))
    stream = pafy.new(url).getbestaudio()
    logger.debug("Found audio/video stream:\n{0}".format(stream))
    filename = ftransc.utils.get_safe_filename(stream.title)
    return stream.download(filepath=filename, quiet=True)


def download_from_youtube_playlist(playlist_url, output_stream_queue=None):
    playlist = pafy.get_playlist(playlist_url)
    files = []
    if playlist and playlist.get("items"):
        cwd = os.getcwd()
        folder_name = os.path.join(
            cwd, ftransc.utils.get_safe_filename(playlist["title"])
        )
        os.mkdir(folder_name)
        os.chdir(folder_name)
        for item in playlist["items"]:
            try:
                stream = item["pafy"].getbestaudio()
            except KeyError:
                continue
            filename = ftransc.utils.get_safe_filename(stream.title)
            output_filename = os.path.join(
                folder_name, stream.download(filepath=filename, quiet=True)
            )
            if output_stream_queue is not None:
                output_stream_queue.put(output_filename)
            else:
                files.append(output_filename)
        os.chdir(cwd)
    return files
