import discord
from discord.ext import commands

class Punishments(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Kick a user from the server
        @commands.command()
        async def kick(self, ctx, member : discord.Member, *, reason = None):
            try:
                await member.kick(reason = reason)
                await ctx.send(f"{member.mention} has been kicked from {ctx.guild.name} for reason: {reason}")
                await member.send(f"You have been kicked from {ctx.guild.name} for reason: {reason}")
            except Exception:
                await ctx.send("Insufficient permissions.")

        # Ban a user from the server
        @commands.command()
        async def ban(self, ctx, member : discord.Member, *, reason = None):
            try:
                await member.ban(reason = reason)
                await ctx.send(f"{member.mention} has been banned from {ctx.guild.name} for reason: {reason}")
                await member.send(f"You have been banned from {ctx.guild.name} for reason: {reason}")
            except Exception:
                await ctx.send("Insufficient permissions.")

        # Unban a user from the server
        @commands.command()
        async def unban(self, ctx, *, member):
            banned_list = await ctx.guilds.bans()
            member_name, member_discriminator = member.split('#')

            for banned_user in banned_list:
                user = banned_user.user

                if(user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"{user.mention} has been unbanned.")
                    return
            await ctx.send(f"{member.name} was not found on the ban list.")

def setup(bot):
    bot.add_cog(Punishments(bot))
