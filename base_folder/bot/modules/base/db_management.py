import base64

from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, FLOAT, BIGINT, DATETIME, ForeignKey, VARCHAR, TEXT, BOOLEAN
from sqlalchemy.orm import relationship

from base_folder.config import Session

'''
The following classes represent there corresponding database table

'''
Base = declarative_base()


class Banlist(Base):
    __tablename__ = "blacklist"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT)


class Errors(Base):
    __tablename__ = "Error"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    guild_id = Column(BIGINT, ForeignKey('guilds.guild_id'))
    error = Column(VARCHAR)
    date = Column(DATETIME)

    guilds = relationship("Guild", back_populates="Error")


class Guild(Base):
    __tablename__ = "guilds"

    guild_id = Column(BIGINT, primary_key=True)
    Error = relationship("Errors", back_populates="guilds")
    user_info = relationship("UserInfo", back_populates="guilds")
    messages = relationship("Messages", back_populates="guilds")
    reactions = relationship("Reaction", back_populates="guilds")
    roles = relationship("Roles", back_populates="guilds")
    settings = relationship("Settings", back_populates="guilds")


class Messages(Base):
    __tablename__ = "messages"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    guild_id = Column(BIGINT, ForeignKey('guilds.guild_id'))
    user_id = Column(BIGINT, ForeignKey('user_info.user_id'))
    message_id = Column(BIGINT)
    message = Column(TEXT)
    time = Column(DATETIME)

    guilds = relationship("Guild", back_populates="messages")
    user_info = relationship("UserInfo", back_populates="messages")
    reactions = relationship("Reaction", back_populates="messages")


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    guild_id = Column(BIGINT, ForeignKey('guilds.guild_id'))
    message_id = Column(BIGINT, ForeignKey("messages.message_id"))
    role_id = Column(BIGINT, ForeignKey("roles.role_id"))
    emoji = Column(CHAR)

    guilds = relationship("Guild", back_populates="reactions")
    roles = relationship("Roles", back_populates="reactions")
    messages = relationship("Messages", back_populates="reactions")


class Roles(Base):
    __tablename__ = "roles"

    guild_id = Column(BIGINT, ForeignKey('guilds.guild_id'))
    role_id = Column(BIGINT, primary_key=True, autoincrement=True)
    role_name = Column(VARCHAR(length=255))

    guilds = relationship("Guild", back_populates="roles")
    reactions = relationship("Reaction", back_populates="roles")


class Settings(Base):
    __tablename__ = "settings"

    guild_id = Column(BIGINT, ForeignKey('guilds.guild_id'), primary_key=True, autoincrement=True, nullable=False)
    standard_role_id = Column(BIGINT, default=0)
    dev_role_id = Column(BIGINT, default=0)
    mod_role_id = Column(BIGINT, default=0)
    admin_role_id = Column(BIGINT, default=0)
    imgwelcome_toggle = Column(BOOLEAN, default=False)
    imgwelcome_text = Column(VARCHAR(length=2000), default="V2VsY29tZSB0byB0aGUgc2VydmVyIHlvdSBsaXR0bGUgdXNlcg==")
    levelsystem_toggle = Column(BOOLEAN, default=False)
    welcome_channel_id = Column(BIGINT, default=0)
    leave_channel_id = Column(BIGINT, default=0)
    lvl_channel_id = Column(BIGINT, default=0)
    cmd_channel_id = Column(BIGINT, default=0)
    stdout_channel_id = Column(BIGINT, default=0)
    prefix = Column(VARCHAR(length=20), default="LQ==")
    Color = Column(VARCHAR(length=25), default="default()")
    leave_text = Column(VARCHAR(2000), default="VXNlciB1c2VyIGxlZnQgdGhlIHNlcnZlci4uLg==")
    warnThreshold = Column(Integer, default=3)
    kickThreshold = Column(Integer, default=2)
    banThreshold = Column(Integer, default=2)
    messageInterval = Column(Integer, default=2500)
    warnMessage = Column(VARCHAR(length=2000), default="Hey $MENTIONUSER, please stop spamming/"
                                                       "sending duplicate messages.")
    kickMessage = Column(VARCHAR(length=2000), default="$USERNAME was kicked for spamming/sending duplicate messages.")
    banMessage = Column(VARCHAR(length=2000), default="$USERNAME was banned for spamming/sending duplicate messages.")
    messageDuplicateCount = Column(Integer, default=5)
    messageDuplicateAccuracy = Column(FLOAT, default=90)
    ignoreBots = Column(BOOLEAN, default=True)

    guilds = relationship("Guild", back_populates="settings")


