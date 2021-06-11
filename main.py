import discord
import json
import os
from discord.ext import commands

bot_token = "ODM3NDAyNjQ1MzQxMjc0MTIy.YIsB_A.xh2rDUNM6VFu6NGBjCuvH1UoM6w"

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

guild_id = 837351222833971211  # Current guild id for the server our bot is in

# Channel and message id's
verification_channel_id: int = None
verification_message_id: int = None
rules_channel_id: int = None
rules_message_id: int = None


def load_variables():
    """
    Load channel and message id's from guilds.json
    """
    global verification_channel_id
    global verification_message_id
    global rules_channel_id
    global rules_message_id

    with open("guilds.json", "r") as f:
        data = json.load(f)

        guilds = data["guilds"]

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
    """
    Prints when the bot is completely online
    """
    print("Bot is online.")


# Error message
@bot.event
async def on_command_error(ctx: discord.ext.commands.context.Context, error: discord.DiscordServerError):
    """
    Catch when an invalid command is used

    :param ctx: discord.ext.commands.context.Context
        Payload of useful information from discord API
    :param error: discord.DiscordServerError
        Error occurred
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')


# Clear text message
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx: discord.ext.commands.context.Context, amount: int):
    """
    Command to clear messages in text channels

    :param ctx:
        Payload of useful information from discord API
    :param amount: int
        Amount of messages to delete
    """
    await ctx.channel.purge(limit=(amount + 1))


# Clear command error message
@clear.error
async def clear_error(ctx: discord.ext.commands.context.Context, error: discord.DiscordServerError):
    """
    Catch error when clear command is used

    :param ctx: discord.ext.commands.context.Context
        Payload of useful information from discord API
    :param error: discord.DiscordServerError
        Error occurred
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')


# Load cogs
@bot.command()
async def load(extension: str):
    """
    Load a cog

    :param extension: str
        Cog extension to be loaded
    """
    bot.load_extension(f"cogs.{extension}")


# Unload cogs
@bot.command()
async def unload(extension: str):
    """
    Unload cog

    :param extension: str
        Cog extension to be unloaded
    """
    bot.unload_extension(f"cogs.{extension}")


# Load current cogs in ./cogs directory
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(bot_token)
