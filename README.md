# M3E5
M3E5 is a Discord bot that implements an chatbot and an home assistant. The chatbot is based on Google's nmt AI, it's a bit hacky but it works. 
If you have any questions or you want to see the bot in action join this [discord](https://discord.gg/GWJ6Jeg)

# Why the name?

I got inspired by the MEE6 but I don't wanted to build a clone of MEE6 instead I want to creat a special unique bot with tons of unique features.<br>
Like a real AI and an home assistant like Alexa.

# Things that are working right now
- Discord bot base
  - the standard prefix is - but it's changeable with -prefix arg 
  - basic commands
    - Ban
    - unban
    - kick
    - clear amount e.g. 100 messages
    - mute/unmute
    - giving someone a role e.g. .give_role @someone @some_role
    - info about a role: how many users the role have and permissions
    - Tempban  but not great implemented
    - Tempmute but not great implemented
    - warn 
    - infractions
    - clear infractions
  - Welcome image
  - db connection
  - Auto roles
  - set default role, admin, dev and mod role
  - Join and leave messages
  - reading/writing to database
  - loading/unloading/reloading cogs is now working if you have the dev role
  - the permissionsystem is currently not working, so you need to set the role id's in permissions.py
  - levelsystem is now working(text based)
- Chatbot 
  - currently trainning but I'm halfway through it

# Critical bugs

- None

# Planned features

I guess it's too much but I will just work my way through all of them :D

- Discord features
  - Multi server bot but for now it will be single server only so you have to change some things
  - Moderation features e.g. muting people etc
  - Auto roles
  - Custom commands
  - Bunch of standard commands like welcome messages and funny commands like .hug <name>
  - Level system
  - Auto task
  - Alerts for various services like Twitch 
  - Music player
  - custom messaging design 
  - Logging Channels to a database
  - Recording meetings ( Voice recording to an mp3 file)
  - Home assistant integration
  - Custom voice channels 
  - poke admins/moderators via Telegram or Email if they aren't online
- Chatbot features
  - Answers to messages like a real human 
  - Discord bridge 
  - Home assistant bridge
  - maybe more but idk now yet
- Home assistant
  - Discord bridge
  - Seamless ai bridge 
  - Disabling a few commands that aren't needed e.g. play a song on youtube, because this gets handeld by the bot
  
 # Install instructions 
 
 I will add them as soon as I have time to make an docker img
 
 ### run instructions
 
 Clone the repo and install requirements and setup a mysql server with the database file I uploaded. 
 In the config you need to paste your bot token, then you can run main.py. 
 Invite your bot to your server and run the following commands to initialize the bot and the database.
 Run the commands in the following order:
 - .builddb
 - .roles_in_db
 - .set_standard_role @role
 - .set_dev  @role
 - .set_mod  @role
 - .set_admin  @role
 - open the bot.db and edit the settings_{guild.id} table and set your welcome and leave channel
 
 If you encounter any bugs or errors please open an issue with steps to reproduce and as much details about the bug or error as you have. Thank you <3
 
# Home assistant

For this part I'm using a modified version of this [assistant](https://github.com/ggeop/Python-ai-assistant).<br> 
All credits for the home assistant goes to [ggeop](https://github.com/ggeop).

The assistant uses nltk, that means that if you write "what time is it" it will understand that you're asking for the current time :D

# Chatbot

As I stated earlier I'm using Google's nmt but a modified version by [daniel-kukiela](https://github.com/daniel-kukiela), the repo can be found [here](https://github.com/daniel-kukiela/nmt-chatbot).
All credits for the chatbot goes to Google and [daniel-kukiela](https://github.com/daniel-kukiela).

# Examples

Below you will find some examples.


## Here are some examples of the chatbot:

Question: Can you sing me a song?
Answer: I'll post it.

Question: You are cute
Answer: I'm so confused.

Question: <3<br>
Answer: <3

Question: i have to get an invite to grab some food from the fridge
Answer: I'll go ahead and get it.

Cute or? isn't it

## For examples of the home assistant please click [here](https://github.com/ggeop/Python-ai-assistant)

Because I don't want to steal any credits or so and I'm lazy xD
