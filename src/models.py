from typing import (
    Optional,
    TypeVar,
    Generic,
    NotRequired,
    TypedDict,
    Literal,
    List
)

T = TypeVar('T')

# Response wrapper
class ErrorItem(TypedDict, total=False):
    message: str
    status: int

class Response(TypedDict, Generic[T]):
    errors: NotRequired[List[ErrorItem]]
    data: Optional[T]


# Anilist API
class MediaTitle(TypedDict):
    romaji: str
    english: str

class MediaCoverImage(TypedDict):
    url: str

class FuzzyDate(TypedDict):
    day: int
    month: int
    year: int

class MediaContent(TypedDict):
    title: MediaTitle
    image:  MediaCoverImage
    idMal: int
    status: Literal[
            "NOT_YET_RELEASED",
            "FINISHED",
            "RELEASING",
            "CANCELED",
            "HIATUS"
            ]
    season: Literal["WINTER", "SPRING", "SUMMER", "FALL"]
    seasonYear: int
    genres: List[str]
    episodes: int
    description: str
    _type: Literal["ANIME", "MANAGA"]
    startDate: FuzzyDate
    endDate: FuzzyDate
    chapters: int
    volumes: int

class Media(TypedDict):
    Media: MediaContent

class PageContent(TypedDict):
    media: List[Media]

class Page(TypedDict):
    Page: PageContent

