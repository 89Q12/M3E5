"""
This helper script is helpful in some situations  like creating the ctx object out of the member object etc
"""
import ast
import asyncio
import datetime
import inspect
from asyncio import run_coroutine_threadsafe
import base64
import time
import discord
from string import Template
from fuzzywuzzy import fuzz

from base_folder.bot.modules.base.db_management import Db
from base_folder.AntiSpam.Exceptions import DuplicateObject, ObjectMismatch, LogicError


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

    def make_states(self, guilds):
        for guild in guilds:
            if guild.id == 616609333832187924:
                self._states[guild.id] = GuildStates(guild, self.loop)

    def create_state(self, guild):
        self._states[guild.id] = GuildStates(guild, self.loop)

    def destruct_state(self, guild):
        del self._states[guild.id]


class GuildStates:
    def __init__(self, guild, loop):
        self.loop = loop
        self.db = Db()
        self.guild = guild
        self.options = self.spamsettings
        self.users = {}
        self._permisson_roles = {}
        self._prefix = None
        self._levelsystem_toggle = None
        self._get_imgtoggle = None
        self._channels = {}

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

    @property
    def spamsettings(self):
        opts = self.db.get_spam_settings(self.guild.id)
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
            "ignorePerms": [8], # TODO: make this customizable
            "ignoreUsers": [], # TODO: make this customizable too
            "ignoreBots": True,
        }
        return options

    async def set_users(self):
       async for user in self.guild.fetch_members():
            print(user)
            user_data = {
                'warnCount': await self.db.get_warns(self.guild.id, user.id),
                'kickCount': await self.db.get_kick_count(self.guild.id, user.id),
            }
            self.users[user.id] = User(user.id, self.guild.id, self.options, user_data)

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

    async def set_imgtoggle(self):
        self._get_imgtoggle = await self.db.get_img(self.guild.id)

    async def set_lvltoggle(self):
        self._levelsystem_toggle = await self.db.get_levelsystem(self.guild.id)

    async def update_channel(self, channelname, channelid):
        self._channels[channelname] = channelid

    async def update_permission_role(self, rolename, roleid):
        self._permisson_roles[rolename] = roleid


