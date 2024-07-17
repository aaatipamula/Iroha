from typing import Annotated, List, Tuple
from datetime import date

SeasonChart = List[Tuple[str, Tuple[date, date]]]

YEAR = 2000
SEASONS: SeasonChart = [('WINTER', (date(YEAR, 1, 1), date(YEAR, 3, 31))),
                       ('SPRING', (date(YEAR, 4, 1), date(YEAR, 5, 31))),
                       ('SUMMER', (date(YEAR, 6, 1), date(YEAR, 9, 30))),
                       ('FALL', (date(YEAR, 10, 1), date(YEAR, 11, 30))),
                       ('WINTER', (date(YEAR, 12, 1), date(YEAR, 12, 31)))]

media_table = {
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

# Converter for search type
def media_converter(key: str):
    key = key.lower()
    if key not in media_table:
        raise ValueError
    media = media_table.get(key, "")
    return media

# Converter for season type
def season_converter(season: str) -> str:
    season = season.upper()
    if season not in ['WINTER', 'FALL', 'SPRING', 'SUMMER']:
        raise ValueError
    return season

MediaType = Annotated[str, media_converter]
SeasonType = Annotated[str, season_converter]

# Returns current season
def curr_season() -> str:
  now = date.today()
  now = now.replace(year=YEAR)
  return next(season for season, (start, end) in SEASONS if start <= now <= end)

