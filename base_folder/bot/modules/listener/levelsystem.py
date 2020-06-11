from discord.ext import commands
from base_folder.queuing.db import edit_settings_levelsystem, update_text_lvl, get_lvl_text, get_levelsystem, \
    get_text_xp, update_xp_text


async def update_data(ctx):
    xp = get_text_xp.delay(ctx.guild.id, ctx.author.id)
    amount = 0
    for msg in range(len(ctx.content)):
        amount += 1
    update_xp_text.delay(ctx.guild.id, ctx.author.id, amount + xp.get())


async def is_enabled(guild: int):
    toggle = get_levelsystem.delay(guild)
    if int(toggle.get()) == 1:
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
        toggle = get_levelsystem.delay(ctx.guild.id)
        if 0 == toggle.get():
            edit_settings_levelsystem.delay(ctx.guild.id, 1)
            await ctx.send("Level system is now enabled")
        else:
            edit_settings_levelsystem.delay(ctx.guild.id, 0)
            await ctx.send("Level system is now disabled")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx is None:
            return
        if ctx.author.id == self.client.user.id:
            return
        if not await is_enabled(ctx.guild.id):
            return
        channel = ctx.guild.system_channel
        await update_data(ctx)
        xp = get_text_xp.delay(ctx.guild.id, ctx.author.id)
        lvl_start = get_lvl_text.delay(ctx.guild.id, ctx.author.id)
        lvl_end = int(float(str(xp.get())) ** (1 / 4))
        if lvl_start.get() < lvl_end:
            update_text_lvl.delay(ctx.guild.id, ctx.author.id, lvl_end)
            await channel.send(f"{ctx.author.mention} reached level {ctx.author} and has now {lvl_end, xp} xp")


def setup(client):
    client.add_cog(Levelsystem(client))
