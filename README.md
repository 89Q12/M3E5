# M3E5
M3E5 is a Discord bot that implements an chatbot and an home assistant. The chatbot is based on Google's nmt AI, it's a bit hacky but it works.

# Why the name?

I got inspired by the MEE6 but I don't wanted to build a clone of MEE6 instead I want to creat a special unique bot with tons of unique features.<br>
Like a real AI and an home assistant like Alexa.

# Things that are working right now
- Discord bot base
  - the current prefix is "."
  - basic commands
    - Ban
    - unban
    - kick
    - clear amount e.g. 100 messages
    - mute/unmute
    - giving someone a role e.g. .give_role @someone @some_role
    - info about a role: how many users the role have and permissions
    - Tempban
  - Welcome image(uncompleted)
  - db connection
  - Auto roles
  - set default role, admin, dev and mod role
  - Join and leave messages
  - reading/writing to database
  - loading/unloading/reloading cogs is now working if you have the dev role
  - levelsystem is now working(text based)
- Chatbot 
  - currently trainning but I'm halfway through it
- Home assistant
  - AI integration 

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
 
 Clone the repo and install requirements. 
 In the config you need paste your bot token, then you can run main.py. 
 Invite your bot to your server and run the commands to initialize the bot and the database.
 Run the commands in the following order:
 - .builddb
 - .roles_in_db
 - .set_standard_role @role
 - .set_dev  @role
 - .set_mod  @role
 - .set_admin  @role
 - open the bot.db and edit the settings_{guild.id} table and set your welcome and leave channel
 
# TODO
  
- The whole discord bot
  - Every feature from the bot list above
  - AI integration
  - home assistant integration
- Refactoring the nmt code base
  - inferencemode 
  - using multiple models 
- Building the home assistant inegration on the assistant side 
  - rewriting main.py from the assistant 
  - disabling some features
  - integration of the nmt AI
  
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

Cute or? isn't it

## For examples of the home assistant please click [here](https://github.com/ggeop/Python-ai-assistant)

Because I don't want to steal any credits or so and I'm lazy xD
