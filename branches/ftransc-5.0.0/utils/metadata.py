import os
import base64

try:
    import mutagen
    import mutagen.id3
    import mutagen.mp3
    import mutagen.mp4
    import mutagen.asf
    import mutagen.flac
    import mutagen.musepack
    import mutagen.oggvorbis
    NO_TAGS = False
except ImportError:
    NO_TAGS = True

from ftransc.utils.tagmap import tags as tagmap

class MetaTag(object):
    """
    handles tag extraction and insertion into and/or from audio files
    """
    __tag_mapping = tagmap.copy()
    exts = __tag_mapping.keys()
    
    if not NO_TAGS:
        __id3_mapping = {
            'artist'        : mutagen.id3.TPE1, 
            'album'         : mutagen.id3.TALB, 
            'title'         : mutagen.id3.TIT2, 
            'genre'         : mutagen.id3.TCON, 
            'year'          : mutagen.id3.TDRC, 
            'tracknumber'   : mutagen.id3.TRCK,
            'composer'      : mutagen.id3.TCOM,
            'lyrics'        : mutagen.id3.USLT,
        }
        __opener = {
            '.mp3'          : mutagen.mp3.Open,
            '.wma'          : mutagen.asf.Open, 
            '.m4a'          : mutagen.mp4.Open, 
            '.flac'         : mutagen.flac.Open,
            '.mpc'          : mutagen.musepack.Open,
            '.ogg'          : mutagen.oggvorbis.Open, 
        }
    else:
        __id3_mapping = {}
        __opener      = {}

    def __init__(self, input_file):
        self.input_file = input_file
        self.tags = {
                'title'         : None, 
                'artist'        : None, 
                'album'         : None, 
                'year'          : None, 
                'genre'         : None, 
                'tracknumber'   : None,
                'composer'      : None,
                'lyrics'        : None,
                'albumart'      : None,
        }
        self.coverart = {
            'mime'  : 'image/jpeg',
            'type'  : 3,
            'ext'   : None,
            'data'  : None,
        }
        self.extract()
    
    def extract(self):
        """
        extracts metadata tags from the audio file
        """
        ext = os.path.splitext(self.input_file)[1].lower()
        if ext in self.exts:
            tags = mutagen.File(self.input_file)
            for tag, key in self.__tag_mapping[ext].iteritems():
                if tag == 'albumart':
                    self._extract_albumart(ext, tags)
                elif key in tags:
                    self.tags[tag] = tags[key][0]
                elif tag == 'lyrics' and key == 'USLT':
                    for id3tag in tags:
                        if id3tag.startswith(key):
                            self.tags[tag] = tags[id3tag].text

    def _extract_albumart(self, ext, tags):
        tag = self.__tag_mapping[ext].get('albumart')
        if tag is None:
            return
        if tag in tags:
            self.coverart['ext'] = ext
            if ext == '.mp3':
                apic = tags[tag]
                self.coverart['mime'] = apic.mime
                self.coverart['data'] = apic.data
            elif ext == '.m4a':
                self.coverart['data'] = tags[tag][0]
            elif ext in ('.ogg', '.flac'):
                encoded_image = tags[tag][0]
                image = mutagen.flac.Picture(base64.b64decode(encoded_image))
                self.coverart['data'] = image.data
                self.coverart['mime'] = image.mime
        elif ext == '.mp3':
            for key in tags:
                if key.startswith(tag):
                    apic = tags[key]
                    self.coverart['mime'] = apic.mime
                    self.coverart['data'] = apic.data

    def insert(self, output_file):
        """
        inserts tags tags into an audio file.
        """        
        ext = os.path.splitext(output_file)[1].lower()
        if ext not in self.__opener:
            return 1
        tags = self.__opener[ext](output_file)
        for tag, value in self.tags.items():
            if value is None or tag not in self.__tag_mapping[ext]:
                continue
            if tag == 'tracknumber' and \
                (isinstance(value, list) or isinstance(value, tuple)) and\
                len(value) == 2:
                value = '%d/%d' % (value[0], value[1])
            if ext == '.mp3':
                if tag == 'lyrics':
                    tags[self.__tag_mapping[ext][tag]] = \
                                    self.__id3_mapping[tag](encoding=3, 
                                                            lang='eng', 
                                                            desc='lyrics',
                                                            text=u'%s' % value)
                else:
                    tags[self.__tag_mapping[ext][tag]] = \
                                self.__id3_mapping[tag](encoding=3, 
                                                        text=[u'%s' % value])
            elif ext in self.exts and ext != '.mp3':
                if tag == 'tracknumber' and ext == '.m4a':
                    try:
                        trkn = [int(i) for i in str(value).split('/')]
                        tags[self.__tag_mapping[ext][tag]] = \
                                [(trkn[0], trkn[1])]
                    except IndexError:
                        tags[self.__tag_mapping[ext][tag]] = [(trkn[0], 0)]
                else:
                    tags[self.__tag_mapping[ext][tag]] = [u'%s' % value]
        tags.save()
        self._insert_albumart(ext, output_file)

    def _insert_albumart(self, ext, output_file):
        if self.coverart['data'] is None:
            return

        if ext == '.m4a':
            tags = mutagen.mp4.MP4(output_file)
            if self.coverart['ext'] == '.mp3':
                if self.coverart['mime'] == 'image/png':
                    mime = mutagen.mp4.MP4Cover.FORMAT_PNG
                else:
                    mime = mutagen.mp4.MP4Cover.FORMAT_JPEG

                coverart = mutagen.mp4.MP4Cover(self.coverart['data'], mime)
                tags['covr'] = [coverart]
                tags.save()
                return

        elif ext == '.mp3':
            audio = mutagen.mp3.MP3(output_file, ID3=mutagen.id3.ID3)
            if self.coverart['ext'] in ('.m4a', '.ogg', '.flac'):
                apic = mutagen.id3.APIC(
                    desc     = u'',
                    encoding = 3,
                    data     = self.coverart['data'],
                    type     = self.coverart['type'],
                    mime     = self.coverart['mime']
                )
                audio.tags.add(apic)
                audio.save()
                return

