import discord
from discord.ext import commands

from base_folder.bot.utils.Permissions_checks import admin
from base_folder.bot.utils.checks import check_args_datatyp, logging_to_channel_stdout, purge_command_in_channel
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
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_welcome(self, ctx, channel_id: int):
        channelwelcome = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channelwelcome.mention} is now the welcome channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("welcome", channel_id)
        edit_settings_welcome.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_leave channel id")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_leave(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the leave channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("leave", channel_id)
        edit_settings_leave.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, name="set_logs", brief="sets the standard logging channel"
                                                                "e.g. for errors and such "
                                                                "set_stdout/set_logs channel id")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_stdout(self, ctx, channel_id: int):
        channelstdout = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channelstdout.mention} is now the standard out channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("stdout", channel_id)
        edit_settings_stdout.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, name="set_ban", brief="sets the standard banning channel"
                                                               "only for bans set_warns channel id. Not required")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_ban(self, ctx, channel_id: int):
        channelban = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channelban.mention} is now the ban channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("ban", channel_id)
        edit_settings_ban.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, name="set_warns", brief="sets the standard warning channel"
                                                                 "only for warnings set_warns channel id. Not required")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_warns(self, ctx, channel_id: int):
        channelwarn = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channelwarn.mention} is now the warn channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("warn", channel_id)
        edit_settings_warn.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, name="set_kicks", brief="sets the standard kicking channel"
                                                                 "only for kicks set_kicks channel id. Not required")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_kicks(self, ctx, channel_id: int):
        channelkick = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channelkick.mention} is now the kick channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("kick", channel_id)
        edit_settings_kick.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_lvl channel id")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_lvl(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the level up channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("lvl", channel_id)
        edit_settings_lvl.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True, brief="sets the leave channel set_cmd channel id")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_cmd(self, ctx, channel_id: int):
        channel = self.client.get_channel(channel_id)
        e = success_embed(self.client)
        e.description = f"{channel.mention} is now the command channel"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_channel("cmd", channel_id)
        edit_settings_cmd.delay(ctx.guild.id, channel_id)

    @commands.command(pass_context=True)
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def prefix(self, ctx, arg: str):
        e = success_embed(self.client)
        await self.client.cache.states[ctx.guild.id].set_prefix(arg)
        prefix = self.client.cache.states[ctx.guild.id].get_prefix
        e.description = f"{prefix} is now the bot prefix"
        await ctx.send(embed=e)
        set_prefix.delay(ctx.guild.id, arg)

    @commands.command(pass_context=True, brief="sets default role set_default @role")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_default(self, ctx, role: discord.Role = None):
        edit_settings_role.delay(ctx.guild.id, role.id, "standard_role_id")
        e = success_embed(self.client)
        e.description = f"{role} is now the default role"
        await self.client.cache.states[ctx.guild.id].update_permission_role("default", role.id)
        await ctx.send(embed=e)

    @commands.command(pass_context=True, brief="sets admin rule set_admin @role")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    async def set_admin(self, ctx, role: discord.Role = None):
        e = success_embed(self.client)
        e.description = f"{role} is now the admin role"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_permission_role("admin", role.id)
        edit_settings_role.delay(ctx.guild.id, role.id, "admin_role_id")

    @commands.command(pass_context=True, brief="sets dev rule set_dev @role")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_dev(self, ctx, role: discord.Role = None):
        e = success_embed(self.client)
        e.description = f"{role} is now the dev role"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_permission_role("dev", role.id)
        edit_settings_role.delay(ctx.guild.id, role.id, "dev_role_id")

    @commands.command(pass_context=True, brief="sets mod rule set_mod @role")
    @commands.guild_only()
    @admin()
    @check_args_datatyp
    @logging_to_channel_stdout
    @purge_command_in_channel
    async def set_mod(self, ctx, role: discord.Role = None):
        e = success_embed(self.client)
        e.description = f"{role} is now the mod role"
        await ctx.send(embed=e)
        await self.client.cache.states[ctx.guild.id].update_permission_role("mod", role.id)
        edit_settings_role.delay(ctx.guild.id, role.id, "mod_role_id")


def setup(client):
    client.add_cog(Custom(client))
