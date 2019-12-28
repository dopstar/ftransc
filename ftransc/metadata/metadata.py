import os
import base64

import mutagen
import mutagen.id3
import mutagen.mp3
import mutagen.mp4
import mutagen.asf
import mutagen.flac
import mutagen.apev2
import mutagen.musepack
import mutagen.oggvorbis


from ftransc.config import TagMap


class Metadata(object):
    """
    handles tag extraction and insertion into and/or from audio files
    """

    __tag_mapping = {}

    __id3_mapping = {
        "artist": mutagen.id3.TPE1,
        "album": mutagen.id3.TALB,
        "title": mutagen.id3.TIT2,
        "genre": mutagen.id3.TCON,
        "year": mutagen.id3.TDRC,
        "tracknumber": mutagen.id3.TRCK,
        "composer": mutagen.id3.TCOM,
        "lyrics": mutagen.id3.USLT,
        "disk": mutagen.id3.TPOS,
    }
    __opener = {
        ".mp3": mutagen.mp3.Open,
        ".wma": mutagen.asf.Open,
        ".m4a": mutagen.mp4.Open,
        ".flac": mutagen.flac.Open,
        ".wv": mutagen.apev2.APEv2,
        ".mpc": mutagen.musepack.Open,
        ".ogg": mutagen.oggvorbis.Open,
    }

    def __init__(self, input_file):
        self.input_file = input_file
        self.input_tags = {key: None for key in self.__id3_mapping}
        self.input_tags["albumart"] = None
        self.input_cover_art = {
            "mime": "image/jpeg",
            "type": 3,
            "ext": None,
            "data": None,
        }

        if not self.__tag_mapping:
            self.__tag_mapping.update(TagMap().as_dict())

        self.extract_tags()

    def extract_tags(self):
        """
        extracts metadata tags from the audio file
        """
        ext = os.path.splitext(self.input_file)[1].lower()
        if ext in self.__tag_mapping:
            tags = mutagen.File(self.input_file)
            for tag, key in self.__tag_mapping[ext].items():
                if tag == "albumart":
                    self._extract_album_art(ext, tags)
                elif key in tags:
                    self.input_tags[tag] = tags[key][0]
                elif tag == "lyrics" and key == "USLT":
                    self.input_tags.update(
                        {
                            tag: tags[id3tag].text
                            for id3tag in tags
                            if id3tag.startswith(key)
                        }
                    )

    def _extract_album_art(self, ext, tags):
        album_art_tag = self.__tag_mapping.get(ext, {}).get("albumart")
        if album_art_tag is not None:
            if album_art_tag in tags:
                self.input_cover_art["ext"] = ext
                if ext == ".mp3":
                    image = tags[album_art_tag]
                    self.input_cover_art["mime"] = image.mime
                    self.input_cover_art["data"] = image.data
                elif ext == ".m4a":
                    self.input_cover_art["data"] = tags[album_art_tag][0]
                elif ext in (".ogg", ".flac"):
                    encoded_image = tags[album_art_tag][0]
                    image = mutagen.flac.Picture(base64.b64decode(encoded_image))
                    self.input_cover_art["data"] = image.data
                    self.input_cover_art["mime"] = image.mime
            elif ext == ".mp3":
                for key in tags:
                    if key.startswith(album_art_tag):
                        image = tags[key]
                        self.input_cover_art["mime"] = image.mime
                        self.input_cover_art["data"] = image.data

    def insert_tags(self, output_file):
        """
        inserts tags tags into an audio file.

        :param output_file: output file name.
        """
        ext = os.path.splitext(output_file)[1].lower()
        try:
            tag_map = self.__tag_mapping[ext]
        except KeyError:
            return

        try:
            output_tags = self.__opener[ext](output_file)
        except mutagen.apev2.APENoHeaderError:
            output_tags = self.__opener[ext]()
        except KeyError:
            return

        for input_tag_name, input_tag_value in self.input_tags.items():
            if input_tag_value is None or input_tag_name not in tag_map:
                continue
            output_tag_name = tag_map[input_tag_name]

            if input_tag_name in ("tracknumber", "disk"):
                if (
                    isinstance(input_tag_value, (list, tuple))
                    and len(input_tag_value) == 2
                ):
                    input_tag_value = "%d/%d" % tuple(input_tag_value)

            if ext == ".mp3":
                if input_tag_name == "lyrics":
                    output_tags[output_tag_name] = self.__id3_mapping[input_tag_name](
                        encoding=3,
                        lang="eng",
                        desc="lyrics",
                        text="%s" % input_tag_value,
                    )
                else:
                    output_tags[output_tag_name] = self.__id3_mapping[input_tag_name](
                        encoding=3, text=["%s" % input_tag_value]
                    )
            elif ext in self.__tag_mapping and ext != ".mp3":
                if input_tag_name == "tracknumber" and ext == ".m4a":
                    if "/" in str(input_tag_value):
                        track_number = [int(i) for i in str(input_tag_value).split("/")]
                        output_tags[output_tag_name] = [
                            (track_number[0], track_number[1])
                        ]
                    else:
                        output_tags[output_tag_name] = [(int(input_tag_value), 0)]
                else:
                    output_tags[output_tag_name] = ["%s" % input_tag_value]

        if ext == ".wv":
            output_tags.save(output_file)
        else:
            output_tags.save()

        self._insert_album_art(ext, output_file)

    def _insert_album_art(self, ext, output_file):
        if self.input_cover_art["data"] is None:
            return

        if ext == ".m4a":
            output_tags = mutagen.mp4.MP4(output_file)
            if self.input_cover_art["ext"] == ".mp3":
                if self.input_cover_art["mime"] == "image/png":
                    mime = mutagen.mp4.MP4Cover.FORMAT_PNG
                else:
                    mime = mutagen.mp4.MP4Cover.FORMAT_JPEG
                image = mutagen.mp4.MP4Cover(self.input_cover_art["data"], mime)
                output_tags["covr"] = [image]
                output_tags.save()
        elif ext == ".mp3":
            audio = mutagen.mp3.MP3(output_file, ID3=mutagen.id3.ID3)
            if self.input_cover_art["ext"] in (".m4a", ".ogg", ".flac"):
                image = mutagen.id3.APIC(
                    desc="",
                    encoding=3,
                    data=self.input_cover_art["data"],
                    type=self.input_cover_art["type"],
                    mime=self.input_cover_art["mime"],
                )
                audio.tags.add(image)
                audio.save()
        elif ext == ".flac":
            tags = mutagen.File(output_file)
            image = mutagen.flac.Picture()
            image.desc = ""
            image.data = self.input_cover_art["data"]
            image.type = self.input_cover_art["type"]
            image.mime = self.input_cover_art["mime"]
            tags.add_picture(image)
            tags.save()
