import discord
import json
import random

if __name__ != '__main__':
    
    commands = json.load(open('./src/commands.json'))
    data = json.load(open('./src/data.json'))
    
    # title only embed
    def embed_b(title):
        a = discord.Embed(title= title, color=0xf2c4a7)
        return a

    # name and value only embed
    def embed_a(name, value):
        a = discord.Embed(color=0xf2c4a7)
        a.add_field(name= name, value= value)
        return a

    # title name and value embed
    def embed_c(title, name, value):
        a = discord.Embed(title= title, color=0xf2c4a7)
        a.add_field(name= name, value= value)
        return a

    # embed on command error
    def cmd_error(value):
        a = discord.Embed(color=0xf2c4a7)
        a.add_field(name= "Error!", value= value)
        return a

    # help command, scalable through the commands.json file
    def help_command(opt):

        opts = ["Help Has Arrived!", "At Your Service!", "HI!"]

        if opt == 'general':
            cmdEmbed = discord.Embed(title=random.choice(opts), color=0xf2c4a7)
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

else:
    print('You cannot run this file!\nPlease run the apcsp_bot.py file!')