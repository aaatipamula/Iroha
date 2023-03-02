from datetime import date

year = 2000
seasons = [('WINTER', (date(year, 1, 1), date(year, 3, 31))),
           ('SPRING', (date(year, 4, 1), date(year, 5, 31))),
           ('SUMMER', (date(year, 6, 1), date(year, 9, 30))),
           ('FALL', (date(year, 10, 1), date(year, 11, 30))),
           ('WINTER', (date(year, 12, 1), date(year, 12, 31)))]

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

# Simple converter for search type
def media_format(form: str) -> str:
  form = form.lower()

  if form not in media_table.keys():
    raise ValueError

  media = media_table.get(form, "")
  return media

# Converter for season type
def season_type(season: str) -> str:
  season = season.upper()

  if season not in ['WINTER', 'FALL', 'SPRING', 'SUMMER']: 
    raise ValueError

  return season

# Returns current season
def curr_season():
  now = date.today()
  now = now.replace(year=year)
  return next(season for season, (start, end) in seasons if start <= now <= end)

