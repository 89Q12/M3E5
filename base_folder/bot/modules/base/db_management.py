import base64
import datetime
from base_folder.bot.config.config import sql

'''
Class to create db management as class
'''


class DbRead:
    def __init__(self):
        self.sql = sql()

    def prefix_lookup(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT prefix FROM settings WHERE guild_id = {guild_id}")
        prefix = c.fetchone()
        conn.commit()
        c.close()
        return prefix[0]

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
        #  returns a role name
        # errors out when  field_name is none bruh
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT {str(field_name)} FROM settings WHERE guild_id={str(guild_id)}")
        role_id = c.fetchone()
        conn.commit()
        c.close()
        return role_id[0]

    async def get_warns(self, guild_id, user_id):
        conn = sql()
        c = conn.cursor()
        c.execute("SELECT warnings FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        warnings = c.fetchone()
        conn.commit()
        c.close()
        return warnings[0]

    async def get_welcome_channel(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT welcome_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        welcome_channel = c.fetchone()
        conn.commit()
        c.close()
        return welcome_channel[0]

    async def get_cmd_channel(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT cmd_channel_id FROM settings WHERE guild_id={guild_id}")
        leave_channel = c.fetchone()
        conn.commit()
        c.close()
        return leave_channel[0]

    async def get_lvl_channel(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT lvl_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        leave_channel = c.fetchone()
        conn.commit()
        c.close()
        return leave_channel[0]

    async def get_leave_channel(self, guild_id):
        # returns the leave channel
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT leave_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        leave_channel = c.fetchone()
        conn.commit()
        c.close()
        return leave_channel[0]

    async def get_leave_text(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT leave_text FROM settings WHERE guild_id={str(guild_id)}")
        leave_text = c.fetchone()
        conn.commit()
        c.close()
        return leave_text[0]

    async def get_img(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT imgwelcome_toggle FROM settings WHERE guild_id={str(guild_id)};")
        img = c.fetchone()
        conn.commit()
        c.close()
        return img[0]

    async def get_img_text(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT imgwelcome_text FROM settings WHERE guild_id={str(guild_id)};")
        text = c.fetchone()
        conn.commit()
        c.close()
        return text[0]

    async def get_text_xp(self, guild_id, user_id):
        # returns the xp amount for a given user
        conn = sql()
        c = conn.cursor()
        c.execute("SELECT text_xp FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        xp = c.fetchone()
        conn.commit()
        c.close()
        return xp[0]

    async def get_lvl_text(self, guild_id, user_id):
        # returns the text lvl  amount for a given user
        conn = sql()
        c = conn.cursor()
        c.execute("SELECT text_lvl FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        lvl = c.fetchone()
        conn.commit()
        c.close()
        return lvl[0]

    async def get_levelsystem(self, guild_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT levelsystem_toggle FROM settings WHERE guild_id =  {str(guild_id)};")
        img = c.fetchone()
        conn.commit()
        c.close()
        return img[0]

    async def get_banned_until(self, user_id):
        conn = sql()
        c = conn.cursor()
        c.execute(f"SELECT banned_until FROM `user_info` WHERE user_id = {user_id} and banned_until IS NOT NULL")
        dates = c.fetchone()
        conn.commit()
        c.close()
        if dates is None:
            return None
        else:
            return dates[0]
