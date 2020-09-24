"""
This helper script is helpful in some situations  like creating the ctx object out of the member object etc
"""
from asyncio import run_coroutine_threadsafe
import base64
import time


from base_folder.bot.modules.base.db_management import Db
from base_folder.config import sql


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
        tic = time.perf_counter()
        r = client.cache.states[ctx.guild.id].get_prefix
        toc = time.perf_counter()
        print(f"Downloaded the tutorial in {toc - tic:0.8f} seconds")
        pre = (base64.b64decode(str(r).encode("utf8"))).decode("utf8")
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
    def __init__(self, guilds: [], loop):
        self.loop = loop
        self._states = {}
        self.guilds: [] = guilds

    @property
    def states(self, guild=None):
        if not guild:
            return self._states
        else:
            return self._states[guild.id]

    def make_states(self):
        for guild in self.guilds:
            self._states[guild.id] = GuildStates(guild, self.loop)
        print(self._states)

    def create_state(self, guild):
        self._states[guild.id] = GuildStates(guild, self.loop)

    def destruct_state(self, guild):
        del self._states[guild.id]


class GuildStates:
    def __init__(self,  guild, loop):
        self.loop = loop
        self.conn = sql()
        self.db = Db(self.conn if self.conn.is_connected() else sql())
        self.guild = guild
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
        self._permisson_roles['mod'] = await self.db.get_settings_role(self.guild.id, "mod_role_id")
        self._permisson_roles['admin'] = await self.db.get_settings_role(self.guild.id, "admin_role_id")
        self._permisson_roles['dev'] = await self.db.get_settings_role(self.guild.id, "dev_role_id")
        self._permisson_roles['default'] = await self.db.get_settings_role(self.guild.id, "standard_role_id")

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
