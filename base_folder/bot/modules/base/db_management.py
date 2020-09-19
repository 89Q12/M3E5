import base64
import datetime
from base_folder.config import sql

'''
Class to create db management as class
'''


class Db:
    def __init__(self):
        self.sql = sql()

    def prefix_lookup(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the prefix for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT prefix FROM settings WHERE guild_id = {guild_id}")
        prefix = c.fetchall()
        conn.commit()
        c.close()
        return prefix[0][0]

    async def roles_from_db(self, guild_id):
        # returns a tuple with all role name's and id's
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT role_id, role_name FROM roles WHERE guild_id={str(guild_id)}")
        roles = c.fetchall()
        conn.commit()
        c.close()
        return roles

    async def get_settings_role(self, guild_id, field_name):
        """

        :param guild_id: the id of the guild
        :param field_name: the name of the role admin_role dev_role etc
        :returns: the role id of the e.g. admin role for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT {str(field_name)} FROM settings WHERE guild_id={str(guild_id)}")
        role_id = c.fetchall()
        conn.commit()
        c.close()
        return role_id[0][0]

    async def get_warns(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the warnings for the given user, can be 0
        """
        conn = sql()
        c = conn.cursor()
        c.execute("SELECT warnings FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        warnings = c.fetchall()
        conn.commit()
        c.close()
        return warnings[0][0]

    async def get_welcome_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the welcome channel for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT welcome_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        welcome_channel = c.fetchall()
        conn.commit()
        c.close()
        return welcome_channel[0][0]

    async def get_cmd_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the command channel for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT cmd_channel_id FROM settings WHERE guild_id={guild_id}")
        leave_channel = c.fetchall()
        conn.commit()
        c.close()
        return leave_channel[0][0]

    async def get_lvl_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the level channel for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT lvl_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        lvl_channel = c.fetchall()
        conn.commit()
        c.close()
        return lvl_channel[0][0]

    async def get_leave_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the leave channel for the given guild
        """
        # returns the leave channel
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT leave_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        leave_channel = c.fetchall()
        conn.commit()
        c.close()
        return leave_channel[0][0]

    async def get_stdout_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the stdout(logging) channel for the given guild
        """
        if guild_id is None or 0:
            raise TypeError
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT stdout_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        stdout_channel = c.fetchall()
        conn.commit()
        c.close()
        return stdout_channel[0][0]

    async def get_leave_text(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the leave text for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT leave_text FROM settings WHERE guild_id={str(guild_id)}")
        leave_text = c.fetchall()
        conn.commit()
        c.close()
        return leave_text[0][0]

    async def get_img(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: wether the welcome image is on or off for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT imgwelcome_toggle FROM settings WHERE guild_id={str(guild_id)};")
        img = c.fetchall()
        conn.commit()
        c.close()
        return img[0][0]

    async def get_img_text(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the welcome text for the image  for the given guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT imgwelcome_text FROM settings WHERE guild_id={str(guild_id)};")
        text = c.fetchall()
        conn.commit()
        c.close()
        return text[0][0]

    async def get_text_xp(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the xp amount for the given user
        """
        conn = sql()
        c = conn.cursor()
        c.execute("SELECT text_xp FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)} LIMIT 1")
        xp = c.fetchall()
        conn.commit()
        c.close()
        return xp[0][0]

    async def get_lvl_text(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the text lvl for the given user
        """
        conn = sql()
        c = conn.cursor()
        c.execute("SELECT text_lvl FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        lvl = c.fetchall()
        conn.commit()
        c.close()
        return lvl[0][0]

    async def get_levelsystem(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: if the levelsytem is on or off for the specific guild
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT levelsystem_toggle FROM settings WHERE guild_id =  {str(guild_id)};")
        img = c.fetchall()
        conn.commit()
        conn.close()
        return img[0][0]

    async def get_banned_until(self, user_id):
        """

        :param user_id: the ID of the user
        :returns: the date the user is allowed to get unbanned if none the user wasn't temp banned
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT banned_until FROM `user_info` WHERE user_id = {user_id} and banned_until IS NOT NULL")
        date = c.fetchall()
        conn.commit()
        c.close()
        if date is None:
            return None
        else:
            return date[0][0]

    async def get_blacklist(self, user_id):
        """
        Searches in the db if the user is blacklisted
        :param user_id: the ID of the user
        :returns: if the user is in the blacklist if false the user isnt blacklisted
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT user_id FROM `blacklist` WHERE user_id = {user_id}")
        user = c.fetchall()
        conn.commit()
        c.close()
        if user is None:
            return False
        else:
            return True

    async def get_message(self, guild_id, message_id):
        """

        :param guild_id: the id of the guild
        :param message_id: the requested message id
        :return: the message and the user_id can be none
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT user_id, message FROM `messages` WHERE message_id = {message_id} and guild_id = {guild_id}")
        message = c.fetchall()
        conn.commit()
        c.close()
        try:
            if message is None:
                return False
            else:
                return message[0]
        except IndexError:
            return None

    async def get_guild(self, user_id):
        """

        :param user_id: the id of the user
        :return: list with a tuple with all guilds inside
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT guild_id FROM `user_info` WHERE user_id = {user_id}")
        guilds = c.fetchall()
        conn.commit()
        c.close()
        try:
            if guilds is None:
                return False
            else:
                return guilds
        except IndexError:
            return None

    async def get_reaction_role(self, guild_id, message_id, emoji):
        """

        :param guild_id: the id of the guild
        :param message_id: the id of the message where a reaction got added
        :param emoji: the added emoji
        :return: the role id that the user should get
        """
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT role_id FROM `reactions` WHERE message_id = {message_id} and emoji = %s", (emoji,))
        roleid = c.fetchall()
        conn.commit()
        c.close()
        if roleid == None:
            return roleid[0][0]
        else:
            return None
