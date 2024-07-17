import json
import random
import datetime
from typing import Tuple, List, TypedDict, Optional, Dict
from os.path import join, dirname

import discord

class Param(TypedDict):
    name: str
    optional: bool
    type: str
    data_type: str
    description: str
    notes: Optional[str]

class Command(TypedDict):
    hidden: bool
    cmd_desc: str
    params: Optional[List[Param]]
    usage: List[str]

commands: Dict[str, Command] = json.load(open(join(dirname(__file__), 'commands.json')))

embed_color = 0xe398be
error_color = 0x991a2d

# Some error occured with the bot
def bot_error(desc: str):
    a = discord.Embed(color=error_color, title="Bot Error", description=desc)
    a.add_field(name="\u200b", value="<:kannapolice:1081426665739145297>")
    return a

def cmd_error(desc: str):
    a = discord.Embed(color=error_color, title="Command Error", description=desc)
    a.add_field(name="\u200b", value="<:kannapolice:1081426665739145297>")
    return a

# Some info message
def info_msg(desc: str):
    a = discord.Embed(color=embed_color, title="Info", description=desc)
    a.add_field(name="\u200b", value="<a:loading:1080977545375264860>")
    return a

# Anilist API error
def api_error(desc: str):
    a = discord.Embed(color=embed_color, title="AnilistAPI Error", description=desc)
    a.add_field(name="\u200b", value="<:kannamad:1081423991035674624>")
    return a

# Dashboard for admin user
async def admin_dashboard(client, starttime: datetime.datetime):
    app_info = await client.application_info()
    td = datetime.datetime.now() - starttime
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    seconds = td.seconds - hours*3600 - minutes*60
    desc = f"**Name**: {app_info.name}\n\
    **Owner**: {app_info.owner}\n\
    **Command Prefix**: {client.command_prefix}\n\n\
    **Latency**: {client.latency:0.2f} Seconds\n\
    **Uptime**: `{td.days} Days {hours} Hours {minutes} Minutes {seconds} Seconds`"
    a = discord.Embed(color=embed_color, title="Admin Dashboard", description=desc)
    return a

# Format the help embed for specific command
def format_command(name: str, command: Command, prefix: str) -> discord.Embed:
    opts = [param['name'] for param in command['params']] if command['params'] else []
    cmdEmbed = discord.Embed(
        title=f"{name} ({', '.join(opts)})",
         color=embed_color,
         description=command["cmd_desc"]
    )
    if command["params"]:
        for param in command["params"]:
            value_format = f"**Type**: {param['type']}\n\
                **Data**: {param['data_type']}\n\
                **Optional**: {param['optional']}\n\
                **Description**: {param['description']}"
            if param.get("notes"):
                value_format += f"\n*Notes*: {param['notes']}"
            cmdEmbed.add_field(name=param["name"], value=value_format)

    cmdEmbed.add_field(name="Usage:", value="\n".join(f'`{prefix}' + use + '`' for use in command["usage"]), inline=False)

    return cmdEmbed

# Help command, scalable through the commands.json file
def help_command(
    opt: str, 
    command_prefix: str, 
    about_me: str, 
    is_owner: bool = False
) -> Tuple[discord.Embed, discord.Embed | None]:

    messages = ["Help Has Arrived!", "At Your Service!"]

    if opt == 'general':
        cmdEmbed = discord.Embed(title=random.choice(messages), color=embed_color, description=about_me)
        for name, command in commands.items():
            if not command.get("hidden"):
                cmdEmbed.add_field(name=name, value=command.get("cmd_desc"), inline=False)
        cmdEmbed.set_footer(text= f"Bot Command Prefix = '{command_prefix}'")
        if is_owner:
            adminEmbed = discord.Embed(
                title="Admin Commands",
                color=embed_color,
                description="Commands for the owner to use."
            )
            for name, command in commands.items():
                if command.get("hidden") and is_owner:
                    adminEmbed.add_field(name=name, value=command.get("cmd_desc"), inline=False)
        else: adminEmbed = None

        return cmdEmbed, adminEmbed

    elif opt in commands:
        cmd = commands.get(opt)
        return format_command(opt, cmd, command_prefix), None # Known type checking error

    return bot_error("Not a valid command."), None

