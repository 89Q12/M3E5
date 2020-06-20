![py_versions](https://img.shields.io/badge/python-3.7_3.8-blue)
# About

M3E5 is a Discord bot that implements an chatbot. The chatbot is based on Google's nmt AI, it's a bit hacky but it works.<br>
The Ai is currently online on telegram, it can be reached via this @Zofiasbaby_bot username. Just write /start then you talk to her.<br>
I try my best to program this bot with focus on perfomance and scalability but I'm still learning.
If you have any questions or you want to see the bot in action join this [discord](https://discord.gg/GWJ6Jeg)

## Why the name?

I got inspired by the MEE6 but I don't wanted to build a clone of MEE6 instead I want to creat a special unique bot with tons of unique features.<br>
Like a real AI and some other features.

## What M3E5 love's and uses

- Docker/Docker-compose
- rabbitmq
- celery
- mysql
- discord.py

# Planned features

![Status](https://img.shields.io/badge/status-completed-green.svg)

For a list with all commands and there usage look at [commads](https://github.com/11Tuvork28/M3E5/blob/master/commands.md)

- Discord bot base
  - the standard prefix is - but it's changeable with -prefix arg 
  - basic Moderation commands
    - Ban
    - unban
    - kick
    - clear amount e.g. 100 messages
    - mute/unmute
    - giving someone a role e.g. .give_role @someone @some_role
    - info about a role e.g. how many users the role have and permissions
    - warn 
    - infractions
    - clear infractions
  - profile shows you your writer rank/xp and warnings
  - Welcome image
  - welcome/leave channel 
  - Auto roles
  - db connection
  - set default role, admin, dev and mod role
  - reading/writing to database
  - loading/unloading/reloading cogs is now working if you have the dev role
  - levelsystem(text based)
  - basic permission system
  - One bot instance can run on multiple servers now without errors
  - when the bot joins a server the database is automatically initialized
  - On server join the owner gets a message with all setup commands that need to be executed
  - celery as queuing system works now
- Chatbot 
  - trained
  - Answers to messages like a real human 

![Status](https://img.shields.io/badge/status-in_progress-red.svg)

- Discord features
  - custom Join and leave messages
  - custom help command
  - anti spam
  - Tempban/mute currently no idea how to do it perfectly 
  - lock/unlock a specific channel for specific roles 
  - Custom commands
  - Bunch of standard commands like welcome messages and funny commands like hug @name
  - Auto tasks
  - Alerts for various services like Twitch and reddit
  - Music player
  - custom messaging design 
  - Logging Channels to a database
  - Recording meetings ( Voice recording to an mp3 file)
  - Custom voice channels 
  - poke admins/moderators via Telegram or Email if they aren't online
  - Advanced permission system, that ueses groups of accepted roles and banned roles per command
  - reaction roles
  - unittests
- Chatbot features
  - Discord bridge 
  - maybe more but idk now yet
 
# Critical bugs

  -Not well documented
  
# Install instructions 
 
 You need to install a few things and I assume that you're using linux:
 - Docker
 - Docker-compose
 - rabbitmq
 - mysql-server
 
 ### First things first:<br>
 - I assume that you're using Linux<br>
 - clone the repo and cd into the cloned repo
 - Instal, for docker [goto](https://docs.docker.com/get-docker/) for docker-compose [goto](https://docs.docker.com/compose/install/).
 
 ### For rabbitmq follow these steps:<br>
- Add the ppa repo to your source list<br>
```echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list ```<br>
- Get the signing key<br>
```wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add - ```<br>
- Then update your system<br>
```sudo apt-get update ```<br>
- Install the rabbitmq server<br>
```sudo apt-get install rabbitmq-server```<br>
- Enable the server as a service<br>
```sudo systemctl enable rabbitmq-server```<br>
- Start the server<br>
```sudo systemctl start rabbitmq-server```<br>
 Now we need to configure a few things<br>
- Create a user<br>
```sudo rabbitmqctl add_user myuser somepassword```<br>
- Create a vhost the name doesn't really matter for us but remember the name cause you need the name a few times<br>
```sudo rabbitmqctl add_vhost myvhost ```<br>
- Create a tag, I used administrator <br>
```sudo rabbitmqctl set_user_tags myuser mytag```<br>
- Setting the permissions for the user<br>
```sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*" ```<br>
### For mysql follow these steps:<br>
- Install mysql-server<br>
```sudo apt install mysql-server```<br>
- Cofigure mysql<br>
```sudo mysql_secure_installation```<br>
- Logging into mysql to adjust somethings<br>
```sudo mysql ```<br>
- You should see a table look for root and the plugin it should be auth_socket but we want to change that<br>
```SELECT user,authentication_string,plugin,host FROM mysql.user;```<br>
- Editing the root user, just change the password to your needs<br>
```ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password';```<br>
```FLUSH PRIVILEGES; ```<br>
- And then check the plugin again, it should now be caching_sha2_password like the others<br>
```SELECT user,authentication_string,plugin,host FROM mysql.user; ```<br>
-then the server<br>
```exit ```<br>
- logging back into the mysql server <br>
```mysql -u root -p```<br>
- Creating a user with all privileges<br>
```CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';```<br>
- Grant all rights<br>
```GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;```<br>
- Now create the bot database
```create database theNameOfTheDb;```<br>
- Now use the db with that command<br>
```use  theNameOfTheDb;```<br>
- Now import the database file, I assume that you're still in the directory of the cloned repo<br>
```source M3E5.sql```<br>
-Thats it, exit the sql server<br>
```exit ```<br>
### Setup the config file
- Navigate to base_folder/bot/config and open the config.py
- Now enter your bot token and all other things.
- Note that you only need to change the rabbitmq server address, username and vhost for celery
- Then run ``` docker-compose up``` and look if everything works if so hit ctrl+c and run ``` docker-compose up -d``` that runs it in detached mode.

### run instructions
 After installing everything invite your bot to your server and run the following commands to initialize the bot and the database.
 Run the commands in the following order:
- -prefix if you want to change the prefix
- -set_leave
- -set_welcome
- -set_lvl
- -set_cmd
- -set_default
- -set_dev
- -set_mod
- -set_admin
 
 If you encounter any bugs or errors please open an issue with steps to reproduce and as much details about the bug or error as you have. Thank you <3

# Chatbot

As I stated earlier I'm using Google's nmt but a modified version by [daniel-kukiela](https://github.com/daniel-kukiela), the repo can be found [here](https://github.com/daniel-kukiela/nmt-chatbot).
All credits for the chatbot goes to Google and [daniel-kukiela](https://github.com/daniel-kukiela).

# Examples

## Screenshots of the message design of some commands:
serverinfo command<br>
![serverinfo command](https://cdn.discordapp.com/attachments/712041605753733152/722159106013528135/unknown.png)<br>
profile command<br>
![profile command](https://cdn.discordapp.com/attachments/680655385102909441/722188507564605520/unknown.png)<br>
command not found error<br>
![not found command error](https://cdn.discordapp.com/attachments/680655385102909441/722188706265563146/unknown.png)<br>
internal error on command<br>
![internal error](https://cdn.discordapp.com/attachments/680655448042504232/722189322174070896/unknown.png)<br>
## Here are some examples of the chatbot:

Question: Can you sing me a song?<br>
Answer: I'll post it.

Question: You are cute<br>
Answer: I'm so confused.

Question: <3<br>
Answer: <3

Question: i have to get an invite to grab some food from the fridge<br>
Answer: I'll go ahead and get it.

Question: What do you think about the human race?<br>
Answer: I think it's a bit of a dick.

Cute or? isn't it
