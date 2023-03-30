from src.application.domain import AudioTags

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with


class RYMtags:
    """RYM data access"""
    def __init__(self):
        self.__driver: webdriver.Chrome = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

    @staticmethod
    def __getSearchURL(artist: str, release: str) -> str:
        """
            Get search URL for artist and release.
            Args:
                artist: The artist to search for.
                album: The release (album/EP...) to search for.
            Returns:
                str: The URL.
        """
        urlStart: str = "https://rateyourmusic.com/search?searchterm="
        #urlEnd: str = "&searchtype=l"
        body: str = quote(artist + release, safe='')
        return urlStart + body

    def getReleaseURL(self, artist: str, release: str) -> str:
        """
            Get album URL from first match in RYM search.
            Args:
                artist: The artist to search for.
                release: The release to search for.
            Returns:
                str: The URL.
        """
        self.__driver.get(RYMtags.__getSearchURL(artist, release))

        element = self.__driver.find_element(By.CLASS_NAME, "searchpage")
        url: str = element.get_attribute("href")
        return url

    def getTagsFromRYM(self, artist: str, release: str) -> dict[AudioTags, str]:
        dic = {}
        url: str = self.getReleaseURL(artist, release)
        self.__driver.get(url)

        tags = self.__driver.find_elements(By.CLASS_NAME, "info_hdr")
        values = self.__driver.find_elements(By.XPATH,
                                                "//table[@class='album_info']/tbody/tr/td")
        #[print(i.text) for i in tags]
        #[print(i.text) for i in values]

        return dic

#rym = RYMtags()
#print(rym.getReleaseURL("The Knife", "Silent Shout"))
#rym.getTagsFromRYM("The Knife", "Silent Shout")
