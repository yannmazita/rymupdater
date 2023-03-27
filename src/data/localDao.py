from pathlib import Path
from mutagen.easyid3 import EasyID3


from src.application.domain import AudioTags


class FileTags:
    """Music file data access"""
    
    @staticmethod
    def getTagsFromFile(path: Path) -> dict[AudioTags, str]:
        """
        Get ID3 tags from file.
        Args:
            path: File path.
        Returns:
            dict[str, str]: dictitonnary of tags and their corresponding value.
        """
        audio: EasyID3 = EasyID3(path)
        tags: dict[AudioTags, str] = {}

        for tag in AudioTags:
            tags[tag.value] = audio[tag.value]

        return tags

    @staticmethod
    def updateFileTags(path: Path, dic: dict[AudioTags, str]) -> None:
        """
        Update ID3 tags in file.
        Args:
            path: File path.
            dic: Dictionnary of AudioTags keys and the corresponding value to update.
        Returns:
            None
        """
        audio: EasyID3 = EasyID3(path)
        for tag in dic:
            audio[tag.value] = dic[tag]


