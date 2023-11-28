from collections.abc import Iterator
from pathlib import Path
from mutagen.id3 import ID3
from mutagen.id3._frames import (
    TIT2,
    TIT3,
    TPE1,
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
    TSOP,
    POPM
)

from rymupdater.domain import ID3Keys


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
        self.__currentFilePath: Path = Path("")
        self.__paths: Iterator[Path] = Path(musicDirectory).rglob("*.mp3")
        self.__currentMP3File: ID3 = ID3()

    @property
    def currentFilePath(self) -> Path:
        """File path of current audio file"""
        return self.__currentFilePath

    def loadNextFile(self) -> bool:
        """Loads next audio file from paths in FileData instance.

        Returns:
            A boolean, true if file was loaded, false otherwise.
        """
        try:
            self.__currentFilePath = Path(next(self.__paths))
        except StopIteration:
            return False

        self.__currentMP3File = ID3(self.__currentFilePath)

        return True

    def getTagsFromFile(self) -> dict[ID3Keys, str]:
        """Gets ID3 tags from loaded file.

        Returns:
            A dictionnary {key: value} where key is an ID3Keys member and value
            the first ID3 frame with the given name.
        """
        tags: dict[ID3Keys, str] = {}

        for frame in ID3Keys:
            try:
                tags[frame] = list(map(str, self.__currentMP3File.getall(frame.value)))[0]
            except IndexError:
                pass

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
                self.__currentMP3File.add(TIT2(encoding=3, text=["" + value + ""]))
            case ID3Keys.TRACK_SUBTITLE:
                self.__currentMP3File.add(TIT3(encoding=3, text=["" + value + ""]))
            case ID3Keys.ARTIST:
                self.__currentMP3File.add(TPE1(encoding=3, text=["" + value + ""]))
            case ID3Keys.ARTIST_SORT:
                self.__currentMP3File.add(TSOP(encoding=3, text=["" + value + ""]))
            case ID3Keys.PERFORMER:
                self.__currentMP3File.add(TPE2(encoding=3, text=["" + value + ""]))
            case ID3Keys.PERFORMER_SORT:
                self.__currentMP3File.add(
                    TXXX(
                        encoding=3,
                        desc="QuodLibet::performersort",
                        text=["" + value + ""],
                    )
                )
            case ID3Keys.CONDUCTOR:
                self.__currentMP3File.add(TPE3(encoding=3, text=["" + value + ""]))
            case ID3Keys.INTERPRETER_REMIXER:
                self.__currentMP3File.add(TPE4(encoding=3, text=["" + value + ""]))
            case ID3Keys.INVOLVED_PEOPLE:
                self.__currentMP3File.add(TIPL(encoding=3, text=["" + value + ""]))
            case ID3Keys.ALBUM_ARTIST:
                self.__currentMP3File.add(
                    TXXX(
                        encoding=3,
                        desc="QuodLibet::albumartist",
                        text=["" + value + ""],
                    )
                )
            case ID3Keys.ALBUM_SORT_ORDER:
                self.__currentMP3File.add(TSO2(encoding=3, text=["" + value + ""]))
            case ID3Keys.TRACK_NUM:
                self.__currentMP3File.add(TRCK(encoding=3, text=["" + value + ""]))
            case ID3Keys.DISC_NUM:
                self.__currentMP3File.add(TPOS(encoding=3, text=["" + value + ""]))
            case ID3Keys.ALBUM:
                self.__currentMP3File.add(TALB(encoding=3, text=["" + value + ""]))
            case ID3Keys.ALBUM_SORT_ORDER:
                self.__currentMP3File.add(TSOA(encoding=3, text=["" + value + ""]))
            case ID3Keys.DISC_SUBTITLE:
                self.__currentMP3File.add(TSST(encoding=3, text=["" + value + ""]))
            case ID3Keys.RELEASE_TIME:
                self.__currentMP3File.add(TDRC(encoding=3, text=["" + value + ""]))
            case ID3Keys.GENRE:
                self.__currentMP3File.add(TCON(encoding=3, text=["" + value + ""]))
            case ID3Keys.DESCRIPTION:
                self.__currentMP3File.add(
                    TXXX(
                        encoding=3,
                        desc="QuodLibet::description",
                        text=["" + value + ""],
                    )
                )
            case ID3Keys.LANGUAGE:
                self.__currentMP3File.add(TLAN(encoding=3, text=["" + value + ""]))
            case ID3Keys.COMPOSER:
                self.__currentMP3File.add(TCOM(encoding=3, text=["" + value + ""]))
            case ID3Keys.COMPOSER_SORT_ORDER:
                self.__currentMP3File.add(TSOC(encoding=3, text=["" + value + ""]))
            case ID3Keys.LABEL:
                self.__currentMP3File.add(TPUB(encoding=3, text=["" + value + ""]))
            case ID3Keys.LABEL_ID:
                self.__currentMP3File.add(
                    TXXX(encoding=3, desc="QuodLibet::labelid", text=["" + value + ""])
                )
            case ID3Keys.MUSICIAN_CREDITS:
                self.__currentMP3File.add(TMCL(encoding=3, text=["" + value + ""]))
            case ID3Keys.WRITTEN_BY:
                self.__currentMP3File.add(TEXT(encoding=3, text=["" + value + ""]))
            case ID3Keys.BPM:
                self.__currentMP3File.add(TBPM(encoding=3, text=["" + value + ""]))
            case ID3Keys.MEDIA:
                self.__currentMP3File.add(TMED(encoding=3, text=["" + value + ""]))
            case ID3Keys.COMPILATION:
                self.__currentMP3File.add(TCMP(encoding=3, text=["" + value + ""]))
            case ID3Keys.COMMENT:
                self.__currentMP3File.add(
                    COMM(encoding=3, lang="eng", desc="desc", text=["" + value + ""])
                )
            case ID3Keys.TEST:
                pass

        self.__currentMP3File.save()
