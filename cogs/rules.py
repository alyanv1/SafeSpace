import discord
from discord.ext import commands
import main


def get_rules() -> str:
    """
    Get's rules from rules_message.txt as a string

    :return: str

    """
    with open("rules_message.txt", "r") as f:
        rules_message = f.read()

    return rules_message


class Rules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update_rules(self, ctx: discord.ext.commands.context.Context):
        """
        Update rules in rules channel

        :param ctx: discord.ext.commands.context.Context
            Payload of useful information from discord API
        """
        channel = ctx.guild.get_channel(main.rules_channel_id)
        message = await channel.fetch_message(main.rules_message_id)

        embed = await format_rules(title="Rules", description="Here are the rules")

        await message.edit(embed=embed)

        print("Rules have been updated.")


async def format_rules(title: str = None, description: str = None) -> discord.Embed:
    """
    Format rules embed to make it look nicer

    :param title: str
        Title of embed
    :param description: str
        Description of embed
    :return embed: discord.Embed
        Embedded rules
    """

    rules_message = get_rules()
    rules_list = rules_message.split("\n")

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
