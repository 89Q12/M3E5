from base_folder.config import sql

'''
Class to create db management as class
'''


class Db:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def prefix_lookup(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the prefix for the given guild
        """
        c = self.cursor
        c.execute(f"SELECT prefix FROM settings WHERE guild_id = {guild_id}")
        prefix = c.fetchone()
        self.conn.commit()
        return prefix[0]

    async def roles_from_db(self, guild_id):
        # returns a tuple with all role name's and id's

        c = self.cursor
        c.execute(f"SELECT role_id, role_name FROM roles WHERE guild_id={str(guild_id)}")
        roles = c.fetchall()
        self.conn.commit()
        return roles

    async def get_settings_role(self, guild_id, field_name):
        """

        :param guild_id: the id of the guild
        :param field_name: the name of the role admin_role dev_role etc
        :returns: the role id of the e.g. admin role for the given guild
        """

        c = self.cursor
        c.execute(f"SELECT {str(field_name)} FROM settings WHERE guild_id={str(guild_id)}")
        role_id = c.fetchone()
        self.conn.commit()
        if role_id is None:
            return 0
        return role_id[0]

    async def get_warns(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the warnings for the given user, can be 0
        """
        c = self.cursor
        c.execute("SELECT warnings FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        warnings = c.fetchone()
        self.conn.commit()
        return warnings[0]

    async def get_welcome_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the welcome channel for the given guild
        """

        c = self.cursor
        c.execute(f"SELECT welcome_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        welcome_channel = c.fetchone()
        self.conn.commit()
        if welcome_channel is None:
            return 0
        return welcome_channel[0]

    async def get_cmd_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the command channel for the given guild
        """
        c = self.cursor
        c.execute(f"SELECT cmd_channel_id FROM settings WHERE guild_id={guild_id}")
        cmd_channel = c.fetchone()
        self.conn.commit()
        if cmd_channel is None:
            return 0
        return cmd_channel[0]

    async def get_lvl_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the level channel for the given guild
        """

        c = self.cursor
        c.execute(f"SELECT lvl_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        lvl_channel = c.fetchone()
        self.conn.commit()
        if lvl_channel is None:
            return 0
        return lvl_channel[0]

    async def get_leave_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the leave channel for the given guild
        """

        c = self.cursor
        c.execute(f"SELECT leave_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        leave_channel = c.fetchone()
        self.conn.commit()
        if leave_channel is None:
            return 0
        return leave_channel[0]

    async def get_stdout_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the stdout(logging) channel for the given guild
        """
        c = self.cursor
        c.execute(f"SELECT stdout_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        stdout_channel = c.fetchone()
        self.conn.commit()
        if stdout_channel is None:
            return 0
        return stdout_channel[0]

    async def get_leave_text(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the leave text for the given guild
        """
        c = self.cursor
        c.execute(f"SELECT leave_text FROM settings WHERE guild_id={str(guild_id)}")
        leave_text = c.fetchall()
        self.conn.commit()
        return leave_text[0][0]

    async def get_img(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: wether the welcome image is on or off for the given guild
        """

        c = self.cursor
        c.execute(f"SELECT imgwelcome_toggle FROM settings WHERE guild_id={str(guild_id)};")
        img = c.fetchone()
        self.conn.commit()
        return img[0]

    async def get_img_text(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the welcome text for the image  for the given guild
        """
        c = self.cursor
        c.execute(f"SELECT imgwelcome_text FROM settings WHERE guild_id={str(guild_id)};")
        text = c.fetchone()
        self.conn.commit()
        return text[0]

    async def get_text_xp(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the xp amount for the given user
        """

        c = self.cursor
        c.execute("SELECT text_xp FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)} LIMIT 1")
        xp = c.fetchone()
        self.conn.commit()
        return xp[0]

    async def get_lvl_text(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the text lvl for the given user
        """

        c = self.cursor
        c.execute("SELECT text_lvl FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        lvl = c.fetchone()
        self.conn.commit()
        return lvl[0]

    async def get_levelsystem(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: if the levelsytem is on or off for the specific guild
        """

        c = self.cursor
        c.execute(f"SELECT levelsystem_toggle FROM settings WHERE guild_id =  {str(guild_id)};")
        img = c.fetchone()
        self.conn.commit()
        return img[0]

    async def get_banned_until(self, user_id):
        """

        :param user_id: the ID of the user
        :returns: the date the user is allowed to get unbanned if none the user wasn't temp banned
        """

        c = self.cursor
        c.execute(f"SELECT banned_until FROM `user_info` WHERE user_id = {user_id} and banned_until IS NOT NULL")
        date = c.fetchone()
        self.conn.commit()
        if date is None:
            return None
        else:
            return date[0]

    async def get_blacklist(self, user_id):
        """
        Searches in the db if the user is blacklisted
        :param user_id: the ID of the user
        :returns: if the user is in the blacklist if false the user isnt blacklisted
        """

        c = self.cursor
        c.execute(f"SELECT user_id FROM `blacklist` WHERE user_id = {user_id}")
        user = c.fetchall()
        self.conn.commit()
        if user[0] is None:
            return False
        else:
            return True

    async def get_message(self, guild_id, message_id):
        """

        :param guild_id: the id of the guild
        :param message_id: the requested message id
        :return: the message and the user_id can be none
        """

        c = self.cursor
        c.execute(f"SELECT user_id, message FROM `messages` WHERE message_id = {message_id} and guild_id = {guild_id}")
        message = c.fetchone()
        self.conn.commit()
        try:
            if message is None:
                return False
            else:
                return message
        except IndexError:
            return None

    async def get_guild(self, user_id):
        """

        :param user_id: the id of the user
        :return: list with a tuple with all guilds inside
        """

        c = self.cursor
        c.execute(f"SELECT guild_id FROM `user_info` WHERE user_id = {user_id}")
        guilds = c.fetchall()
        self.conn.commit()
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
        c = self.cursor
        c.execute(f"SELECT role_id FROM `reactions` WHERE message_id = {message_id} and emoji = %s", (emoji,))
        roleid = c.fetchone()
        self.conn.commit()
        if roleid is None:
            return None
        else:
            return roleid[0]

    async def leaderboard(self, guild_id):
        """

        :param guild_id:  the id of the guild
        :return: the leaderboard by rank/level with xp
        """
        c = self.cursor
        c.execute(f"SELECT user_id, text_lvl, text_xp FROM user_info WHERE guild_id ={guild_id}  ORDER BY text_lvl DESC LIMIT 10")
        ranks = c.fetchall()
        self.conn.commit()
        return ranks
