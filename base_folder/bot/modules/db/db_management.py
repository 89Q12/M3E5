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
            create_db(id, name)
    except Exception as e:
        create_db(id, name)
        print("Error: " + str(e))


def create_db(id, guild_name):
    conn = connector()
    create_table1 = '''CREATE TABLE "''' + guild_name + '''" (
                        "id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        "userid"	INTEGER UNIQUE,
                        "username"	TEXT,
                        "guildid"	INTEGER
                    );'''

    # create tables with the attrs of create_tables
    if conn is not None:
        conn.execute(create_table1)
        conn.execute("INSERT INTO " + guild_name + "(guildid) VALUES('" + str(id) + "')")
        print("Sucess")
        conn.commit()
        conn.close()
        return True
    else:
        print("Error! cannot create the database connection.")
        return False


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


def roles_from_db(ctx):
    conn = connector()
    c = conn.cursor()
    message = []
    for i in ctx.guild.roles:
        conn.execute("SELECT * FROM roles_" + i.guild.name + " WHERE roleid=?", (i.id,))
        message = str(c.fetchone())
        message += message
    return message


