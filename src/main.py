import discord
import traceback as tb
import logging
import embeds
import os
from time import sleep
from datetime import date
from os.path import join, dirname
from dotenv import load_dotenv
from typing import Optional
from converters import curr_season, media_format, season_type
from anilistApi import media_query, seasonal_query
from discord.ext import commands

# Declaring gateway intents, discord.py >= 2.0 feature
intent = discord.Intents().default()
intent.message_content = True

# Logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# dotenv load variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL"))
TOKEN = os.environ.get("TOKEN")
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX")
ABOUT_ME = os.environ.get("ABOUT_ME")

# Bot class
client = commands.Bot(command_prefix="?", intents=intent, case_insensitive=True, help_command=None)

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
async def search(ctx, search_format: Optional[media_format] = "TV", *, search_string):

    response = media_query(search_string, search_format)

    if response.get("errors") is None:
        anime = response["data"]["Media"]
        await ctx.send(embed=embeds.anime_card(anime))
        return

    await ctx.send(embed=embeds.cmd_error(response["errors"][0]["message"]))

# Search for seasonal anime.
@client.command()
async def seasonal(ctx, results: Optional[int] = 3, season: Optional[season_type] = curr_season(), year: Optional[int] = date.today().year):

    response = seasonal_query(season, year, results)

    if response.get("errors") is None:
        anime_cards = embeds.seasonal_cards(response["data"]["Page"]["media"])

        for anime in anime_cards:
            await ctx.send(embed=anime)
            sleep(0.5)

        return

    await ctx.send(embed=embeds.cmd_error(response["errors"][0]["message"]))

# Redefined help command
@client.command()
async def help(ctx, opt="general"):

    await ctx.send(embed=embeds.help_command(opt, COMMAND_PREFIX, ABOUT_ME))

# General error handling for all commands, if a command does not have error handling explicitly called this function will handle all errors.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=embeds.cmd_error("Not a command!"))

    else:
        print(error)
        err_channel = client.get_channel(DUMP_CHANNEL)
        if err_channel is None:
            raise Exception("Not a valid channel.")

        await err_channel.send(f"```Error: {error}\nMessage: {ctx.message.content}\nAuthor: {ctx.author}\nServer: {ctx.message.guild}\nLink: {ctx.message.jump_url}\nTraceback: {''.join(tb.format_exception(None, error, error.__traceback__))}```")

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

