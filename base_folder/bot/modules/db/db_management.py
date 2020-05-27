import discord
from discord.ext import commands
import sqlite3

'''
Connection settings and other unused functions
'''


def connector():
    conn = sqlite3.connect('bot.db')
    return conn


async def rename_table(guild_id, settings=None):
    conn = connector()
    c = conn.cursor()
    if settings is None:
        try:
            c.execute("DROP TABLE name_" + str(guild_id) + "_old;")
            create_db(guild_id)
        except sqlite3.OperationalError as e:
            c.execute("ALTER TABLE name_" + str(guild_id) + " RENAME TO name_" + str(guild_id) + "_old;")
            conn.commit()
            create_db(guild_id)
    return


'''
Creating tables, checking if a given table exists
'''


def check_for_guild_db(guild_id):
    conn = connector()
    try:
        conn.execute("SELECT * FROM name_" + str(guild_id) + " ;")
        if conn is not None:
            conn.commit()
            conn.close()
        else:
            create_db(guild_id)
    except sqlite3.OperationalError as e:
        create_db(guild_id)
    try:
        conn = connector()
        conn.execute("SELECT * FROM roles_" + str(guild_id) + " ;")
        if conn is not None:
            conn.commit()
            conn.close()
        else:
            create_roles(guild_id)
    except sqlite3.OperationalError as e:
        create_roles(guild_id)
    try:
        conn = connector()
        conn.execute("SELECT * FROM settings_" + str(guild_id) + " ;")
        if conn is not None:
            conn.commit()
            conn.close()
        else:
            create_settings(guild_id)
    except sqlite3.OperationalError as e:
        create_settings(guild_id)


def create_db(guild_id):
    conn = connector()
    create_main_table = '''create table if not exists "name_''' + str(guild_id) + '''" (
                        "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "userid"	INTEGER UNIQUE,
                        "username"	TEXT,
                        "guildid"	INTEGER,
                        "warnings"  INTEGER,
                        "text_xp"   INTEGER,
                        "text_lvl"  INTEGER,
                        "voice_xp"  INTEGER,
                        "voice_lvl"  INTEGER
                    );'''

    # create tables with the attrs of create_tables
    if conn is not None:
        conn.execute(create_main_table)
        conn.commit()
        conn.close()
        return True
    else:
        print("Error! cannot create the database connection.")
        return False


def create_settings(guild_id):
    conn = connector()
    c = conn.cursor()
    create_settings_table = '''create table if not exists "settings_''' + str(guild_id) + '''" (
                        "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "standard_role_id"	INTEGER,
                        "admin_role_id"	TEXT,
                        "mod_role_id"	TEXT,
                        "dev_role_id"	TEXT,
                        "imgwelcome"	TEXT,
                        "imgwelcome_text"	TEXT,
                        "welcome_channel"	INTEGER,
                        "leave_channel"	INTEGER 
                    );'''
    c.execute(create_settings_table)
    conn.commit()
    c.close()


def create_roles(guild_id):
    conn = connector()
    c = conn.cursor()
    create_table2 = '''create table if not exists "roles_''' + str(guild_id) + '''" (
                        "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "name"	TEXT,
                        "roleid"	INTEGER
                    );'''
    c.execute(create_table2)
    conn.commit()


'''
reading/ writing to db e.g. users and roles
'''


def random_settings(guild_id):
    conn = connector()
    c = conn.cursor()
    c.execute("INSERT INTO settings_" + str(guild_id) + " (mod_role_id) VALUES ('test')")
    conn.commit()
    c.close()


def roles_to_db(guild_id, role_name, role_id):
    conn = connector()
    c = conn.cursor()
    '''
    Checks if a given else writes it in the db
    '''
    c.execute("SELECT * FROM 'roles_" + str(guild_id) + "' WHERE roleid=?", (str(role_id),))
    sql = c.fetchone()
    if sql:
        return True
    else:
        c.execute("INSERT INTO roles_" + str(guild_id)
                  + " (name, roleid) VALUES ('"
                  + str(role_name)
                  + "', '{0}')".format(str(role_id)))
        conn.commit()
        c.close()


