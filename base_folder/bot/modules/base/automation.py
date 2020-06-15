import asyncio
from datetime import datetime, timedelta
import time

'''
Automated tasksbackground tasks
'''


async def main_loop_background_tasks(self):
    await self.wait_until_ready()
    closed = self.is_closed()
    while not closed:
        print("s")
        await asyncio.sleep(10)


async def get_guilds(client):
    """
    :param client: discord.py object with all bot functions that discord.py has
    :returns: a list with all guilds
    """
    return client.guilds


async def get_banned_member(client):
    """
    :param client: discord.py object with all bot functions that discord.py has
    :returns: a list with all temp banned members
    """
    members = []
    for guild in await get_guilds(client):
        for member in await guild.bans():
            if member.reason.endswith("."):
                members.append(member.user.id)
    return members


async def get_banned_until(client):
    """
    :param client: discord.py object with all bot functions that discord.py has
    :returns: a list with banned until dates
    """
    members = await get_banned_member(client)
    dates = []
    for user in members:
        date = await client.sql.get_banned_until(user)
        if date is None:
            pass
        else:
            dates.append(date)
    return dates


async def unban_at_date():
    """
    :param client: discord.py object with all bot functions that discord.py has
    :returns: dispatches a function that unbans a user at the banned_until date

    members = await get_banned_member(client)
    dates = await get_banned_until(client)
    """
    hour = 0
    minute = 0
    second = 0
    for i in range(len(members)):
        hour = dates[i].hour
        minute = dates[i].minute
        second = dates[i].seconds

class AllMatch(set):
    """Universal set - match everything"""
    def __contains__(self, item): return True


allMatch = AllMatch()


def conv_to_set(obj):  # Allow single integer to be provided
    if isinstance(obj, (int)):
        return {obj}  # Single item
    if not isinstance(obj, set):
        obj = set(obj)
    return obj

# The actual Event class
class Event(object):
    def __init__(self, action, min=None, hour=None,
                 day=None, month=None, dow=None,
                 args=(), kwargs=None):
        if dow is None:
            dow = allMatch
        if hour is None:
            hour = allMatch
        if min is None:
            min = allMatch
        if month is None:
            month = allMatch
        if kwargs is None:
            kwargs = {}
        if day is None:
            day = allMatch
        self.mins = conv_to_set(min)
        self.hours= conv_to_set(hour)
        self.days = conv_to_set(day)
        self.months = conv_to_set(month)
        self.dow = conv_to_set(dow)
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t):
        """Return True if this event should trigger at the specified datetime"""
        return ((t.minute     in self.mins) and
                (t.hour       in self.hours) and
                (t.day        in self.days) and
                (t.month      in self.months) and
                (t.weekday()  in self.dow))

    def check(self, t):
        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)


class CronTab(object):
    def __init__(self, *events):
        self.events = events

    def run(self):
        t=datetime(*datetime.now().timetuple()[:5])
        while 1:
            for e in self.events:
                e.check(t)

            t += timedelta(minutes=1)
            while datetime.now() < t:
                time.sleep((t - datetime.now()).seconds)