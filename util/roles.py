import discord.utils
from discord import Guild

from util.timezones import gather_utc


async def create_roles(guild: Guild):
    for i in gather_utc():
        await guild.create_role(
            name=i.upper(),
            reason="timezone",
        )


async def delete_roles(guild: Guild):
    for i in gather_utc():
        get = discord.utils.get(guild.roles, name=i.upper())
        if get:
            await get.delete()
