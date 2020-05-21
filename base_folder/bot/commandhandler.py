import discord
from discord.ext import commands


def is_command(message):
    print(message.content)
    return True


def main(message):
    return message.content
