import os
import sys
import time
import logging
import multiprocessing


import ftransc.core.queue
import ftransc.utils





def determine_number_of_workers(number_of_files, desired_number_of_workers):
    num_processes = multiprocessing.cpu_count()
    if desired_number_of_workers > 0:
        return desired_number_of_workers
    if number_of_files < num_processes:
        return number_of_files
    return num_processes


def cli():
    opt, files = ftransc.utils.parse_args()

    if opt.silent:
        log_level = logging.CRITICAL
    elif opt.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    log_format = '[%(levelname)s] %(message)s'
    logging.basicConfig(stream=sys.stdout, level=log_level, format=log_format)

    if os.environ['USER'] == 'root':
        raise SystemExit('It is not safe to run ftransc as root.')

    if not files and not opt.walk and not opt.cdrip:
        raise SystemExit("ftransc: no input file")

    files = sorted(list(set(files)))  # remove duplicates
    home_directory = os.getcwd()
    audio_format = opt.format.lower()
    audio_quality = opt.quality.lower()
    audio_preset = ftransc.utils.get_audio_presets(audio_format, audio_quality=audio_quality, external_encoder=opt.external_encoder)

    if opt.walk is not None:
        walker = os.walk(opt.walk)
        for working_directory, _, files in os.walk(opt.walk):
            break
        else:
            worker_directory, files = '.', []
        os.chdir(working_directory)

    if opt.cdrip:
        files = ftransc.utils.rip_compact_disc()

    queue = multiprocessing.JoinableQueue()
    for filename in files:
        queue.put(filename)

    time.sleep(1)  # wait a sec before start processing. queue might not be full yet
    num_workers = determine_number_of_workers(len(files), opt.num_procs)
    output_directory = ftransc.utils.create_directory(opt.outdir)
    for process_count in range(1, num_workers + 1):
        process_name = 'P%d' % process_count
        worker_args = (queue, process_name, home_directory, output_directory, audio_format, audio_preset, opt)
        process = multiprocessing.Process(target=ftransc.core.queue.worker, args=worker_args)
        process.daemon = True
        process.start()

    queue.close()
    queue.join()
