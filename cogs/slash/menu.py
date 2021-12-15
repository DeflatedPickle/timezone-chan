from discord import File
from discord.ext.commands import Cog
from discord.utils import get
from discord_slash import SlashContext, ComponentContext
from discord_slash.cog_ext import cog_subcommand, cog_component
from discord_slash.utils.manage_components import create_select, create_actionrow, create_select_option

from config import read_config
from util.timezones import gather_utc


class CogSlashMenu(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_subcommand(
        base="menu",
        name="utc",
        description="Sends a message with a map and a dropdown of UTC time-zones",
        guild_ids=read_config(),
    )
    async def _create_menu_utc(self, ctx: SlashContext):
        if ctx.author.id != self.bot.get_guild(ctx.guild_id).owner_id: return
        await self.bot.wait_until_ready()

        select = create_select(
            options=[
                create_select_option(
                    label=p,
                    value=p,
                ) for p in gather_utc()
            ],
            custom_id="timezonechan_utc_menu",
            placeholder="Choose your time-zone",
            min_values=1,
            max_values=1,
        )
        action_row = create_actionrow(select)

        await ctx.send(
            file=File(
                fp="res/img.png",
                filename="map.png",
            ),
            components=[action_row],
        )

    @cog_component()
    async def timezonechan_utc_menu(self, ctx: ComponentContext):
        await self.bot.wait_until_ready()

        for i in ctx.author.roles:
            if "utc" in i.name.lower():
                await ctx.author.remove_roles(i)

        await ctx.author.add_roles(get(ctx.guild.roles, name=ctx.selected_options[0]))

        await ctx.send(f"Set your timezone to {ctx.selected_options[0]}!", hidden=True)

    # @cog_subcommand(
    #     base="menu",
    #     name="europe",
    #     description="Creates the selects for Europe",
    #     guild_ids=read_config(),
    # )
    # async def _create_menu_europe(self, ctx: SlashContext):
    #     if ctx.author.id != self.bot.get_guild(ctx.guild_id).owner_id: return
    #     await self.bot.wait_until_ready()
    #
    #     p = gather_places("europe")
    #     g = [p[x:x + 25] for x in range(0, len(p), 25)]
    #     c = 0
    #     t = len(g)
    #
    #     for i in g:
    #         c += 1
    #         # select = create_select(
    #         #     options=[
    #         #         create_select_option(
    #         #             label=p,
    #         #             value=p,
    #         #         ) for p in i
    #         #     ],
    #         #     placeholder="Choose your time-zone",
    #         #     min_values=1,
    #         #     max_values=1,
    #         # )
    #         # action_row = create_actionrow(select)
    #
    #         b = []
    #
    #         for p in i:
    #             b.append(create_button(
    #                 style=ButtonStyle.blurple,
    #                 label=p
    #             ))
    #
    #         rows = []
    #         for s in [b[x:x + 5] for x in range(0, len(b), 5)]:
    #             rows.append(create_actionrow(*s))
    #
    #         await ctx.send(
    #             content=f"Europe ({c}/{t})",
    #             components=rows
    #         )
