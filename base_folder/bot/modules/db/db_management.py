import discord
from discord.ext import commands
import sqlite3


def connector():
    conn = sqlite3.connect('bot.db')
    return conn


def check_for_guild_db(id, name):
    conn = connector()
    try:
        conn.execute("SELECT * FROM " + name + ";")
        if conn is not None:
            conn.commit()
            conn.close()
            return True
        else:
            create_db(name)
    except Exception as e:
        create_db(name)
        print("Error: " + str(e))


def create_db(guild_name):
    conn = connector()
    create_table1 = '''CREATE TABLE "''' + guild_name + '''" (
                        "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "userid"	INTEGER UNIQUE,
                        "username"	TEXT,
                        "guildid"	INTEGER,
                        "text_xp"   INTEGER,
                        "text_lvl"  INTEGER,
                        "voice_xp"  INTEGER,
                        "voice_lvl"  INTEGER
                    );'''

    # create tables with the attrs of create_tables
    if conn is not None:
        conn.execute(create_table1)
        conn.commit()
        conn.close()
        return True
    else:
        print("Error! cannot create the database connection.")
        return False


async def rename_table(guild_name, settings=None):
    conn = connector()
    c = conn.cursor()
    if settings is None:
        try:
            c.execute("DROP TABLE " + guild_name + "_old;")
            create_db(guild_name)
        except sqlite3.OperationalError as e:
            c.execute("ALTER TABLE " + guild_name + " RENAME TO " + guild_name + "_old;")
            conn.commit()
            create_db(guild_name)
    return


def is_user_indb(user, userid, guild_name, guildid):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT * FROM " + guild_name + " WHERE userid=" + str(userid) + ";")
    sql = c.fetchone()
    if sql:
        return True
    else:
        sql = "INSERT INTO " + guild_name + " (username, userid, guildid) VALUES ('" + user + "', '" + str(userid) + "', '" + str(guildid) + "')"
        c.execute(sql)
        conn.commit()
        conn.close()


def roles_to_db(guildname, name, id):
    conn = connector()
    c = conn.cursor()
    create_table2 = '''create table if not exists "roles_''' + guildname + '''" (
                        "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "name"	TEXT,
                        "roleid"	INTEGER
                    );'''
    c.execute(create_table2)
    conn.commit()
    c.execute("SELECT * FROM 'roles_" + guildname + "' WHERE roleid=?", (id,))
    sql = c.fetchone()
    if sql:
        return True
    else:
        c.execute("INSERT INTO roles_" + guildname + " (name, roleid) VALUES ('" + str(name) + "', '{0}')".format(id))
        conn.commit()
        c.close()


async def roles_from_db(guildname):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT name, roleid FROM roles_" + guildname + " WHERE id > 1;")
    roles = c.fetchall()
    c.close()
    return roles


async def get_role(guildname, roleid):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT name FROM roles_" + guildname + " WHERE roleid =" + roleid + " ;")
    role_name = c.fetchone()
    c.close()
    return role_name[0]


def create_settings(guildname):
    conn = connector()
    c = conn.cursor()
    create_table = '''create table if not exists "settings_''' + guildname + '''" (
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
    c.execute(create_table)
    conn.commit()
    c.close()


async def edit_settings_role(guildname, roleid, fieldname="standard_role_id"):
    conn = connector()
    c = conn.cursor()
    create_settings(guildname)
    c.execute("UPDATE settings_" + guildname + " SET " + fieldname + " = " + roleid + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_img(guildname, img="False"):
    conn = connector()
    c = conn.cursor()
    create_settings(guildname)
    c.execute("UPDATE settings_" + guildname + " SET  imgwelcome= " + str(img) + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_img_text(guildname, img="Welcome {0.mention} to {1}!"):
    conn = connector()
    c = conn.cursor()
    create_settings(guildname)
    c.execute("UPDATE settings_" + guildname + " SET  imgwelcome_text= " + str(img) + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_welcome(guildname, channelid):
    conn = connector()
    c = conn.cursor()
    create_settings(guildname)
    c.execute("UPDATE settings_" + guildname + " SET leave_channel = " + channelid + " WHERE id = 1")
    conn.commit()
    c.close()


async def edit_settings_leave(guildname, channelid):
    conn = connector()
    c = conn.cursor()
    create_settings(guildname)
    c.execute("UPDATE settings_" + guildname + " SET welcome_channel = " + channelid + " WHERE id = 1")
    conn.commit()
    c.close()


async def get_settings_role(guildname, fieldname):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT " + fieldname + " FROM settings_" + guildname + " WHERE id = 1 ;")
    roleid = c.fetchone()
    c.close()
    return roleid[0]


async def update_xp_text(guildname, userid, amount):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE " + guildname + " SET text_xp = " + str(amount) + " WHERE userid = " + str(userid) + ";")
    conn.commit()
    c.close()


async def get_text_xp(guildname, userid):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT text_xp FROM " + guildname + " WHERE userid =  " + str(userid) + ";")
    roleid = c.fetchone()
    c.close()
    if roleid is None:
        return None
    else:
        return roleid[0]


async def get_lvl_text(guildname, userid):
    conn = connector()
    c = conn.cursor()
    c.execute("SELECT text_lvl FROM " + guildname + " WHERE userid =  " + str(userid) + ";")
    roleid = c.fetchone()
    c.close()
    if roleid is None:
        return None
    else:
        return roleid[0]


async def update_text_lvl(guildname, userid, amount=1):
    conn = connector()
    c = conn.cursor()
    c.execute("UPDATE " + guildname + " SET text_lvl = " + str(amount) + " WHERE userid = " + str(userid))
    conn.commit()
    c.close()


'''
if __name__ == "__main__":
    test = await get_settings("EA19B_und_bekannte", "standard_role_id")
    print(type(test))
'''