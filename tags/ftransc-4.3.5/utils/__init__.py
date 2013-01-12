import urllib
def read_playlist(playlist):
    try:
        return open(playlist, 'r').readlines()
    except IOError:
        raise SystemExit('unable to read playlist file: %s' % (str(playlist)))

def m3u_extract(playlist, mode=None):
    if mode is not None and mode == 'playlist':
        playlist = playlist
    else:
        playlist = read_playlist(playlist)

    songs = [s.replace('file:/', '') for s in playlist if s]
    return [urllib.url2pathname(song.strip()) for song in songs\
            if song and not song.startswith('#')]

def pls_extract(playlist):
    songs = read_playlist(playlist)
    return [i.strip().split('file://')[1]\
            for i in songs if i.strip().startswith('File')]

def xspf_extract(playlist):
    songs = read_playlist(playlist)
    return [urllib.url2pathname(song.strip().replace('<location>file://', '').replace('</location>', ''))\
            for song in songs if '<location>file://' in song]