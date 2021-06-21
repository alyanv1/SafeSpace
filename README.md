# SafeSpace
![alt text](https://i.imgur.com/xWAlDiO.jpg)
## Description
SafeSpace is a Discord Bot which aims to reduce toxicity in Discord Servers through virtue of an affirmed TOS system and automated offensive message detection.

## About
This bot was created by Alyan, Jonathan, and Taleiven, with the vision of eradicating oppression and marginalization issues in Discord communities. In May of 2021, we set out to create a tool that would allow Discord users to reduce negativity in their servers through the regulation/enforcement of server terms of service and through server message moderation.


# Features
A list of our bot's features!


## Entrance System/Terms & Conditions, + Customization
![alt text](https://i.imgur.com/8Tut5WY.png)

The SafeSpace Discord Bot contains a verification system. Upon joining, new users will be required to agree to a server's rules, as well as terms and conditions. This can be done with a reaction to the verification message, which will then grant the user access to the server.
### Setup
- Add the bot to your server
- Create a rules and verification channel with ".set_rules_channel [channel name]" and ".set_ver_channel [channel name]" respectively
- Set the rules with ".set_rules [rule title:rule description\n...]" <- Use this format (it's easier to write the rules in a notepad first then copy and pasting it into the message)
- Set the verification message with ".set_ver_message [message]"
- Give the @everyone role only the following permissions: "View Channels" and "Read Message History"
- Create a verification role with ".set_ver_role [role name]"
- Edit the verification role permissions to your liking in the Discord server settings
- IMPORTANT: Be sure to set the bot's "Safe Space"' role above the verification role in the role topology of your server, bot will not work properly otherwise

You have now setup the bot on your server!

## Kick System
(Picture of kick system)

Kick users from the server with a simple command.

`.kick <@username#0000> <reason>`
Kick a user for a specified reason. Leave `<reason>` field blank for None.

## Ban/Unban System
(Picture of ban/unban system)

Ban and Unban users from the server with simple commands.

`.ban <@username#0000> <reason>`
Ban a user for a specified reason. Leave `<reason>` field blank for None.

`.unban <username#0000>`
Unban a user.

## Warning System/Message Removal
(Picture of warning system/message removal)

When an offensive message sent by a user, it will be detected by the bot. The user will recieve a warning, and the offensive message will be removed.

If a user reaches X warnings, they will be banned from the server. 

(Related commands/syntax)


# Feedback & Bug Reports
Give us feedback on our project/report bugs!
## Github Issues
(Explanation of how this works)
## Message Us
Contact xxxxxx@xxxx.xxx, xxxxxx@xxxx.xxx, or xxxxxx@xxxx.xxx, to send us messages.
