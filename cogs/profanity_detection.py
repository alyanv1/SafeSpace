import traceback

import discord
from discord.ext import commands
from better_profanity import profanity
from cogs import server_setup

profanity.load_censor_words_from_file("offensive_words.txt")


class Detection(commands.Cog):
    """
    This class has our profanity detection system in place
    """

    def __init(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Detect when a message contains profanity and delete it
        
        :param message: discord.Message
            Message to be checked
        """
        if not message.author.bot:
            guild_info = server_setup.get_guild_info(message.guild)
            warned_users = guild_info["warnedUsers"]

            if profanity.contains_profanity(message.content):
                await message.delete()
                await message.channel.send(f"{message.author.mention} that is not allowed!")

                try:
                    found_user = False

                    for user in warned_users:
                        if user["userID"] == message.author.id:
                            found_user = True
                            amount_of_warns = user["numOfWarns"]
                            amount_of_warns += 1
                            user["numOfWarns"] = amount_of_warns

                            if amount_of_warns >= 15:
                                await message.author.ban(reason="15 warnings reached.")
                                await message.channel.send(
                                    f"{message.author.mention} has been banned for reaching 15 warnings.")
                            if amount_of_warns == 5 or amount_of_warns == 10:
                                await message.author.kick(reason=f"{amount_of_warns} warnings reached.")
                                await message.channel.send(
                                    f"{message.author.mention} has been kicked for reaching {amount_of_warns} warnings.")

                    if not found_user:
                        warn_user_info = {
                            "userID": message.author.id,
                            "numOfWarns": 1
                        }

                        warned_users.append(warn_user_info)

                    guild_info["warnedUsers"] = warned_users
                    server_setup.update_guild(guild_info=guild_info)

                except:
                    traceback.print_exc()
                    print("User could not be warned or kicked.")


def setup(bot):
    bot.add_cog(Detection(bot))
