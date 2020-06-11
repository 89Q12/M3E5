import base64


from celery import Celery, Task
from base_folder.bot.config.config import sql

app = Celery('tasks')
app.config_from_object('base_folder.celeryconfig')


@app.task
def add(guild_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT prefix FROM settings WHERE guild_id = '{guild_id}'")
    x = c.fetchone()
    return x[0]


'''
Initialize the tables
'''


class DatabaseTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = sql()
        return self._db


@app.task(base=DatabaseTask)
def initialize_all(guild_id):
    initialize_guilds(guild_id)
    initialize_settings(guild_id)


@app.task(base=DatabaseTask)
def initialize_guilds(guild_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"INSERT INTO guilds (`guild_id`) VALUES ({guild_id});")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def initialize_settings(guild_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"INSERT INTO settings (guild_id) VALUES ({guild_id});")
    conn.commit()
    c.close()
    return


'''
General per guild settings
'''


@app.task(base=DatabaseTask)
def is_user_indb(user, user_id, guild_id):
    # Checks if a given user is in the db else writes it in the db
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT user_id FROM user_info WHERE user_id ={user_id} and guild_id={guild_id}")
    u = c.fetchone()
    if u is None:
        c.execute(f"INSERT INTO user_info (username, user_id, guild_id) "
                  f"VALUES ('{str(user)} ', '{str(user_id)}', '{str(guild_id)}')")
        conn.commit()
        c.close()
    else:
        return


@app.task(base=DatabaseTask)
def on_error(guild_id, error):
    conn = sql()
    c = conn.cursor()
    error = (base64.b64encode(str(error).encode("utf8"))).decode("utf8")
    c.execute(f"INSERT into Error (guild_id, error) VALUES ('{guild_id}', '{error}')")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def insert_message(guild_id, user_id, message, time):
    conn = sql()
    c = conn.cursor()
    message = (base64.b64encode(str(message).encode("utf8"))).decode("utf8")
    c.execute(f"INSERT into messages (guild_id, user_id, message, time) "
              f"VALUES ('{guild_id}', '{user_id}', '{message}', '{time}')")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def prefix_lookup(guild_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT prefix FROM settings WHERE guild_id = {guild_id}")
    prefix = c.fetchone()
    c.close()
    return prefix[0]


@app.task(base=DatabaseTask)
def set_prefix(guild_id, prefix):
    conn = sql()
    c = conn.cursor()
    prefix = (base64.b64encode(str(prefix).encode("utf8"))).decode("utf8")
    c.execute(f"UPDATE settings SET prefix='{prefix}' WHERE guild_id ={guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_warns(guild_id, user_id):
    # returns the number of warnings a user has
    conn = sql()
    c = conn.cursor()
    c.execute("SELECT warnings FROM user_info WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    warnings = c.fetchone()
    c.close()
    return warnings[0]


@app.task(base=DatabaseTask)
def edit_warns(guild_id, user_id, amount):
    # sets warn with given amount
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET warnings={str(amount)} WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def edit_muted_at(guild_id, user_id, date):
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET muted_at='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_muted_at(guild_id, user_id):
    # returns the number of warnings a user has
    conn = sql()
    c = conn.cursor()
    c.execute("SELECT muted_at FROM user_info WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    warnings = c.fetchone()
    c.close()
    return warnings[0]


@app.task(base=DatabaseTask)
def muted_until(guild_id, user_id, date):
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET muted_until='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()


@app.task(base=DatabaseTask)
def edit_banned_at(guild_id, user_id, date):
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET banned_at='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_banned_at(guild_id, user_id):
    # returns the number of warnings a user has
    conn = sql()
    c = conn.cursor()
    c.execute("SELECT banned_at FROM user_info WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    warnings = c.fetchone()
    c.close()
    return warnings[0]


@app.task(base=DatabaseTask)
def banned_until(guild_id, user_id, date):
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET banned_until='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return

'''
Role settings 
'''


@app.task(base=DatabaseTask)
def roles_to_db(guild_id, role_name, role_id):
    # Checks if a given role is in the db else writes it in the db
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT role_id FROM roles WHERE role_id={str(role_id)} and guild_id={str(guild_id)}")
    sq = c.fetchone()
    if sq:
        return True
    else:
        c.execute(f"INSERT INTO roles (guild_id, role_name, role_id) "
                  f"VALUES ('{guild_id}', '{str(role_name)}', '{str(role_id)}')")
        conn.commit()
        return


@app.task(base=DatabaseTask)
def roles_from_db(guild_id):
    # returns a tuple with all role name's and id's
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT role_id, role_name FROM roles WHERE guild_id={str(guild_id)}")
    roles = c.fetchall()
    c.close()
    return roles


@app.task(base=DatabaseTask)
def remove_role(guild_id, role_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"DELETE FROM roles WHERE role_id = {role_id} and guild_id = {guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def edit_settings_role(guild_id, role_id, field_name):
    # Let's you set roles e.g. mod role
    conn = sql()
    c = conn.cursor()
    c.execute(f"INSERT INTO settings (guild_id,{field_name}) VALUES ('{guild_id}','{role_id}')"
              f"ON DUPLICATE KEY UPDATE {field_name}='{role_id}'")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_role(guild_id, role_id):
    #  returns a role name when a role id is given
    # errors out when role id is none bruh
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT role_name FROM roles WHERE role_id={str(role_id)} "
              f"and guild_id ={guild_id};")
    role_name = c.fetchone()
    return role_name[0]


@app.task(base=DatabaseTask)
def get_settings_role(guild_id, field_name):
    #  returns a role name
    # errors out when  field_name is none bruh
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT {str(field_name)} FROM settings WHERE guild_id={str(guild_id)}")
    role_id = c.fetchone()
    c.close()
    return role_id[0]


'''
end of roles settings

Channel settings and warning settings
'''


@app.task(base=DatabaseTask)
def edit_settings_welcome(guild_id, channel_id):
    # sets the welcome_channel to the given channel id
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE settings SET welcome_channel_id={str(channel_id)} WHERE guild_id = {guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def edit_settings_leave(guild_id, channel_id):
    # sets the leave_channel to the given channel id
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE settings SET leave_channel_id ={str(channel_id)}"
              f"WHERE guild_id = {guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_welcome_channel(guild_id):
    # returns the  welcome channel
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT welcome_channel_id FROM settings WHERE guild_id={str(guild_id)}")
    welcome_channel = c.fetchone()
    c.close()
    if welcome_channel is None:
        return "you need to set a channel first"
    else:
        return welcome_channel[0]


@app.task(base=DatabaseTask)
def get_leave_channel(guild_id):
    # returns the leave channel
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT leave_channel_id FROM settings WHERE guild_id={str(guild_id)}")
    leave_channel = c.fetchone()
    c.close()
    if leave_channel is None:
        return "you need to set a channel first"
    else:
        return leave_channel[0]


'''
end of channel and warning settings

Welcomeimg
'''


@app.task(base=DatabaseTask)
def edit_settings_img(guild_id, img):
    # Unused for now but it will be used for the welcome image function
    # sets the column imgwelcome to 1/enabled or 0/disabled
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE settings SET imgwelcome_toggle={str(img)} WHERE guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def edit_settings_img_text(self, guild_id, img="Welcome {0.mention} to {1}!"):
    # Unused for now but it will be used for the welcome image function
    # sets the message text in the column imgwelcome_text to what ever you enter
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE settings SET imgwelcome_text={str(img)} WHERE guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_img(guild_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT imgwelcome_toggle FROM settings WHERE guild_id={str(guild_id)};")
    img = c.fetchone()
    c.close()
    return img[0]


@app.task(base=DatabaseTask)
def get_img_text(guild_id):
    conn = sql()
    c = conn.cursor()
    c.execute(f"SELECT imgwelcome_text FROM settings WHERE guild_id={str(guild_id)};")
    text = c.fetchone()
    c.close()
    return text[0]


'''
End of general settings

Level system 
'''


@app.task(base=DatabaseTask)
def update_xp_text(guild_id, user_id, amount):
    # updates the xp amount for a given user
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET text_xp={str(amount)} WHERE user_id={str(user_id)} a"
              f"nd guild_id={str(guild_id)};")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def get_text_xp(guild_id, user_id):
    # returns the xp amount for a given user
    conn = sql()
    c = conn.cursor()
    c.execute("SELECT text_xp FROM user_info WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    xp = c.fetchone()
    c.close()
    return xp[0]


@app.task(base=DatabaseTask)
def get_lvl_text(guild_id, user_id):
    # returns the text lvl  amount for a given user
    conn = sql()
    c = conn.cursor()
    c.execute("SELECT text_lvl FROM user_info WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    lvl = c.fetchone()
    c.close()
    if lvl is None:
        return None
    else:
        return lvl[0]


@app.task(base=DatabaseTask)
def update_text_lvl(guild_id, user_id, amount=1):
    # updates the text lvl for a given user
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET text_lvl = {str(amount)}  WHERE user_id ="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask)
def edit_settings_levelsystem(guild_id, toggler):
    # Unused for now but it will be used for the welcome image function
    # sets the column level system to 1/enabled or 0/disabled
    conn = sql()
    c = conn.cursor()
    c.execute(f"UPDATE settings SET levelsystem_toggle= {str(toggler)} WHERE guild_id={guild_id}")
    conn.commit()
    c.close()
    return True


@app.task(base=DatabaseTask)
def get_levelsystem(guild_id):
    conn = get_levelsystem.db
    c = conn.cursor()
    c.execute(f"SELECT levelsystem_toggle FROM settings WHERE guild_id =  {str(guild_id)};")
    img = c.fetchone()
    c.close()
    return img[0]