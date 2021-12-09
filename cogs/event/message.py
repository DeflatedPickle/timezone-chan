from discord.ext.commands import Cog


class CogEventMessage(Cog):
    def __init__(self, bot):
        self.bot = bot
