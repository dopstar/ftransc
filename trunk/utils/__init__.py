import os
import urllib
import tempfile
import subprocess

from ftransc.utils.constants import SUPPORTED_FORMATS, DEPENDENCIES

def show_dep_status(dep_name, dep_status, deps, fmts, check=False):
    rd = "\033[0;31m"   #red
    gr = "\033[0;32m"   #green
    nc = "\033[0m"      #no color
    if dep_status:
        if check:
            print2(dep_name + '...' + gr + " installed" + nc)
    else:
        if check:
            print2("%s_______ %s not installed _______%s" % (rd, dep_name, nc))
        if deps:
            for fmt in deps[dep_name]:
                fmts.remove(fmt)
                
            return fmts

def check_deps(check=False, list_formats=False):
    """
    checks whether all dependencies for this script are installed or not.
    """

    module_map = {
                    'python-mutagen': 'mutagen',
                    'python-qt4'    : 'PyQt4',
                 }
    for dep in DEPENDENCIES:
        status = subprocess.Popen(["which", dep], 
                                   stdout=subprocess.PIPE).communicate()[0].strip() 
        show_dep_status(dep, status, DEPENDENCIES, SUPPORTED_FORMATS, check=check)

    for pkg, mod in module_map.iteritems():
        try:
            import mod
            show_dep_status(pkg, False, {}, [], check=check) #negative logic
        except ImportError:
            show_dep_status(pkg, True, {}, [], check=check)
    if check:
        raise SystemExit(0)
    if list_formats:
        supported_formats = list(SUPPORTED_FORMATS)
        supported_formats.sort()
        print "Supported Formats:"
        for fmt in supported_formats:
            print "\t%s" % fmt
        raise SystemExit(0)


    return SUPPORTED_FORMATS


def upgrade_version(current_version):
    """
    upgrades to the latest available version
    """
    
    trunk_url = 'http://ftransc.googlecode.com/svn/trunk/'
    tmp_dir = tempfile.mktemp(prefix='ftransc_')
    ftransc_doc_dir = '/usr/share/doc/ftransc'
    if os.environ['USER'] != 'root':
        raise SystemExit('try using "sudo", you have to be "root" on this one.')
    target  = '%s/version' % trunk_url
    try:
        latest  = map(int, urllib.urlopen(target).read().strip().split('.'))
    except IOError:
        raise SystemExit('ftransc upgrade failed: \033[1;31moffline\033[0m')
    current = map(int, current_version.split('.'))
    latest_version = '.'.join(map(str, latest))

    if latest > current:
        cmd = ['svn', 'export', trunk_url, tmp_dir]
        with open('/dev/null', 'w') as devnull:
            subprocess.Popen(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=devnull).communicate()
            os.chdir(ftransc_doc_dir)
            cmd = ['make', 'uninstall']
            subprocess.Popen(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=devnull).communicate()
            cmd = ['make', 'install']
            os.chdir(tmp_dir)
            subprocess.Popen(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=devnull).communicate()
            os.chdir('..')
            cmd = ['rm', '-r', '-f', tmp_dir]
            subprocess.Popen(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=devnull).communicate()
            raise SystemExit('upgraded from version [\033[0;31m%s\033[0m] to version [\033[0;32m%s\033[0m]' % \
                     (current_version, latest_version))
    raise SystemExit('You are already on the latest version.')

def print2(msg, noreturn=False, silent=False):
    if not silent:
        if noreturn:
            print msg,
        else:
            print msg

def read_playlist(playlist):
    try:
        return open(playlist, 'r').readlines()
    except IOError:
        raise SystemExit('unable to read playlist file: %s' % (str(playlist)))

def m3u_extract(playlist, mode=None):
    if mode == 'playlist':
        playlist = playlist
    else:
        playlist = read_playlist(playlist)
    songs = [s.replace('file:/', '') for s in playlist if s]
    return [urllib.url2pathname(song.strip()) for song in songs \
            if song and not song.startswith('#')]

def pls_extract(playlist):
    songs = read_playlist(playlist)
    return [i.strip().split('file://')[1] \
            for i in songs if i.strip().startswith('File')] 

def xspf_extract(playlist): 
    songs = read_playlist(playlist)
    return [urllib.url2pathname(song.strip().replace('<location>file://', '').replace('</location>', '')) \
            for song in songs if '<location>file://' in song]

def rip_compact_disc():
    base_folder = os.path.expanduser('~/ftransc/ripped_albums')
    os.system('mkdir -p %s' % base_folder)
    walker = os.walk(base_folder)
    parent_folder, child_folders, child_files = walker.next()
    dest_folder = 'CD-%d' % (len(child_folders) + 1)
    os.system('mkdir -p %s/%s' % (base_folder, dest_folder))
    os.chdir('%s/%s' % (base_folder, dest_folder))
    print 'Ripping Compact Disc (CD)...'
    os.system('cdparanoia -B >/dev/null 2>&1')
    print 'Finished ripping CD'
    walker = os.walk('%s/%s' % (base_folder, dest_folder))
    parent_folder, child_folders, child_files = walker.next()
    return child_files

