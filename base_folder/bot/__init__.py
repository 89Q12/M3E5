from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from base_folder.config import MAIN_BOT_TOKEN
from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.logger import Log as stdout
import base_folder.bot.utils.helper as helper


class MainBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=helper.prefix, case_insensitive=True)
        self.sql = Db()  # creates an sql connection object that's accessible via the client object
        self.log = stdout()
        self.scheduler = AsyncIOScheduler()
        self.helper = helper

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

    # async def on_error(self, err, *args, **kwargs):
    #     raise

    # async def on_command_error(self, ctx, exc):
    #     raise getattr(exc, "original", exc)

    async def on_ready(self):
        if not self.scheduler.running:
            self.scheduler.start()
        self.client_id = (await self.application_info()).id
        print("Bot ready.")

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)