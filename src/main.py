import traceback as tb
import logging
import embeds
import os
import sys
from random import choice
from datetime import date
from os.path import join, dirname
from typing import Optional

from converters import curr_season, media_format, season_type
from anilistApi import media_query, seasonal_query, mal_id_query

import discord
from discord.ext import commands
from requests.exceptions import Timeout
from dotenv import load_dotenv

# Declaring gateway intents, discord.py >= 2.0 feature
intent = discord.Intents().default()
intent.message_content = True

# Logging
handler = logging.StreamHandler(stream=sys.stdout)

# Loading message queue
loading_messages = []

# dotenv load variables
dotenv_path = join(dirname(__file__), 'data', '.env')
load_dotenv(dotenv_path=dotenv_path)

DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "0"))
TOKEN = os.environ.get("TOKEN", "")
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", "?")
ABOUT_ME = os.environ.get("ABOUT_ME", "")

GREETINGS = [
    "Hi!",
    "Hello :)",
    "<a:loading:1080977545375264860>",
    "Hey there!",
    "Nom",
    "<a:Wokege:1127434204603486208>",
    "<:rikkaSalute:1127434201919135766>",
    "<a:wave:1004493976201592993>",
    "<:Blobneutral:1127434200363040948>",
    "<:kannamad:1081423991035674624>",
    "<:kannapolice:1081426665739145297>",
    "Huh?"
]

async def send_loading(ctx):
    await ctx.send("Loading... <a:loading:1080977545375264860>", ephemeral=True, delete_after=10)

# Bot class
client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intent, case_insensitive=True, help_command=None)

# Startup function, prints a ready message in the terminal and sends a ready message
@client.event
async def on_ready():
    print('I am ready')
    bot_channel = client.get_channel(DUMP_CHANNEL)
    await bot_channel.send("I am ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Waiting..."))

# Ping
@client.command()
async def ping(ctx):
    await ctx.send(choice(GREETINGS))

# Search for anime using the anilist api returns one result.
@client.command()
@commands.before_invoke(send_loading)
async def search(ctx, search_format: Optional[media_format]="TV", *, search_string):

    try: 
        response = media_query(search_string, search_format)

        if response.get("errors") is None:
            anime = response["data"]["Media"]
            await ctx.send(embed=embeds.anime_card(anime))
            return

        await ctx.send(embed=embeds.api_error(response["errors"][0]["message"]))

    except Timeout:
        await ctx.send(embed=embeds.bot_error("Request timed out."))

# Search for seasonal anime.
@client.command()
@commands.before_invoke(send_loading)
async def seasonal(ctx, results: Optional[int] = 3, season: Optional[season_type]=curr_season(), year: Optional[int] = date.today().year):

    try:
        response = seasonal_query(season, year, results)

        if response.get("errors"):
            await ctx.send(embed=embeds.api_error(response["errors"][0]["message"]))
            return

        anime_cards = embeds.seasonal_cards(response["data"]["Page"]["media"])
        await ctx.send(embeds=anime_cards)

    except Timeout:
        await ctx.send(embed=embeds.bot_error("Request timed out."))

@client.command()
@commands.before_invoke(send_loading)
async def info(ctx, mal_id: int):

    try:
        response = mal_id_query(mal_id)

        if response.get("errors") is None:
            await ctx.send(embed=embeds.anime_card(response["data"]["Media"]))
            return

        await ctx.send(embed=embeds.api_error(response["errors"][0]["message"]))

    except Timeout:
        await ctx.send(embed=embeds.bot_error("Request timed out."))


# Redefined help command
@client.command()
async def help(ctx, opt="general"):

    await ctx.send(embed=embeds.help_command(opt, ctx.prefix, ABOUT_ME))

# General error handling for all commands, if a command does not have error handling explicitly called this function will handle all errors.
@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        await ctx.send(embed=embeds.bot_error("Not a command!"))

    elif isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=embeds.bot_error(str(err)))

    else:
        print(err)
        err_channel = client.get_channel(DUMP_CHANNEL)
        if err_channel is None:
            raise Exception("Not a valid channel.")

        await err_channel.send(f"```Error: {err}\nMessage: {ctx.message.content}\nAuthor: {ctx.author}\nServer: {ctx.message.guild}\nLink: {ctx.message.jump_url}\nTraceback: {''.join(tb.format_exception(None, err, err.__traceback__))}```")

# A function that runs on every message sent.
@client.event
async def on_message(message):

    # Ignores if user is client (self), generally good to have in this function.
    if message.author == client.user:
        return

    elif client.user.mentioned_in(message):
        await message.channel.send(choice(GREETINGS))

    # Process any commands before on message event is processed
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(TOKEN, log_handler=handler)

