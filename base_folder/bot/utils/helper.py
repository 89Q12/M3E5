"""
This helper script is helpful in some situations  like creating the ctx object out of the member object etc
"""
from asyncio import run_coroutine_threadsafe
from string import Template
import logging
import asyncio
import datetime
from copy import deepcopy
import discord
from fuzzywuzzy import fuzz


from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.utils.exceptions import DuplicateObject, ObjectMismatch, LogicError, MissingGuildPermissions

class Ctx:
    """
    Not the fully featured ctx object but its doing the job
    """

    def __init__(self, member):
        self.member = member
        self.guild = member.guild
        self.author = member


def prefix(client, ctx):
    try:
        pre = client.cache.states[ctx.guild.id].get_prefix
        return pre
    except Exception:
        return "-"


def loadmodules(modules, client):
    for extension in modules:
        try:
            client.load_extension(extension)
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


'''
This class is designed to hold all data that the bot uses extensively and the class is designed in a way that it can
reload the data on change.
'''
# TODO: Look above


class DbCache:
    def __init__(self, loop=None):
        self.loop = loop
        self._states = {}

    @property
    def states(self, guild=None):
        if not guild:
            return self._states
        else:
            return self._states[guild.id]

    def make_states(self, guilds, logger):
        for guild in guilds:
            self._states[guild.id] = GuildStates(guild, self.loop, logger)

    def create_state(self, guild):
        self._states[guild.id] = GuildStates(guild, self.loop)

    def destruct_state(self, guild):
        del self._states[guild.id]


class GuildStates:
    def __init__(self, guild, loop, logger):
        self.loop = loop
        self.db = Db()
        self.guild = guild
        self.logger = logger
        self.options = {}
        self.users = {}
        self._permisson_roles = {}
        self._prefix = None
        self._levelsystem_toggle = None
        self._get_imgtoggle = None
        self._channels = {}
        self.banned_channels_cmd = []
        self.banned_roles_cmd = []
        self.banned_users_cmd = []
        self.banned_channels_spam = []
        self.banned_roles_spam = []
        self.banned_users_spam = []

    @property
    def get_prefix(self):
        if self._prefix is None:
            self._prefix = self.db.prefix_lookup(self.guild.id)
        return self._prefix

    @property
    def get_levelsystem(self):
        if self._levelsystem_toggle is None:
            run_coroutine_threadsafe(self.set_lvltoggle(), self.loop)
        return self._levelsystem_toggle

    @property
    def get_imgtoggle(self):
        if self._get_imgtoggle is None:
            run_coroutine_threadsafe(self.set_imgtoggle(), self.loop)
        return self._get_imgtoggle

    @property
    def get_perm_list(self):
        role_list = []
        for r in self._permisson_roles:
            role_list.append(self._permisson_roles[r])
        return role_list

    async def set_spamsettings(self):
        opts = await self.db.get_spam_settings(self.guild.id)
        options = {
            "warnThreshold": opts[0][0],
            "kickThreshold": opts[0][1],
            "banThreshold": opts[0][2],
            "messageInterval": opts[0][3],
            "warnMessage": opts[0][4],
            "kickMessage": opts[0][5],
            "banMessage": opts[0][6],
            "messageDuplicateCount": opts[0][7],
            "messageDuplicateAccuracy": opts[0][8],
            "ignorePerms": [8],  # TODO: make this customizable
            "ignoreUsers": [],  # TODO: make this customizable too
            "ignoreBots": True,
            "dc_channel": self._channels["stdout"]
        }
        self.options = options

    async def set_users(self):
        for user in self.guild.members:
            user_data = {
                'warnCount': await self.db.get_warns(self.guild.id, user.id),
                'kickCount': await self.db.get_kick_count(self.guild.id, user.id),
            }
            self.users[user.id] = User(user.id, self.guild.id, self.options, user_data, self.logger)

    def get_role(self, rolename="admin"):
        role_id = self._permisson_roles[rolename]
        return role_id

    def get_channel(self, channelname="stdout"):
        channelid = self._channels[channelname]
        if channelid == 0:
            run_coroutine_threadsafe(self.set_channels(), self.loop)
        return channelid

    async def set_prefix(self, newprefix):
        self._prefix = newprefix

    async def set_permission_roles(self):
        self._permisson_roles['mod'] = await self.db.get_mod_role(self.guild.id)
        self._permisson_roles['admin'] = await self.db.get_admin_role(self.guild.id)
        self._permisson_roles['dev'] = await self.db.get_dev_role(self.guild.id)
        self._permisson_roles['default'] = await self.db.get_standard_role(self.guild.id)

    async def set_channels(self):
        self._channels['leave'] = await self.db.get_leave_channel(self.guild.id)
        self._channels['welcome'] = await self.db.get_welcome_channel(self.guild.id)
        self._channels['stdout'] = await self.db.get_stdout_channel(self.guild.id)
        self._channels['lvl'] = await self.db.get_lvl_channel(self.guild.id)
        self._channels['cmd'] = await self.db.get_cmd_channel(self.guild.id)

    async def set_banned_lists(self):
        self.banned_channels_cmd = await self.db.get_banned_channels_cmd(self.guild.id)
        self.banned_roles_cmd = await self.db.get_banned_roles_cmd(self.guild.id)
        self.banned_users_cmd = await self.db.get_banned_users_cmd(self.guild.id)
        self.banned_channels_spam = await self.db.get_banned_channels_spam(self.guild.id)
        self.banned_roles_spam = await self.db.get_banned_roles_spam(self.guild.id)
        self.banned_users_spam = await self.db.get_banned_users_spam(self.guild.id)

    async def set_imgtoggle(self):
        self._get_imgtoggle = await self.db.get_img(self.guild.id)

    async def set_lvltoggle(self):
        self._levelsystem_toggle = await self.db.get_levelsystem(self.guild.id)

    async def update_channel(self, channelname, channelid):
        self._channels[channelname] = channelid

    async def update_permission_role(self, rolename, roleid):
        self._permisson_roles[rolename] = roleid

    async def destruct_User(self, userid):
        del self.users[userid]


