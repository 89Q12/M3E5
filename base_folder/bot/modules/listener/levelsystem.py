from discord.ext import commands
from queuing.db import edit_settings_levelsystem, update_text_lvl, update_xp_text
from base_folder.bot.modules.base.get_from_db import Db

async def update_data(ctx, db):
    xp = db.get_text_xp(ctx.guild.id, ctx.author.id)
    amount = 0
    for msg in range(len(ctx.content)):
        amount += 1
    xp = amount + xp
    update_xp_text.delay(ctx.guild.id, ctx.author.id, xp)


async def is_enabled(guild: int, db):
    toggle = db.get_levelsystem(guild)
    if int(toggle.get()) == 1:
        return True
    else:
        return False


class Levelsystem(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = Db(client)

    @commands.group(pass_context=True)
    async def levelsystem(self, ctx):
        # Base command
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @levelsystem.command(name="toggle")
    async def levelsystem_toggle(self, ctx):
        # Toggle on/off the level system
        await ctx.channel.purge(limit=1)
        toggle = await self.db.get_levelsystem(ctx.guild.id)
        if 0 == toggle:
            await ctx.send("Level system is now enabled")
            edit_settings_levelsystem.delay(ctx.guild.id, 1)
        else:
            await ctx.send("Level system is now disabled")
            edit_settings_levelsystem.delay(ctx.guild.id, 0)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx is None:
            return
        if ctx.author.id == self.client.user.id:
            return
        channel = ctx.guild.system_channel
        await update_data(ctx, self.db)
        xp = await self.db.get_text_xp(ctx.guild.id, ctx.author.id)
        lvl_start = await self.db.get_lvl_text(ctx.guild.id, ctx.author.id)
        lvl_end = int(float(str(xp)) ** (1 / 4))
        if lvl_start < lvl_end:
            await channel.send(f"{ctx.author.mention} reached level {ctx.author} and has now {lvl_end, xp} xp")
            update_text_lvl.delay(ctx.guild.id, ctx.author.id, lvl_end)


def setup(client):
    client.add_cog(Levelsystem(client))
