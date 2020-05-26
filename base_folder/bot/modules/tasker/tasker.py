import discord
from discord.ext import commands
import asyncio

'''
May be used later on
async def runtasks(client):
    await client.wait_until_ready()
    while client != client.is_closed:
        await asyncio.sleep(10)
'''


async def debun(time, ctx, member: str = "",):
    await asyncio.sleep(time*6)
    reason = "You have been unbanned. Time is over. Please behave"
    if member == "":
        await ctx.send("Please specify username as text")
        return
    bans = await ctx.guild.bans()
    for b in bans:
        if b.user.name == member:
            await ctx.guild.unban(b.user, reason=reason)
            await ctx.send(f"User {member} was unbanned")
            return
    await ctx.send("User was not found in ban list.")
