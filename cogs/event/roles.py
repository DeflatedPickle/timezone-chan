from discord import Guild
from discord.ext.commands import Cog

from util.roles import create_roles


class CogEventRoles(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await create_roles(guild)
