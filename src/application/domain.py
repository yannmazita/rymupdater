from enum import Enum


class ID3Keys(Enum):
    TITLE = "TIT2"
    TRACK_SUBTITLE = "TIT3"
    ARTIST = "TPE1"
    ORIGINAL_ARTIST = "TOPE"
    BAND = "TPE2"
    INTERPRETER_REMIXER = "TPE4"
    INVOLVED_PEOPLE = "TIPL"
    ALBUM_ARTIST = "TXXX:QuodLibet::albumartist"
    ALBUM_ARTIST_SORT_ORDER = "TSO2"
    TRACK_NUM = "TRCK"
    DISC_NUM = "TPOS"
    ALBUM = "TALB"
    ALBUM_SORT_ORDER = "TSOA"
    SET_SUBTITLE = "TSST"
    RECORDING_TIME = "TDRC"
    RELEASE_TIME = "TDRL"
    GENRE = "TCON"
    DESCRIPTION = "TXXX:QuodLibet::description"
    LANG = "TLAN"
    COMPOSER = "TCOM"
    COMPOSER_SORT_ORDER = "TSOC"
    LABEL = "TPUB"
    LABEL_ID = "TXXX:QuodLibet::labelid"
    MUSICIAN_CREDITS = "TMCL"
    WRITTEN_BY = "TEXT"
    ISRC = "ISRC"
    BPM = "TBPM"
    MEDIA = "TMED"
    COMPILATION = "TCMP"


class RYMtags(Enum):
    ARTIST = "Artist"
    DATE = "Released"
    GENRE = "Genres"
    DESCRIPTION = "Descriptors"

