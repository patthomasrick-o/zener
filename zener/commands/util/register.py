from discord.ext.commands import Bot
from .rm import Rm


async def register(bot: Bot):
    await bot.add_cog(Rm(bot))
