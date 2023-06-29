from src.application.services import RYMupdater

from pathlib import Path
from collections.abc import Iterator


class Cli():
    def __init__(self, musicDirectory: str):
        """CLI main services"""
        self.__rym: RYMupdater = RYMupdater()
        self.__filePaths: Iterator[Path] = self.__rym.tagLibrary(Path(musicDirectory))

    def displayCurrentFilePath(self) -> None:
        """ Displays the path of the current audio file.

        This method iterates through the file path generator without interrupting
        the execution of the tagging service.
        """
        for path in self.__filePaths:
            print(f"Current file: {path}")
