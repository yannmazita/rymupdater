from src.data.localDao import FileData
from src.data.webDao import RYMdata
import src.application.domain as domain

from pathlib import Path


class RYMupdater:
    """ RYM main services
    """

    def __init__(self):
        """Initialiazes the instance.
        """
        self.__fileData: FileData | None = None
        self.__rymData: RYMdata | None = None

    def initializeData(self, musicDirectory: Path) -> None:
        """Initialiazes data access objects.

        Args:
            musicDirectory: The path of the music directory.
        Returns:
            None.
        """
        self.__fileData = FileData(musicDirectory)
        self.__rymData = RYMdata()

    def loadNextFile(self) -> bool:
        """Loads next audio file.

        Returns:
            A boolean, true if file was loaded, false otherwise.
        """
        assert self.__fileData is not None
        return self.__fileData.loadNextFile()

    def getTagsFromFile(self) -> dict[domain.ID3Keys, list[str]]:
        """Gets ID3 tags from loaded file.

        Returns:
            A dictionnary {key: value} where key is an ID3Keys member and value
            a list of ID3 frames with the given name.
        """
        assert self.__fileData is not None
        return self.__fileData.getTagsFromFile()

    def updateFileTag(self, frame: domain.ID3Keys, value: str) -> None:
        """Update ID3 frame in loaded file.

        This will replace the old frame value if the frame exists already.

        Args:
            frame: ID3 frame to update.
            value: Corresponding value.
        Returns:
            None
        """
        assert self.__fileData is not None
        self.__fileData.updateFileTag(frame, value)

    def getReleaseURL(self, artist: str, release: str) -> str:
        """Gets release URL from first match in RYM search.

        Args:
            artist: The name of the artist to search for.
            release: The name of the release to search for.
        Returns:
            The URL of the release.
        """
        assert self.__rymData is not None
        return self.__rymData.getReleaseURL(artist, release)

    def getIssueURLs(self, releaseUrl: str) -> list[str]:
        """Gets URLs for every issue of given release.

        Each issue of a given release has a URL ending either with its own number or
        '.p' indicating it is the primary issue. The primary issue url is not the main
        url (without any suffix).

        Args:
            releaseUrl: The URL of the release to search for.
        Returns:
            A list of URLs.
        """
        assert self.__rymData is not None
        return self.__rymData.getIssueURLs(releaseUrl)

    def getIssueTags(self, issueUrl: str) -> dict[domain.RYMtags, str]:
        """Gets tags from issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A dictionnary {key: value} where key is a RYMtags member and value its
            corresponding value.
        """
        assert self.__rymData is not None
        return self.__rymData.getIssueTags(issueUrl)

    def getIssueTracklist(self, issueUrl: str) -> dict[str, str]:
        """Gets a tracklist from an issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A dictionnary {key: value} where key is a tracklist number and value a track name.
        """
        assert self.__rymData is not None
        return self.__rymData.getIssueTracklist(issueUrl)

    def getIssueCredits(self, issueUrl: str) -> dict[str, dict[str, str]]:
        """Gets credits from an issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A nested dictionnary {artist, {role, tracks}} where artist is an artist name,
            role is the credited role and tracks is a string of tracks
            where the artist is credited.
            When tracks is empty, it assumed that the artist has the given role on every track.
        """
        assert self.__rymData is not None
        return self.__rymData.getIssueCredits(issueUrl)
