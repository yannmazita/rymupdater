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

    @staticmethod
    def getReleaseURL(driver: webdriver.Chrome, artist: str, release: str) -> str:
        """
            Get album URL from first match in RYM search.
            Args:
                driver: Selenium web driver.
                artist: The artist to search for.
                release: The release to search for.
            Returns:
                str: The URL.
        """
        driver.get(RYMtags.__getSearchURL(artist, release))

        releaseLocator = locate_with(By.CLASS_NAME, "searchpage").below({By.TAG_NAME: "h3"})
        element = driver.find_element(releaseLocator)
        url: str = element.get_attribute("href")
        return url

    def getTagsFromRYM(self, driver: webdriver.Chrome, artist: str, release: str) -> dict[AudioTags, str]:
        dic = {}
        url: str = self.getReleaseURL(driver, artist, release)
        driver.get(url)

        mainTagLocator = locate_with(By.CLASS_NAME, "info_hdr")
        elements = driver.find_elements(mainTagLocator)


        return dic

rym = RYMtags()
driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
print(rym.getReleaseURL(driver, "The Knife", "Silent Shout"))
