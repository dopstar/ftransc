import os
import urllib
import subprocess

def check_deps(check=False):
    """
    checks whether all dependencies for this script are installed or not.
    """
    deps = {
            'mutagen-inspect'   : [],
            'ffmpeg'            : [
                                    'mp3', 
                                    'ogg', 
                                    'wma', 
                                    'm4a', 
                                    'flac', 
                                    'wav', 
                                    'mpc',
                                  ],
            'lame'              : ['mp3'],
            'flac'              : ['flac'],
            'faac'              : ['m4a'],
            'oggenc'            : ['ogg'],
            'mppenc'            : ['mpc'],
            }
    for dep in deps:
        pkg = subprocess.Popen(["which", dep], 
                               stdout=subprocess.PIPE).communicate()[0].strip() 
        if check:
            print2(dep + '...' + rd + " not installed" + nc if not pkg \
                    else dep + '...' + gr + " installed" + nc)
        else:
            if not pkg:
                print2("%s_______ %s not installed _______%s" % (rd, dep, nc))
                for fmt in deps[dep]:
                    supported_formats.remove(fmt)
    if check:
        raise SystemExit(0)

def upgrade_version(current_version):
    """
    upgrades to the current available version
    """
    
    trunk_url = 'http://ftransc.googlecode.com/svn/trunk/'
    tmp_dir = '/tmp/tmp-ftransc_upgrade-tmp'
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
            raise SystemExit('upgraded from version [%s] to version [%s]' % \
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
    os.system('cdparanoia -Q')
    os.system('cdparanoia -B')
    walker = os.walk('%s/%s' % (base_folder, dest_folder))
    parent_folder, child_folders, child_files = walker.next()
    return child_files

