import discord
import traceback as tb
import json
import logging
import embeds
import requests
from typing import Optional
from discord.ext import commands
from discord.errors import NotFound

#Declaring gateway intents, discord.py >= 2.0 feature
intent = discord.Intents().default()
intent.message_content = True

#Logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#Pulls json info from data.json in the /src folder of the project and initalizes the discord bot.
data = json.load(open('./src/data.json'))
client = commands.Bot(command_prefix="?", intents=intent, case_insensitive=True, help_command=None)

#Startup function, prints a ready message in the terminal and sends a ready message to a channel specified in the data.json file.
@client.event
async def on_ready():
    print('I am ready')
    bot_channel = client.get_channel(data.get('dump_channel'))
    await bot_channel.send("I am ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="testing..."))

@client.command()
async def ping(ctx):
    await ctx.send("Pong")

# Search for anime using the jikan api
@client.command()
async def search(ctx, num: Optional[int]=1, *query):

    print(query)
    print(num)

    request_string = f"https://api.jikan.moe/v4/anime?limit={num}&q={'%20'.join(query)}&order_by=members"

    res = requests.get(request_string)
    data = res.json()

    for anime in data["data"]:

        print(anime["year"], anime["season"])

        await ctx.send(embed=embeds.anime_card(anime))

# Redefined help command
@client.command()
async def help(ctx, opt="general"):

    await ctx.send(embed=embeds.help_command(opt))

# General error handling for all commands, if a command does not have error handling explicitly called this function will handle all errors.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, NotFound):
        ctx.send(embed=embeds.cmd_error("This is not a command!"))

    else:
        print(error)
        err_channel = client.get_channel(data.get("dump_channel"))
        await err_channel.send(f"```Error: {error}\nMessage: {ctx.message.content}\nAuthor: {ctx.author}\nServer: {ctx.message.guild}\nLink: {ctx.message.jump_url}\nTraceback: {''.join(tb.format_exception(None, error, error.__traceback__))}```")

#A function that runs on every message sent.
@client.event
async def on_message(message):

    #Ignores if user is client (self), generally good to have in this function.
    if message.author == client.user:
        return

    #process any commands before on message event is processed
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(data["token"], log_handler=handler)

