import os
import sys
import logging
import asyncio
import traceback as tb
from random import choice
from datetime import date
from os.path import join, dirname
from typing import Optional, Annotated

import embeds as ext
from converters import curr_season, media_format, season_type
from anilistApi import media_query, seasonal_query, mal_id_query

import discord
from discord.ext import commands
from dotenv import load_dotenv
from requests.exceptions import Timeout

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

greetings = [
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

# Bot class
client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intent, case_insensitive=True, help_command=None)

# Startup function, prints a ready message in the terminal and sends a ready message
@client.event
async def on_ready():
    print('I am ready')
    bot_channel = client.get_channel(DUMP_CHANNEL)
    await bot_channel.send("I am ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Waiting..."))

# ping
@client.command()
async def ping(ctx):
    await ctx.send(choice(greetings))

# Search for anime using the anilist api returns one result.
@client.command()
async def search(ctx, search_format: Optional[Annotated[str, media_format]]="TV", *, search_string):

    try:
        async with ctx.typing():
            response = media_query(search_string, search_format)

        if response.get("errors") is None:
            anime = response["data"]["Media"]
            await ctx.send(embed=ext.anime_card(anime))
            return

        await ctx.send(embed=ext.api_error(response["errors"][0]["message"]))

    except Timeout:
        await ctx.send(embed=ext.bot_error("Request timed out."))

# Search for seasonal anime.
@client.command()
async def seasonal(
    ctx,
    results: Optional[int] = 3,
    season: Optional[Annotated[str, season_type]] = curr_season(),
    year: Optional[int] = date.today().year
):

    try:
        async with ctx.typing():
            response = seasonal_query(season, year, results)

        if response.get("errors"):
            await ctx.send(embed=ext.api_error(response["errors"][0]["message"]))
            return

        anime_cards = ext.seasonal_cards(response["data"]["Page"]["media"])
        await ctx.send(embeds=anime_cards)

    except Timeout:
        await ctx.send(embed=ext.bot_error("Request timed out."))

@client.command()
async def info(ctx, mal_id: int):

    try:
        async with ctx.typing():
            response = mal_id_query(mal_id)

        if response.get("errors") is None:
            await ctx.send(embed=ext.anime_card(response["data"]["Media"]))
            return

        await ctx.send(embed=ext.api_error(response["errors"][0]["message"]))

    except Timeout:
        await ctx.send(embed=ext.bot_error("Request timed out."))

# Redefined help command
@client.command()
async def help(ctx, opt="general"):
    is_owner = await client.is_owner(ctx.author)
    embeds = ext.help_command(opt, ctx.prefix, ABOUT_ME, is_owner=is_owner)
    await ctx.send(embeds=embeds)

##################
# Admin Commands #
##################

@client.group()
@commands.is_owner()
async def admin(ctx):
    if not ctx.invoked_subcommand:
        await ctx.send(choice(greetings))

@admin.command(name="kill")
async def kill_bot(ctx):
    await ctx.send(f"NOOOOO PLEASE {client.get_emoji(1145147159260450907)}") # :cri: emoji

    def check(reaction, user):
        return client.is_owner(user) and reaction.emoji == client.get_emoji(1136812895859134555) #:asukaL: emoji

    try:
        await client.wait_for("reaction_add", timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send(client.get_emoji(994378239675990029))
    else:
        await ctx.send(client.get_emoji(1145090024333918320))
        exit()

@admin.command()
async def lock(ctx):
    global LOCK
    if LOCK:
        await ctx.send(embed=ext.bot_error("Commands already locked."))
    else:
        LOCK = True
        await ctx.send(embed=ext.info_msg("Commands are now locked."))

@admin.command()
async def unlock(ctx):
    global LOCK
    if not LOCK:
        await ctx.send(embed=ext.bot_error("Commands are already unlocked."))
    else:
        LOCK = False
        await ctx.send(embed=ext.info_msg("Commands are now unlocked."))


# General error handling for all commands, if a command does not have error handling explicitly called this function will handle all errors.
@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        await ctx.send(embed=ext.bot_error("Not a command!"))

    elif isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=ext.bot_error(str(err)))

    else:
        print(err)
        err_channel = client.get_channel(DUMP_CHANNEL)
        await err_channel.send(f"```Error: {err}\n\
        Message: {ctx.message.content}\n\
        Author: {ctx.author}\n\
        Server: {ctx.message.guild}\n\
        Link: {ctx.message.jump_url}\n\
        Traceback: {''.join(tb.format_exception(None, err, err.__traceback__))}```")

# A function that runs on every message sent.
@client.event
async def on_message(message):

    # Ignores if user is client (self), generally good to have in this function.
    if message.author == client.user:
        return

    elif client.user.mentioned_in(message):
        await message.channel.send(choice(greetings))

    # Process any commands before on message event is processed
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(TOKEN, log_handler=handler)

