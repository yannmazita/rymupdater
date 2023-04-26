from src.application.domain import RYMtags

from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.relative_locator import locate_with
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

    def getTagsFromAlbumInfo(self, releaseUrl: str) -> dict[RYMtags, str]:
        """
        Get release tags from first match in RYM search.
        Args:
            releaseUrl: The URL of the release to search for.
        Returns:
            dict[RYMtags, str]: RYM tags and their value.
        """
        dic: dict[RYMtags, str] = {}
        self.__getPage(releaseUrl)

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
            element: WebElement = issue.find_element(By.CLASS_NAME, "sametitle")
            # With these locators the URLs are found twice in the DOM.
            # This try/except block allows to go through the first occurences of the URLs.
            try:
                primaryIndicator: WebElement = issue.find_element(
                    By.CLASS_NAME, "primary_indicator"
                )
                if flag:
                    break
                else:
                    flag = True
            except NoSuchElementException:
                pass
            urls.append(element.get_attribute("href"))

        return urls

    def getIssueTracklist(self, issueUrl: str) -> dict[str, str]:
        dic: dict[str, str] = {}
        self.__getPage(issueUrl)
        tracks: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//div[@itemprop='track']"
        )

        for track in tracks:
            tracklistNum: WebElement = track.find_element(
                By.XPATH, "./span[@class='tracklist_num']"
            )
            tracklistTitle: WebElement = track.find_element(
                By.XPATH,
                "./span[@class='tracklist_title']/span[@itemprop='name']/span[@class='rendered_text']",
            )
            dic[tracklistNum.get_attribute("innerText")] = tracklistTitle.get_attribute(
                "innerText"
            )
        return dic


rym = RYMdata()
# rym.getIssueTracklist(rym.getIssueURLs(rym.getReleaseURL("The Knife", "Silent Shout"))[0]))
