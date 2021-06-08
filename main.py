import discord
import json
import os
from discord.ext import commands

bot_token = ""


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

guild_id = 837351222833971211

with open("guilds.json", "r") as f:
    data = json.load(f)

    guilds = data["guilds"]

verification_channel_id: int = None
verification_message_id: int = None
rules_channel_id: int = None
rules_message_id: int = None


def load_variables():
    global verification_channel_id
    global verification_message_id
    global rules_channel_id
    global rules_message_id

    for guild in guilds:
        if guild["guildID"] == guild_id:
            verification_channel_id = guild["verificationChannelID"]
            verification_message_id = guild["verificationMessageID"]

            rules_channel_id = guild["rulesChannelID"]
            rules_message_id = guild["rulesMessageID"]


load_variables()


# Ready message
@bot.event
async def on_ready():
    print("Bot is online.")


# Error message
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')


# Clear text message
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=(amount + 1))


# Clear command error message
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')


# Load cogs
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


# Unload cogs
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(bot_token)
