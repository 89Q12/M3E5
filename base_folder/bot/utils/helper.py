"""
This helper script is helpful in some situations  like creating the ctx object out of the member object etc
"""
from asyncio import run_coroutine_threadsafe

from base_folder.bot.modules.base.db_management import Db
from base_folder.bot.modules.listener.listern_antispam import User


'''
This class is designed to hold all data that the bot uses extensively and the class is designed in a way that it can
reload the data on change.
'''


class Ctx:
    """
    Not the fully featured ctx object but its doing the job
    """

    def __init__(self, member):
        self.member = member
        self.guild = member.guild
        self.author = member


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

    def create_state(self, guild, logger):
        self._states[guild.id] = GuildStates(guild, self.loop, logger)

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
            "warn_threshold": opts[0][0],
            "kick_threshold": opts[0][1],
            "ban_threshold": opts[0][2],
            "message_interval": opts[0][3],
            "guild_warn_message": opts[0][4],
            "guild_kick_message": opts[0][5],
            "guild_ban_message": opts[0][6],
            "user_kick_message": opts[0][5],
            "user_ban_message": opts[0][6],
            "message_duplicate_count": opts[0][7],
            "message_duplicate_accuracy": opts[0][8],
            "ignore_perms": [8],  # TODO: make this customizable
            "ignore_channels": self.banned_channels_spam,
            "ignore_Users": self.banned_users_spam,
            "ignore_roles": self.banned_roles_cmd,
            "ignore_guilds": [],
            "ignore_bots": True,
        }
        self.options = options

    async def set_user(self, userid, stdChannel, warnchannel, kick, banchannel):
        user_data = {
            'warnCount': await self.db.get_warns(self.guild.id, userid),
            'kickCount': await self.db.get_kick_count(self.guild.id, userid),
        }
        self.users[userid] = User(userid, self.guild.id, self.options, user_data, self.logger,
                                  stdChannel, warnchannel, kick,banchannel)

    def get_role(self, rolename="admin"):
        role_id = self._permisson_roles[rolename]
        return role_id

    def get_channel(self, channelname="stdout"):
        try:
            channelid = self._channels[channelname]
            if channelid == 0:
                run_coroutine_threadsafe(self.set_channels(), self.loop)
                return self._channels[channelname]
            return channelid
        except KeyError:
            return 0

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
        self._channels["warn"] = await self.db.get_warn_channel(self.guild.id)
        self._channels["kick"] = await self.db.get_kick_channel(self.guild.id)
        self._channels["ban"] = await self.db.get_ban_channel(self.guild.id)

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

    async def destruct_user(self, userid):
        del self.users[userid]
