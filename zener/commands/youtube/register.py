from discord.ext.commands import Bot
from .join import JoinCommand
from .leave import LeaveCommand
from .stop import StopCommand
from .youtube import YouTubeCommand


async def register(bot: Bot):
    await bot.add_cog(JoinCommand(bot))
    await bot.add_cog(LeaveCommand(bot))
    await bot.add_cog(StopCommand(bot))
    await bot.add_cog(YouTubeCommand(bot))
