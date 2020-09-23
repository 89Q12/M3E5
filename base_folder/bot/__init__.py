import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from base_folder.config import MAIN_BOT_TOKEN, sql
from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.logger import Log as stdout
import base_folder.bot.utils.helper as helper


class MainBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=helper.prefix, case_insensitive=True)
        self.client_id = 0
        self.log = stdout()
        self.sql = Db(sql())
        self.scheduler = AsyncIOScheduler()
        self.helper = helper
        self.cache = None

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
        if self.cache is None:
            self.cache = self.helper.DbCache(self.guilds, self.loop)
            self.cache.make_states()
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    # async def on_error(self, err, *args, **kwargs):
    #     raise

    # async def on_command_error(self, ctx, exc):
    #     raise getattr(exc, "original", exc)

    async def on_ready(self):
        if not self.scheduler.running:
            self.scheduler.start()
        for guild in self.guilds:
            await self.cache.states[guild.id].set_permission_roles()
            await self.cache.states[guild.id].set_channels()
        self.client_id = (await self.application_info()).id
        await self.change_presence(activity=discord.Game(name="Crushing data..."))
        print("Bot ready.")

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)