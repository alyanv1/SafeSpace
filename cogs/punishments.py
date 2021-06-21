import traceback

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from cogs import server_setup


class Punishments(commands.Cog):
    """
    These are the punishment commands available with this bot
    """
    def __init__(self, bot):
        self.bot = bot

    # Kick a user from the server
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kick a user from the server

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param member: discord.Member
            User to be kicked
        :param reason: str
            Reason for kicking member
        """
        try:
            await member.send(f"You have been kicked from {ctx.guild.name} for reason: {reason}")
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked from {ctx.guild.name} for reason: {reason}")
        except Exception:
            await ctx.send("Insufficient permissions.")
            traceback.print_exc()

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to kick users.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: discord.ext.commands.context.Context, member: discord.Member, *, reason=None):
        """
        Ban a user from the server

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param member: discord.Member
            User to be banned
        :param reason: str
            Reason for banning member
        """
        try:
            await member.send(f"You have been banned from {ctx.guild.name} for reason: {reason}")
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned from {ctx.guild.name} for reason: {reason}")
        except Exception:
            await ctx.send("Insufficient permissions.")
            traceback.print_exc()

    @ban.error
    async def ban_error(self, ctx, error):
        """
        Handle errors for ban command

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param error:
        """
        print(f"Error: {error}")
        print(f"Error type: {type(error)}")
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to ban users.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """
        Unban a user from the server

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param member: discord.Member
            User to be unbanned
        """
        banned_list = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for banned_user in banned_list:
            user = banned_user.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.send(f"{user.mention} has been unbanned.")
                await ctx.guild.unban(user)

                guild_info = server_setup.get_guild_info(ctx.guild)

                warned_users = guild_info["warnedUsers"]

                index = 0
                for warned_user in warned_users:
                    print(f"{warned_user['userID']}, {user.id}")
                    if warned_user["userID"] == user.id:
                        print('here')
                        new_user_info = warned_user
                        new_user_info["numOfWarns"] = 0
                        warned_users[index] = new_user_info

                        print(warned_users)

                        guild_info["warnedUsers"] = warned_users

                        server_setup.update_guild(guild_info=guild_info)

                        return
                return
        await ctx.send(f"{member.name} was not found on the ban list.")

    @unban.error
    async def unban_error(self, ctx, error):
        """
        Handle errors for unban command

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param error:
        """
        print(f"Error: {error}")
        print(f"Error type: {type(error)}")
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to unban users.")


def setup(bot):
    bot.add_cog(Punishments(bot))
