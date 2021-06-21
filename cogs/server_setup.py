import traceback

import discord
from discord.ext import commands
import json
import main


def get_guilds():
    """
    Getter method to get guilds data from guilds.json
    """
    with open("guilds.json", "r") as f:
        data = json.load(f)

    guilds = data["guilds"]
    return guilds


def get_guild_info(guild: discord.Guild) -> dict:
    """
    Getter method to get guild data of a specified guild

    :param guild: discord.Guild
    :return: dict
        Python dictionary of all stored guild data
    """
    guilds = get_guilds()

    for g in guilds:
        if g["guildID"] == guild.id:
            return g


def update_guild(guild_info: dict):
    """
    Update the data of a guild in guilds.json

    :param guild_info: dict
        Python dictionary of stored data for a specific guild
    """
    guilds = get_guilds()
    index = 0
    for g in guilds:
        if g["guildID"] == guild_info["guildID"]:
            guilds[index] = guild_info
        index += 1

    new_data = {"guilds": guilds}

    with open("guilds.json", "w") as f:
        json.dump(new_data, f, indent=4)


def get_channel(guild: discord.Guild, channel_id: int):
    """
    Get a specified channel with it's id

    :param guild: discord.Guild
    :param channel_id: int
    :return:
    """
    for channel in guild.channels:
        if channel.id == channel_id:
            return channel


def get_role(guild: discord.Guild, role_id) -> discord.Role:
    """
    Get a specified role with it's id

    :param guild: discord.Guild
    :param role_id: int
    :return: discord.Role
        Intended role
    """
    for role in guild.roles:
        if role.id == role_id:
            return role


