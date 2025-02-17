import re
from typing import List
from datetime import date
import discord

from models import FuzzyDate, MediaContent

# Change this somehow
embed_color = 0xe398be

# Status Codes
status = {
    "FINISHED": "Completed",
    "RELEASING": "Airing",
    "NOT_YET_RELEASED": "Upcoming",
    "CANCELED": "Canceled",
    "HIATUS": "Hiatus"
}

# Format the aired string
def get_aired_str(start: FuzzyDate, end: FuzzyDate) -> str:
    start_date = date(start['year'] or 1, start['month'] or 1, start['day'] or 1)
    end_date = date(end['year'] or 1, end['month'] or 1, end['day'] or 1)

    final_str = ""
    if start_date != date(1, 1, 1):
        final_str += start_date.strftime("%B %y -")
    else:
        return "TBD"

    if end_date != date(1, 1, 1):
        final_str += end_date.strftime("%B %y")
    else:
        final_str += "TBD"

    return final_str

# Format the season string
def get_season_string(season: str | None, year: int | None) -> str:
    if season is None or year is None:
        return "TBD"
    return season + " " + str(year)

# Format the anime card
def anime_card(anime: MediaContent) -> discord.Embed:
    aired = get_aired_str(anime["startDate"], anime["endDate"])
    season = get_season_string(anime['season'], anime['seasonYear'])

    # format url
    url = f"https://myanimelist.net/{anime['_type'].lower()}/{anime['idMal']}"

    # format the description
    description = re.sub(r"</?[a-z]*>", "", anime.get("description", "N/A"))

    # Create the embed
    card = discord.Embed(title=anime["title"]["romaji"], color=embed_color, url=url)
    card.set_image(url=anime["image"]["url"])
    card.add_field(name="English Title:", value=anime["title"]["english"])

    if anime["_type"] == "ANIME":
        card.add_field(name="Status:", value=status.get(anime["status"], "?"))
        card.add_field(name="Aired:", value=aired)
        card.add_field(name="Season:", value=season)
        card.add_field(name="Episodes:", value=anime.get('episodes', '0'))

    else:
        card.add_field(name="Chapters:", value=anime['chapters'])
        card.add_field(name="Volumes:", value=anime['volumes'])

    card.add_field(name="Genres:", value=", ".join(anime["genres"]))

    if len(description) > 1024:
        indx = description[0:1024].rindex(".")
        first_half = description[0:indx+1]
        second_half = description[indx+1::]
        card.add_field(name="Description:", value=first_half, inline=False)
        card.add_field(name="\u200b", value=second_half, inline=False)
    else:
        card.add_field(name="Description:", value=description, inline=False)

    card.set_footer(text="Search with: '?search'")

    return card

# format the seasonal anime card
def seasonal_cards(shows: List[MediaContent]) -> List[discord.Embed]:
    anime_cards = []

    for anime in shows: 
        # format the url
        url = f"https://myanimelist.net/anime/{anime['idMal']}"

        # format the description
        description = re.sub(r"</?[a-z]*>", "", anime.get("description", "N/A"))

        # define embed
        card = discord.Embed(title=anime["title"]["romaji"], color=embed_color, url=url)
        card.set_image(url=anime["image"]["url"])
        card.add_field(name="English Title:", value=anime["title"]["english"])
        card.add_field(name="Genres", value=", ".join(anime["genres"]))

        if len(description) > 1024:
            indx = description[0:1024].rindex(".")
            first_half = description[0:indx+1]
            second_half = description[indx+1::]
            card.add_field(name="Description:", value=first_half, inline=False)
            card.add_field(name="\u200b", value=second_half, inline=False)
        else:
            card.add_field(name="Description:", value=description, inline=False)

        card.set_footer(text=f"MAL ID: {anime['idMal']}")

        anime_cards.append(card)

    return anime_cards

