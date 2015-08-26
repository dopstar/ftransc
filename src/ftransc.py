#!/usr/bin/python
"""
ftransc is a script that bundles up utilities for audio conversion.
"""

import os
import sys
import time
import multiprocessing


from ftransc.utils.constants import (
    VERSION,
    LOGFILE,
    NO_TAGS,
)
from ftransc.utils.convert import convert

from ftransc.utils import (
    upgrade_version,
    print2,
    m3u_extract,
    pls_extract,
    xspf_extract,
    rip_compact_disc,
    parse_args,
    get_profile
)
from ftransc.utils.metadata import MetaTag

quality_presets = {}

if __name__ == "__main__":
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    pink = "\033[1;35m"
    cyan = "\033[1;36m"
    nc = "\033[0m"

    opt, files = parse_args()

    if opt.upgrade:
        upgrade_version(VERSION)

    if os.environ['USER'] == 'root':
        raise SystemExit('It is not safe to run ftransc as root.')

    if 'convert to ' in sys.argv[0]:
        opt.format = sys.argv[0].split()[-1]
        opt.notify = True
        opt.logfile = '/tmp/ftransc.log'

    LOGFILE = '/dev/stdout' if opt.debug else opt.logfile
    SILENT = opt.silent
    no_tags = NO_TAGS if NO_TAGS else opt.no_tags

    files = sorted(list(set(files)))  # remove duplicates
    home = os.getcwd()
    fmt = opt.format.lower()
    qual = opt.quality.lower()

    preset = get_profile(fmt, qual, opt.presets, opt.external_encoder, opt.check, opt.list_formats)

    if not files and not opt.walk and not opt.m3u and not opt.pls and not opt.xspf and not opt.cdrip:
        raise SystemExit("ftransc: no input file")

    if opt.walk is not None:
        walker = os.walk(opt.walk)
        dest_dir, dummy, files = walker.next()
        pwd = os.getcwd()
        os.chdir(dest_dir)

    outdir = ''
    if opt.outdir is not None:
        outdir = os.path.abspath(os.path.expanduser(opt.outdir))
        if not os.path.isdir(outdir):
            try:
                os.mkdir(outdir)
            except OSError:
                outdir = ''

    if opt.m3u is not None:
        files = m3u_extract(opt.m3u)
    elif opt.pls is not None:
        files = pls_extract(opt.pls)
    elif opt.xspf is not None:
        files = xspf_extract(opt.xspf)
    if opt.cdrip:
        files = rip_compact_disc()

    old_dir = ''
    total = len(files)
    fails = 0

    def consume_queue(input_q, cpucount):
        global outdir
        global fails
        while True:
            if input_q.empty():
                print2("Terminating ftransc process running on %s" % cpucount)
                break
            progress = 100.0 * (total - input_q.qsize() + 1) / float(total)
            filename = input_q.get(False)
            new_dir = os.path.dirname(filename)
            ifile = os.path.basename(filename)
            logfile = open(LOGFILE, 'a', 0)
            ofile = os.path.splitext(ifile)[0] + "." + fmt
            if outdir:
                ofile = outdir + os.sep + ofile
                if not outdir.endswith(os.sep):
                    outdir += os.sep
            if new_dir:
                if not os.path.isabs(new_dir):
                    new_dir = home + os.path.sep + new_dir

                new_dir = os.path.realpath(new_dir)
                if new_dir != os.getcwd():
                    os.chdir(new_dir)
            else:
                if os.getcwd() != home and not os.walk:
                    os.chdir(home)

            if ofile == ifile:
                print2("%.1f%%| %s| %s%s%s | input = output | %sskipped%s\n" % \
                       (progress, cpucount, blue, ifile, nc, yellow, nc))
                fails += 1
                input_q.task_done()
                continue
            if not os.path.exists(ifile):
                print2("%.1f%%| %s| %s%s%s | %sdoes not exist%s\n" % \
                       (progress, cpucount, blue, ifile, nc, red, nc))
                fails += 1
                input_q.task_done()
                continue
            if os.path.isfile(ofile) and not opt.overwrite:
                print2("%.1f%%| %s| %s%s%s | use '-w' to overwrite | %sskipped%s\n" % \
                       (progress, cpucount, blue, ifile, nc, yellow, nc))
                fails += 1
                input_q.task_done()
                continue
            if os.path.isdir(ifile) and opt.walk is None:
                print2("%.1f%%| %s| %s%s%s |  use '--directory' | %sskipped%s\n" % \
                       (progress, cpucount, blue, ifile, nc, yellow, nc))
                fails += 1
                input_q.task_done()
                continue

            swp_file = ".%s.swp" % ifile
            if os.path.isfile(swp_file) and not opt.unlock:
                print2("%.1f%%| %s| %s%s%s | use '-u' to unlock | %sskipped%s\n" % \
                       (progress, cpucount, blue, ifile, nc, yellow, nc))
                fails += 1
                input_q.task_done()
                continue
            elif not os.path.isfile(swp_file):
                try:
                    with open(swp_file, 'w'):
                        pass
                except IOError:
                    input_q.task_done()
                    raise SystemExit("%.1f%%| %s| %sNo permissions%s to write to this folder" % \
                                     (progress, cpucount, red, nc))

            try:
                if not no_tags:
                    metadata = MetaTag(ifile)
            except IOError:
                print2("%.1f%%| %s| %s%d/%d%s | %s%s%s | %sUnreadable%s\n" %
                       (progress, cpucount, blue, ifile, nc, red, nc))
                os.remove(swp_file)
                fails += 1
                input_q.task_done()
                continue

            if convert(ifile, fmt, outdir, preset, logfile, opt.external_encoder):
                print2("%.1f%%| %s| to %s | %s%s%s | %sSuccess%s\n" % \
                       (progress, cpucount, fmt.upper(), blue, ifile, nc, green, nc), noreturn=True)
                if opt.remove:
                    os.remove(ifile)
                os.remove(swp_file)
            else:
                print2("%.1f%%| %s| to %s | %s%s%s | %sFail%s\n" % \
                       (progress, cpucount, fmt.upper(), blue, ifile, nc, red, nc), noreturn=True)
                os.remove(swp_file)
                fails += 1
                input_q.task_done()
                continue

            try:
                if not no_tags:
                    metadata.insert(ofile)
                    del metadata
            except Exception, err:
                if opt.debug:
                    print2("%.1f%%| %s| %s%s%s\n" % (progress, cpucount, red, err.message, nc))
            logfile.close()

            input_q.task_done()


    proc_colors = {0: pink, 1: cyan}
    q = multiprocessing.JoinableQueue()
    for filename in files:
        q.put(filename)
    num_procs = multiprocessing.cpu_count()
    if 0 < opt.num_procs < num_procs:
        num_procs = opt.num_procs
    if len(files) < num_procs:
        num_procs = len(files)

    time.sleep(1)  # wait a sec before start processing. queue might not be full yet
    for pcount in xrange(1, num_procs + 1):
        proc_name = '%sCPU%d%s' % (proc_colors[pcount % 2], pcount, nc)
        x = multiprocessing.Process(target=consume_queue, args=(q, proc_name))
        x.daemon = True
        x.start()

    q.close()
    q.join()
