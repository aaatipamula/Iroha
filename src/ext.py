import discord

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

# replace null values with a "N/A"
def check_values(anime: dict):
    for key, value in anime.items():
        if value is None:
            anime[key] = "N/A"
        elif type(value) is dict:
            check_values(value)

# Format the anime card
def anime_card(anime: dict) -> discord.Embed:

    check_values(anime)

    # format the aired string
    aired = f"{anime['startDate']['month']}/{anime['startDate']['day']}/{anime['startDate']['year']} to {anime['endDate']['month']}/{anime['endDate']['day']}/{anime['endDate']['year']}"

    # format the url
    url = f"https://myanimelist.net/{anime['type'].lower()}/{anime['idMal']}"

    # format the description
    description = anime.get("description", "?").replace("<br>", "").replace("<i>", "").replace("</br>", "").replace("</i>", "")

    # define embed
    card = discord.Embed(title=anime["title"]["romaji"].title(), color=embed_color, url=url)
    card.set_image(url=anime["image"]["url"])
    card.add_field(name="English Title:", value=anime["title"]["english"].title())

    if anime["type"] == "ANIME":
        card.add_field(name="Status:", value=status.get(anime["status"], "?"))
        card.add_field(name="Aired:", value=aired)
        card.add_field(name="Season:", value=f"{anime['season'].capitalize()} {anime['seasonYear']}")
        card.add_field(name="Episodes:", value=anime["episodes"])

    else:
        card.add_field(name="Chapters:", value=anime["chapters"])
        card.add_field(name="Volumes:", value=anime["volumes"])

    card.add_field(name="Genres", value=" ".join(anime["genres"]))

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
def seasonal_cards(shows: list) -> list[discord.Embed]:

    anime_cards = []

    for anime in shows: 

        check_values(anime)

        # format the url
        url = f"https://myanimelist.net/anime/{anime['idMal']}"

        # format the description
        description = anime.get("description", "N/A").replace("<br>", "").replace("<i>", "").replace("</br>", "").replace("</i>", "")

        # define embed
        card = discord.Embed(title=anime["title"]["romaji"].title(), color=embed_color, url=url)
        card.set_image(url=anime["image"]["url"])
        card.add_field(name="English Title:", value=anime["title"]["english"].title())
        card.add_field(name="Genres", value=" ".join(anime["genres"]))

        if len(description) > 1024:
            indx = description[0:1024].rindex(".")
            first_half = description[0:indx+1]
            second_half = description[indx+1::]
            card.add_field(name="Description:", value=first_half, inline=False)
            card.add_field(name="\u200b", value=second_half, inline=False)

        else:
            card.add_field(name="Description:", value=description, inline=False)

        card.set_footer(text=f"MAL Id: {anime['idMal']}")

        anime_cards.append(card)

    return anime_cards

