from src.application.domain import RYMtags

from urllib.parse import quote

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
        self.__driver.get(searchUrl)

        element = self.__driver.find_element(By.CLASS_NAME, "searchpage")
        url: str = element.get_attribute("href")
        return url

    def getTagsFromAlbumInfo(self, releaseUrl: str) -> dict[RYMtags, str]:
        """
        Get release tags from first match in RYM search.
        Args:
            releaseUrl: The URL of the release to search for.
        Returns:
            dict[RYMtags, str]: RYM tags and their value.
        """
        dic: dict[RYMtags, str] = {}
        self.__driver.get(releaseUrl)

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
                # dic[RYMtags(head.text)] = ",".join([i.text for i in data])
                dic[RYMtags(head.text)] = data.text.replace("\n", ", ")
            except ValueError:
                # Tag is not defined in RYMtags enum.
                pass

        return dic


rym = RYMdata()
print(rym.getTagsFromAlbumInfo(rym.getReleaseURL("The Knife", "Silent Shout")))
