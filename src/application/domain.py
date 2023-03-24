#from mutagen.easyid3 import EasyID3

class MusicFile:
    """Music file tags"""
    def __init__(self) -> None:
        self.__title: str = ""
        self.__artist: str = ""
        self.__album: str = ""
        self.__albumartist: str = ""
        self.__date: str = ""
        self.__description: str = ""
        self.__discsubtitle: str = ""
        self.__genre: str = ""
        self.__labelid: str = ""
        self.__language: str = ""
        self.__organization: str = ""
        self.__performer: str = ""
        self.__tracknumber: str = ""
        self.__discnumber: str = ""
    

    @property
    def title(self) -> str:
        """Song title field"""
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = title

    @property
    def artist(self) -> str:
        """Artist name field"""
        return self.__artist

    @artist.setter
    def artist(self, artist: str):
        self.__artist = artist

    @property
    def album(self) -> str:
        """Album name field"""
        return self.__album

    @album.setter
    def album(self, album: str) -> None:
        self.__album = album

    @property
    def albumartist(self) -> str:
        """Album artist field"""
        return self.__albumartist

    @albumartist.setter
    def albumartist(self, albumArtist) -> None:
        self.__albumartist = albumArtist

    @property
    def date(self) -> str:
        """Song date field"""
        return self.__date

    @date.setter
    def date(self, date: str) -> None:
        self.__date = date

    @property
    def description(self) -> str:
        """Song description field"""
        return self.__description

    @description.setter
    def description(self, description: str) -> None:
        self.__description = description
    
    @property
    def discsubtitle(self) -> str:
        """Disc subtitle field"""
        return self.__discsubtitle

    @discsubtitle.setter
    def discsubtitle(self, discSubtitle: str) -> None:
        self.__discsubtitle = discSubtitle

    @property
    def genre(self) -> str:
        """Song genre field"""
        return self.__genre

    @genre.setter
    def genre(self, genre: str) -> None:
        self.__genre = genre

    @property
    def labelid(self) -> str:
        """Album label ID field"""
        return self.__labelid

    @labelid.setter
    def labelid(self, labelId: str) -> None:
        self.__labelid = labelId

    @property
    def language(self) -> str:
        """Song language field"""
        return self.__language
    
    @language.setter
    def language(self, language: str) -> None:
        self.__language = language

    @property
    def organization(self) -> str:
        """Song organization (label) field"""
        return self.__organization

    @organization.setter
    def organization(self, organization: str) -> None:
        self.__organization = organization

    @property
    def performer(self) -> str:
        """Song performer field"""
        return self.__performer

    @performer.setter
    def performer(self, performer: str) -> None:
        self.__performer = performer

    @property
    def tracknumber(self) -> str:
        """Song track number field"""
        return self.__tracknumber

    @tracknumber.setter
    def tracknumber(self, trackNumber: str) -> None:
        self.__tracknumber = trackNumber

    @property
    def discnumber(self) -> str:
        """Song discnumber field"""
        return self.__discnumber

    @discnumber.setter
    def discnumber(self, discNumber: str) -> None:
        self.__discnumber = discNumber