class User:
    """
    The overall handler & entry point from any discord bot,
    this is responsible for handling interaction with Guilds etc

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
    """A class dedicated to maintaining a user, and any relevant messages in a single guild.

    """

    __slots__ = [
        "_id",
        "_guildId",
        "_messages",
        "options",
        "warnCount",
        "kickCount",
        "bot",
        "duplicateCounter",
    ]

    def __init__(self, id, guildId, options, user_data):
        """
        Set the relevant information in order to maintain
        and use a per User object for a guild

        Parameters
        ==========
        id : int
            The relevant user id
        guildId : int
            The guild (id) this user is belonging to
        options : Dict
            The options we need to check against
        """
        self.id = int(id)
        self.guildId = int(guildId)
        self._messages = []
        self.options = options
        self.warnCount = user_data["warnCount"]
        self.kickCount = user_data["kickCount"]
        self.duplicateCounter = 1

    def __repr__(self):
        return (
            f"{self.__class__.__name__} object. User id: {self.id}, Guild id: {self.guildId}, "
            f"Len Stored Message {len(self._messages)}"
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
            When the comparison object is not of type `Message`
        """
        if not isinstance(other, User):
            raise ValueError("Expected two User objects to compare")

        if self.id == other.id and self.guildId == other.guildId:
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
        return hash((self.id, self.guildId))

    def propagate(self, value: discord.Message):
        """
        This method handles a message object and then adds it to
        the relevant user

        Parameters
        ==========
        value : discord.Message
            The message that needs to be propagated out
        """
        if not isinstance(value, discord.Message):
            raise ValueError("Expected message of type: discord.Message")

        message = Message(
            value.id,
            value.clean_content,
            value.author.id,
            value.channel.id,
            value.guild.id,
        )
        for messageObj in self.messages:
            if message == messageObj:
                raise DuplicateObject

        # TODO Add checks for if there isn't any content. If there isn't
        #      we shouldn't bother saving them

        # TODO Compare incoming message to other messages in order
        relationToOthers = []
        for messageObj in self.messages[::-1]:
            # This calculates the relation to each other
            relationToOthers.append(
                fuzz.token_sort_ratio(message.content, messageObj.content)
            )

        self.messages = message

        # Check if this message is a duplicate of the most recent messages
        for i, proportion in enumerate(relationToOthers):
            if proportion >= self.options["messageDuplicateAccuracy"]:
                """
                The handler works off an internal message duplicate counter 
                so just increment that and then let our logic process it
                """
                self.duplicateCounter += 1
                message.isDuplicate = True
                break  # we don't want to increment to much

        if self.duplicateCounter >= self.options["messageDuplicateCount"]:
            print("Punish time")
            # We need to punish the user with something

            # TODO Figure out why the logic likes having +1 of the actual count
            #      before it decides its time to actually punish the user properly

            if (
                    self.duplicateCounter >= self.options["warnThreshold"]
                    and self.warnCount < self.options["kickThreshold"]
                    and self.kickCount < self.options["banThreshold"]
            ):
                print("Warn time")
                """
                The user has yet to reach the warn threshold,
                after the warn threshold is reached this will
                then become a kick and so on
                """
                # We are still in the warning area
                channel = value.channel
                message = Template(self.options["warnMessage"]).safe_substitute(
                    {
                        "MENTIONUSER": value.author.mention,
                        "USERNAME": value.author.display_name,
                    }
                )

                asyncio.ensure_future(self.SendToObj(channel, message))
                self.warnCount += 1

            elif (
                    self.warnCount >= self.options["kickThreshold"]
                    and self.kickCount < self.options["banThreshold"]
            ):
                print("kick time")
                # We should kick the user
                dcChannel = value.channel
                message = Template(self.options["kickMessage"]).safe_substitute(
                    {
                        "MENTIONUSER": value.author.mention,
                        "USERNAME": value.author.display_name,
                    }
                )
                asyncio.ensure_future(
                    self.KickFromGuild(
                        value.guild,
                        value.author,
                        dcChannel,
                        f"You were kicked from {value.guild.name} for spam.",
                        message,
                    )
                )
                self.kickCount += 1

            elif self.kickCount >= self.options["banThreshold"]:
                print("ban time")
                # We should ban the user
                pass

            else:
                print("else?")
                raise LogicError

    async def SendToObj(self, messageableObj, message):
        """
        Send a given message to an abc.messageable object

        This does not handle exceptions, they should be handled
        on call as I did not want to overdo this method with
        the required params to notify users.

        Parameters
        ----------
        messageableObj : abc.Messageable
            Where to send message
        message : String
            The message to send

        Raises
        ------
        discord.HTTPException
            Failed to send
        discord.Forbidden
            Lacking permissions to send

        """
        await messageableObj.send(message)

    async def KickFromGuild(self, guild, user, dcChannel, userMessage, guildMessage):
        try:
            try:
                await self.SendToObj(user, userMessage)
            except discord.HTTPException:
                await self.SendToObj(
                    user,
                    f"Sending a message to {user.mention} about their kick failed.",
                )
            finally:
                try:
                    await guild.kick(user, reason="Spamming")
                except discord.Forbidden:
                    await self.SendToObj(
                        dcChannel, f"I do not have permission to kick: {user.mention}"
                    )
                except discord.HTTPException:
                    await self.SendToObj(
                        dcChannel, f"An error occurred trying to kick: {user.mention}"
                    )
                finally:
                    try:
                        await self.SendToObj(dcChannel, guildMessage)
                    except discord.HTTPException:
                        print(
                            f"Failed to send message.\n"
                            f"Guild: {dcChannel.guild.name}({dcChannel.guild.id})\n"
                            f"Channel: {dcChannel.name}({dcChannel.id})"
                        )
        except Exception as e:
            raise e

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._id = value

    @property
    def guildId(self):
        return self._guildId

    @guildId.setter
    def guildId(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._guildId = value

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

        if value.authorId != self.id or value.guildId != self.guildId:
            raise ObjectMismatch

        for message in self._messages:
            if message == value:
                raise DuplicateObject

        self._messages.append(value)


class Message:
    """
    The overall handler & entry point from any discord bot,
    this is responsible for handling interaction with Guilds etc

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
        "_channelId",
        "_guildId",
        "_content",
        "_authorId",
        "_creationTime",
        "_isDuplicate",
    ]

    def __init__(self, id, content, authorId, channelId, guildId):
        """
        Set & store a smaller object footprint then a standard
        message object for memory purposes :)

        Parameters
        ==========
        id : int
            The id of the message
        content : String
            The actual message content
        authorId : int
            The author of said message
        channelId : int
            The channel this message is in
        guildId : int
            The guild this message belongs to

        Raises
        ======
        ValueError
            When an item is not the correct type for conversion

        Notes
        =====
        This enforces strict types by conversion and type checking
        pass through of the correct type is required.
        """
        self.id = int(id)
        self.content = str(content)
        self.authorId = int(authorId)
        self.channelId = int(channelId)
        self.guildId = int(guildId)
        self.isDuplicate = False
        self._creationTime = datetime.datetime.now(datetime.timezone.utc)

    def __repr__(self):
        return (
            f"'{self.__class__.__name__} object. Content: {self.content}, Message Id: {self.id}, "
            f"Author Id: {self.authorId}, Channel Id: {self.channelId}, Guild Id: {self.guildId}' "
            f"Creation time: {self._creationTime}"
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
            When the comparison object is not of type `Message`
        """
        if not isinstance(other, Message):
            raise ValueError

        if (
                self.id == other.id
                and self.authorId == other.authorId
                and self.channelId == other.channelId
                and self.guildId == other.guildId
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
        return hash((self.id, self.authorId, self.guildId, self.channelId))

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
    def authorId(self):
        return self._authorId

    @authorId.setter
    def authorId(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._authorId = value

    @property
    def channelId(self):
        return self._channelId

    @channelId.setter
    def channelId(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._channelId = value

    @property
    def guildId(self):
        return self._guildId

    @guildId.setter
    def guildId(self, value):
        if not isinstance(value, int):
            raise ValueError("Expected integer")
        self._guildId = value

    @property
    def creationTime(self):
        return self._creationTime

    @creationTime.setter
    def creationTime(self, value):
        # We don't want creationTime changed
        return

    @property
    def isDuplicate(self):
        return self._isDuplicate

    @isDuplicate.setter
    def isDuplicate(self, value):
        if not isinstance(value, bool):
            raise ValueError("isDuplicate should be a bool")

        self._isDuplicate = value
