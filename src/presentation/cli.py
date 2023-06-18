from src.application.services import RYMupdater

from pathlib import Path


class Cli():
    def __init__(self):
        self.__rym: RYMupdater = RYMupdater()

    def displayCurrentFilePath(self) -> None:
        print(f"Current file: ")
