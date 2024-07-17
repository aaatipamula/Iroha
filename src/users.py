from random import choice as random_choice
from datetime import date
from typing import Awaitable, Callable
import functools

from converters import curr_season, MediaType, SeasonType
from anilistApi import media_query, seasonal_query, mal_id_query
from ext import anime_card, seasonal_cards
from bot.embeds import help_command, api_error, bot_error

import discord
from discord.ext import commands
from requests.exceptions import Timeout

# DUMP_CHANNEL = int(os.environ.get("DUMP_CHANNEL", "0"))
# TOKEN = os.environ.get("TOKEN", "")
# COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", "?")
# ABOUT_ME = os.environ.get("ABOUT_ME", "")

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

def handle_timeout(f: Callable[..., Awaitable[None]]) -> Callable[..., Awaitable[None]]:
    @functools.wraps(f)
    async def wrapper(*args, **kwargs) -> None:
        try:
            await f(*args, **kwargs)
        except Timeout:
            ctx: commands.Context = args[1] # Kinda hacky but if it works ig
            await ctx.send(embed=bot_error("Request timed out."))
    return wrapper
    

class UserCog(commands.Cog):
    def __init__(self, bot: commands.Bot, about_me: str) -> None:
        self.bot = bot
        self.about_me = about_me

    # Ping
    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(random_choice(GREETINGS))

    # Search for anime using the anilist api returns one result.
    @handle_timeout
    @commands.command()
    async def search(self, ctx: commands.Context, media: MediaType="TV", *, search_string: str) -> None:
        response = media_query(search_string, media)
        if response.get("errors") is None:
            anime = response["data"]["Media"]
            await ctx.send(embed=anime_card(anime))
            return
        await ctx.send(embed=api_error(response["errors"][0]["message"]))

    # Search for seasonal anime.
    @handle_timeout
    @commands.command()
    async def seasonal(
        self,
        ctx: commands.Context,
        results: int=3,
        season: SeasonType=curr_season(),
        year: int=date.today().year
    ) -> None:
            response = seasonal_query(season, year, results)
            if response.get("errors"):
                await ctx.send(embed=api_error(response["errors"][0]["message"]))
                return
            anime_cards = seasonal_cards(response["data"]["Page"]["media"])
            await ctx.send(embeds=anime_cards)

    @handle_timeout
    @commands.command()
    async def info(self, ctx: commands.Context, mal_id: int) -> None:
            response = mal_id_query(mal_id)

            if response.get("errors") is None:
                await ctx.send(embed=anime_card(response["data"]["Media"]))
                return

            await ctx.send(embed=api_error(response["errors"][0]["message"]))

    # Redefined help command
    @commands.command()
    async def help(self, ctx: commands.Context, opt="general") -> None:
        is_owner = await self.bot.is_owner(ctx.author)
        userHelp, adminHelp = help_command(opt, ctx.prefix, self.about_me, is_owner=is_owner) # Known type checking error
        await ctx.send(embed=userHelp)
        if adminHelp is not None:
            await ctx.reply(embed=adminHelp, ephemeral=True)


    # A function that runs on every message sent.
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if message.author == self.bot.user:
            return

        elif self.bot.user.mentioned_in(message):  # Known type checking error
            await message.channel.send(random_choice(GREETINGS))

