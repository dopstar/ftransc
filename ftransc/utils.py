import os
import optparse

import ftransc
from ftransc.config import AudioPresets
from ftransc.errors import AudioPresetError


def get_audio_presets(audio_format, audio_quality='normal', external_encoder=False):
    """
    Gets audio presets for a given audio format and audio quality from the config file.

    :param audio_format:
    :param audio_quality:
    :param external_encoder:
    :return:
    """

    default_audio_quality = 'normal'
    audio_presets = AudioPresets().as_dict()
    encoder_type = 'ext' if external_encoder else 'int'
    audio_preset_name = '{0}_{1}'.format(audio_format, encoder_type)
    if audio_preset_name not in audio_presets:
        fallback_encoder_type = 'ext' if encoder_type == 'int' else 'int'
        fallback_audio_preset_name = '{0}_{1}'.format(audio_format, fallback_encoder_type)
        if fallback_audio_preset_name not in audio_presets:
            raise AudioPresetError("The audio format [%s] has no audio preset." % audio_format)
        audio_preset_name = fallback_audio_preset_name

    selected_audio_preset = audio_presets[audio_preset_name]
    if audio_quality not in selected_audio_preset:
        audio_quality = default_audio_quality
    return selected_audio_preset[audio_quality]


def parse_args():
    parser = optparse.OptionParser(usage="%prog [options] [files]", version=ftransc.__version__)
    parser.add_option('-f', '--format', type=str, default='mp3',
                      help='audio format to convert to')
    parser.add_option('-q', '--quality', type=str, default='normal',
                      help='audio quality preset')
    parser.add_option('-c', '--check', dest='check', action='store_true',
                      help='check dependencies')
    parser.add_option('-r', '--remove', dest='remove', action='store_true',
                      help='remove original file after converting successfully')
    parser.add_option('-d', '--decode', dest='decode', action='store_true',
                      help='decode file .wav format')
    parser.add_option('-w', '--over', dest='overwrite', action='store_true',
                      help='overwrite destination file if it exists already')
    parser.add_option('-u', '--unlock', dest='unlock', action='store_true',
                      help='unlock a locked file and convert')
    parser.add_option('--directory', dest="walk", type=str,
                      help='convert all files inside the given directory')
    parser.add_option('-o', '--outdir',
                      help='Put converted file into specified folder')
    parser.add_option('--cd', '--cdrip', dest='cdrip', action='store_true',
                      default=False, help='rip Compact Disc (CD) digital audio')
    parser.add_option('--list-formats', dest='list_formats', action='store_true', default=False,
                      help='Show available audio formats to convert to')
    parser.add_option('-p', '--processes', dest='num_procs', default=0, type=int,
                      help='Use the specified number of parallel processes. CPU count is the maximum.')
    parser.add_option('-x', '--ext-encoder', action='store_true', dest='external_encoder',
                      help='Use external encoder (if available)')
    parser.add_option('--debug', action='store_true', help='Show debug messages.')
    parser.add_option('-s', '--silent', action='store_true', help='Be very less verbose.')
    return parser.parse_args()


def rip_compact_disc():
    base_folder = os.path.expanduser('~/ftransc/ripped_albums')
    os.system('mkdir -p %s' % base_folder)
    walker = os.walk(base_folder)
    parent_folder, child_folders, child_files = next(walker)
    dest_folder = 'CD-%d' % (len(child_folders) + 1)
    os.system('mkdir -p %s/%s' % (base_folder, dest_folder))
    os.chdir('%s/%s' % (base_folder, dest_folder))
    print('Ripping Compact Disc (CD)...')
    os.system('cdparanoia -B >/dev/null 2>&1')
    print('Finished ripping CD')
    walker = os.walk('%s/%s' % (base_folder, dest_folder))
    parent_folder, child_folders, child_files = next(walker)
    return child_files
