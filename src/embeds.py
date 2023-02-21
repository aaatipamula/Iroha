import discord
import json
import random


commands = json.load(open('./src/commands.json'))
data = json.load(open('./src/data.json'))

# title only embed
def embed_b(title):
    a = discord.Embed(title= title, color=data.get("color"))
    return a

# name and value only embed
def embed_a(name, value):
    a = discord.Embed(color=data.get("color"))
    a.add_field(name= name, value= value)
    return a

# title name and value embed
def embed_c(title, name, value):
    a = discord.Embed(title= title, color=data.get("color"))
    a.add_field(name= name, value= value)
    return a

# embed on command error
def cmd_error(value):
    a = discord.Embed(color=data.get("color"))
    a.add_field(name="Error!", value=value)
    return a

# Format the anime card
def anime_card(anime: dict):

    status: dict = {
        "FINISHED": "Completed",
        "RELEASING": "Airing",
        "NOT_YET_RELEASED": "Upcoming",
        "CANCELED": "Canceled",
        "HIATUS": "Hiatus"
    }

    url = f"https://myanimelist.net/anime/{anime['idMal']}"
    
    # format the aired string
    aired = f"{anime['startDate'].get('month', '?')}/{anime['startDate'].get('day', '?')}/{anime['startDate'].get('year', '?')} to {anime['endDate'].get('month', '?')}/{anime['endDate'].get('day', '?')}/{anime['endDate'].get('year', '?')}"

    # format the description
    description = anime.get("description", "?").replace("<br>", "")

    card = discord.Embed(title=anime["title"].get("romaji", "?").capitalize(), color=0xe398be, url=url)
    card.set_image(url=anime["image"]["url"])
    card.add_field(name="English Title:", value=anime["title"].get("english", "?").capitalize())
    card.add_field(name="Status:", value=status.get(anime["status"], "?"))
    card.add_field(name="Aired:", value=aired)
    card.add_field(name="Season:", value=f"{anime['season'].capitalize()} {anime['seasonYear']}")
    card.add_field(name="Genres", value=" ".join(anime["genres"]))
    card.add_field(name="Episodes", value=anime.get("episodes", "?"))
    card.add_field(name="Description:", value=description, inline=False)
    card.set_footer(text="Search with: ?search")
    return card

# help command, scalable through the commands.json file
def help_command(opt):

    opts = ["Help Has Arrived!", "At Your Service!"]

    if opt == 'general':
        cmdEmbed = discord.Embed(title=random.choice(opts), color=data.get("color"))
        cmdEmbed.add_field(name="About Me:", value=data.get('about_me'))
        for x in commands:
            cmdEmbed.add_field(name=f"*{x}*", value="\u200b", inline=False)
        cmdEmbed.set_footer(text= f"Bot Command Prefix = \'{data.get('command_prefix')}\'")
        return cmdEmbed

    elif opt not in commands:
        return cmd_error("Not a valid option.")

    elif opt in commands:
        cmd = commands.get(opt)
        return embed_c(f"{opt} {cmd[0]}", cmd[1], cmd[2])

