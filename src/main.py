import os
import sys
import traceback as tb
from datetime import datetime
from os.path import join, dirname

from users import UserCog
from bot.admin import AdminCog
from bot.embeds import cmd_error, bot_error

import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands

# load the .env file
dotenv_path = join(dirname(__file__), 'data', '.env')

try:
    load_dotenv(dotenv_path=dotenv_path)
except FileNotFoundError:
    print(".env not found")

# grab our env vars
DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", ""))
TOKEN = os.environ.get("TOKEN", "")
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX")
ABOUT_ME = os.environ.get("ABOUT_ME", "")
START_DATETIME = datetime.now()

# Declaring gateway intents, discord.py >= 2.0 feature
intent = discord.Intents.default()
intent.message_content = True
intent.reactions = True

# Log to stdout without color
handler = logging.StreamHandler(stream=sys.stdout)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

# Discord Bot instance
client = commands.Bot(
    command_prefix=COMMAND_PREFIX or ".",
    intents=intent, 
    case_insensitive=True, # case insensitive commands
    help_command=None
)

# Create our cogs 
admin_cog = AdminCog(client, DUMP_CHANNEL, START_DATETIME)
user_cog = UserCog(client, ABOUT_ME)

# Setup client startup
@client.event
async def on_ready():
    await client.add_cog(admin_cog)
    await client.add_cog(user_cog)
    game = discord.Game("Hello, I'm Iroha")
    await client.change_presence(activity=game)
    print('Iroha is ready...')

# General error handling for all commands.
# NOTE: Change this soon
@client.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        await ctx.send(embed=bot_error("Not a command!"))

    elif isinstance(err, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=cmd_error(str(err)))

    elif isinstance(err, commands.errors.UserInputError):
        await ctx.send(embed=cmd_error(str(err)))

    elif isinstance(err, commands.errors.CheckFailure):
        await ctx.send(embed=cmd_error("You are not allowed to use this command."))

    elif isinstance(err, commands.errors.NotOwner):
        await ctx.send(embed=cmd_error("You are not allowed to use this command."))

    elif isinstance(err, commands.errors.BadArgument):
        await ctx.send(embed=cmd_error("You likely used an argument wrong, refer to the documentation for this command."))

    else:
        print(err)
        err_channel = client.get_channel(DUMP_CHANNEL)
        if err_channel:
            # Known type checking error
            await err_channel.send(f"```Error: {err}\n\
                Message: {ctx.message.content}\n\
                Author: {ctx.author}\n\
                Server: {ctx.message.guild}\n\
                Link: {ctx.message.jump_url}\n\
                Traceback: {''.join(tb.format_exception(None, err, err.__traceback__))}```")

if __name__ == '__main__':
    client.run(TOKEN, log_handler=handler, log_formatter=formatter)