class User:
    """
    I modified the code but most of the code belongs to:

    MIT License

    Copyright (c) 2020 Skelmis

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    """A class dedicated to maintaining a member, and any relevant messages in a single guild.
    """

    __slots__ = [
        "_id",
        "_guild_id",
        "_messages",
        "options",
        "warn_count",
        "kick_count",
        "duplicate_counter",
        "logger",
        "BAN",
        "KICK",
    ]

    def __init__(self, id, guild_id, options, user_data,logger):
        """
        Set the relevant information in order to maintain
        and use a per User object for a guild
        Parameters
        ==========
        bot : commands.bot
            Bot instance
        id : int
            The relevant member id
        guild_id : int
            The guild (id) this member is belonging to
        options : Dict
            The options we need to check against
        """
        self.id = int(id)
        self.guild_id = int(guild_id)
        self._messages = []
        self.options = options
        self.warn_count = user_data["warnCount"]
        self.kick_count = user_data["kickCount"]
        self.duplicate_counter = 1
        self.logger = logger
        self.KICK = "kick"
        self.BAN = "ban"

    def __repr__(self):
        return (
            f"'{self.__class__.__name__} object. User id: {self.id}, Guild id: {self.guild_id}, "
            f"Len Stored Messages {len(self._messages)}'"
        )

    def __str__(self):
        return f"{self.__class__.__name__} object for {self.id}."

    def __eq__(self, other):
        """
        This is called with a 'obj1 == obj2' comparison object is made
        Checks against stored id's to figure out if they are
        representing the same User or not
        Parameters
        ----------
        other : User
            The object to compare against
        Returns
        -------
        bool
            `True` or `False` depending on whether they are the same or not
        Raises
        ======
        ValueError
            When the comparison object is not of ignore_type `Message`
        """
        if not isinstance(other, User):
            raise ValueError("Expected two User objects to compare")

        if self.id == other.id and self.guild_id == other.guild_id:
            return True
        return False

    def __hash__(self):
        """
        Given we create a __eq__ dunder method, we also needed
        to create one for __hash__ lol
        Returns
        -------
        int
            The hash of all id's
        """
        return hash((self.id, self.guild_id))

    def propagate(self, value: discord.Message):
        """
        This method handles a message object and then adds it to
        the relevant member
        Parameters
        ==========
        value : discord.Message
            The message that needs to be propagated out
        """
        if not isinstance(value, discord.Message):
            raise ValueError("Expected message of ignore_type: discord.Message")

        self.clean_up(datetime.datetime.now(datetime.timezone.utc))

        # No point saving empty messages, although discord shouldn't allow them anyway
        if not bool(value.content and value.content.strip()):
            return
        else:
            message = Message(
                value.id,
                value.clean_content,
                value.author.id,
                value.channel.id,
                value.guild.id,
            )

        for message_obj in self.messages:
            # This calculates the relation to each other
            if message == message_obj:
                raise DuplicateObject

            elif (
                fuzz.token_sort_ratio(message.content, message_obj.content)
                >= self.options["message_duplicate_accuracy"]
            ):
                """
                The handler works off an internal message duplicate counter 
                so just increment that and then let our logic process it
                """
                self.duplicate_counter += 1
                message.is_duplicate = True

                if self.duplicate_counter >= self.options["message_duplicate_count"]:
                    break

        # We check this again, because theoretically the above can take awhile to process etc

        self.messages = message
        self.logger.log.info(f"Created Message: {message.id}")

        if self.duplicate_counter >= self.options["message_duplicate_count"]:
            self.logger.log.debug(
                f"Message: ({message.id}) requires some form of punishment"
            )
            # We need to punish the member with something

            if (
                self.duplicate_counter >= self.options["warn_threshold"]
                and self.warn_count < self.options["kick_threshold"]
                and self.kick_count < self.options["ban_threshold"]
            ):
                self.logger.log.debug(f"Attempting to warn: {message.author_id}")
                """
                The member has yet to reach the warn threshold,
                after the warn threshold is reached this will
                then become a kick and so on
                """
                # We are still in the warning area
                channel = value.channel
                guild_message = transform_message(
                    self.options["guild_warn_message"],
                    value,
                    {"warn_count": self.warn_count, "kick_count": self.kick_count},
                )

                asyncio.ensure_future(send_to_obj(channel, guild_message))
                self.warn_count += 1

            elif (
                self.warn_count >= self.options["kick_threshold"]
                and self.kick_count < self.options["ban_threshold"]
            ):
                # Set this to False here to stop processing other messages, we can revert on failure

                self.logger.log.debug(f"Attempting to kick: {message.author_id}")
                # We should kick the member
                guild_message = transform_message(
                    self.options["guild_kick_message"],
                    value,
                    {"warn_count": self.warn_count, "kick_count": self.kick_count},
                )
                user_message = transform_message(
                    self.options["user_kick_message"],
                    value,
                    {"warn_count": self.warn_count, "kick_count": self.kick_count},
                )
                asyncio.ensure_future(
                    self._punish_user(value, user_message, guild_message, self.KICK,)
                )
                self.kick_count += 1

            elif self.kick_count >= self.options["ban_threshold"]:
                # Set this to False here to stop processing other messages, we can revert on failure

                self.logger.log.debug(f"Attempting to ban: {message.author_id}")
                # We should ban the member
                guild_message = transform_message(
                    self.options["guild_ban_message"],
                    value,
                    {"warn_count": self.warn_count, "kick_count": self.kick_count},
                )
                user_message = transform_message(
                    self.options["user_ban_message"],
                    value,
                    {"warn_count": self.warn_count, "kick_count": self.kick_count},
                )
                asyncio.ensure_future(
                    self._punish_user(value, user_message, guild_message, self.BAN,)
                )
                self.kick_count += 1

            else:
                raise LogicError

    async def _punish_user(self, value, user_message, guild_message, method):
        """
        A generic method to handle multiple methods of punishment for a user.
        Currently supports: kicking, banning
        TODO: mutes
        Parameters
        ----------
        value : discord.Message
            Where we get everything from :)
        user_message : str
            A message to send to the user who is being punished
        guild_message : str
            A message to send in the guild for whoever is being punished
        method : str
            A string denoting the ignore_type of punishment
        Raises
        ======
        LogicError
            If you do not pass a support punishment method
        """
        guild = value.guild
        member = value.author
        dc_channel = self.options["dc_channel"]
        if method != self.KICK and method != self.BAN:
            raise LogicError(f"{method} is not a recognized punishment method.")

        # Check we have perms to punish
        perms = guild.me.guild_permissions
        if not perms.kick_members and method == self.KICK:
            raise MissingGuildPermissions(
                f"I need kick perms to punish someone in {guild.name}"
            )

        elif not perms.ban_members and method == self.BAN:
            raise MissingGuildPermissions(
                f"I need ban perms to punish someone in {guild.name}"
            )

        # We also check they don't own the guild, since ya know...
        elif guild.owner_id == member.id:
            raise MissingGuildPermissions(
                f"I cannot punish {member.display_name}({member.id}) "
                f"because they own this guild. ({guild.name})"
            )

        # Ensure we can actually punish the user, for this
        # we just check our top role is higher then them
        elif guild.me.top_role.position < member.top_role.position:
            self.logger.warn(
                f"I might not be able to punish {member.display_name}({member.id}) in {guild.name}({guild.id}) "
                "because they are higher then me, which means I could lack the ability to kick/ban them."
            )

        m = None

        try:
            # Attempt to message the punished member, about their punishment
            try:
                m = await send_to_obj(member, user_message)
            except discord.HTTPException:
                await send_to_obj(
                    dc_channel,
                    f"Sending a message to {member.mention} about their {method} failed.",
                )
                self.logger.warn(
                    f"Failed to message User: ({member.id}) about {method}"
                )
            finally:

                # Even if we can't tell them they are being punished
                # We still need to punish them, so try that
                try:
                    if method == self.KICK:
                        await guild.kick(
                            member, reason="Automated punishment from DPY Anti-Spam."
                        )
                        self.logger.log.info(f"Kicked User: ({member.id})")
                    elif method == self.BAN:
                        await guild.ban(
                            member, reason="Automated punishment from DPY Anti-Spam."
                        )
                        self.logger.log.info(f"Banned User: ({member.id})")
                    else:
                        raise NotImplementedError
                except discord.Forbidden:
                    await send_to_obj(
                        dc_channel,
                        f"I do not have permission to kick: {member.mention}",
                    )
                    self.logger.log.warn(f"Required Permissions are missing for: {method}")
                    if m is not None:
                        await send_to_obj(
                            member,
                            "I failed to punish you because I lack permissions, but still you shouldn't spam.",
                        )
                        await m.delete()

                except discord.HTTPException:
                    await send_to_obj(
                        dc_channel,
                        f"An error occurred trying to {method}: {member.mention}",
                    )
                    self.logger.log.warn(
                        f"An error occurred trying to {method}: {member.id}"
                    )
                    if m is not None:
                        await send_to_obj(
                            member,
                            "I failed to punish you because I lack permissions, but still you shouldn't spam.",
                        )
                        await m.delete()

                else:
                    try:
                        await send_to_obj(dc_channel, guild_message)
                    except discord.HTTPException:
                        self.logger.log.error(
                            f"Failed to send message.\n"
                            f"Guild: {dc_channel.guild.name}({dc_channel.guild.id})\n"
                            f"Channel: {dc_channel.name}({dc_channel.id})"
                        )
        except Exception as e:
            raise e

    def get_correct_duplicate_count(self):
        """
        Given the internal math has an extra number cos
        accuracy this simply returns the correct value
        Returns
        -------
        self.duplicate_counter - 1
        """
        return self.duplicate_counter - 1

    def clean_up(self, current_time):
        """
        This logic works around checking the current
        time vs a messages creation time. If the message
        is older by the config amount it can be cleaned up
        """
        self.logger.debug("Attempting to remove outdated Message's")

        def _is_still_valid(message):
            """
            Given a message, figure out if it hasnt
            expired yet based on timestamps
            """
            difference = current_time - message.creation_time
            offset = datetime.timedelta(
                milliseconds=self.options.get("message_interval")
            )

            if difference >= offset:
                return False
            return True

        current_messages = []
        outstanding_messages = []

        for message in self._messages:
            if _is_still_valid(message):
                current_messages.append(message)
            else:
                outstanding_messages.append(message)

        self._messages = deepcopy(current_messages)

        # Now if we have outstanding messages we need
        # to process them and see if we need to deincrement
        # the duplicate counter as we are removing them from
        # the queue otherwise everything stacks up
        for outstanding_message in outstanding_messages:
            if outstanding_message.is_duplicate:
                self.duplicate_counter -= 1
                self.logger.log.debug(
                    f"Removing duplicate Message: {outstanding_message.id}"
                )
            elif self.logger.log.isEnabledFor(logging.DEBUG):
                self.logger.log.debug(f"Removing Message: {outstanding_message.id}")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._id = value

    @property
    def guild_id(self):
        return self._guild_id

    @guild_id.setter
    def guild_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._guild_id = value

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        """
        Raises
        ======
        DuplicateObject
            It won't maintain two message objects with the same
            id's, and it will complain about it haha
        """
        if not isinstance(value, Message):
            raise ValueError("Expected Message object")

        if value.author_id != self.id or value.guild_id != self.guild_id:
            raise ObjectMismatch

        for message in self._messages:
            if message == value:
                raise DuplicateObject

        self._messages.append(value)


class Message:
    """
    I modified the code but most of the code belongs to:

    MIT License

    Copyright (c) 2020 Skelmis

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    """Represents a lower level object needed to maintain messages
    """

    __slots__ = [
        "_id",
        "_channel_id",
        "_guild_id",
        "_content",
        "_author_id",
        "_creation_time",
        "_is_duplicate",
    ]

    def __init__(self, id, content, author_id, channel_id, guild_id):
        """
        Set & store a smaller object footprint then a standard
        message object for memory purposes :)
        Parameters
        ==========
        id : int
            The id of the message
        content : String
            The actual message content
        author_id : int
            The author of said message
        channel_id : int
            The channel this message is in
        guild_id : int
            The guild this message belongs to
        Raises
        ======
        ValueError
            When an item is not the correct ignore_type for conversion
        Notes
        =====
        This enforces strict types by conversion and ignore_type checking
        pass through of the correct ignore_type is required.
        """
        self.id = int(id)
        self.content = str(content)
        self.author_id = int(author_id)
        self.channel_id = int(channel_id)
        self.guild_id = int(guild_id)
        self.is_duplicate = False
        self._creation_time = datetime.datetime.now(datetime.timezone.utc)

    def __repr__(self):
        return (
            f"'{self.__class__.__name__} object. Content: {self.content}, Message Id: {self.id}, "
            f"Author Id: {self.author_id}, Channel Id: {self.channel_id}, Guild Id: {self.guild_id} "
            f"Creation time: {self._creation_time}'"
        )

    def __str__(self):
        return f"{self.__class__.__name__} object - '{self.content}'"

    def __eq__(self, other):
        """
        This is called with a 'obj1 == obj2' comparison object is made
        Checks everything besides message content to figure out if a message
        is the same or not
        Parameters
        ----------
        other : Message
            The object to compare against
        Returns
        -------
        bool
            `True` or `False` depending on whether they are the same or not
        Raises
        ======
        ValueError
            When the comparison object is not of ignore_type `Message`
        Notes
        =====
        Does not check creation time, because that can be different
        and this is mainly used to ensure we don't create duplicates
        and creation time is this class's time not the message's time
        """
        if not isinstance(other, Message):
            raise ValueError

        if (
            self.id == other.id
            and self.author_id == other.author_id
            and self.channel_id == other.channel_id
            and self.guild_id == other.guild_id
        ):
            return True
        return False

    def __hash__(self):
        """
        Given we create a __eq__ dunder method, we also needed
        to create one for __hash__ lol
        Returns
        -------
        int
            The hash of all id's
        """
        return hash((self.id, self.author_id, self.guild_id, self.channel_id))

    @property
    def id(self):
        """
        The `getter` method
        """
        return self._id

    @id.setter
    def id(self, value):
        """
        The `setter` method
        """
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._id = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        try:
            self._content = str(value)
        except ValueError:
            raise ValueError("Expected String")

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._author_id = value

    @property
    def channel_id(self):
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._channel_id = value

    @property
    def guild_id(self):
        return self._guild_id

    @guild_id.setter
    def guild_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._guild_id = value

    @property
    def creation_time(self):
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value):
        # We don't want creationTime changed
        return

    @property
    def is_duplicate(self):
        return self._is_duplicate

    @is_duplicate.setter
    def is_duplicate(self, value):
        if not isinstance(value, bool):
            raise ValueError("isDuplicate should be a bool")

        self._is_duplicate = value


