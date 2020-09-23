import asyncio

from discord.ext import commands
import discord
from base_folder.celery.db import insert_reaction
"""
This will be for custom reaction roles on messages for this to work somethings are neeeded:
    - guild id of the guild 
    - message id and store it
    - emoji's
        - check if its custom -> return because custom is not supported yet else get the id and store it
    - role id that should be given to the member
    
So 4 functions are needed:
- add reaction message
    - write the message id, guild id, emoji id and role id id in the db 
    - react with the emoji's to the message
- delete the reaction message from the db
    - delete everything from db tbl reactions role by message id and the emoji id
    - remove the reactions
- listener on_raw_reaction_add
    - check if its a custom reaction if yes return else proceed
    - check the message id against the db if the message id isnt returned return
    - get the emoji id, guild id  and get the the role id associated with the message id, guild id and  emoji id 
    - get the role by the role id and give it to the given member 
- listener on_raw_reaction_remove
    - check the message id against the db if the message id isnt retuned return
    - get the emoji id, guild id  and get the the role id associated with the message id, guild id and  emoji id 
    - get the role by the role id and remove it from the given member 
"""


class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Adds reactions to a message")
    async def add_reaction(self, ctx, messageid: int, channel: discord.TextChannel):
        """

        :param ctx: is the current context, guild etc
        :param messageid: the message id to react on
        :param channel: the channel with the message to react to
        :return: nothing
        """
        async with ctx.channel.typing():
            message = await channel.fetch_message(messageid)

        try:
            def check(reaction, user):
                return user == message.author
            await ctx.send("Please react to the message above with the emoji of your choice. You have 20 secs to do so")
            reaction_tupel = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
            reaction = reaction_tupel[0]
            emoji = reaction.emoji
            print(type(emoji))
            print(emoji)
        except asyncio.TimeoutError:
            await ctx.send("Timed out please resend the command"+'👎')
            return
        else:
            await ctx.send("Done " + '👍')
        try:
            await ctx.send("Now please mention a role you want to give a user when then user"
                           " reacts with a the given emote. You have 30 seconds todo sp")

            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel
            m = await self.client.wait_for('message', timeout=20.0, check=check)
            role = m.role_mentions
        except asyncio.TimeoutError:
            await ctx.send("Timed out please resend the command"+'👎')
            return
        else:
            await ctx.send("Done " + '👍')
        await message.add_reaction(emoji)
        insert_reaction.delay(ctx.guild.id, messageid, role[0].id, emoji)

    @commands.command(brief="deletes reactions from a message, cant be undone")
    async def del_reaction(self, messageid: int, emoji: discord.emoji):
        """

        :param messageid: the message id to react on
        :param emoji: the emoji that the bot reacted with
        :return:nothing
        """
        pass
    # TODO: Refactor following event so that it doesnt raise anything

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.member.bot:
            if payload.emoji.name:
                try:
                    roleid = await self.client.sql.get_reaction_role(payload.guild_id, payload.message_id, payload.emoji.name)
                    role = discord.utils.get(payload.member.guild.roles, id=roleid)
                    await payload.member.add_roles(role, reason="reaction added", atomic=True)
                except TypeError:
                    return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if not payload.guild_id:
            return
        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member.bot:
            try:
                roleid = await self.client.sql.get_reaction_role(payload.guild_id, payload.message_id, payload.emoji.name)
                role = discord.utils.get(guild.roles, id=roleid)
                await member.remove_roles(role, reason="reaction removed", atomic=True)
            except TypeError:
                return


def setup(client):
    client.add_cog(ReactionRoles(client))
