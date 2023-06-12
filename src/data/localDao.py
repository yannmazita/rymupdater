from collections.abc import Iterator
from pathlib import Path
from mutagen.id3 import ID3
from mutagen.id3._frames import (
    TIT2,
    TIT3,
    TPE1,
    TOPE,
    TPE2,
    TPE3,
    TPE4,
    TIPL,
    TXXX,
    TSO2,
    TRCK,
    TPOS,
    TALB,
    TSOA,
    TSST,
    TDRC,
    TDRL,
    TCON,
    TLAN,
    TCOM,
    TSOC,
    TPUB,
    TMCL,
    TEXT,
    TBPM,
    TMED,
    TCMP,
    COMM,
)

from src.application.domain import ID3Keys


class FileData:
    """Music file data access.

    A FileData instance is used as a data access object (DAO) to be used elsewhere.
    Any service requiring access to audio files should be implemented in this class.
    """

    def __init__(self, musicDirectory: Path):
        """Initiliazes the instance based on the path of the music directory.

        Args:
            musicDirectory: The path of the music directory.
        """
        # self.__paths: Iterator[Path] = iter([])
        self.__currentPath: Path = Path("")
        self.__paths: Iterator[Path] = Path(musicDirectory).rglob("*.mp3")
        self.__currentMP3File: ID3 = ID3()

    def loadNextFile(self) -> bool:
        """Loads next audio file from paths in FileData instance.

        Returns:
            A boolean, true if file was loaded, false otherwise.
        """
        try:
            self.__currentPath = Path(next(self.__paths))
        except StopIteration:
            return False

        self.__currentMP3File = ID3(self.__currentPath)

        return True

    def getTagsFromFile(self) -> dict[ID3Keys, list[str]]:
        """Gets ID3 tags from loaded file.

        Returns:
            A dictionnary {key: value} where key is an ID3Keys member and value
            a list of ID3 frames with the given name.
        """
        tags: dict[ID3Keys, list[str]] = {}

        for frame in ID3Keys:
            tags[frame] = self.__currentMP3File.getall(frame.value)

        return tags

    def updateFileTag(self, frame: ID3Keys, value: str) -> None:
        """Update ID3 frame in loaded file.

        This will replace the old frame value if the frame exists already.

        Args:
            frame: ID3 frame to update.
            value: Corresponding value.
        Returns:
            None
        """

        match frame:
            case ID3Keys.TITLE:
                self.__currentMP3File["TIT2"] = TIT2(encoding=3, text=["" + value + ""])
            case ID3Keys.TRACK_SUBTITLE:
                self.__currentMP3File["TIT3"] = TIT3(encoding=3, text=["" + value + ""])
            case ID3Keys.ARTIST:
                self.__currentMP3File["TPE1"] = TPE1(encoding=3, text=["" + value + ""])
            case ID3Keys.PERFORMER:
                self.__currentMP3File["TOPE"] = TOPE(encoding=3, text=["" + value + ""])
            case ID3Keys.BAND:
                self.__currentMP3File["TPE2"] = TPE2(encoding=3, text=["" + value + ""])
            case ID3Keys.CONDUCTOR:
                self.__currentMP3File["TPE3"] = TPE3(encoding=3, text=["" + value + ""])
            case ID3Keys.INTERPRETER_REMIXER:
                self.__currentMP3File["TPE4"] = TPE4(encoding=3, text=["" + value + ""])
            case ID3Keys.INVOLVED_PEOPLE:
                self.__currentMP3File["TIPL"] = TIPL(encoding=3, text=["" + value + ""])
            case ID3Keys.ALBUM_ARTIST:
                self.__currentMP3File.add(TXXX(encoding=3,desc="QuodLibet::albumartist",text=["" + value + ""],))
            case ID3Keys.ALBUM_SORT_ORDER:
                self.__currentMP3File["TSO2"] = TSO2(encoding=3, text=["" + value + ""])
            case ID3Keys.TRACK_NUM:
                self.__currentMP3File["TRCK"] = TRCK(encoding=3, text=["" + value + ""])
            case ID3Keys.DISC_NUM:
                self.__currentMP3File["TPOS"] = TPOS(encoding=3, text=["" + value + ""])
            case ID3Keys.ALBUM:
                self.__currentMP3File["TALB"] = TALB(encoding=3, text=["" + value + ""])
            case ID3Keys.ALBUM_SORT_ORDER:
                self.__currentMP3File["TSOA"] = TSOA(encoding=3, text=["" + value + ""])
            case ID3Keys.DISC_SUBTITLE:
                self.__currentMP3File["TSST"] = TSST(encoding=3, text=["" + value + ""])
            case ID3Keys.RECORDING_TIME:
                self.__currentMP3File["TDRC"] = TDRC(encoding=3, text=["" + value + ""])
            case ID3Keys.RELEASE_TIME:
                self.__currentMP3File["TDRL"] = TDRL(encoding=3, text=["" + value + ""])
            case ID3Keys.GENRE:
                self.__currentMP3File["TCON"] = TCON(encoding=3, text=["" + value + ""])
            case ID3Keys.DESCRIPTION:
                self.__currentMP3File.add(TXXX(encoding=3,desc="QuodLibet::description",text=["" + value + ""],))
            case ID3Keys.LANGUAGE:
                self.__currentMP3File["TLAN"] = TLAN(encoding=3, text=["" + value + ""])
            case ID3Keys.COMPOSER:
                self.__currentMP3File["TCOM"] = TCOM(encoding=3, text=["" + value + ""])
            case ID3Keys.COMPOSER_SORT_ORDER:
                self.__currentMP3File["TSOC"] = TSOC(encoding=3, text=["" + value + ""])
            case ID3Keys.LABEL:
                self.__currentMP3File["TPUB"] = TPUB(encoding=3, text=["" + value + ""])
            case ID3Keys.LABEL_ID:
                self.__currentMP3File.add(TXXX(encoding=3, desc="QuodLibet::labelid", text=["" + value + ""]))
            case ID3Keys.MUSICIAN_CREDITS:
                self.__currentMP3File["TMCL"] = TMCL(encoding=3, text=["" + value + ""])
            case ID3Keys.WRITTEN_BY:
                self.__currentMP3File["TEXT"] = TEXT(encoding=3, text=["" + value + ""])
            case ID3Keys.BPM:
                self.__currentMP3File["TBPM"] = TBPM(encoding=3, text=["" + value + ""])
            case ID3Keys.MEDIA:
                self.__currentMP3File["TMED"] = TMED(encoding=3, text=["" + value + ""])
            case ID3Keys.COMPILATION:
                self.__currentMP3File["TCMP"] = TCMP(encoding=3, text=["" + value + ""])
            case ID3Keys.COMMENT:
                self.__currentMP3File.add(COMM(encoding=3, lang="eng", desc="desc", text=["" + value + ""]))

        self.__currentMP3File.save()


file = FileData(Path("/home/yann/music"))
# first track is "the knife/silent shout/07 - like a pen.mp3"
file.loadNextFile()
file.updateFileTag(ID3Keys.BAND, "perfomer test, BAND")
print(file.getTagsFromFile())
