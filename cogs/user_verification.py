import discord
from discord.ext import commands
from cogs import rules


class UserVerification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm_welcome_message(self, member: discord.Member = None):
        """
        Direct message's welcome message to given user

        :param member: discord.Member
            User to be messaged
        """

        if member is not None:
            try:
                embed = await rules.format_rules(title="Welcome to the server!",
                                                 description="Be sure to follow the rules you have agreed"
                                                             " to and enjoy your time here!")
                await member.send(embed=embed)

                print(f"{member.display_name} has been dmed.")
            except:
                print("User could not be messaged.")

        else:
            print("No user provided.")


def setup(bot):
    bot.add_cog(UserVerification(bot))