def is_user_indb(user, user_id, guild_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM name_" + str(guild_id) + " WHERE userid=" + str(user_id) + ";")
    sql = c.fetchone()
    if sql:
        return
    else:
        sql = "INSERT INTO name_" + str(guild_id) +\
              " (username, userid, guildid) VALUES" \
              " ('" + str(user) + "', '" + str(user_id)\
              + "', '" + str(guild_id) + "')"
        c.execute(sql)
        conn.commit()
        conn.close()


async def roles_from_db(guild_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT name, roleid FROM roles_" + str(guild_id) + " WHERE id > 1;")
    roles = c.fetchall()
    c.close()
    return roles


async def edit_settings_role(guild_id, role_id, field_name="standard_role_id"):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT id FROM settings_" + str(guild_id))
    if c.fetchone() is None:
        c.close()
        random_settings(guild_id)
        conn = connector()
        c = conn.cursor()
        c.execute("UPDATE settings_" + str(guild_id) + " SET " + str(field_name) + " = " + str(role_id) + " WHERE id=1")
        conn.commit()
        c.close()
    else:
        conn = connector()
        c = conn.cursor()
        c.execute("UPDATE settings_" + str(guild_id) + " SET " + str(field_name) + " = " + str(role_id) + " WHERE id=1")
        conn.commit()
        c.close()


async def edit_settings_img(guild_id, img="False"):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE settings_" + str(guild_id) + " SET  imgwelcome= " + str(img) + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_img_text(guild_id, img="Welcome {0.mention} to {1}!"):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE settings_" + str(guild_id) + " SET  imgwelcome_text= " + str(img) + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_welcome(guild_id, channel_id):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE settings_" + str(guild_id) + " SET leave_channel = " + str(channel_id) + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_leave(guild_id, channel_id):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE settings_" + str(guild_id) + " SET welcome_channel = " + str(channel_id) + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_warns(guild_id, user_id, amount):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE name_" + str(guild_id) + " SET warnings = " + str(amount) + " WHERE userid = " + str(user_id))
    conn.commit()
    c.close()


async def get_role(guild_id, role_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT name FROM roles_" + str(guild_id) + " WHERE roleid =" + str(role_id) + " ;")
    role_name = c.fetchone()
    c.close()
    return role_name[0]


async def get_settings_role(guild_id, field_name):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT " + str(field_name) + " FROM settings_" + str(guild_id) + " WHERE id = 1 ;")
    roleid = c.fetchone()
    c.close()
    return roleid[0]


async def get_warns(guild_id, user_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT warnings FROM name_" + str(guild_id) + " WHERE userid =" + str(user_id) + ";")
    warnings = c.fetchone()
    c.close()
    if warnings is None:
        return 0
    else:
        return warnings[0]


async def get_welcome_channel(guild_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT welcome_channel FROM settings_" + str(guild_id))
    welcome_channel = c.fetchone()
    if welcome_channel is None:
        return "you need to set a channel first"
    else:
        return welcome_channel[0]


async def get_leave_channel(guild_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT leave_channel FROM settings_" + str(guild_id))
    leave_channel = c.fetchone()
    if leave_channel is None:
        return "you need to set a channel first"
    else:
        return leave_channel[0]


'''
Levelsystem 
'''


async def update_xp_text(guild_id, user_id, amount):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE name_" + str(guild_id) + " SET text_xp = " + str(amount) + " WHERE userid = " + str(user_id) + ";")
    conn.commit()
    c.close()


async def get_text_xp(guild_id, user_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT text_xp FROM name_" + str(guild_id) + " WHERE userid =  " + str(user_id) + ";")
    xp = c.fetchone()
    c.close()
    if xp is None:
        return None
    else:
        return xp[0]


async def get_lvl_text(guild_id, user_id):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT text_lvl FROM name_" + str(guild_id) + " WHERE userid =  " + str(user_id) + ";")
    lvl = c.fetchone()
    c.close()
    if lvl is None:
        return None
    else:
        return lvl[0]


async def update_text_lvl(guild_id, user_id, amount=1):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE name_" + str(guild_id) + " SET text_lvl = " + str(amount) + " WHERE userid = " + str(user_id))
    conn.commit()
    c.close()

'''
Test area
'''

'''
if __name__ == "__main__":
    test = await get_settings("EA19B_und_bekannte", "standard_role_id")
    print(type(test))
'''