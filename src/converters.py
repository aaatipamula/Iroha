from typing import Annotated
from datetime import date

from models import MediaFormat, Season, SeasonChart, MediaMap

YEAR = 2003 # Select a default year
SEASONS: SeasonChart = [
    ('WINTER', date(YEAR, 1, 1), date(YEAR, 3, 31)),
    ('SPRING', date(YEAR, 4, 1), date(YEAR, 5, 31)),
    ('SUMMER', date(YEAR, 6, 1), date(YEAR, 9, 30)),
    ('FALL',   date(YEAR, 10, 1), date(YEAR, 11, 30)),
    ('WINTER', date(YEAR, 12, 1), date(YEAR, 12, 31))
]

MEDIA_MAP: MediaMap = {
    "show": "TV",
    "short": "TV_SHORT",
    "movie": "MOVIE",
    "special": "SPECIAL",
    "ova": "OVA",
    "ona": "ONA",
    "music": "MUSIC",
    "manga": "MANGA",
    "novel": "NOVEL",
    "oneshot": "ONE_SHOT"
}

# Converter for search format
def format_converter(key: str) -> MediaFormat:
    key = key.lower()
    return MEDIA_MAP[key]

# Converter for season type
def season_converter(season: str) -> Season:
    season = season.upper()
    if season in ('WINTER', 'SPRING', 'FALL', 'SUMMER'):
        return season
    raise ValueError

# Annotate the functions to appease type checker
FormatConverter = Annotated[MediaFormat, format_converter]
SeasonConverter = Annotated[Season, season_converter]

# Returns current season
def curr_season() -> Season:
  now = date.today()
  now = now.replace(year=YEAR)
  return next(season for season, start, end in SEASONS if start <= now <= end)

