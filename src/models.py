from typing import (
    Dict,
    Optional,
    TypeVar,
    Generic,
    NotRequired,
    TypedDict,
    Literal,
    Tuple,
    List
)

from datetime import date

T = TypeVar('T')

Status = Literal['NOT_YET_RELEASED', 'FINISHED', 'RELEASING', 'CANCELED', 'HIATUS']
Season = Literal['WINTER', 'SPRING', 'FALL', 'SUMMER']
SeasonChart = List[Tuple[Season, date, date]]
MediaFormat = Literal[
               "TV",
               "TV_SHORT",
               "MOVIE",
               "SPECIAL",
               "OVA",
               "ONA",
               "MUSIC",
               "MANGA",
               "NOVEL",
               "ONE_SHOT"
               ]
MediaMap = Dict[str, MediaFormat]

# Response wrapper items
class ErrorItem(TypedDict, total=False):
    message: str
    status: int

class Response(TypedDict, Generic[T]):
    errors: NotRequired[List[ErrorItem]]
    data: Optional[T]


# Anilist GraphQL API Types
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
    image: MediaCoverImage
    idMal: int
    status: Status
    season: Season
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
    media: List[MediaContent]

class Page(TypedDict):
    Page: PageContent

