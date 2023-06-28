from src.data.localDao import FileData
from src.data.webDao import RYMdata
import src.application.domain as domain

from pathlib import Path
from datetime import datetime
from collections.abc import Iterator
from itertools import zip_longest
import re


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

    def __getTagsFromFile(self) -> dict[domain.ID3Keys, str]:
        """Gets ID3 tags from loaded file.

        Returns:
            A dictionnary {key: value} where key is an ID3Keys member and value
            the first ID3 frame with the given name.
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

    def __updateTags(
        self,
        rymTags: dict[domain.RYMtags, str],
        id3Tags: dict[domain.ID3Keys, list[str]],
    ):
        """Updates ID3 frames in loaded file using rymTags and id3Tags.

        This will iterate through the keys in the dictionnaries and update the file
        accordingly.
        """
        pass

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

    def __formatLabelAndLabelID(
        self, retrievedTags: dict[domain.RYMtags, str]
    ) -> dict[domain.RYMtags, str]:
        """Formats LABEL and LABEL_ID entries in RYMtags dictionnary.

        Both label and label id get retrieved in the same RYMtags element from rateyourmusic.com.
        This method ensures the dictionnary making up the retrieved tags has both of them
        with their own key.

        Args:
            retrievedTags: The dictionnary of tags retrieved from rateyourmusic.com.
        Returns:
            The modified dictionnary.
        """
        updatedDictionnary: dict[domain.RYMtags, str] = retrievedTags
        labelAndLabelID: str = updatedDictionnary[domain.RYMtags.LABEL_AND_LABEL_ID]
        labelSplit: list[str] = [i.lstrip() for i in labelAndLabelID.split(" /")]
        updatedDictionnary.pop(domain.RYMtags.LABEL_AND_LABEL_ID)
        updatedDictionnary[domain.RYMtags.LABEL] = labelSplit[0]
        updatedDictionnary[domain.RYMtags.LABEL_ID] = labelSplit[1]
        return updatedDictionnary

    def __formatReleaseTime(
        self, retrievedTags: dict[domain.RYMtags, str]
    ) -> dict[domain.RYMtags, str]:
        """Formats RELEASE_TIME entry in RYMtags dictionnary.

        The release time might get retrieved in various date formats from rateyourmusic.com.
        This method ensures the dictionnary making up the retrieved tags has
        a standard date format for the release time.

        Args:
            retrievedTags: The dictionnary of tags retrieved from rateyourmusic.com.
        Returns:
            The formated dictionnary.
        """
        updatedDictionnary: dict[domain.RYMtags, str] = retrievedTags
        rDate: str = updatedDictionnary[domain.RYMtags.RELEASE_TIME]
        if not rDate.isdigit():
            updatedDictionnary[domain.RYMtags.RELEASE_TIME] = datetime.strptime(
                rDate, "%d %B %Y"
            ).strftime("%d-%m-%Y")
        return updatedDictionnary

    def __formatLanguageCode(
        self, retrievedTags: dict[domain.RYMtags, str]
    ) -> dict[domain.RYMtags, str]:
        """Formats LANGUAGE entry in RYMtags dictionnary.

        The issue language is retrieved in full form instead of the of the ISO 639-2
        standard for language codes.

        Args:
            retrievedTags: The dictionnary of tags retrieved from rateyourmusic.com.
        Returns:
            The formated dictionnary.
        """
        updatedDictionnary: dict[domain.RYMtags, str] = retrievedTags
        longLanguageFormat: str = updatedDictionnary[domain.RYMtags.LANGUAGE]
        iso6392LanguageFormat: str = domain.Iso6392Codes[longLanguageFormat].value
        updatedDictionnary[domain.RYMtags.LANGUAGE] = iso6392LanguageFormat
        return updatedDictionnary

    def __formatRYMTagsDictionnary(
        self, retrievedTags: dict[domain.RYMtags, str]
    ) -> dict[domain.RYMtags, str]:
        """Formats tags retrieved from rateyourmusic.com.

        RYMtags dictionnaries may not have the expected format. This method ensures that each
        RYMtags pair can be successfully mapped to an ID3Keys pair with usual formating.

        Args:
            retrievedTags: The dictionnary of tags retrieved from rateyourmusic.com.
        Returns:
            The formated dictionnary.
        """
        updatedDictionnary: dict[domain.RYMtags, str] = self.__formatLanguageCode(
            self.__formatLabelAndLabelID(self.__formatReleaseTime(retrievedTags))
        )
        return updatedDictionnary

    def __formatSortingTags(
        self, retrievedTags: dict[domain.ID3Keys, str]
    ) -> dict[domain.ID3Keys, str]:
        """Formats sorting entries in ID3Keys dictionnary.

        By default sorting tags are not populated. This method ensures that each sorting
        tag has the correct value.

        Args:
            retrievedTags: The dictionnary of tags retrieved from the MP3 file.
        Returns:
            The formated dictionnary.
        """
        updatedDictionnary: dict[domain.ID3Keys, str] = retrievedTags

        for sortKey in ["PERFORMER", "ALBUM_ARTIST", "COMPOSER"]:
            updatedDictionnary.setdefault(domain.ID3Keys[sortKey], "")

        artist: str = updatedDictionnary[domain.ID3Keys.ARTIST]

        if len(updatedDictionnary[domain.ID3Keys.PERFORMER]) == 0:
            updatedDictionnary[domain.ID3Keys.PERFORMER] = artist
        if re.search("^The ", updatedDictionnary[domain.ID3Keys.PERFORMER]):
            performerSort: str = updatedDictionnary[domain.ID3Keys.PERFORMER][
                0
            ].replace("The ", "", 1)
        else:
            pass

        if len(updatedDictionnary[domain.ID3Keys.ALBUM_ARTIST]) == 0:
            updatedDictionnary[domain.ID3Keys.ALBUM_ARTIST] = artist
        if re.search("^The ", updatedDictionnary[domain.ID3Keys.ALBUM_ARTIST]):
            albumArtistSort: str = updatedDictionnary[domain.ID3Keys.ALBUM_ARTIST][
                0
            ].replace("The ", "", 1)
        else:
            pass

        if len(updatedDictionnary[domain.ID3Keys.COMPOSER]) == 0:
            pass
        else:
            if re.search("^The ", updatedDictionnary[domain.ID3Keys.COMPOSER]):
                composerSort: str = updatedDictionnary[domain.ID3Keys.COMPOSER][
                    0
                ].replace("The ", "", 1)

        # Files are expected to have at least artist and album tags.
        if re.search("^The ", updatedDictionnary[domain.ID3Keys.ARTIST]):
            artistSort: str = updatedDictionnary[domain.ID3Keys.ARTIST].replace(
                "The ", ""
            )
        if re.search("^The ", updatedDictionnary[domain.ID3Keys.ALBUM]):
            albumSort: str = updatedDictionnary[domain.ID3Keys.ALBUM].replace(
                "The ", ""
            )

        try:
            updatedDictionnary[domain.ID3Keys.ARTIST_SORT] = artistSort
        except UnboundLocalError:
            pass
        try:
            updatedDictionnary[domain.ID3Keys.ALBUM_SORT_ORDER] = albumSort
        except UnboundLocalError:
            pass
        try:
            updatedDictionnary[domain.ID3Keys.PERFORMER_SORT] = performerSort
        except UnboundLocalError:
            pass
        try:
            updatedDictionnary[domain.ID3Keys.ALBUM_ARTIST_SORT_ORDER] = albumArtistSort
        except UnboundLocalError:
            pass
        try:
            updatedDictionnary[domain.ID3Keys.COMPOSER_SORT_ORDER] = composerSort
        except UnboundLocalError:
            pass
        return updatedDictionnary

    def __formatID3KeysTagDictionnary(
        self, retrievedTags: dict[domain.ID3Keys, str]
    ) -> dict[domain.ID3Keys, str]:
        """Formats tags retrieved from audio file.

        Tags in audio files may miss sorting keys or other tags. This method ensures
        id3 keys are properly populated.

        Args:
            retrievedTags: The dictionnary of tags retrieved from the MP3 file.
        Returns:
            The formated dictionnary.
        """
        updatedDictionnary: dict[domain.ID3Keys, str] = self.__formatSortingTags(
            retrievedTags
        )
        return updatedDictionnary

    def tagLibrary(self, musicDirectory: Path) -> Iterator[Path]:
        """Tags every .mp3 file in the music library.

        Args:
            musicDirectory: The path of the music directory.
        Returns:
            Iterator of audio file paths.
        """
        self.__initializeData(musicDirectory)
        currentArtist: str = ""
        currentRelease: str = ""
        currentReleaseUrl: str = ""
        currentIssueUrl: str = ""
        while self.__loadNextFile() is not False:
            assert self.__fileData is not None
            yield self.__fileData.currentFilePath

            initialTags: dict[domain.ID3Keys, str] = self.__getTagsFromFile()
            artist: str = initialTags[domain.ID3Keys.ARTIST]
            release: str = initialTags[domain.ID3Keys.ALBUM]
            if (artist != currentArtist) or (release != currentRelease):
                currentArtist = artist
                currentRelease = release
                currentReleaseUrl = self.__getReleaseURL(artist, release)
                currentIssueUrl: str = self.__getIssueURLs(currentReleaseUrl)[0]

            rymTags: dict[domain.RYMtags, str] = self.__formatRYMTagsDictionnary(
                self.__getIssueTags(currentIssueUrl)
            )
            id3Tags: dict[
                domain.ID3Keys, str
            ] = self.__formatID3KeysTagDictionnary(initialTags)

            for rymTag in rymTags:
                self.__updateFileTag(domain.ID3Keys[rymTag.name], rymTags[rymTag])

            for id3Tag in id3Tags:
                try:
                    self.__updateFileTag(id3Tag, id3Tags[id3Tag])
                except IndexError:
                    pass
