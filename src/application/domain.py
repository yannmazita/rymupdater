from enum import Enum


class ID3Keys(Enum):
    TITLE = "TIT2"
    TRACK_SUBTITLE = "TIT3"
    ARTIST = "TPE1"
    ARTIST_SORT = "TSOP"    # Should be "performer sort" but shows up as "artistsort in Quod Libet
    PERFORMER = "TPE2"  # Should be "band" but shows up as performer in Quod Libet
    PERFORMER_SORT = "TXXX:QuodLibet::performersort"
    CONDUCTOR = "TPE3"  # classical music
    INTERPRETER_REMIXER = "TPE4"  # Intrepreter or remixer or modifier.
    INVOLVED_PEOPLE = "TIPL"  # Engineers, producers, mixers...
    ALBUM_ARTIST = "TXXX:QuodLibet::albumartist"
    ALBUM_ARTIST_SORT_ORDER = "TSO2"
    TRACK_NUM = "TRCK"
    DISC_NUM = "TPOS"  # Part of set.
    ALBUM = "TALB"
    ALBUM_SORT_ORDER = "TSOA"
    DISC_SUBTITLE = "TSST"  # Set subtitle.
    # RECORDING_TIME = "TDRC"
    RELEASE_TIME = "TDRC"   # Should be TDRL but TDRC is used by every media player.
    GENRE = "TCON"
    DESCRIPTION = "TXXX:QuodLibet::description"
    LANGUAGE = "TLAN"
    COMPOSER = "TCOM"  # classical music
    COMPOSER_SORT_ORDER = "TSOC"  # classical music
    LABEL = "TPUB"
    LABEL_ID = "TXXX:QuodLibet::labelid"
    MUSICIAN_CREDITS = "TMCL"
    WRITTEN_BY = "TEXT"
    # ISRC = "ISRC"
    BPM = "TBPM"
    MEDIA = "TMED"
    COMPILATION = "TCMP"  # '0' or '1'
    COMMENT = "COMM"
    STATS = "POPM"
    TEST = ""


class RYMtags(Enum):
    ARTIST = "Artist"
    GENRE = "Genres"
    DESCRIPTION = "Descriptors"
    LANGUAGE = "Language"
    # RECORDING_TIME = "Recorded"
    RELEASE_TIME = "Released"
    LABEL_AND_LABEL_ID = "Issue details"    # Format: "LABEL / LABEL_ID /"
    LABEL = "not-used-label"  # Is not found individually on the webpage
    LABEL_ID = "not-used-label-id"  # Is not found individually on the webpage
