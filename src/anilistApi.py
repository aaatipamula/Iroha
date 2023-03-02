import requests

# Simple converter for search argument
def media_format(form: str) -> str:

  form = form.lower()

  key = {
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

  if form not in key.keys():
    raise ValueError

  media = key.get(form, "")
  return media

def query(search_string: str, form: str) -> dict:

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

    # Define our query variables and values that will be used in the query request
    variables = {
      'search': search_string,
      'format': form
    }

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)

    json_response = response.json()

    return json_response

