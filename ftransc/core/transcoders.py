import os
import subprocess


from ftransc.constants import (
    EXTERNAL_FORMATS,
    EXTERNAL_ENCODERS,
    EXTERNAL_ENCODER_OUTPUT_OPT,
    FFMPEG_AVCONV,
    LOGFILE
)


def transcode(input_file_name, output_audio_format, output_folder='./', audio_preset=None, external_encoder=False):
    with open(LOGFILE, 'w') as log_fd:
        output_folder = output_folder or './'
        audio_preset = audio_preset or ''
        output_audio_format = output_audio_format.lower()
        base_input_file_name, input_ext = os.path.splitext(input_file_name)
        output_file_name = output_folder + '/' + base_input_file_name + '.' + output_audio_format

        encoder = _get_external_encoder(output_audio_format)
        cmdline = [FFMPEG_AVCONV, '-y', '-i', input_file_name]

        if encoder and (external_encoder or output_audio_format in EXTERNAL_FORMATS):
            output_opt = EXTERNAL_ENCODER_OUTPUT_OPT.get(encoder, '')
            cmdline += ["-f", "wav", "/dev/stdout"]
            cmdline2 = [encoder] + audio_preset.split() + ['-']
            if output_opt:
                cmdline2 += [output_opt]
            cmdline2 += [output_file_name]

            pipeline1 = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=log_fd)
            pipeline = subprocess.Popen(cmdline2, stdin=pipeline1.stdout, stdout=subprocess.PIPE, stderr=log_fd)
        else:
            cmdline += audio_preset.split() + [output_file_name]
            pipeline = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=log_fd)

        pipeline.communicate()
        return pipeline.returncode == 0


def _get_external_encoder(audio_format):
    return EXTERNAL_ENCODERS.get(audio_format)
