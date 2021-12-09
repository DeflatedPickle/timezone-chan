from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_subcommand

from config import read_config
from util.roles import delete_roles, create_roles
from util.timezones import gather_timezones


class CogSlashRoles(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_subcommand(
        base="roles",
        name="delete",
        description="Deletes all roles created by this bot",
        guild_ids=read_config(),
    )
    async def _remove_roles(self, ctx: SlashContext):
        if ctx.author.id != self.bot.get_guild(ctx.guild_id).owner_id: return
        await self.bot.wait_until_ready()

        await delete_roles(ctx.guild)

        await ctx.send("Deleted all the roles I made for you")

    @cog_subcommand(
        base="roles",
        name="reset",
        description="Resets all roles created by this bot",
        guild_ids=read_config(),
    )
    async def _roles_reset(self, ctx: SlashContext):
        if ctx.author.id != self.bot.get_guild(ctx.guild_id).owner_id: return
        await self.bot.wait_until_ready()

        await delete_roles(ctx.guild)
        await create_roles(ctx.guild)

        await ctx.send("Reset all the roles I made for you")

    @cog_subcommand(
        base="roles",
        name="clear",
        description="Clears all roles users have that were created by this bot",
        guild_ids=read_config(),
    )
    async def _roles_clear(self, ctx: SlashContext):
        if ctx.author.id != self.bot.get_guild(ctx.guild_id).owner_id: return
        await self.bot.wait_until_ready()

        for k in gather_timezones().keys():
            for m in ctx.guild.members:
                for r in m.roles:
                    if r.name == k:
                        await m.remove_roles(r)

        await ctx.send("Cleared all the roles I made from users")
