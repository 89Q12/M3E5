import base64
from abc import ABC
from base_folder.queuing.worker import app, Task
from base_folder.bot.config.config import sql
from mysql import connector
import re
'''
Initialize the tables
'''


class DatabaseTask(Task, ABC):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = sql()
        try:
            conn = self._db
            conn.cursor()
        except Exception:
            self._db = sql()
        return self._db


@app.task(base=DatabaseTask, ignore_result=False)
def initialize_guild(guild_id):
    conn = initialize_guild.db
    c = conn.cursor()
    c.execute(f"INSERT INTO guilds (`guild_id`) VALUES ({guild_id});")
    conn.commit()
    c.execute(f"INSERT INTO settings (guild_id) VALUES ({guild_id});")
    conn.commit()
    c.close()
    return


'''
General per guild settings
'''


@app.task(base=DatabaseTask, ignore_result=True)
def is_user_indb(user_name, user_id, guild_id):
    # Checks if a given user is in the db else writes it in the db
    conn = is_user_indb.db
    c = conn.cursor()
    try:
        c.execute(f"INSERT INTO user_info (username, user_id, guild_id) "
                  f"VALUES ('{str(user_name)} ', '{str(user_id)}', '{str(guild_id)}')")
        conn.commit()
    except:
        return


@app.task(base=DatabaseTask, ignore_result=True)
def on_error(guild_id, error):
    conn = on_error.db
    c = conn.cursor()
    c.execute(f"INSERT into Error (guild_id, error) VALUES ('{guild_id}', %s)", (error,))
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def set_prefix(guild_id, prefix):
    conn = set_prefix.db
    c = conn.cursor()
    prefix = (base64.b64encode(str(prefix).encode("utf8"))).decode("utf8")
    c.execute(f"UPDATE settings SET prefix='{prefix}' WHERE guild_id ={guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_warns(guild_id, user_id, amount):
    # sets warn with given amount
    conn = edit_warns.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET warnings={str(amount)} WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_muted_at(guild_id, user_id, date):
    conn = edit_muted_at.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET muted_at='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def muted_until(guild_id, user_id, date):
    conn = muted_until.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET muted_until='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_banned_at(guild_id, user_id, date):
    conn = edit_banned_at.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET banned_at='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def banned_until(guild_id, user_id, date):
    conn = banned_until.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET banned_until='{date}' WHERE user_id="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


'''
Role settings 
'''


@app.task(base=DatabaseTask, ignore_result=True)
def roles_to_db(guild_id, role_name, role_id):
    # Checks if a given role is in the db else writes it in the db
    conn = roles_to_db.db
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


@app.task(base=DatabaseTask, ignore_result=True)
def remove_role(guild_id, role_id):
    conn = remove_role.db
    c = conn.cursor()
    c.execute(f"DELETE FROM roles WHERE role_id = {role_id} and guild_id = {guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_role(guild_id, role_id, field_name):
    # Let's you set roles e.g. mod role
    conn = edit_settings_role.db
    c = conn.cursor()
    c.execute(f"INSERT INTO settings (guild_id,{field_name}) VALUES ('{guild_id}','{role_id}')"
              f"ON DUPLICATE KEY UPDATE {field_name}='{role_id}'")
    conn.commit()
    c.close()
    return


'''
end of roles settings

Channel settings and warning settings
'''


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_welcome(guild_id, channel_id):
    # sets the welcome_channel to the given channel id
    conn = edit_settings_welcome.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET welcome_channel_id={str(channel_id)} WHERE guild_id = '{guild_id}'")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_leave(guild_id, channel_id):
    # sets the leave_channel to the given channel id
    conn = edit_settings_leave.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET leave_channel_id ={str(channel_id)} WHERE guild_id ='{guild_id}'")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_cmd(guild_id, channel_id):
    # sets the leave_channel to the given channel id
    conn = edit_settings_leave.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET cmd_channel_id ={str(channel_id)} WHERE guild_id ='{guild_id}'")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def set_leave_text(guild_id, text):
    # sets the leave_channel to the given channel id
    conn = edit_settings_leave.db
    c = conn.cursor()
    text = base64.b64encode(text.encode("utf8")).decode("utf8")
    c.execute(f"UPDATE settings SET leave_text ='{str(text)}' WHERE guild_id ='{guild_id}'")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_lvl(guild_id, channel_id):
    # sets the leave_channel to the given channel id
    conn = edit_settings_leave.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET lvl_channel_id ={str(channel_id)} WHERE guild_id ='{guild_id}'")
    conn.commit()
    c.close()
    return


'''
end of channel and warning settings

Welcomeimg
'''


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_img(guild_id, img):
    # Unused for now but it will be used for the welcome image function
    # sets the column imgwelcome to 1/enabled or 0/disabled
    conn = edit_settings_img.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET imgwelcome_toggle={str(img)} WHERE guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_img_text(guild_id, img="Welcome {0.mention} to {1}!"):
    # Unused for now but it will be used for the welcome image function
    # sets the message text in the column imgwelcome_text to what ever you enter
    conn = edit_settings_img_text.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET imgwelcome_text={str(img)} WHERE guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


'''
End of general settings

Level system 
'''


@app.task(base=DatabaseTask, ignore_result=True)
def update_xp_text(guild_id, user_id, amount):
    # updates the xp amount for a given user
    conn = update_xp_text.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET text_xp={str(amount)} WHERE user_id={str(user_id)} and guild_id={str(guild_id)};")
    conn.commit()
    c.close()
    return


@app.task(ignore_result=True)
def update_text_lvl(guild_id, user_id, amount=1):
    # updates the text lvl for a given user
    conn = update_xp_text.db
    c = conn.cursor()
    c.execute(f"UPDATE user_info SET text_lvl = {str(amount)}  WHERE user_id ="
              f"{str(user_id)} and guild_id={str(guild_id)}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def edit_settings_levelsystem(guild_id, toggler):
    # Unused for now but it will be used for the welcome image function
    # sets the column level system to 1/enabled or 0/disabled
    conn = edit_settings_levelsystem.db
    c = conn.cursor()
    c.execute(f"UPDATE settings SET levelsystem_toggle= {str(toggler)} WHERE guild_id={guild_id}")
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def insert_message(guild_id, userid, messageid, channelid, message):
    """

    :param guild_id: id of the guild the data is for
    :param userid: the id of the user given by the api
    :param messageid: the id of the message
    :param channelid: the channel id the message was sent in
    :param message: message content itself
    :return: nothing
    """

    conn = insert_message.db
    c = conn.cursor()
    c.execute(f"INSERT INTO `messages`(`guild_id`, `user_id`, `message_id`, `channel_id`, `message`)"
              f"VALUES ('{guild_id}','{userid}','{messageid}','{channelid}', %s)", (message,))
    conn.commit()
    c.close()
    return
<<<<<<< Updated upstream


@app.task(base=DatabaseTask, ignore_result=True)
def insert_reaction(guild_id, message_id, roleid, emoji):
    """

    :param guild_id: id of the guild the data is for
    :param channelid: the channel id the reaction message was sent in
    :param message_id: the id of the message
    :param roleid: the role a user should get if the user reacts
    :param emoji: the emoji the bot reacted with
    :return:
    """
    conn = insert_message.db
    c = conn.cursor()
    c.execute(f"INSERT INTO `reactions`(`guild_id`, `message_id`, `role_id`, `emoji`) VALUES ('{guild_id}',"
              f"'{message_id}','{roleid}', %s)", (emoji,))
    conn.commit()
    c.close()
    return


@app.task(base=DatabaseTask, ignore_result=True)
def update_role_name(guild_id, roleid, name):
    """

    :param guild_id: id of the guild the data is for
    :param roleid: the role that should be updated
    :param name: the new name of the role
    :return:
    """
    conn = update_role_name.db
    c = conn.cursor()
    c.execute(f"UPDATE `roles` SET `role_name`={name} WHERE 'guild_id' = {guild_id} and 'roleid' = {roleid}")
    conn.commit()
    c.close()
    return
