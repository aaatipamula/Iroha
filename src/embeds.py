import discord
import json
import random

commands = json.load(open('./src/commands.json'))

embed_color = 0xe398be

# title only embed
def embed_b(title):
    a = discord.Embed(title= title, color=embed_color)
    return a

# name and value only embed
def embed_a(name, value):
    a = discord.Embed(color=embed_color)
    a.add_field(name= name, value= value)
    return a

# title name and value embed
def embed_c(title, name, value):
    a = discord.Embed(title= title, color=embed_color)
    a.add_field(name= name, value= value)
    return a

# embed on command error
def cmd_error(value):
    a = discord.Embed(color=embed_color)
    a.add_field(name="Error!", value=value)
    return a

# Format the anime card
def anime_card(anime: dict) -> discord.Embed:

    status: dict = {
        "FINISHED": "Completed",
        "RELEASING": "Airing",
        "NOT_YET_RELEASED": "Upcoming",
        "CANCELED": "Canceled",
        "HIATUS": "Hiatus"
    }


    # format the aired string
    aired = f"{anime['startDate'].get('month', '?')}/{anime['startDate'].get('day', '?')}/{anime['startDate'].get('year', '?')} to {anime['endDate'].get('month', '?')}/{anime['endDate'].get('day', '?')}/{anime['endDate'].get('year', '?')}"

    # format the url
    url = f"https://myanimelist.net/{anime['type']}/{anime['idMal']}"

    # format the description
    description = anime.get("description", "?").replace("<br>", "").replace("<i>", "")

    # define embed
    card = discord.Embed(title=anime["title"].get("romaji", "?").title(), color=embed_color, url=url)
    card.set_image(url=anime["image"]["url"])
    card.add_field(name="English Title:", value=anime["title"].get("english", "?").title())

    if anime["type"] == "ANIME":
        card.add_field(name="Status:", value=status.get(anime["status"], "?"))
        card.add_field(name="Aired:", value=aired)
        card.add_field(name="Season:", value=f"{anime.get('season', '?').capitalize()} {anime.get('seasonYear', '?')}")
        card.add_field(name="Episodes:", value=anime.get("episodes", "?"))

    else:
        card.add_field(name="Chapters:", value=anime.get("chapters"))

    card.add_field(name="Genres", value=" ".join(anime["genres"]))
    card.add_field(name="Description:", value=description, inline=False)
    card.set_footer(text="Search with: '?search'")

    return card

# format the command embed
def format_command(name: str, command: dict) -> discord.Embed:
    cmdEmbed = discord.Embed(title=name, color=embed_color, description=command["description"])
    if not command["options"] is None:
        for option in command["options"]:
            cmdEmbed.add_field(name=option["name"], value=option["description"])

    return cmdEmbed

# help command, scalable through the commands.json file
def help_command(opt: str, command_prefix: str, about_me: str) -> discord.Embed:

    messages = ["Help Has Arrived!", "At Your Service!"]

    if opt == 'general':
        cmdEmbed = discord.Embed(title=random.choice(messages), color=embed_color, description=about_me)
        for command in commands:
            cmdEmbed.add_field(name=command, value="\u200b", inline=False)
        cmdEmbed.set_footer(text= f"Bot Command Prefix = '{command_prefix}'")
        return cmdEmbed

    elif opt in commands:
        cmd = commands.get(opt)
        return format_command(opt, cmd)

    return cmd_error("Not a valid option.")

