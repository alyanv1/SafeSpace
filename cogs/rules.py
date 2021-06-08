import discord
from discord.ext import commands
import main


class Rules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update_rules(self, ctx):
        with open("rules_message.txt", "r") as f:
            rules_message = f.read()

        channel = ctx.guild.get_channel(main.rules_channel_id)
        message = await channel.fetch_message(main.rules_message_id)

        await message.edit(content=str(rules_message))


def setup(bot):
    bot.add_cog(Rules(bot))
