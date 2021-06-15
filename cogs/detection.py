import discord
from discord.ext import commands
import main
import json
from better_profanity import profanity

profanity.load_censor_words_from_file("offensive.txt")


class Detection(commands.Cog):

    def __init(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                await message.delete()
                await message.channel.send("ducking mengrel")


def setup(bot):
    bot.add_cog(Detection(bot))
