from random import choice as random_choice
from datetime import date
from typing import Optional, Callable
import functools

from discord.utils import Coro

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

def handle_timeout(f: Callable[..., Coro[None]]) -> Callable[..., Coro[None]]:
    @functools.wraps(f)
    async def wrapper(*args, **kwargs) -> None:
        ctx: commands.Context = args[1] # Kinda hacky but if it works ig
        try:
            async with ctx.typing():
                await f(*args, **kwargs)
        except Timeout:
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
    @commands.command()
    @handle_timeout
    async def search(self, ctx: commands.Context, media: Optional[MediaType], *, search_string: str) -> None:
        media = media or "TV"

        response = media_query(search_string, media)
        err = response.get("errors")
        data = response.get("data")

        if err:
            await ctx.send(embed=api_error(err[0]["message"]))
            return
        if data:
            await ctx.send(embed=anime_card(data["Media"]))
        else:
            await ctx.send(embed=api_error("No data was found"))

    # Search for seasonal anime.
    @commands.command()
    @handle_timeout
    async def seasonal(
        self,
        ctx: commands.Context,
        results: Optional[int],
        season: Optional[SeasonType],
        year: Optional[int]
    ) -> None:
        results = results or 3
        season = season or curr_season()
        year = year or date.today().year

        response = seasonal_query(season, year, results)
        err = response.get("errors")
        data = response.get("data")

        if err:
            await ctx.send(embed=api_error(err[0]["message"]))
            return
        if data:
            anime_cards = seasonal_cards(data["Page"]["media"])
            await ctx.send(embeds=anime_cards)
        else:
            await ctx.send(embed=api_error("No data was found"))


    @commands.command()
    @handle_timeout
    async def info(self, ctx: commands.Context, mal_id: int) -> None:
        response = mal_id_query(mal_id)
        err = response.get("errors")
        data = response.get("data")

        if err:
            await ctx.send(embed=api_error(err[0]["message"]))
            return
        if data:
            await ctx.send(embed=anime_card(data["Media"]))
            return
        else:
            await ctx.send(embed=api_error("No data was found"))

    # Redefined help command
    @commands.command()
    async def help(self, ctx: commands.Context, *, opt="general") -> None:
        is_owner = await self.bot.is_owner(ctx.author)
        userHelp, adminHelp = help_command(opt, ctx.prefix, self.about_me, is_owner=is_owner) # Known type checking error
        await ctx.send(embed=userHelp)
        if adminHelp is not None:
            await ctx.reply(embed=adminHelp, mention_author=False, ephemeral=True)


    # A function that runs on every message sent.
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return

        elif self.bot.user.mentioned_in(message):  # Known type checking error
            await message.channel.send(random_choice(GREETINGS))

