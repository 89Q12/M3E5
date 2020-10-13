import discord
from discord.ext import commands
from base_folder.bot.utils.Permissions import admin
from base_folder.config import success_embed
from base_folder.celery.db import *

'''
All commands that a guild team can use to customize the bot to there needs.
'''

# TODO: Adding custom color for embeds


class Custom(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''
    Custom settings
    '''

    @commands.command(pass_context=True, brief="sets the welcome channel set_welcome channel id")
    @commands.guild_only()
    @admin()
    async def set_welcome(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        channelwelcome = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channelwelcome.mention} is now the welcome channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("welcome",channel_id)
        edit_settings_welcome.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_leave channel id")
    @commands.guild_only()
    @admin()
    async def set_leave(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the leave channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("leave",channel_id)
        edit_settings_leave.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_lvl channel id")
    @commands.guild_only()
    @admin()
    async def set_lvl(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the level up channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("lvl", channel_id)
        edit_settings_lvl.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_cmd channel id")
    @commands.guild_only()
    @admin()
    async def set_cmd(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the command channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("cmd", channel_id)
        edit_settings_cmd.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @admin()
    async def prefix(self, ctx, arg):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        e = success_embed(self.client)
        e.description = f"{arg} is now the bot prefix"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].set_prefix(arg)
        set_prefix.delay(ctx.guild.id, arg)

    @commands.command(pass_context=True, brief="sets default role set_default @role")
    @commands.guild_only()
    @admin()
    async def set_default(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel =self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        edit_settings_role.delay(ctx.guild.id, role.id, "standard_role_id")
        e = success_embed(self.client)
        e.description = f"{role} is now the default role"
        await self.client.cache.states[ctx.guild.id].update_permission_role("default", role.id)
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @admin()
    async def set_admin(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel)
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        e = success_embed(self.client)
        e.description = f"{role} is now the admin role"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_permission_role("admin", role.id)
        edit_settings_role.delay(ctx.guild.id, role.id, "admin_role_id")

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @admin()
    async def set_dev(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        e = success_embed(self.client)
        e.description = f"{role} is now the dev role"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_permission_role("dev", role.id)
        edit_settings_role.delay(ctx.guild.id, role.id, "dev_role_id")

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @admin()
    async def set_mod(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(self.client.cache.states[ctx.guild.id].get_channel())
        if stdoutchannel is not None:
            await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        e = success_embed(self.client)
        e.description = f"{role} is now the mod role"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_permission_role("mod", role.id)
        edit_settings_role.delay(ctx.guild.id, role.id, "mod_role_id")


def setup(client):
    client.add_cog(Custom(client))
