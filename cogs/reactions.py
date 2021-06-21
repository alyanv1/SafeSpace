import discord
from discord.ext import commands
from cogs import user_verification
from cogs import server_setup


class Reactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.raw_models.RawReactionActionEvent):
        """
        Check to see if reaction is added onto verification message; if so, give user a role

        :param payload: discord.raw_models.RawReactionActionEvent
            Useful information from discord API
        """
        if payload.member != self.bot.user:
            guild_info = server_setup.get_guild_info(self.bot.get_guild(payload.guild_id))

            if guild_info["verifiedRoleID"] is not None:
                if payload.message_id == guild_info["verificationMessageID"]:
                    guild = self.bot.get_guild(payload.guild_id)
                    verified_role = server_setup.get_role(guild=guild, role_id=guild_info["verifiedRoleID"])
                    member = payload.member

                    await user_verification.dm_welcome_message(member=member)

                    if member is not None:
                        await member.add_roles(verified_role)
                    else:
                        print('Member not found.')
            elif payload.channel_id == guild_info["verificationChannelID"]:
                verification_message = await server_setup.get_channel(self.bot.get_guild(payload.guild_id),
                                                                      guild_info["verificationChannelID"]).fetch_message(
                    guild_info["verificationMessageID"])
                await verification_message.remove_reaction(payload.emoji, payload.member)

                print("Verified role must be setup before reaction can work.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.raw_models.RawReactionActionEvent):
        """
        Check to see if reaction is removed from verification message; if so, remove role from user

        :param payload: discord.raw_models.RawReactionActionEvent
            Useful information from discord API
        """
        if payload.member != self.bot.user:
            guild_info = server_setup.get_guild_info(self.bot.get_guild(payload.guild_id))

            if guild_info["verifiedRoleID"] is not None:
                msg_id = payload.message_id
                if msg_id == guild_info["verificationMessageID"]:
                    guild = self.bot.get_guild(payload.guild_id)

                    verified_role = server_setup.get_role(guild=guild, role_id=guild_info["verifiedRoleID"])

                    member = guild.get_member(payload.user_id)
                    if member is not None:
                        await member.remove_roles(verified_role)
                    else:
                        print('Member not found.')


def setup(bot):
    bot.add_cog(Reactions(bot))
