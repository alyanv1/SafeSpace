import discord
import json
import os
from discord.ext import commands

bot_token: str

with open("bot_token", "r") as f:
    bot_token = f.read()


def get_prefix(client, message):
    with open("guilds.json", "r") as f:
        data = json.load(f)

    guilds = data["guilds"]

    for guild in guilds:
        if guild["guildID"] == message.guild.id:
            return guild["prefix"]


bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())


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
@commands.has_permissions(administrator=True)
async def load(extension: str):
    """
    Load a cog

    :param extension: str
        Cog extension to be loaded
    """
    bot.load_extension(f"cogs.{extension}")
    print(f"{extension} has been loaded.")


# Unload cogs
@bot.command()
@commands.has_permissions(administrator=True)
async def unload(extension: str):
    """
    Unload cog

    :param extension: str
        Cog extension to be unloaded
    """
    bot.unload_extension(f"cogs.{extension}")
    print(f"{extension} has been unloaded.")


# Load current cogs in ./cogs directory
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename} has been loaded.")

bot.run(bot_token)
