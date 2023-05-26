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
    """RYM data access.

    A RYMdata instance is used as a data access object (DAO) to be used elsewhere.
    Any service requiring access to rateyourmusic.com should be implemented in this class.
    A release is merely an artist name and single/EP/album etc name. Each release has at lease one
    issue. Issues of the same release can have different tracks, label IDs etc.
    """

    def __init__(self):
        """Initiliazes the instance."""
        self.__driver: webdriver.Chrome = webdriver.Chrome(
            service=ChromiumService(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            )
        )

    def __getPage(self, url: str) -> None:
        if self.__driver.current_url != url:
            self.__driver.get(url)

    def getReleaseURL(self, artist: str, release: str) -> str:
        """Gets release URL from first match in RYM search.

        Args:
            artist: The name of the artist to search for.
            release: The name of the release to search for.
        Returns:
            The URL of the release.
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
        """Gets URLs for every issue of given release.

        Each issue of a given release has a URL ending either with its own number or
        '.p' indicating it is the primary issue. The primary issue url is not the main
        url (without any suffix).

        Args:
            releaseUrl: The URL of the release to search for.
        Returns:
            A list of URLs. For example for the release 'The Knife - Silent Shout':

                [
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout.p/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-3/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-6/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-7/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-2/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-1/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-5/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-8/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-9/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-4/",
                    "https://rateyourmusic.com/release/album/the-knife/silent-shout-12/",
                ]

            Note that issues 10 and 11 are missing, they both redirect to the main URL:
                "https://rateyourmusic.com/release/album/the-knife/silent-shout"
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
        """Gets tags from issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A dictionnary {key: value} where key is a RYMtags member and value its
            corresponding value. For example the primary issue of The Knife - Silent Shout":

                {<RYMtags.ARTIST: 'Artist'>: 'The Knife',
                 <RYMtags.DATE: 'Released'>: '20 March 2006',
                 <RYMtags.RECORDING_TIME: 'Recorded'>: 'March 2004 - November 2005',
                 ...,
                 <RYMtags.LANGUAGE: 'Language'>: 'English'}
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
        """Gets tracklist from issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A dictionnary {key: value} where key is a tracklist number and value a track name.
            For example the BRILCD103DLX issue of "The Knife - Silent Shout":

                {
                    "Disc: 1": "Disk I - Silent Shout",
                    "1.1": "Silent Shout",
                    "1.2": "Neverland",
                    ...,
                    "Disc: 2": "Disk II - Silent Shout an Audiovisual Experience (Live Audio)",
                    "2.1": "Pass This On",
                    "2.2": "The Captain",
                    ...,
                    "Disc: 3": "Disk III - Silent Shout an Audiovisual Experience (DVD) Live Recording in 5.1",
                    "3.1": "Pass This On",
                    ...,
                    "3.22": "When I Found the Knife (Short Film)",
                }
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

            # Track titles always have tracklist numbers and disc titles are always bold.
            # For example, if on the same disc, track 1-10 are regular audio files and track 11-22
            # are music videos then the ul where div[@itemprop='track'] elements are found will
            # feature a "track" (ie: li[@class='track']/div[@itemprop='track'])
            # between tracks 1-10 and 11-22 without a track number and with
            # italic inner text (not bold).
            # Such "tracks" are ignored.
            trackNumInnerText: str = tracklistNum.get_attribute("innerText").strip()
            trackTitleInnerText: str = tracklistTitle.get_attribute("innerText")
            element: WebElement | None = None
            if not trackNumInnerText:
                try:
                    element = tracklistTitle.find_element(By.TAG_NAME, "b")
                except NoSuchElementException:
                    pass
                if element is not None:
                    discNumber += 1
                    tracklist[f"Disc: {discNumber}"] = trackTitleInnerText
            else:
                # rateyourmusic track numbers may not have the format
                # '{disc number}.{track number}'
                if discNumber != 0 and trackNumInnerText.isdigit():
                    tracklist[f"{discNumber}.{trackNumInnerText}"] = trackTitleInnerText
                else:
                    tracklist[trackNumInnerText] = trackTitleInnerText

        return tracklist

    # minor_credits_ forgotten
    def getIssueCredits(self, issueUrl: str) -> dict[str, dict[str, str]]:
        """Get credits from issue URL.

        Args:
            issueUrl: The URL of the issue.
        Returns:
            A nested dictionnary {artist, {role, tracks}} where artist is an artist name,
            role is the credited role and tracks is a string of tracks
            where the artist is credited.
            When tracks is empty, it assumed that the artist has the given role on every track.
            For example the primary issue of "The Knife - Silent Shout":

                {
                    "The Knife": {
                        "music": "",
                        "lyrics": "",
                        "recording engineer": "",
                        "programming": "",
                        "performer": "",
                        "producer": "",
                        "vocals": "",
                        "mixing": "",
                    },
                    "Henrik Jonsson": {"mastering engineer": ""},
                    "Johan Toorell": {},
                    "Jay-Jay Johanson": {"vocals": "6", "lyrics": "6"},
                    "Christoffer Berg": {"mixing": "1-7, 9, 11"},
                    "Pelle Gunnerfeldt": {"mixing": "8, 10"},
                }
        """

        issueCredits: dict[str, dict[str, str]] = {}
        self.__getPage(issueUrl)
        mainCreds: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//ul[@id='credits_']/li"
        )
        minorCreds: list[WebElement] = self.__driver.find_elements(
            By.XPATH, "//div[@id='minor_credits_']/li"
        )
        creds: list[WebElement] = mainCreds + minorCreds

        for credit in creds:
            # Credited artist has a link to their RYM page
            try:
                artist: WebElement = credit.find_element(By.CLASS_NAME, "artist")
            # Credited artist doesn't have a link to their RYM page
            except NoSuchElementException:
                try:
                    artist: WebElement = credit.find_element(By.TAG_NAME, "span")
                # Fails on empty li item
                except NoSuchElementException:
                    pass

            rawRoles: list[WebElement] = credit.find_elements(
                By.CLASS_NAME, "role_name"
            )
            roles: dict[str, str] = {}
            for role in rawRoles:
                tracksText: str = ""
                try:
                    tracksText = role.find_element(
                        By.CLASS_NAME, "role_tracks"
                    ).get_attribute("innerText")
                except NoSuchElementException:
                    pass
                try:
                    roleText: str = role.get_attribute("innerText")
                except UnboundLocalError:
                    roleText: str = role.find_element(
                        By.XPATH, "./span[@class='rendered_text']"
                    ).get_attribute("innerText")
                # Bare get_attribute on spans sometimes also gets text from childs
                try:
                    newRoleText: str = roleText.replace(tracksText, "")
                    if newRoleText == "":
                        roles[roleText] = tracksText
                    else:
                        roles[newRoleText] = tracksText
                except UnboundLocalError:
                    pass

            # track_minor_show_ class elements are not artist names.
            # they are part of small menu thing
            if artist.get_attribute("id") != "track_minor_show_":
                issueCredits[artist.get_attribute("innerText")] = roles

        return issueCredits