"""
LICENSE
The MIT License (MIT)
Copyright (c) 2020 Skelmis
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
LICENSE
"""

"""
A short utility for random functions which don't fit into an object
"""


def embed_to_string(embed) -> str:
    """
    Parameters
    ----------
    embed : discord.Embed
        The embed to turn into a string
    Returns
    -------
    str
        The content of the string
    """
    content = ""
    embed = embed.to_dict()

    if "title" in embed:
        content += f"{embed['title']}\n"

    if "description" in embed:
        content += f"{embed['description']}\n"

    if "footer" in embed:
        if "text" in embed["footer"]:
            content += f"{embed['footer']['text']}\n"

    if "author" in embed:
        if "name" in embed["author"]:
            content += f"{embed['author']['name']}\n"

    if "fields" in embed:
        for field in embed["fields"]:
            content += f"{field['name']}\n{field['value']}\n"

    return content


def dict_to_embed(data, message, counts):
    """
    Given a dictionary, will attempt to build a
    valid discord.Embed object to return
    Parameters
    ----------
    data : dict
        The given item to try build an embed from
    message : discord.Message
        Where we get all our info from
    counts : dict
        Our current warn & kick counts
    Returns
    -------
    discord.Embed
    """
    allowed_avatars = ["$USERAVATAR", "$BOTAVATAR", "$GUILDICON"]

    if "title" in data:
        data["title"] = substitute_args(data["title"], message, counts)

    if "description" in data:
        data["description"] = substitute_args(data["description"], message, counts)

    if "footer" in data:
        if "text" in data["footer"]:
            data["footer"]["text"] = substitute_args(
                data["footer"]["text"], message, counts
            )

        if "icon_url" in data["footer"]:
            if data["footer"]["icon_url"] in allowed_avatars:
                data["footer"]["icon_url"] = substitute_args(
                    data["footer"]["icon_url"], message, counts
                )

    if "author" in data:
        if "name" in data["author"]:
            data["author"]["name"] = substitute_args(
                data["author"]["name"], message, counts
            )

        if "icon_url" in data["author"]:
            if data["author"]["icon_url"] in allowed_avatars:
                data["author"]["icon_url"] = substitute_args(
                    data["author"]["icon_url"], message, counts
                )

    if "fields" in data:
        for field in data["fields"]:
            name = substitute_args(field["name"], message, counts)
            value = substitute_args(field["value"], message, counts)
            field["name"] = name
            field["value"] = value

            if "inline" not in field:
                field["inline"] = True

    if "timestamp" in data:
        data["timestamp"] = message.created_at.isoformat()

    if "colour" in data:
        data["color"] = data["colour"]

    data["type"] = "rich"

    return discord.Embed.from_dict(data)


