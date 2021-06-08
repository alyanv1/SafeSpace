from discord.ext import commands
import main
import json


class Entrance(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        verification_channel = await guild.create_text_channel("verification-v2")
        verification_channel_id = verification_channel.id
        await verification_channel.set_permissions(guild.default_role, send_messages=False)
        await verification_channel.send("React to this message to verify yourself!")

        print("Message created")

        last_message = verification_channel.last_message
        verification_message_id = verification_channel.last_message_id
        emoji = '👍'
        await last_message.add_reaction(emoji)

        rules_channel = await guild.create_text_channel("rules")
        rules_channel_id = rules_channel.id
        await rules_channel.send("[placeholder]")

        rules_message_id = rules_channel.last_message_id

        with open('guilds.json', 'r') as f:
            data = json.load(f)
            guilds = data["guilds"]
            info = {"guildID": guild.id,
                    "verificationChannelID": verification_channel_id,
                    "verificationMessageID": verification_message_id,
                    "rulesChannelID": rules_channel_id,
                    "rulesMessageID": rules_message_id}
            guilds.append(info)

            new_data = {"guilds": guilds}

        print(new_data)

        with open('guilds.json', 'w') as f:
            json.dump(new_data, f, indent=4)
            print('Written to guilds.json')

        main.verification_message_id = verification_message_id
        main.verification_channel_id = verification_channel_id

        print(main.verification_channel_id)

        main.load_variables()


def setup(bot):
    bot.add_cog(Entrance(bot))
