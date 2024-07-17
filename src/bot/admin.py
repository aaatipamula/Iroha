from datetime import datetime
from asyncio import TimeoutError

from discord import Game
from discord.ext import commands

from bot.embeds import admin_dashboard, cmd_error, info_msg

class AdminCog(commands.Cog):
    def __init__(
        self, 
        bot: commands.Bot, 
        log_channel_id: int,
        start_datetime: datetime,
        # NOTE: Make this an enviornment variable eventually
        confirmation_emote_id: int = 1136812895859134555 #:L_: emoji 
    ) -> None:
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.confim_emote_id = confirmation_emote_id

        self.start_datetime = start_datetime
        self.locked = False

    @property
    def log_channel(self):
        return self.bot.get_channel(self.log_channel_id)

    @property
    def confim_emote(self):
        return self.bot.get_emoji(self.confim_emote_id)

    @commands.group(pass_context=True)
    async def admin(self, ctx) -> None:
        if not ctx.invoked_subcommand:
            embed = await admin_dashboard(self.bot, self.start_datetime)
            await ctx.send(embed=embed)

    @admin.command()
    async def status(self, ctx, *, status: str) -> None:
        game = Game(status)
        await self.bot.change_presence(activity=game)
        await ctx.reply(f"Changed To: {status}", mention_author=False, ephemeral=False)

    @admin.command(name="kill")
    async def kill_bot(self, ctx) -> None:
        await ctx.send(f"NOOOOO PLEASE {self.bot.get_emoji(1145147159260450907)}") # :cri: emoji

        def check(reaction, user):
            return self.bot.is_owner(user) and reaction.emoji == self.confim_emote

        try:
            await self.bot.wait_for("reaction_add", timeout=10.0, check=check)
        except TimeoutError:
            await ctx.send(self.bot.get_emoji(994378239675990029))
        else:
            await ctx.send(self.bot.get_emoji(1145090024333918320))
            exit(0)

    @admin.command()
    async def lock(self, ctx) -> None:
        if self.locked:
            await ctx.send(embed=cmd_error("Commands already locked."))
        else:
            self.locked = True
            await ctx.send(embed=info_msg("Commands now locked."))

    @admin.command()
    async def unlock(self, ctx) -> None:
        if not self.locked:
            await ctx.send(embed=cmd_error("Commands already unlocked."))
        else:
            self.locked = False
            await ctx.send(embed=info_msg("Commands now unlocked."))

    # check if commands are locked
    async def bot_check(self, ctx) -> bool:
        if await self.bot.is_owner(ctx.author):
            return True
        return not self.locked

    # checks if the author is the owner
    async def cog_check(self, ctx) -> bool:
        return await self.bot.is_owner(ctx.author)

