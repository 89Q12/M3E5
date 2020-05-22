import logging


def token():
    return "NjY0MTc3MDI4MTE5MDAzMTM2.XsZ_bg.oyr7jMdr-IBh5nsaKvO-pvvUnu0"


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
