from src.application.domain import RYMtags

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class RYMdata:
    """RYM data access"""

    def __init__(self):
        self.__driver: webdriver.Chrome = webdriver.Chrome(
            service=ChromiumService(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        )

    def __getPage(self, url: str) -> None:
        if self.__driver.current_url != url:
            self.__driver.get(url)

    def getReleaseURL(self, artist: str, release: str) -> str:
        """
        Get release URL from first match in RYM search.
        Args:
            artist: The artist to search for.
            release: The release to search for.
        Returns:
            str: The URL.
        """
        urlStart: str = "https://rateyourmusic.com/search?searchterm="
        # urlEnd: str = "&searchtype=l"
        body: str = quote(artist + release, safe="")
        searchUrl: str = urlStart + body
        self.__getPage(searchUrl)

        element = self.__driver.find_element(By.CLASS_NAME, "searchpage")
        url: str = element.get_attribute("href")

        return url

    def getIssueURLs(self, releaseUrl: str) -> list[str]:
        """
        Get URLs for every issue of given release.
        Args:
            releaseUrl: The URL of the release to search for.
        Returns:
            list[str]: List of URLs.
        """
        self.__getPage(releaseUrl)
        urls: list[str] = []
        issues: list[WebElement] = self.__driver.find_elements(
            By.CLASS_NAME, "issue_title"
        )

        flag: bool = False
        for issue in issues:
            try:
                # issues contains the same elements twice, this block avoids iterating twice
                primaryIndicator: WebElement = issue.find_element(
                    By.CLASS_NAME, "primary_indicator"
                )
                if flag:
                    break
                else:
                    flag = True
            except NoSuchElementException:
                pass

            try:
                # Some issue urls (like unauthorized issues) may not be found
                # in the "sametitle" class.
                element: WebElement = issue.find_element(By.CLASS_NAME, "sametitle")
                link: str = element.get_attribute("href")
                if link is None:
                    # If the current webdriver url is equal to the current issue url,
                    # there is no link to click on and link is None.
                    urls.append(self.__driver.current_url)
                else:
                    urls.append(link)
            except NoSuchElementException:
                element: WebElement = issue.find_element(By.TAG_NAME, "a")
                link: str = element.get_attribute("href")
                urls.append(link)

        return urls

    def getIssueTags(self, issueUrl: str) -> dict[RYMtags, str]:
        """
        Get tags from issue URL.
        Args:
            issueUrl: The URL of the issue.
        Returns:
            dict[RYMtags, str]: RYM tags and their value.
        """
        dic: dict[RYMtags, str] = {}
        self.__getPage(issueUrl)

        albumInfoRows: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//table[@class='album_info']/tbody/tr"
        )

        for row in albumInfoRows:
            head: WebElement = row.find_element(
                By.CLASS_NAME, "info_hdr"
            )  # head for current row
            data: WebElement = row.find_element(
                By.TAG_NAME, "td"
            )  # data for current row
            try:
                dic[RYMtags(head.text)] = data.text.replace("\n", ", ")
            except ValueError:
                # Tag is not defined in RYMtags enum.
                pass

        return dic

    def getIssueTracklist(self, issueUrl: str) -> dict[str, str]:
        """
        Get tracklist from issue URL.
        Args:
            issueUrl: The URL of the issue.
        Returns:
            dict[str, str]: Dictionnary of tracklist numbers and tracklist titles.
        """
        tracklist: dict[str, str] = {}
        self.__getPage(issueUrl)
        tracks: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//div[@itemprop='track']"
        )
        discNumber: int = 0

        for track in tracks:
            tracklistNum: WebElement = track.find_element(
                By.XPATH, "./span[@class='tracklist_num']"
            )
            # For some reason using .text on spans returns empty strings.
            tracklistTitle: WebElement = track.find_element(
                By.XPATH,
                "./span[@class='tracklist_title']/span[@itemprop='name']/span[@class='rendered_text']",
            )

            if tracklistNum.get_attribute("innerText") == "":
                # Disc titles do not have tracklist numbers.
                tracklist[f"Disc: {discNumber + 1}"] = tracklistTitle.get_attribute(
                    "innerText"
                )
            else:
                tracklist[
                    tracklistNum.get_attribute("innerText")
                ] = tracklistTitle.get_attribute("innerText")
        return tracklist

    def getIssueCredits(self, issueUrl: str) -> dict[str, dict[str, list[str]]]:
        """
        Get credits from issue URL.
        Args:
            issueUrl: The URL of the issue.
        Returns:
            dict[str, dict[str, list[str]]]: Issue credits
        """
        issueCredits: dict[str, dict[str, list[str]]] = {}
        self.__getPage(issueUrl)
        creds: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//ul[@id='credits_']/li"
        )

        for credit in creds:
            try:
                # Credited artist has a link to their RYM page
                artist: WebElement = credit.find_element(By.CLASS_NAME, "artist")
            except NoSuchElementException:
                # Credited artist doesn't have a link to their RYM page
                artist: WebElement = credit.find_element(By.TAG_NAME, "span")

            rawRoles: list[WebElement] = credit.find_elements(
                By.CLASS_NAME, "role_name"
            )
            roles: dict[str, list[str]] = {}
            for role in rawRoles:
                rawTracks: list[WebElement] = role.find_elements(
                    By.CLASS_NAME, "role_tracks"
                )
                roles[role.get_attribute("innerText")] = [
                    track.get_attribute("innerText") for track in rawTracks
                ]

            # track_minor_show_ class elements are not artist names.
            if artist.get_attribute("id") != "track_minor_show_":
                issueCredits[artist.get_attribute("innerText")] = roles

        return issueCredits
