import mysql.connector
from discord.embeds import EmptyEmbed
import datetime
import discord.embeds

'''
Config
'''
BOT_TOKEN = "TOKEN"

# Sql config
SQL_IP = "the address of your server. it should be localhost"
SQL_USER = "username"
SQL_passwd = "yourpassword"
SQL_DB = "DB_name"
SQL_AUTH_PLUGIN = "mysql_native_password"

# Celery config
broker_url = 'amqp://username:password@ipaddress of your server:5672/vhost'
result_backend = 'amqp://username:password@ipaddress of your server:5672/vhost'
imports = ('base_folder.queuing.db',)
include = ['base_folder.queuing']
task_cls = 'base_folder.queuing.db:DatabaseTask'
timezone = 'Europe/Berlin'

'''
SQL
'''


def sql():
    mydb = mysql.connector.connect(
      host=SQL_IP,
      user=SQL_USER,
      passwd=SQL_passwd,
      database=SQL_DB,
      auth_plugin=SQL_AUTH_PLUGIN
    )
    return mydb


'''
Embeds
'''


def success_embed(client):
    e = build_embed(
        title="Success!",
        author=client.user.name,
        author_img=client.user.avatar_url,
        timestamp=datetime.datetime.now())
    return e


def error_embed(client):
    e = build_embed(
        title="Error!",
        author=client.user.name,
        author_img=client.user.avatar_url,
        timestamp=datetime.datetime.now(),
        color=discord.Color.red())
    return e


def build_embed(**params):
    # Copyright 2017 Zack Rauen www.ZackRauen.com
    title = params.get("title", EmptyEmbed)
    description = params.get("description", EmptyEmbed)
    color = params.get("color", discord.Color.blurple())
    url = params.get("url", EmptyEmbed)
    author = params.get("author", "")
    author_url = params.get("author_url", EmptyEmbed)
    author_img = params.get("author_img", EmptyEmbed)
    footer = params.get("footer", "")
    footer_img = params.get("footer_img", EmptyEmbed)
    timestamp = params.get("timestamp", EmptyEmbed)
    image = params.get("image", "")
    thumbnail = params.get("thumbnail", "")
    sections = params.get("sections", params.get("fields", []))
    e = discord.Embed()
    e.title = title
    e.description = description
    e.colour = color
    e.url = url
    if author:
        e.set_author(name=author, url=author_url, icon_url=author_img)
    if footer:
        e.set_footer(text=footer, icon_url=footer_img)
    e.timestamp = timestamp
    e.set_image(url=image)
    e.set_thumbnail(url=thumbnail)
    if sections:
        populate(e, sections)
    return e


def populate(embed: discord.Embed, sections: list):
    # Copyright 2017 Zack Rauen www.ZackRauen.com
    for section in sections:
        name = section.get("name", "")
        value = section.get("value", "")
        inline = section.get("inline", True)
        if not name or not value:
            continue
        embed.add_field(name=name, value=value, inline=inline)

