# List of all commands and there usage

Permission levels
|  level  | description | role requried |
|:-------------|:----|:----|
| member| normal member can only use user commands| default |
| dev | can use some dev commands + member permissions | dev|
| mod | can use moderation commands + dev permissions | mod|
| admin | can use nearly every command + mod permissions | admin|
| guild owner | can use every command except internal bot commands + admin permission | no role needed |
| bot owner | can only use bot internal commands |no role needed |

## Customization commads
Permission level admin or higher required 
|      Command  |description|usage|
|:-------------|:----|:----|
| prefix   | sets the prefix |prefix - |
| set_default |sets default role | set_default @role |
| set_dev |sets dev rule  |set_dev @role |
| set_mod | sets mod rule  |set_mod @role|
| set_admin|sets admin rule  |set_admin @role|
| set_leave|sets the leave channel  |set_leave channel id |
| set_welcome| sets the welcome channel s |et_welcom channel id |
| set_cmd  |sets the command channel where the bot logs commands  |set_cmd channel id |
| set_lvl | sets the leave channel  |set_lvl channel id |
| imgwelcome toggle | turns the img welcome on and off | imgwelcome toggle |
| imgwelcome text | the welcome text that the use sees on join | imgwelcome text  |
| imgwelcome img | the image that should be used | imgwelcome img |
| imgwelcome test | test the img welcome on you | imgwelcome test  |
| levelsystem toggle | turns the  levelsystem on and off | levelsystem toggle |
| add_reaction | Adds a reaction role to any message that the command author wrote| message id channel id then follow the instructions|

## Moderation commands
Permission level mod or higher required 
|      Command   |description|usage|
|:-------------|:----|:----|
| clear |clears a givien amount of messages |clear amount |
| infractions |shows how many infractions a member has |infractions @member|
| kick| kicks a given member| kick @member reason|
| mute | mutes a member | mute @member reason |
| slowmode|enables/disables slowmode with custom delay | slowmode seconds 0-120 |
| warn| warns a member, adds 1 warning| warn @member |
| ban | bans a given member| ban @member reason|
| unban | unbans a member | unban @member reason|
| unmute|  unmutes a member| unmute @member |
| clear_infractions | clear all infractions of a member | clear_infractions @member|
| give_role| gives a member a role| role  @role @member|

## Dev commands
Permission level dev or higher required 
|      Command   |description|usage|
|:-------------|:----|:----|
| builddb | initializes the db use with caution | builddb |
| roles_in_db | rites all roles in the db | roles_in_db |
| show_roles | shows all roles that are in the db, can be used as a test | how_roles |

Permission level bot owner required 

|      Command   |description|usage|
|:-------------|:----|:----|
| load | loads a given module | load name or folder.name oder folder.subfolder.name e.g load base.dev oder load imgwelcome | 
| reload | reloads a given module| reload  name or folder.name oder folder.subfolder.name |
|unload | unloads a given module | unload name or folder.name oder folder.subfolder.name |

## User commnads
Permission level member or higher required
more commands will follow
|      Command   |description|usage|
|:-------------|:----|:----|
| profile | shows the profile of the member like text xp etc| profile |
| roleinfo |Shows the color of role and how many members's the role has and some other things | roleinfo @role |
| leaderboard | Shows the leaderboard of the server sorted by level dsc | leaderboard |
| leaderboard | Shows the leaderboard of the server sorted by level dsc | leaderboard |
| server_info | Shows info about the current guild e.g created at etc | server_info |

## Music
Permission level member or higher required
|      Command   |description|usage|
|:-------------|:----|:----|
| join | the bot joins your voice channel |join |
| leave | the bot leaves your voice channel | leave |
| stop | the bot leaves your voice channel | stop |
| play | plays a song from a given url | play url |
| nowplaying | shows the playlist, the current song, if loop is enabled and current index and len of the play list | nowplaying |
| queue | shows the queue | queue| 
| pause | pauses the bot  | pause |
| skip | skips the current song | skip |
| volume | changes the volume of the bot | volume 50 or 80 or so |
| jumpqueue | moves a given song to a given position | jumpqueue song index future index e.g. jumpqueue 2 5|

