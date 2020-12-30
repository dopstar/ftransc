import os
import re
import pathlib
import optparse
import multiprocessing

import urllib.parse

import ftransc
from ftransc.config import AudioPresets
from ftransc.errors import AudioPresetError


def get_audio_presets(audio_format, audio_quality="normal", external_encoder=False):
    """
    Gets audio presets for a given audio format and audio quality from the config file.

    :param audio_format:
    :param audio_quality:
    :param external_encoder:
    :return:
    """

    default_audio_quality = "normal"
    audio_presets = AudioPresets().as_dict()
    encoder_type = "ext" if external_encoder else "int"
    audio_preset_name = "{0}_{1}".format(audio_format, encoder_type)
    if audio_preset_name not in audio_presets:
        fallback_encoder_type = "ext" if encoder_type == "int" else "int"
        fallback_audio_preset_name = "{0}_{1}".format(
            audio_format, fallback_encoder_type
        )
        if fallback_audio_preset_name not in audio_presets:
            raise AudioPresetError(
                "The audio format [%s] has no audio preset." % audio_format
            )
        audio_preset_name = fallback_audio_preset_name

    selected_audio_preset = audio_presets[audio_preset_name]
    if audio_quality not in selected_audio_preset:
        audio_quality = default_audio_quality
    return selected_audio_preset[audio_quality]


def get_audio_formats():
    audio_presets = AudioPresets().as_dict()
    return sorted(list({key.split("_")[0].strip() for key in audio_presets}))


def parse_args(version=ftransc.__version__):
    parser = optparse.OptionParser(usage="%prog [options] [files]", version=version)
    parser.add_option(
        "-f", "--format", type=str, default="mp3", help="audio format to convert to"
    )
    parser.add_option(
        "-q", "--quality", type=str, default="normal", help="audio quality preset"
    )
    parser.add_option(
        "-c", "--check", dest="check", action="store_true", help="check dependencies"
    )
    parser.add_option(
        "-r",
        "--remove",
        dest="remove",
        action="store_true",
        help="remove original file after converting successfully",
    )
    parser.add_option(
        "-d",
        "--decode",
        dest="decode",
        action="store_true",
        help="decode file .wav format",
    )
    parser.add_option(
        "-w",
        "--over",
        dest="overwrite",
        action="store_true",
        help="overwrite destination file if it exists already",
    )
    parser.add_option(
        "-u",
        "--unlock",
        dest="unlock",
        action="store_true",
        help="unlock a locked file and convert",
    )
    parser.add_option(
        "--directory",
        dest="walk",
        type=str,
        help="convert all files inside the given directory",
    )
    parser.add_option("-o", "--outdir", help="Put converted file into specified folder")
    parser.add_option(
        "--cd",
        "--cdrip",
        dest="cdrip",
        action="store_true",
        default=False,
        help="rip Compact Disc (CD) digital audio",
    )
    parser.add_option(
        "--list-formats",
        dest="list_formats",
        action="store_true",
        default=False,
        help="Show available audio formats to convert to",
    )
    parser.add_option(
        "-p",
        "--processes",
        dest="num_procs",
        default=0,
        type=int,
        help="Use the specified number of parallel processes. CPU count is the maximum.",
    )
    parser.add_option(
        "-x",
        "--ext-encoder",
        action="store_true",
        dest="external_encoder",
        help="Use external encoder (if available)",
    )
    parser.add_option("--debug", action="store_true", help="Show debug messages.")
    parser.add_option(
        "-s", "--silent", action="store_true", help="Be very less verbose."
    )
    parser.add_option(
        "--force-root",
        action="store_true",
        dest="force_root",
        help="Take the risk and enable running ftransc as root user"
    )
    return parser.parse_args()


def rip_compact_disc():
    base_dir = pathlib.Path("~/ftransc/ripped_albums").expanduser().absolute()
    base_dir.mkdir(parents=True, exist_ok=True)
    _, child_folders, _ = next(os.walk(base_dir))

    child_dir = base_dir.joinpath(f"CD-{len(child_folders) + 1}")
    child_dir.mkdir(parents=True, exist_ok=True)

    os.chdir(child_dir)
    print("Ripping Compact Disc (CD)...")
    os.system("cdparanoia -B >/dev/null 2>&1")
    print("Finished ripping CD")

    _, _, child_files = next(os.walk(child_dir))
    return child_files


def is_url(url):
    return (
        url
        and not os.path.isfile(url)
        and isinstance(url, str)
        and (url.startswith("http://") or url.startswith("https://"))
    )


def is_youtube_playlist(url):
    return is_url(url) and urllib.parse.urlparse(url).path.startswith("/playlist")


def get_safe_filename(filename):
    if not filename:
        return filename
    regex = re.compile(r'[\s)(\]\[}{><!#&%*~`|\\/"\']+', re.DOTALL)
    return regex.sub(r"_", filename.strip())


def has_youtube_playlist(files):
    return bool(files) and any(is_youtube_playlist(filename) for filename in files)


def determine_number_of_workers(files, desired_number_of_workers):
    num_processes = multiprocessing.cpu_count()
    number_of_files = len(files)
    contains_youtube_playlist = has_youtube_playlist(files)
    if desired_number_of_workers > 0:
        if contains_youtube_playlist:
            return desired_number_of_workers
        return min([desired_number_of_workers, number_of_files])
    if number_of_files < num_processes:
        if has_youtube_playlist(files):
            return num_processes
        return number_of_files
    return num_processes
