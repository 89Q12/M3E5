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


async def deban(time, ctx, member: str = "",):
    await asyncio.sleep(time*600)
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


async def demute(time, ctx,  member: discord.Member = None):
    await asyncio.sleep(time * 600)
    try:
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))  # removes muted role
        await ctx.send(f"{member.mention} has been unmuted")
    except Exception as e:
        await ctx.send(f"{member.mention} already unmuted or {member.mention} was never muted")
