from src.application.domain import RYMtags
from src.application.domain import DiscogsTags

from urllib.parse import quote
import discogs_client

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class RYMdata:
    """RYM data access"""

    def __init__(self):
        self.__driver: webdriver.Chrome = webdriver.Chrome(
            service=ChromiumService(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        )

    @staticmethod
    def __getSearchURL(artist: str, release: str) -> str:
        """
        Get search URL for artist and release.
        Args:
            artist: The artist to search for.
            release: The release (album/EP...) to search for.
        Returns:
            str: The URL.
        """
        urlStart: str = "https://rateyourmusic.com/search?searchterm="
        # urlEnd: str = "&searchtype=l"
        body: str = quote(artist + release, safe="")
        return urlStart + body

    def getReleaseURL(self, artist: str, release: str) -> str:
        """
        Get release URL from first match in RYM search.
        Args:
            artist: The artist to search for.
            release: The release to search for.
        Returns:
            str: The URL.
        """
        self.__driver.get(RYMdata.__getSearchURL(artist, release))

        element = self.__driver.find_element(By.CLASS_NAME, "searchpage")
        url: str = element.get_attribute("href")
        return url

    def getTagsFromRYM(self, artist: str, release: str) -> dict[RYMtags, str]:
        """
        Get release tags from first match in RYM search.
        Args:
            artist: The artist to search for.
            release: The release to search for.
        Returns:
            dict[RYMtags, str]: RYM tags and their value.
        """
        dic: dict[RYMtags, str] = {}
        url: str = self.getReleaseURL(artist, release)
        self.__driver.get(url)

        rows: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//table[@class='album_info']/tbody/tr"
        )

        for row in rows:
            head: WebElement = row.find_element(
                By.CLASS_NAME, "info_hdr"
            )  # head for current row
            data: WebElement = row.find_element(
                By.TAG_NAME, "td"
            )  # data for current row
            try:
                # dic[RYMtags(head.text)] = ",".join([i.text for i in data])
                dic[RYMtags(head.text)] = data.text.replace("\n", ", ")
            except ValueError:
                # Tag is not defined in RYMtags enum.
                pass

        return dic


class DiscogsData:
    """Discogs data access"""

    def __init__(self, token: str):
        self.__client: discogs_client.Client = discogs_client.Client(
            user_agent="rymupdater/0.1", user_token=token
        )

    def __getReleaseID(self, title: list[str] = [], labelID: str = "") -> str:
        """
        Get Discogs release ID.
        Args:
            title: List of ["title", "release name"].
            labelID: Release label ID.
        Returns:
            str: Release ID.
        """
        results = self.__client.search(
            artist=title[0],
            release_title=title[1],
            type="release",
            barcode=labelID,
        )
        releaseID: str = results.page(1)[0].id

        return releaseID

    def getTagsFromDiscogs(
        self, title: list[str] = [], labelID: str = ""
    ) -> dict[DiscogsTags, str]:
        """
        Get release tags from first match in Discogs search.
        Args:
            title: List of ["title", "release name"].
            labelID: Release label ID.
        Returns:
            dict[DiscogsTags, str]: Discogs tags and their value.
        """
        dic: dict[DiscogsTags, str] = {}
        id = self.__getReleaseID(title, labelID)
        release = self.__client.release(id)

        return dic


token = ""  # put personal access token here
discogs: DiscogsData = DiscogsData(token)
discogs.getTagsFromDiscogs(["The Knife", "Silent Shout"], "8686096500307")
