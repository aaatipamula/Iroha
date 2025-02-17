import requests

from models import Response, Media, Page

# Make the HTTP Api request
def send(query: str, variables: dict):
  url = 'https://graphql.anilist.co'
  response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
  return response.json()

def seasonal_query(season: str, year: int, results: int) -> Response[Page]:
  # Query structure for graphql
  query = '''
  query ($season: MediaSeason, $year: Int, $perPage: Int) {
    Page (page: 1, perPage: $perPage){

      media (season: $season, seasonYear: $year, sort: POPULARITY_DESC, isAdult: false) {
        title {
          romaji(stylised: true)
          english(stylised: true)
        }
        image: coverImage {
          url: large
        }
        idMal
        status
        season
        seasonYear
        genres
        episodes
        description
        type
        startDate {
          year
          month
          day
        }
        endDate {
          year
          month
          day
        }
        chapters
        volumes
      }
    }
  }
  '''

  variables = {
    'season': season,
    'year': year,
    'perPage': results
  }

  return send(query, variables)

def media_query(search_string: str, form: str) -> Response[Media]:
  # query structure for GraphQL
  query = '''
  query ($search: String, $format: MediaFormat) {
    Media (search: $search, format: $format, sort: SEARCH_MATCH) {
      title {
        romaji(stylised: true)
        english(stylised: true)
      }
      image: coverImage {
        url: extraLarge
      }
      idMal
      status
      season
      seasonYear
      genres
      episodes
      description
      _type: type
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      chapters
      volumes
    }
  }
  '''

  variables = {
    'search': search_string,
    'format': form
  }

  return send(query, variables)

def mal_id_query(mal_id: int) -> Response[Media]:
  # query structure for GraphQL
  query = '''
  query ($anime_id: Int) {
    Media (idMal: $anime_id) {
      title {
        romaji(stylised: true)
        english(stylised: true)
      }
      image: coverImage {
        url: extraLarge
      }
      idMal
      status
      season
      seasonYear
      genres
      episodes
      description
      type
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      chapters
      volumes
    }
  }
  '''

  variables = {
    'anime_id': mal_id
  }

  return send(query, variables)

