import logging


def token():
    return ""
    
def sql():
    mydb = mysql.connector.connect(
      host="",
      user="",
      passwd="
      database='M3E5',
    )
    return mydb
    
    
def prefix():
    return "-"


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
