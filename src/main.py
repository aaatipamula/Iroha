import discord
import traceback as tb
import json
import embeds
from discord.ext import commands
from discord.errors import NotFound

#Pulls json info from data.json in the /src folder of the project and initalizes the discord bot.
data = json.load(open('./src/data.json'))
client = commands.Bot(command_prefix = data.get('command_prefix'),  case_insensitive= True, help_command= None)

#Startup function, prints a ready message in the terminal and sends a ready message to a channel specified in the data.json file.
@client.event
async def on_ready():
    print('I am ready')
    bot_channel = client.get_channel(data.get('dump_channel'))
    await bot_channel.send("I am ready.")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="testing..."))

#Simple command, asynchronus fuction that sends a "HELLO WORLD" message to any user who calls command.
@client.command()
async def example(ctx):
    await ctx.send(embed=embeds.embed_a('HELLO WORLD'))

#Error handling specifically for the example() function if the function calls for any additional arguments they can be handled with the 'isinstance(error, commands.MissingRequiredArgument)' if statement for any missing arguments and so on. 
@example.error
async def example_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        msg = '```Please enter the missing argument!```'
        await ctx.send(msg)
    else:
        await ctx.send(f"```{error}```")

#General error handling for all commands, if a command does not have error handling explicitly called this function will handle all errors.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, NotFound):
        ctx.send(embed=embeds.cmd_error("This is not a command!"))

    else:
        print(error)
        err = client.get_channel(data.get("dump_channel"))
        await err.send(f"```Error: {error}\nMessage: {ctx.message.content}\nAuthor: {ctx.author}\nServer: {ctx.message.guild}\nLink: {ctx.message.jump_url}\nTraceback: {''.join(tb.format_exception(None, error, error.__traceback__))}```")

#A function that runs on every message sent.
@client.event
async def on_message(message):
    
    #Ignores if user is client (self), generally good to have in this function.
    if message.author == client.user:
        return
        
    #process any commands before on message event is processed
    await client.process_commands(message)

if __name__ == '__main__':
    client.run(data.get('token'))

else: print('Please run as main file')