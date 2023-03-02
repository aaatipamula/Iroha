import requests

# Make the HTTP Api request
def send(query: str, variables: dict):
  url = 'https://graphql.anilist.co'
  response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
  return response.json()

def seasonal_query(season: str, year: int, results: int):
  # Query structure for graphql
  query = '''
  query ($season: MediaSeason, $year: Int, $perPage: Int) {
    Page (page: 1, perPage: $perPage){
      media (season: $season, seasonYear: $year, sort: POPULARITY_DESC, isAdult: false) {
        title {
          romaji
          english
        }
        image: coverImage {
          url: medium
        }
        idMal
        genres
        description
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

def media_query(search_string: str, form: str) -> dict:
  # query structure for GraphQL
  query = '''
  query ($search: String, $format: MediaFormat) {
    Media (search: $search, format: $format, sort: SEARCH_MATCH) {
      title {
        romaji
        english
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
    'search': search_string,
    'format': form
  }

  return send(query, variables)

