import re
from datetime import datetime

from discord import Message, Reaction, Member
from discord.ext.commands import Cog

from util.timezones import same_timezone, get_timezone_role, timezone_difference


class CogEventMessage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot: return
        await self.bot.wait_until_ready()

        for i in message.mentions:
            if not same_timezone(message.author, i):
                d = timezone_difference(message.author, i)

                if d > 0:
                    p = "ahead of"
                else:
                    p = "behind"

                await message.reply(
                    content=f"{i.mention} is {d * -1} hours {p} you"
                )
