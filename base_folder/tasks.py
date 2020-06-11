from celery import Celery
from base_folder.bot.config.config import sql
import mysql.connector
app = Celery('tasks')
app.config_from_object('base_folder.celeryconfig')


@app.task
def add(sql, guild_id):
    conn = sql
    c = conn.cursor()
    c.execute(f"SELECT prefix FROM settings WHERE guild_id = '{guild_id}'")
    x = c.fetchone()
    return x[0]

