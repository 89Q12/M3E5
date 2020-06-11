import base64

'''
Class to create db management as class
'''


class Db:
    def __init__(self, client):
        self.sql = client.sql

    def prefix_lookup(self, guild_id):
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT prefix FROM settings WHERE guild_id = {guild_id}")
        prefix = c.fetchone()
        return prefix[0]

    async def roles_from_db(self, guild_id):
        # returns a tuple with all role name's and id's
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT role_id, role_name FROM roles WHERE guild_id={str(guild_id)}")
        roles = c.fetchall()
        return roles

    async def get_settings_role(self, guild_id, field_name):
        #  returns a role name
        # errors out when  field_name is none bruh
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT {str(field_name)} FROM settings WHERE guild_id={str(guild_id)}")
        role_id = c.fetchone()
        return role_id[0]

    async def get_warns(self, guild_id, user_id):
        # returns the number of warnings a user has
        conn = self.sql
        c = conn.cursor()
        c.execute("SELECT warnings FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        warnings = c.fetchone()
        if warnings is None:
            return 0
        else:
            return warnings[0]

    async def get_welcome_channel(self, guild_id):
        # returns the  welcome channel
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT welcome_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        welcome_channel = c.fetchone()
        if welcome_channel is None:
            return "you need to set a channel first"
        else:
            return welcome_channel[0]

    async def get_leave_channel(self, guild_id):
        # returns the leave channel
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT leave_channel_id FROM settings WHERE guild_id={str(guild_id)}")
        leave_channel = c.fetchone()
        if leave_channel is None:
            return "you need to set a channel first"
        else:
            return leave_channel[0]

    async def get_img(self, guild_id):
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT imgwelcome_toggle FROM settings WHERE guild_id={str(guild_id)};")
        img = c.fetchone()
        return img[0]

    async def get_img_text(self, guild_id):
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT imgwelcome_text FROM settings WHERE guild_id={str(guild_id)};")
        text = c.fetchone()
        return text[0]

    async def get_text_xp(self, guild_id, user_id):
        # returns the xp amount for a given user
        conn = self.sql
        c = conn.cursor()
        c.execute("SELECT text_xp FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        xp = c.fetchone()
        return xp[0]

    async def get_lvl_text(self, guild_id, user_id):
        # returns the text lvl  amount for a given user
        conn = self.sql
        c = conn.cursor()
        c.execute("SELECT text_lvl FROM user_info WHERE user_id="
                  f"{str(user_id)} and guild_id={str(guild_id)}")
        lvl = c.fetchone()
        if lvl is None:
            return None
        else:
            return lvl[0]

    async def get_levelsystem(self, guild_id):
        conn = self.sql
        c = conn.cursor()
        c.execute(f"SELECT levelsystem_toggle FROM settings WHERE guild_id =  {str(guild_id)};")
        img = c.fetchone()
        return img[0]