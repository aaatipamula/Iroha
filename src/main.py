import discord
import traceback as tb
import logging
import embeds
import os
from datetime import date
from os.path import join, dirname
from dotenv import load_dotenv
from typing import Optional
from requests.exceptions import Timeout
from converters import curr_season, media_format, season_type
from anilistApi import media_query, seasonal_query, mal_id_query
from discord.ext import commands

# Declaring gateway intents, discord.py >= 2.0 feature
intent = discord.Intents().default()
intent.message_content = True

# Logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')

# Loading message queue
loading_messages = []

# dotenv load variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL"))
TOKEN = os.environ.get("TOKEN")
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX")
ABOUT_ME = os.environ.get("ABOUT_ME")

print(COMMAND_PREFIX)

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="testing..."))

# ping
@client.command()
async def ping(ctx):
    await ctx.send("Pong")

# Search for anime using the anilist api returns one result.
@client.command()
@commands.before_invoke(send_loading)
async def search(ctx, search_format: Optional[media_format] = "TV", *, search_string):

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
async def seasonal(ctx, results: Optional[int] = 3, season: Optional[season_type] = curr_season(), year: Optional[int] = date.today().year):

    try:
        response = seasonal_query(season, year, results)

        if response.get("errors") is None:
            anime_cards = embeds.seasonal_cards(response["data"]["Page"]["media"])
            await ctx.send(embeds=anime_cards)
            return

        await ctx.send(embed=embeds.api_error(response["errors"][0]["message"]))

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

    # Process any commands before on message event is processed
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(TOKEN, log_handler=handler)

