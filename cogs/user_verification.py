import discord
from discord.ext import commands
from cogs import server_setup
from cogs import rules


async def dm_welcome_message(member: discord.Member = None):
    """
    Direct message's welcome message to given user

    :param member: discord.Member
        User to be messaged
    """
    if member is not None:
        try:
            guild_info = server_setup.get_guild_info(member.guild)

            if guild_info["rules"] is not None:
                rules_content = guild_info["rules"]

                embed = await rules.format_rules(rules=rules_content, title=f"Welcome to {member.guild.name}!",
                                                 description="Be sure to follow the rules you have agreed"
                                                             " to and enjoy your time here!")
                await member.send(embed=embed)

                print(f'{member} has agreed to the rules on "{member.guild.name}".')
            else:
                await member.send("Rules must be set before you may agree to them.")
        except:
            print(f"{member} could not be messaged.")

    else:
        print("No user provided.")


class UserVerification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(UserVerification(bot))
