import json
import discord
from discord.ext import commands
from cogs import server_setup


def get_rules() -> str:
    """
    Get's rules from rules_message.txt as a string

    :return: str
        Rules as a string
    """
    with open("rules_message.txt", "r") as f:
        rules_message = f.read()

    return rules_message


class Rules(commands.Cog):
    """
    Setup the rules using these commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_rules(self, ctx: discord.ext.commands.context.Context, *, rules: str):
        """
        Update rules in rules channel

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        :param rules: str
            Rules to be set
        """
        guild_info = server_setup.get_guild_info(ctx.guild)

        if guild_info["rulesChannelID"] is not None:
            rules_channel = server_setup.get_channel(guild=ctx.guild, channel_id=guild_info["rulesChannelID"])
            embed = await format_rules(rules=rules, title="Rules",
                                       description="You must follow these rules at all times")

            if guild_info["rulesMessageID"] is not None:
                message = await rules_channel.fetch_message(guild_info["rulesMessageID"])

                await message.edit(embed=embed)

            else:
                message = await rules_channel.send(embed=embed)
                guild_info["rulesMessageID"] = message.id

                server_setup.update_guild(guild_info=guild_info)

            guild_info["rules"] = rules
            server_setup.update_guild(guild_info=guild_info)

        else:
            await ctx.send("You must create a rules channel before you may set the rules message.")

        print("Rules have been updated.")


async def format_rules(rules: str = None, title: str = None, description: str = None) -> discord.Embed:
    """
    Format rules embed to make it look nicer

    :param rules: str
        Rules to be set
    :param title: str
        Title of embed
    :param description: str
        Description of embed
    :return embed: discord.Embed
        Embedded rules
    """
    if rules is not None:
        rules_list = rules.split("\n")

        embed = discord.Embed(
            title=title,
            description=description,
            colour=discord.Colour.blue()
        )

        embed.set_footer(text="Safe Space Discord Bot")

        for rule in rules_list:
            contents = rule.split(":")
            embed.add_field(name=str(contents[0]), value=f'`{str(contents[1])}`', inline=False)
        return embed


def setup(bot):
    bot.add_cog(Rules(bot))
