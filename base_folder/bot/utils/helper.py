"""
This is helper script like creating the ctx object out of the member object etc
"""


class Ctx:
    def __init__(self, member):
        self.member = member
        self.guild = member.guild
        self.author = member