class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT)
    username = Column(String)
    guild_id = Column(BIGINT, ForeignKey('guilds.guild_id'))
    warnings = Column(Integer)
    kickCount = Column(Integer)
    text_xp = Column(BIGINT)
    text_lvl = Column(Integer)
    voice_xp = Column(Integer)
    voice_lvl = Column(Integer)
    banned_at = Column(DATETIME)
    banned_until = Column(DATETIME)
    muted_at = Column(DATETIME)
    muted_until = Column(DATETIME)

    guilds = relationship("Guild", back_populates="user_info")
    messages = relationship("Messages", back_populates="user_info")


class Db:
    """
    This class is more or less a layer on top of sqlalchemy,
    that can read data from the database and represent it in useful forms.
    """
    def __init__(self, ):
        self.session = Session()

    def prefix_lookup(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the prefix for the given guild
        """
        prefix = self.session.query(Settings.prefix).filter_by(guild_id=guild_id).one()
        prefix = (base64.b64decode(str(prefix[0]).encode("utf8"))).decode("utf8")
        self.session.commit()
        return prefix

    async def roles_from_db(self, guild_id):
        # returns a tuple with all role name's and id's

        roles = self.session.query(Roles.role_name, Roles.role_id).filter_by(guild_id=guild_id).all()
        self.session.commit()
        return roles

    async def get_admin_role(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the role id of the e.g. admin role for the given guild
        """

        role_id = self.session.query(Settings.admin_role_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return role_id[0]

    async def get_dev_role(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the role id of the e.g. admin role for the given guild
        """

        role_id = self.session.query(Settings.dev_role_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return role_id[0]

    async def get_mod_role(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the role id of the e.g. admin role for the given guild
        """

        role_id = self.session.query(Settings.mod_role_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return role_id[0]

    async def get_standard_role(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the role id of the e.g. admin role for the given guild
        """

        role_id = self.session.query(Settings.standard_role_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return role_id[0]

    async def get_warns(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the warnings for the given user, can be 0
        """
        warnings = self.session.query(UserInfo.warnings).filter(UserInfo.guild_id == guild_id,
                                                                UserInfo.user_id == user_id).all()
        self.session.commit()
        if not warnings:
            return 0
        return warnings[0][0]

    async def get_welcome_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the welcome channel for the given guild
        """

        welcome_channel = self.session.query(Settings.welcome_channel_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return welcome_channel[0]

    async def get_cmd_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the command channel for the given guild
        """

        cmd_channel = self.session.query(Settings.cmd_channel_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return cmd_channel[0]

    async def get_lvl_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the level channel for the given guild
        """

        lvl_channel = self.session.query(Settings.lvl_channel_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return lvl_channel[0]

    async def get_leave_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the leave channel for the given guild
        """

        leave_channel = self.session.query(Settings.leave_channel_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return leave_channel[0]

    async def get_stdout_channel(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the stdout(logging) channel for the given guild
        """

        stdout_channel = self.session.query(Settings.stdout_channel_id).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return stdout_channel[0]

    async def get_leave_text(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the leave text for the given guild
        """

        leave_text = self.session.query(Settings.leave_text).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return leave_text[0]

    async def get_img(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: wether the welcome image is on or off for the given guild
        """

        img = self.session.query(Settings.imgwelcome_toggle).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return img[0]

    async def get_img_text(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: the welcome text for the image  for the given guild
        """

        text = self.session.query(Settings.imgwelcome_text).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return text[0]

    async def get_text_xp(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the xp amount for the given user
        """

        xp = self.session.query(UserInfo.text_xp).filter(UserInfo.guild_id == guild_id,
                                                         UserInfo.user_id == user_id).one()
        self.session.commit()
        return xp[0]

    async def get_lvl_text(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the text lvl for the given user
        """

        lvl = self.session.query(UserInfo.text_lvl).filter(UserInfo.guild_id == guild_id,
                                                           UserInfo.user_id == user_id).one()
        self.session.commit()
        return lvl[0]

    async def get_levelsystem(self, guild_id):
        """

        :param guild_id: the id of the guild
        :returns: if the levelsytem is on or off for the specific guild
        """

        lvl_toggle = self.session.query(Settings.levelsystem_toggle).filter_by(guild_id=guild_id).one()
        self.session.commit()
        return lvl_toggle[0]

    async def get_banned_until(self, user_id, guild_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the date the user is allowed to get unbanned if none the user wasn't temp banned
        """

        date = self.session.query(Settings.levelsystem_toggle).filter(Settings.guild_id == guild_id,
                                                                      UserInfo.user_id == user_id).one()
        self.session.commit()
        return date[0]

    async def get_blacklist(self, user_id):
        """
        Searches in the db if the user is blacklisted
        :param user_id: the ID of the user
        :returns: if the user is in the blacklist if false the user isnt blacklisted
        """

        user = self.session.query(Banlist.user_id).filter_by(user_id=user_id).one()
        self.session.commit()
        if user_id in user:
            return True
        else:
            return False

    async def get_message(self, guild_id, message_id):
        """

        :param guild_id: the id of the guild
        :param message_id: the requested message id
        :return: the message content and the user_id in a list, can be none
        """

        message = self.session.query(Messages.message, Messages.user_id).filter(Messages.message_id == message_id,
                                                                                Messages.guild_id == guild_id).all()
        self.session.commit()
        return message

    async def get_guild(self, user_id):
        """

        :param user_id: the id of the user
        :return: list with all guild ids inside
        """

        guilds = self.session.query(UserInfo.guild_id).filter_by(user_id=user_id).all()
        self.session.commit()
        return guilds

    async def get_reaction_role(self, guild_id, message_id, emoji):
        """

        :param guild_id: the id of the guild
        :param message_id: the id of the message where a reaction got added
        :param emoji: the added emoji
        :return: the role id that the user should get
        """

        roleid = self.session.query(Reaction.role_id).filter(Reaction.message_id == message_id,
                                                             Reaction.guild_id == guild_id,
                                                             Reaction.emoji == emoji).one()
        self.session.commit()
        return roleid[0]

    async def leaderboard(self, guild_id):
        """

        :param guild_id:  the id of the guild
        :return: the leaderboard by rank/level with xp type list with tuples inside
        """

        ranks = self.session.query(UserInfo.text_lvl, UserInfo.text_xp,
                                   UserInfo.user_id).filter(UserInfo.guild_id == guild_id).order_by(
            UserInfo.text_xp.desc())[0:10]
        self.session.commit()
        return ranks

    def get_spam_settings(self, guild_id):
        """

        :param guild_id: the id of the given guild
        :return: list of tuples with all spam settings
        =============================
        tuple contents
        =============================
        warnThreshold : int, optional
            This is the amount of messages in a row that result in a warning within the messageInterval
        kickThreshold : int, optional
            The amount of 'warns' before a kick occurs
        banThreshold : int, optional
            The amount of 'kicks' that occur before a ban occurs
        messageInterval : int, optional
            Amount of time a message is kept before being discarded.
            Essentially the amount of time (In milliseconds) a message can count towards spam
        warnMessage : str, optional
            The message to be sent upon warnThreshold being reached
        kickMessage : str, optional
            The message to be sent up kickThreshold being reached
        banMessage : str, optional
            The message to be sent up banThreshold being reached
        messageDuplicateCount : int, optional
            Amount of duplicate messages needed to trip a punishment
        messageDuplicateKick : int, optional
            Amount of duplicate messages needed within messageInterval to trip a kick
        messageDuplicateBan : int, optional
            Amount of duplicate messages needed within messageInterval to trip a ban
        messageDuplicateAccuracy : float, optional
            How 'close' messages need to be to be registered as duplicates (Out of 100)
        ignorePerms : list, optional
            The perms (ID Form), that bypass anti-spam
        ignoreUsers : list, optional
            The users (ID Form), that bypass anti-spam
        ignoreBots : bool, optional
            Should bots bypass anti-spam?
        """

        settings = self.session.query(Settings.warnThreshold, Settings.kickThreshold, Settings.banThreshold,
                         Settings.messageInterval, Settings.warnMessage, Settings.kickMessage,Settings.banMessage,
                         Settings.messageDuplicateCount, Settings.messageDuplicateAccuracy
                         ).filter(UserInfo.guild_id==guild_id)
        self.session.commit()
        return settings

    async def get_kick_count(self, guild_id, user_id):
        """

        :param guild_id: the id of the guild
        :param user_id: the ID of the user
        :returns: the warnings for the given user, can be 0
        """

        kickcount = self.session.query(UserInfo.kickCount).filter(UserInfo.guild_id == guild_id,
                                                                  UserInfo.user_id == user_id).all()
        self.session.commit()
        if not kickcount:
            return 0
        return kickcount[0][0]
