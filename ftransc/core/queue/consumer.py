import os
try:
    import Queue as queue
except ImportError:
    import queue
import logging

import blessings

from ftransc.metadata import Metadata
from ftransc.core import transcode, is_url, download_from_youtube


term = blessings.Terminal()
logger = logging.getLogger(__name__)


def worker(input_q, cpu_count, home_directory, output_directory, audio_format, audio_preset, options):
    while True:
        if input_q.empty():
            logger.info(term.bold("Shutting down worker: %s"), cpu_count)
            break
        try:
            progress = input_q.qsize()
        except NotImplementedError:
            progress = 1
        try:
            filename = input_q.get(False)
        except queue.Empty as err:
            logger.debug("%s: %s", type(err), str(err))
            continue
        if is_url(filename):
            url = filename
            filename = download_from_youtube(url)
        new_dir = os.path.dirname(filename)
        input_file_name = os.path.basename(filename)
        output_file_name = os.path.splitext(input_file_name)[0] + "." + audio_format
        if output_directory:
            output_file_name = output_directory + os.sep + output_file_name
            if not output_directory.endswith(os.sep):
                output_directory += os.sep
        if new_dir:
            if not os.path.isabs(new_dir):
                new_dir = home_directory + os.path.sep + new_dir

            new_dir = os.path.realpath(new_dir)
            if new_dir != os.getcwd():
                os.chdir(new_dir)
        else:
            if os.getcwd() != home_directory and not os.walk:
                os.chdir(home_directory)

        if output_file_name == input_file_name:
            logger.warning(term.yellow(
                "[{0:2}][{1}] {2} [input = output][skipped]".format(
                    progress, cpu_count, input_file_name
                )
            ))
            input_q.task_done()
            continue
        if not os.path.exists(input_file_name):
            logger.warning(term.yellow(
                "[{0:2}][{1}] {2} [does not exist]".format(
                    progress, cpu_count, input_file_name
                )
            ))
            input_q.task_done()
            continue
        if os.path.isfile(output_file_name) and not options.overwrite:
            logger.warning(term.yellow(
                '[{0:2}][{1}] {2} [use "-w" to overwrite][skipped]'.format(
                    progress, cpu_count, input_file_name
                )
            ))
            input_q.task_done()
            continue
        if os.path.isdir(input_file_name) and options.walk is None:
            logger.warning(term.yellow(
                '[{0:2}][{1}] {2} [use "--directory"][skipped]'.format(
                    progress, cpu_count, input_file_name
                )
            ))
            input_q.task_done()
            continue

        swp_file = ".%s.swp" % input_file_name
        if os.path.isfile(swp_file) and not options.unlock:
            logger.warning(term.yellow(
                '[{0:2}][{1}] {2} [use "-u" to unlock][skipped]'.format(
                    progress, cpu_count, input_file_name
                )
            ))
            input_q.task_done()
            continue
        elif not os.path.isfile(swp_file):
            try:
                with open(swp_file, 'w'):
                    pass
            except IOError as err:
                input_q.task_done()
                logger.fatal(term.red(
                    "[{0:2}][{1}] No permissions to write to this folder".format(
                        progress, cpu_count
                    )
                ))
                raise SystemExit(str(err))

        try:
            metadata = Metadata(input_file_name)
        except IOError:
            logger.warning(term.yellow(
                '[{0:2}][{1}] Unreadable'.format(
                    progress, cpu_count, input_file_name
                )
            ))
            os.remove(swp_file)
            input_q.task_done()
            continue

        if transcode(input_file_name, audio_format, output_directory, audio_preset, options.external_encoder):
            logger.info(term.green('[{0:2}][{1}][to {2}] {3} [Success]'.format(
                progress, cpu_count, audio_format.upper(), input_file_name
            )))
            if options.remove:
                os.remove(input_file_name)
            os.remove(swp_file)
        else:
            logger.error(term.bold_red('[{0:2}][{1}][to {2}] {3} [Fail]'.format(
                progress, cpu_count, audio_format.upper(), input_file_name
            )))
            os.remove(swp_file)
            input_q.task_done()
            continue

        metadata.insert_tags(output_file_name)
        input_q.task_done()
