import discord
from discord.ext import commands
import main
from cogs import user_verification


class Reactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Reaction added onto message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.raw_models.RawReactionActionEvent):
        """
        Check to see if reaction is added onto verification message; if so, give user a role

        :param payload: discord.raw_models.RawReactionActionEvent
            Useful information from discord API
        """

        if payload.member != self.bot.user:
            msg_id = payload.message_id
            if msg_id == main.verification_message_id:
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
                role = discord.utils.get(guild.roles, name='Cool')
                member = payload.member

                await user_verification.UserVerification.dm_welcome_message(payload, member)

                if member is not None:
                    await member.add_roles(role)
                else:
                    print('Member not found.')

    # Reaction removed from message
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.raw_models.RawReactionActionEvent):
        """
        Check to see if reaction is removed from verification message; if so, remove role from user

        :param payload: discord.raw_models.RawReactionActionEvent
            Useful information from discord API
        """

        if payload.member != self.bot.user:
            msg_id = payload.message_id
            if msg_id == main.verification_message_id:
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
                role = discord.utils.get(guild.roles, name='Cool')
                member = guild.get_member(payload.user_id)
                if member is not None:
                    await member.remove_roles(role)
                else:
                    print('Member not found.')


def setup(bot):
    bot.add_cog(Reactions(bot))
