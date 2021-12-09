from discord import Intents
from discord.ext.commands import Bot
from discord_slash import SlashCommand

from config import read_config, write_config, read_id

intents = Intents.default()
intents.guilds = True
intents.members = True

bot = Bot(
    command_prefix="!",
    self_bot=True,
    help_command=None,
    intents=intents,
)
slash = SlashCommand(
    bot,
    sync_commands=True,
)


@bot.event
async def on_ready():
    print(f"timezones! how do they work?")

    config = read_config()

    for i in bot.guilds:
        if i.id not in config:
            config[i.id] = {
            }

    write_config(config)


if __name__ == "__main__":
    from cogs.event.roles import CogEventRoles
    from cogs.event.message import CogEventMessage
    from cogs.slash.roles import CogSlashRoles
    from cogs.slash.menu import CogSlashMenu

    bot.add_cog(CogEventRoles(bot))
    bot.add_cog(CogEventMessage(bot))
    bot.add_cog(CogSlashRoles(bot))
    bot.add_cog(CogSlashMenu(bot))

    bot.run(read_id())
