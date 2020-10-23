![py_versions](https://img.shields.io/badge/python-3.7_3.8-blue)
# About
M3E5 is a Discord bot that has many features and commands. The goal is a bot that can do most things fast and stable and it may include a chat bot gpt2 and some other AI stuff if I find the time for it.<br>
I try my best to program this bot with focus on performance and scalability but I'm still learning.
If you have any questions or you want to see the bot in action join this [discord](https://discord.gg/GWJ6Jeg)

## Why the name?

I got inspired by the MEE6 but I don't wanted to build a clone of MEE6 instead I want to creat a special unique bot with tons of unique features.<br>
Like a real AI and some other features.

## What M3E5 loves and uses

- Docker/Docker-compose
- redis
- celery
- mysql
- discord.py

# Planned features

![Status](https://img.shields.io/badge/status-completed-green.svg)

For a list with all commands and there usage look at [commands](https://github.com/11Tuvork28/M3E5/blob/master/commands.md)

- Discord bot base
  - the standard prefix is - but it's changeable with -prefix arg 
  - basic Moderation commands
  - profile shows you your writer rank/xp and warnings
  - Music player has still some bugs DEPRECATED!
      - youtube/playlists
      - Soundcloud/playlists
  - Welcome image
  - custom Join and leave messages
  - welcome/leave channel 
  - Auto roles
  - tempmute
  - db connection
  - Logging messages to a database
  - set default role, admin, dev and mod role
  - reading/writing to database
  - loading/unloading/reloading cogs is now working if you have the dev role
  - levelsystem(text based)
  - basic permission system
  - when the bot joins a server the database is automatically initialized
  - On server join the owner gets a message with all setup commands that need to be executed
  - celery
  - reaction roles


![Status](https://img.shields.io/badge/status-in_progress-red.svg)

- Discord features
  - custom help command
  - tempban
  - anti spam
  - lock/unlock a specific channel for specific roles 
  - Custom commands
  - Bunch of standard commands like welcome messages and funny commands like hug @name
  - Auto tasks
  - Alerts for various services like Twitch and Reddit
  - Music player
    - Spotify
  - custom messaging design 
  - Recording meetings ( Voice recording to an mp3 file)
  - Custom voice channels 
  - poke admins/moderators via Telegram or Email if they aren't online
  - Ticket/Support system maybe 
  - Advanced permission system, that uses groups of accepted roles and banned roles per command
  - unittests
  - Web interface but I will open a seperate repository for that
    - basic api

 
# Critical bugs

  - You will get IP banned from youtube if you use the music cog, therefore its deprecated for now and shouldn't be used
  - Not well documented
  - The antispam system has some bugs
  
# Install instructions 
 
 You need to install a few things and I assume that you're using linux:
 - Docker
 - Docker-compose
 - mysql-server
 
 ### First things first:<br>
 - I assume that you're using Linux<br>
 - clone the repo and cd into the cloned repo
 - Install, for docker [goto](https://docs.docker.com/get-docker/) for docker-compose [goto](https://docs.docker.com/compose/install/).

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
-That's it, exit the sql server<br>
```exit ```<br>
### Setup the config file
- Change the Somepassword argument in the docker-compose file to your choice it should be very long
- Change the flowering things in base_folder/config
    - Now enter your bot token and all other things.
    - Note that you only need to change "yourpassword" value for the brocker/backend address to the value you set in your docker compose file
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
