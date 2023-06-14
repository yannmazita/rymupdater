from src.data.localDao import FileData
from src.data.webDao import RYMdata
import src.application.domain as domain

from pathlib import Path


class RYMupdater:
    """RYM main services"""

    def __init__(self):
        """Initialiazes the instance."""
        self.__fileData: FileData | None = None
        self.__rymData: RYMdata | None = None

    def __initializeData(self, musicDirectory: Path) -> None:
        """Initialiazes data access objects.

        Args:
            musicDirectory: The path of the music directory.
        Returns:
            None.
        """
        self.__fileData = FileData(musicDirectory)
        self.__rymData = RYMdata()

    def __loadNextFile(self) -> bool:
        """Loads next audio file.

        Returns:
            A boolean, true if file was loaded, false otherwise.
        """
        assert self.__fileData is not None
        return self.__fileData.loadNextFile()

    def __getTagsFromFile(self) -> dict[domain.ID3Keys, list[str]]:
        """Gets ID3 tags from loaded file.

        Returns:
            A dictionnary {key: value} where key is an ID3Keys member and value
            a list of ID3 frames with the given name.
        """
        assert self.__fileData is not None
        return self.__fileData.getTagsFromFile()

    def __updateFileTag(self, frame: domain.ID3Keys, value: str) -> None:
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

    def __getReleaseURL(self, artist: str, release: str) -> str:
        """Gets release URL from first match in RYM search.

        Args:
            artist: The name of the artist to search for.
            release: The name of the release to search for.
        Returns:
            The URL of the release.
        """
        assert self.__rymData is not None
        return self.__rymData.getReleaseURL(artist, release)

    def __getIssueURLs(self, releaseUrl: str) -> list[str]:
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

    def __getIssueTags(self, issueUrl: str) -> dict[domain.RYMtags, str]:
        """Gets tags from issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A dictionnary {key: value} where key is a RYMtags member and value its
            corresponding value.
        """
        assert self.__rymData is not None
        return self.__rymData.getIssueTags(issueUrl)

    def __getIssueTracklist(self, issueUrl: str) -> dict[str, str]:
        """Gets a tracklist from an issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A dictionnary {key: value} where key is a tracklist number and value a track name.
        """
        assert self.__rymData is not None
        return self.__rymData.getIssueTracklist(issueUrl)

    def __getIssueCredits(self, issueUrl: str) -> dict[str, dict[str, str]]:
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

    def __separateIssueDetails(
        self, retrievedTags: dict[domain.RYMtags, str]
    ) -> dict[domain.RYMtags, str]:
        """Separates label name from label id.

        Both label and label id get retrieved in the same RYMtags element from the Internet.
        This method ensures the dictionnary making up the retrieved tags has both of them
        with their own key.

        Args:
            retrievedTags: The dictionnary of tags retrieved from rateyourmusic.com.
        Returns:
            The modified dictionnary.
        """
        updatedDictionnary: dict[domain.RYMtags, str] = retrievedTags
        labelAndLabelID: str = updatedDictionnary[domain.RYMtags.LABEL_AND_LABEL_ID]
        labelSplit: list[str] = labelAndLabelID.split(" / ")
        updatedDictionnary.pop(domain.RYMtags.LABEL_AND_LABEL_ID)
        updatedDictionnary[domain.RYMtags.LABEL] = labelSplit[0]
        updatedDictionnary[domain.RYMtags.LABEL_ID] = labelSplit[1]
        return updatedDictionnary

    def tagLibrary(self, musicDirectory: Path) -> None:
        """Tags every .mp3 file in the music library.

        Args:
            musicDirectory: The path of the music directory.
        Returns:
            None
        """
        self.__initializeData(musicDirectory)
        currentArtist: str = ""
        currentRelease: str = ""
        currentReleaseUrl: str = ""
        currentIssueUrl: str = ""
        while self.__loadNextFile() is not False:
            initialTags: dict[domain.ID3Keys, list[str]] = self.__getTagsFromFile()
            artist: str = initialTags[domain.ID3Keys.ARTIST][0]
            release: str = initialTags[domain.ID3Keys.ALBUM][0]
            if (artist != currentArtist) or (release != currentRelease):
                currentArtist = artist
                currentRelease = release
                currentReleaseUrl = self.__getReleaseURL(artist, release)
                currentIssueUrl: str = self.__getIssueURLs(currentReleaseUrl)[0]
            tags: dict[domain.RYMtags, str] = self.__separateIssueDetails(
                self.__getIssueTags(currentIssueUrl)
            )

            for rymTag in tags:
                self.__updateFileTag(domain.ID3Keys[rymTag.name], tags[rymTag])
