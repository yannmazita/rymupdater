from src.application.domain import AudioTags
from src.application.domain import RYMtags

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from selenium.webdriver.common.by import By


class RYMdata:
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
        self.__driver.get(RYMdata.__getSearchURL(artist, release))

        element = self.__driver.find_element(By.CLASS_NAME, "searchpage")
        url: str = element.get_attribute("href")
        return url

    def getTagsFromRYM(self, artist: str, release: str) -> dict[AudioTags, str]:
        """
            Get release tags from firt match in RYM search.
            Args:
                artist: The artist to search for.
                release: The release to search for.
            Returns:

        """
        dic = {}
        url: str = self.getReleaseURL(artist, release)
        self.__driver.get(url)

        #album_info = self.__driver.find_element(By.XPATH, "//table[@class='album_info']/tbody")
        #rows = album_info.find_elements(By.XPATH, "./tr")
        rows = self.__driver.find_elements(By.XPATH, "//table[@class='album_info']/tbody/tr")

        for row in rows:
            head = row.find_element(By.CLASS_NAME, "info_hdr")  # head for current row
            data = row.find_elements(By.TAG_NAME, "td")         # data for current row
            try:
                dic[RYMtags(head.text)]
            except ValueError:
                pass
        return dic

rym = RYMdata()
print(rym.getReleaseURL("The Knife", "Silent Shout"))
rym.getTagsFromRYM("The Knife", "Silent Shout")
