import discord
from discord.ext import commands
from discord import Intents
from discord.ext.commands import errors
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from base_folder.config import MAIN_BOT_TOKEN
from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.logger import Log as stdout
from base_folder.bot.utils.checks import *
import base_folder.bot.utils.helper as helper


class MainBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=helper.prefix, case_insensitive=True, guild_subscriptions=True,
                         fetch_offline_members=True, intents=Intents.all())
        self.client_id = 0
        self.Version = 3.0
        self.log = stdout()
        self.scheduler = AsyncIOScheduler()
        self.helper = helper
        self.cache = self.helper.DbCache(self.loop)
        self.sql = Db()
        self.booted = False

    def run(self, modules):
        helper.loadmodules(modules, self)
        print("Running bot...")
        super().run(MAIN_BOT_TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_ready(self):
        if super().is_ready():
            self.booted = True
            if not self.scheduler.running:
                self.scheduler.start()
            self.cache.make_states(self.guilds, self.log)
            for guild in self.guilds:
                await self.cache.states[guild.id].set_spamsettings()
                await self.cache.states[guild.id].set_permission_roles()
                await self.cache.states[guild.id].set_channels()
                await self.cache.states[guild.id].set_users()
                await self.cache.states[guild.id].set_banned_lists()

            self.client_id = (await self.application_info()).id
            await self.change_presence(activity=discord.Game(name="Crushing data..."))
            print("Bot ready.")

    @banned_channel_list_cmd
    @banned_user_list_cmd
    @banned_roles_list_cmd
    async def invoke(self, ctx):
        """|coro|
        *Just added to run checks, so I get the code more dry*
        Invokes the command given under the invocation context and
        handles all the internal event dispatch mechanisms.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context to invoke.
        """
        if ctx.command is not None:
            self.dispatch('command', ctx)
            try:
                if await self.can_run(ctx, call_once=True):
                    await ctx.command.invoke(ctx)
                else:
                    raise errors.CheckFailure('The global check once functions failed.')
            except errors.CommandError as exc:
                await ctx.command.dispatch_error(ctx, exc)
            else:
                self.dispatch('command_completion', ctx)
        elif not ctx.internal:
            pass
        elif ctx.invoked_with:
            # TODO: Add the ability for custom commands here!
            exc = errors.CommandNotFound('Command "{}" is not found'.format(ctx.invoked_with))
            self.dispatch('command_error', ctx, exc)

    async def process_commands(self, msg):
        """
        This gets the context and invokes the cmd
        :param msg: message from on message event
        """
        ctx = await self.get_context(msg, cls=commands.Context)
        await self.cache.states[ctx.guild.id].users[ctx.author.id].propagate(msg)
        custom_cmds = []
        if ctx.command in custom_cmds:
            ctx.internal = False
            await self.invoke(ctx)
            return
        ctx.internal = True
        await self.invoke(ctx)

    @banned_user_list_spam
    @banned_channel_list_spam
    @banned_roles_list_spam
    async def process_spam(self, ctx):
        await self.cache.states[ctx.guild.id].users[ctx.author.id].propagate(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            if self.booted:
                await self.process_commands(msg)
                return
            await msg.channel.send(f"The bot is still booting.")
