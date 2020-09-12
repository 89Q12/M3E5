import discord
from discord.ext import commands
from base_folder.bot.config.Permissions import Auth
from base_folder.bot.config.config import success_embed
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
    async def set_welcome(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the welcome channel"
        await ctx.send(embed=e)
        edit_settings_welcome.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_leave channel id")
    @commands.guild_only()
    async def set_leave(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the leave channel"
        await ctx.send(embed=e)
        edit_settings_leave.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_lvl channel id")
    @commands.guild_only()
    async def set_lvl(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the level up channel"
        await ctx.send(embed=e)
        edit_settings_lvl.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_cmd channel id")
    @commands.guild_only()
    async def set_cmd(self, ctx, channel_id: int):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the command channel"
        await ctx.send(embed=e)
        edit_settings_cmd.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True)
    async def prefix(self, ctx, arg):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).is_admin() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        e = success_embed(self.client)
        e.description = f"{arg} is now the bot prefix"
        await ctx.send(embed=e)
        set_prefix.delay(ctx.guild.id, arg)

    @commands.command(pass_context=True, brief="sets default role set_default @role")
    @commands.guild_only()
    async def set_default(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        edit_settings_role.delay(ctx.guild.id, role.id, "standard_role_id")
        e = success_embed(self.client)
        e.description = f"{role} is now the default role"
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    async def set_admin(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        e = success_embed(self.client)
        e.description = f"{role} is now the admin role"
        await ctx.send(embed=e)
        edit_settings_role.delay(ctx.guild.id, role.id, "admin_role_id")

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    async def set_dev(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        e = success_embed(self.client)
        e.description = f"{role} is now the dev role"
        await ctx.send(embed=e)
        edit_settings_role.delay(ctx.guild.id, role.id, "dev_role_id")

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    async def set_mod(self, ctx, role: discord.Role = None):
        await ctx.channel.purge(limit=1)
        stdoutchannel = self.client.get_channel(await self.client.sql.get_stdout_channel(ctx.guild.id))
        await self.client.log.stdout(stdoutchannel, ctx.message.content, ctx)
        if await Auth(self.client, ctx).permissions() >= 3:
            pass
        else:
            raise commands.errors.CheckFailure
        e = success_embed(self.client)
        e.description = f"{role} is now the mod role"
        await ctx.send(embed=e)
        edit_settings_role.delay(ctx.guild.id, role.id, "mod_role_id")


def setup(client):
    client.add_cog(Custom(client))
