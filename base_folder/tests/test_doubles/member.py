class Member:
    """
    Member class test double for the member object
    """
    def __init__(self, guild, member):
        self.guild = guild
        self.member = member

    def __repr__(self):
        return self.member
