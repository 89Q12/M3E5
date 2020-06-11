# About

M3E5 is a Discord bot that implements an chatbot and an home assistant. The chatbot is based on Google's nmt AI, it's a bit hacky but it works. I try my best to program this bot with focus on perfomance and scalability.
The Ai is currently online on telegram, it can be reached via this @Zofiasbaby_bot username. Just write /start then you talk to her. 
If you have any questions or you want to see the bot in action join this [discord](https://discord.gg/GWJ6Jeg)

## Why the name?

I got inspired by the MEE6 but I don't wanted to build a clone of MEE6 instead I want to creat a special unique bot with tons of unique features.<br>
Like a real AI and an home assistant like Alexa.

# Planned features

![Status](https://img.shields.io/badge/status-completed-green.svg)

- Discord bot base
  - the standard prefix is - but it's changeable with -prefix arg 
  - basic Moderation commands
    - Ban
    - unban
    - kick
    - clear amount e.g. 100 messages
    - mute/unmute
    - giving someone a role e.g. .give_role @someone @some_role
    - info about a role: how many users the role have and permissions
    - warn 
    - infractions
    - clear infractions
    - info about a role
  - Welcome image
  - welcome/leave channel 
  - db connection
  - Auto roles
  - set default role, admin, dev and mod role
  - Join and leave messages
  - reading/writing to database
  - loading/unloading/reloading cogs is now working if you have the dev role
  - levelsystem is now working(text based)
  - basic permission system
- Chatbot 
  - currently trainning but I'm halfway through it
  

![Status](https://img.shields.io/badge/status-in%20progress-red.svg)

- Discord features
  - Tempban/mute will be ready as soon as I have the celery implemention ready
  - lock/unlock a specific channel for specific roles 
  - Multi server bot but for now it will be single server only so you have to change some things
  - Custom commands
  - Bunch of standard commands like welcome messages and funny commands like .hug <name>
  - Auto tasks
  - Alerts for various services like Twitch and reddit
  - Music player
  - custom messaging design 
  - Logging Channels to a database
  - Recording meetings ( Voice recording to an mp3 file)
  - Home assistant integration
  - Custom voice channels 
  - poke admins/moderators via Telegram or Email if they aren't online
  - Advanced permission system, that ueses groups of accepted roles and banned roles per command
  - celery as queuing system, the brocker will be redis. With that the bot becomes scaleable and background tasks get easier to manage
- Chatbot features
  - Answers to messages like a real human 
  - Discord bridge 
  - Home assistant bridge
  - maybe more but idk now yet
- Home assistant
  - Discord bridge
  - Seamless ai bridge 
  - Disabling a few commands that aren't needed e.g. play a song on youtube, because this gets handeld by the bot
 
# Critical bugs

  - Not enough in the code comments D: hehe
  
# Install instructions 
 
 I'm working on an docker img infrastructure but atm follow the run instructions 
 
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
 
 If you encounter any bugs or errors please open an issue with steps to reproduce and as much details about the bug or error as you have. Thank you <3
 
# Home assistant

For this part I'm using a modified version of this [assistant](https://github.com/ggeop/Python-ai-assistant).<br> 
All credits for the home assistant goes to [ggeop](https://github.com/ggeop).

The assistant uses nltk, that means that if you write "what time is it" it will understand that you're asking for the current time :D

# Chatbot

As I stated earlier I'm using Google's nmt but a modified version by [daniel-kukiela](https://github.com/daniel-kukiela), the repo can be found [here](https://github.com/daniel-kukiela/nmt-chatbot).
All credits for the chatbot goes to Google and [daniel-kukiela](https://github.com/daniel-kukiela).

# Examples
## Here are some examples of the chatbot:

Question: Can you sing me a song?
Answer: I'll post it.

Question: You are cute
Answer: I'm so confused.

Question: <3<br>
Answer: <3

Question: i have to get an invite to grab some food from the fridge
Answer: I'll go ahead and get it.

Question: What do you think about the human race?
Answer: I think it's a bit of a dick.

Cute or? isn't it

## For examples of the home assistant please click [here](https://github.com/ggeop/Python-ai-assistant)

Because I don't want to steal any credits or so and I'm lazy xD
