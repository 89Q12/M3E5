import unittest
from base_folder.bot.utils.helper import DbCache, GuildStates, Ctx
from base_folder.bot.utils.logger import Log

from base_folder.tests.test_doubles.guild import Guild
from base_folder.tests.test_doubles.member import Member


class GuildStateTest(unittest.TestCase):
    """Class ctx"""
    def test_init_ctx(self):
        ctx = Ctx(member=Member(Guild(616609333832187924), "Test"))
        self.assertEqual(ctx.guild.id, 616609333832187924)

    """Db cache class"""
    def test_init_dbcache_str(self):
        cache = DbCache()
        self.assertEqual(cache.__str__(), "Dbcache with states 0 in it")

    def test_init_dbcache_loop(self):
        cache = DbCache(loop="loop")
        self.assertEqual(cache.loop, "loop")

    def test_dbcache_get_states_none_guildid(self):
        cache = DbCache()
        self.assertEqual(cache.states, {})

    def test_dbcache_make_states(self):
        cache = DbCache()
        cache.make_states([Guild(616609333832187924), Guild(616609333832187923)], logger=Log())
        self.assertEqual(cache._states[616609333832187924].__repr__(),
                         GuildStates(Guild(616609333832187924), logger=Log(), loop=None).__repr__())
        self.assertEqual(cache._states[616609333832187923].__repr__(),
                         GuildStates(Guild(616609333832187923), logger=Log(), loop=None).__repr__())
        self.assertEqual(cache.__str__(), "Dbcache with states 2 in it")

    def test_dbcache_create_state(self):
        cache = DbCache()
        cache.create_state(Guild(616609333832187924), logger=Log())
        self.assertEqual(cache._states[616609333832187924].__repr__(),
                         GuildStates(Guild(616609333832187924), logger=Log(), loop=None).__repr__())
        self.assertEqual(cache.__str__(), "Dbcache with states 1 in it")

    def test_dbcache_destruct_state(self):
        cache = DbCache()
        cache.create_state(Guild(616609333832187924), logger=Log())
        cache.destruct_state(Guild(616609333832187924))
        self.assertEqual(cache.__str__(), "Dbcache with states 0 in it")

    """GuildState class"""
    def test_GuildState_init(self):
        guild = Guild(616609333832187924)
        logger = Log()
        guildstate = GuildStates(guild, logger=logger, loop=None)
        self.assertEqual(guildstate.guild, guild)
        self.assertEqual(guildstate.logger, logger)
        self.assertEqual(guildstate.options, {})
        self.assertEqual(guildstate.loop, None)

    def test_GuildState_prefix(self):
        guild = Guild(616609333832187924)
        logger = Log()
        guildstate = GuildStates(guild, logger=logger, loop=None)
        self.assertEqual(guildstate.get_prefix, "-")

    def test_GuildState_get_levelsystem(self):
        guild = Guild(616609333832187924)
        logger = Log()
        guildstate = GuildStates(guild, logger=logger, loop=None)
        guildstate._levelsystem_toggle = 1
        self.assertEqual(guildstate.get_levelsystem, 1)


if __name__ == '__main__':
    unittest.main()