def substitute_args(message, value, counts) -> str:
    """
    Given the options string, return the string
    with the relevant values substituted in
    Parameters
    ----------
    message : str
        The string to substitute with values
    value : discord.Message
        Where we get our values from to substitute
    counts : dict
        Our current warn & kick counts
    Returns
    -------
    str
        The correctly substituted message
    """
    return Template(message).safe_substitute(
        {
            "MENTIONUSER": value.author.mention,
            "USERNAME": value.author.display_name,
            "USERID": value.author.id,
            "BOTNAME": value.guild.me.display_name,
            "BOTID": value.guild.me.id,
            "GUILDID": value.guild.id,
            "GUILDNAME": value.guild.name,
            "TIMESTAMPNOW": datetime.datetime.now().strftime("%I:%M:%S %p, %d/%m/%Y"),
            "TIMESTAMPTODAY": datetime.datetime.now().strftime("%d/%m/%Y"),
            "WARNCOUNT": counts["warn_count"],
            "KICKCOUNT": counts["kick_count"],
            "USERAVATAR": value.author.avatar_url,
            "BOTAVATAR": value.guild.me.avatar_url,
            "GUILDICON": value.guild.icon_url,
        }
    )


def transform_message(item, value, counts):
    """
    Given an item of two possible values, create
    and return the correct thing
    Parameters
    ----------
    item : [str, dict]
        Either a straight string or dict to turn in an embed
    value : discord.Message
        Where things come from
    counts : dict
        Our current warn & kick counts
    Returns
    -------
    [str, discord.Embed]
    """
    if isinstance(item, str):
        return substitute_args(item, value, counts)

    return dict_to_embed(deepcopy(item), value, counts)


async def send_to_obj(messageable_obj, message) -> discord.Message:
    """
    Send a given message to an abc.messageable object
    This does not handle exceptions, they should be handled
    on call as I did not want to overdo this method with
    the required params to notify users.
    Parameters
    ----------
    messageable_obj : abc.Messageable
        Where to send message
    message : str, dict
        The message to send
        Can either be a straight string or a discord.Embed
    Raises
    ------
    discord.HTTPException
        Failed to send
    discord.Forbidden
        Lacking permissions to send
    Returns
    =======
    discord.Message
        The sent messages object
    """
    if isinstance(message, discord.Embed):
        return await messageable_obj.send(embed=message)
    return await messageable_obj.send(message)