from discord.ext import commands
import main
import json


class Prefix(commands.Cog):
    """
    Change bot prefix
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix: str):
        """
        Change the bot prefix

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param prefix: str
            New prefix
        """
        with open("guilds.json", "r") as f:
            data = json.load(f)

        guilds = data["guilds"]

        for guild in guilds:
            if guild["guildID"] == ctx.guild.id:
                guild["prefix"] = prefix

        new_data = {"guilds": guilds}

        with open("guilds.json", "w") as f:
            json.dump(new_data, f, indent=4)


def setup(bot):
    bot.add_cog(Prefix(bot))