class ServerSetup(commands.Cog):
    """
    Setup the bot using these commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """
        Commands to be run when bot joins a server; creates rules and verification channel and stores their respective
        id's, and creates verification method with a reaction

        :param guild: discord.Guild
            Guild that bot join's
        """
        # Store data
        with open('guilds.json', 'r') as f:
            data = json.load(f)
            guilds = data["guilds"]
            info = {"guildID": guild.id,
                    "verificationChannelID": None,
                    "verificationMessageID": None,
                    "rulesChannelID": None,
                    "rulesMessageID": None,
                    "verifiedRoleID": None,
                    "prefix": ".",
                    "rules": None,
                    "warnedUsers": []}
            guilds.append(info)

            new_data = {"guilds": guilds}

        with open('guilds.json', 'w') as f:
            json.dump(new_data, f, indent=4)
            print('Written to guilds.json')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """
        Removes server information when bot leaves a server

        :param guild: discord.Guild
            Server that bot left
        """
        with open("guilds.json", "r") as f:
            guilds = json.load(f)["guilds"]

        for g in guilds:
            print(f"GuildID: {guild.id}")
            if g["guildID"] == guild.id:
                guilds.remove(g)
                print("Guild has been removed.")

        new_data = {"guilds": guilds}

        with open("guilds.json", "w") as f:
            json.dump(new_data, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        """
        Check if deleted role is verification role and remove information from guilds.json accordingly

        :param role: discord.Role
            Deleted role
        """
        guild_info = get_guild_info(role.guild)

        if role.id == guild_info["verifiedRoleID"]:
            guild_info["verifiedRoleID"] = None
            update_guild(guild_info=guild_info)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """
        Check if verification or rules channels are deleted and remove their information from guilds.json accordingly

        :param channel:
            Deleted channel
        """
        guild_info = get_guild_info(channel.guild)

        print(f"Channel type: {type(channel)}")

        if guild_info["verificationChannelID"] == channel.id:
            guild_info["verificationChannelID"] = None
            guild_info["verificationMessageID"] = None

            update_guild(guild_info=guild_info)

        elif guild_info["rulesChannelID"] == channel.id:
            guild_info["rulesChannelID"] = None
            guild_info["rulesMessageID"] = None
            guild_info["rules"] = None

            update_guild(guild_info=guild_info)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """
        Check if deleted message is verification or rules message and remove their information from guilds.json
        accordingly

        :param message: discord.Message
            Deleted message
        """

        guild_info = get_guild_info(message.guild)

        print(message.id)

        if message.id == guild_info["verificationMessageID"]:
            guild_info["verificationMessageID"] = None
            print(f'Verification message has been deleted from "{message.guild.name}"')
        elif message.id == guild_info["rulesMessageID"]:
            guild_info["rulesMessageID"] = None
            guild_info["rules"] = None
            print(f'Rules message has been deleted from "{message.guild.name}"')

        update_guild(guild_info=guild_info)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_ver_role(self, ctx: discord.ext.commands.context.Context, role_name: str = "Verified"):
        """
        Creates/edits the verification role

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param role_name: str
            Name of verification role
        """
        guild_info = get_guild_info(ctx.guild)

        if guild_info["verifiedRoleID"] is None:
            verified_role = await ctx.guild.create_role(name=role_name)
            verified_role_id = verified_role.id

            guild_info["verifiedRoleID"] = verified_role_id
            update_guild(guild_info=guild_info)
            await ctx.send("Verified role created.")

        else:
            for role in ctx.guild.roles:
                if role.id == guild_info["verifiedRoleID"]:
                    await role.edit(name=role_name)
                    await ctx.send("Verified role name changed.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_ver_channel(self, ctx: discord.ext.commands.context.Context, *, channel_name: str):
        """
        Creates/edits verification channel

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param channel_name: str
            Name of verification channel
        """
        if channel_name is not None:
            guild_info = get_guild_info(ctx.guild)

            if guild_info["verificationChannelID"] is not None:
                verification_channel = get_channel(guild=ctx.guild, channel_id=guild_info["verificationChannelID"])

                await verification_channel.edit(name=channel_name)

            else:
                verification_channel = await ctx.guild.create_text_channel(channel_name)
                verification_channel_id = verification_channel.id
                await verification_channel.set_permissions(ctx.guild.default_role, send_messages=False)

                guild_info["verificationChannelID"] = verification_channel_id
                update_guild(guild_info=guild_info)
        else:
            await ctx.send("Please specify a channel name.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_ver_message(self, ctx: discord.ext.commands.context.Context, *, message: str = None):
        """
        Creates/edits an embed of the verification message

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param message: str
            Verification message
        """
        if message is not None:
            guild_info = get_guild_info(ctx.guild)

            if guild_info["verificationChannelID"] is not None:
                verification_channel = get_channel(guild=ctx.guild, channel_id=guild_info["verificationChannelID"])

                embed = discord.Embed(title=message,
                                      colour=discord.Colour.blue())
                embed.set_footer(text="Safe Space Discord Bot")

                if guild_info["verificationMessageID"] is not None:
                    verification_message = await verification_channel.fetch_message(guild_info["verificationMessageID"])
                    await verification_message.edit(embed=embed)

                else:
                    verification_message = await verification_channel.send(embed=embed)
                    verification_message_id = verification_message.id
                    guild_info["verificationMessageID"] = verification_message_id
                    update_guild(guild_info=guild_info)
            else:
                await ctx.send("You must create a verification channel before you may set a verification message.")
        else:
            await ctx.send("Please specify a message.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_ver_reaction(self, ctx: discord.ext.commands.context.Context):
        """
        Adds a reaction to the verification message

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        """
        guild_info = get_guild_info(ctx.guild)

        message = await get_channel(guild=ctx.guild, channel_id=guild_info["verificationChannelID"]).fetch_message(
            guild_info["verificationMessageID"])

        await message.add_reaction('👍')
        print("Reaction added")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_rules_channel(self, ctx: discord.ext.commands.context.Context, *, channel_name: str = None):
        """
        Creates/edits rules channel

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param channel_name: str
            Name of rules channel
        """

        if channel_name is not None:
            guild_info = get_guild_info(ctx.guild)

            if guild_info["rulesChannelID"] is not None:
                rules_channel = get_channel(guild=ctx.guild, channel_id=guild_info["rulesChannelID"])

                await rules_channel.edit(name=channel_name)

            else:
                rules_channel = await ctx.guild.create_text_channel(channel_name)
                rules_channel_id = rules_channel.id
                await rules_channel.set_permissions(ctx.guild.default_role, send_messages=False)

                guild_info["rulesChannelID"] = rules_channel_id
                update_guild(guild_info=guild_info)
        else:
            await ctx.send("Please specify a channel name.")


def setup(bot):
    bot.add_cog(ServerSetup(bot))
