from discord.ext import commands
from base_folder.bot.config.config import success_embed
from base_folder.queuing.db import update_text_lvl, update_xp_text


async def update_data(ctx, xp):
    amount = 0
    for i in str(ctx.content).split(" "):
        amount += 1
    xp += amount
    update_xp_text.delay(ctx.guild.id, ctx.author.id, xp)
    return xp


async def _enabled(client, guildid):
    if await client.sql.get_levelsystem(guildid) == 1:
        return True
    else:
        return False


class Levelsystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content is None:
            return
        if not await _enabled(self.client, message.guild.id):
            return
        if message.author.id == self.client.user.id:
            return
        channel_id = await self.client.sql.get_lvl_channel(message.guild.id)
        if channel_id == 0 or None:
            channel = message.guild.system_channel
        else:
            channel = self.client.get_channel(channel_id)
        xp_before = await self.client.sql.get_text_xp(message.guild.id, message.author.id)
        xp_after = await update_data(message, xp_before)
        e = success_embed(self.client)
        lvl_start = await self.client.sql.get_lvl_text(message.guild.id, message.author.id)
        lvl_end = int(float(str(xp_after)) ** (1 / 4))
        if lvl_start < lvl_end:
            e.title = "LEEVEEL UP"
            e.description = f"{message.author.mention} reached level {lvl_end} and has now {xp_after}xp"
            await channel.send(embed=e)
            update_text_lvl.delay(message.guild.id, message.author.id, lvl_end)
            update_xp_text.delay(message.guild.id, message.author.id, xp_after)


def setup(client):
    client.add_cog(Levelsystem(client))
