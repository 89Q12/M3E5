"""
This is helper script like creating the ctx object out of the member object etc
"""
import base64


class Ctx:
    def __init__(self, member):
        self.member = member
        self.guild = member.guild
        self.author = member


def prefix(objclient, ctx):
    r = objclient.sql.prefix_lookup(ctx.guild.id)
    pre = (base64.b64decode(str(r).encode("utf8"))).decode("utf8")
    return pre


def loadmodules(modules, client):
    for extension in modules:
        try:
            client.load_extension(extension)
            print('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))