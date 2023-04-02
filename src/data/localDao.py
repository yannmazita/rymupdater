from pathlib import Path
from mutagen.id3 import ID3

from src.application.domain import ID3Keys


class FileData:
    """Music file data access"""

    @staticmethod
    def getTagsFromFile(path: Path) -> dict[ID3Keys, str]:
        """
        Get ID3 tags from file.
        Args:
            path: File path.
        Returns:
            dict[ID3Keys, str]: dictitonnary of tags and their corresponding value.
        """
        audio: ID3 = ID3(path)
        tags: dict[ID3Keys, str] = {}

        return tags

    @staticmethod
    def updateFileTags(path: Path, dic: dict[ID3Keys, str]) -> None:
        """
        Update ID3 tags in file.
        Args:
            path: File path.
            dic: Dictionnary of AudioTags keys and the corresponding value to update.
        Returns:
            None
        """
        audio: ID3 = ID3(path)
        for tag in dic:
            audio[tag.value] = dic[tag]
