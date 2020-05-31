from discord.ext import commands
from modules.base.db.db_management import update_xp_text, get_text_xp,\
    get_lvl_text, update_text_lvl, \
    edit_settings_levelsystem, get_levelsystem


async def update_data(ctx):
    xp = await get_text_xp(ctx.guild.id, ctx.author.id)
    amount = 0
    if xp is None:
        amount = 5
        await update_xp_text(ctx.guild.id, ctx.author.id, amount)
    else:
        amount = 5 + xp
        await update_xp_text(ctx.guild.id, ctx.author.id, amount)


async def is_enabled(guild: int):
    if int(await get_levelsystem(guild)) == 1:
        return True
    else:
        return False


class Levelsystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(pass_context=True)
    async def levelsystem(self, ctx):
        # Base command
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @levelsystem.command(name="toggle")
    async def levelsystem_toggle(self, ctx):
        # Toggle on/off the level system
        await ctx.channel.purge(limit=1)
        toggle = int(await get_levelsystem(ctx.guild.id))
        if 0 == toggle:
            await edit_settings_levelsystem(ctx.guild.id, 1)
            await ctx.send("Level system is now enabled")
        else:
            await edit_settings_levelsystem(ctx.guild.id, 0)
            await ctx.send("Level system is now disabled")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        channel = ctx.guild.system_channel
        if ctx.author.id == self.client.user.id:
            return
        if not await is_enabled(ctx.guild.id):
            return
        await update_data(ctx)
        xp = await get_text_xp(ctx.guild.id, ctx.author.id)
        lvl_start = await get_lvl_text(ctx.guild.id, ctx.author.id)
        lvl_end = int(float(str(xp)) ** (1 / 4))
        if lvl_start is None:
            await update_text_lvl(ctx.guild.id, ctx.author.id)
            lvl_start = await get_lvl_text(ctx.guild.id, ctx.author.id)
        if lvl_start < lvl_end:
            await update_text_lvl(ctx.guild.id, ctx.author.id, lvl_end)
            await channel.send(f"{ctx.author.mention} reached level {ctx.author} and has now {lvl_end, xp} xp")


def setup(client):
    client.add_cog(Levelsystem(client))
