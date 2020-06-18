[![made-with](https://img.shields.io/badge/Made%20with-Python_3.6_or_higher-1f425f.svg)](https://www.python.org/) [![made-with](https://img.shields.io/badge/Made%20with-Discord.py_1.3.3-1f425f.svg)](https://discordpy.readthedocs.io/en/latest/) 

# Discord-Bot [![Version](https://img.shields.io/badge/Version-1.0-yellow.svg)]()
by [ArthurBoddaert](https://github.com/ArthurBoddaert) and [delepoulle](https://github.com/delepoulle)

This project is a discord bot created in order to manage discord server's users
This bot includes several point
- Creation of lists of users and roles
- Publication of surveys
- Publication of a message to a given population
- Distribution discord roles to a large amount of user

## Installation

You can find informations about virtual environment [here](https://docs.python.org/3/library/venv.html)

1. To start, you have to clone the project and go into the folder
```
git clone https://github.com/ArthurBoddaert/Discord-Bot
cd Discord-Bot
```

2. In the previously cloned project, you can create a virtual environment
```
python3 -m venv ./my_virtual_environment
```

3. Then you can activate it
```
source ./my_virtual_environment/bin/activate
```

4. Now that the virtual environment is activated, you can install the dependencies
```
pip install discord.py==1.3.3
pip install pandas==1.0.4
pip install matplotlib==3.2.1
```

5. Open the **config.json** file and fill it with your informations
```json
{
	"prefix": "YOUR BOT PREFIX",
	"token": "YOUR DISCORD TOKEN",
}
```
The prefix is the succession of characters which will be used to call the commands
The token is your discord bot token, which can be found on https://discord.com/developers after registering an app

6. Run **bot.py**
```
python bot.py
```

## Features

The examples given will consider the bot token is '**--**'

This bot offers the possibility to use the following commands:

#### rolelist command

The 'rolelist' creates a list of the existing roles on a server.

Example: 
- --rolelist

#### list command

The 'list' command creates a list of all users who have a role on a server
you can add a few arguments in order to change the result of this command
- Followed by a role name, the command will display every user with the specified role
- Followed by a status, the command will display every user with the specified status. The statutes are 'online', 'offline', 'idle' and 'dnd' (dnd=do not disturb)
- Followed by the name of a voice channel, the command will display every user in the specified channel
- Followed by '-o' and a file name, the bot will upload a file containing the list of the users on the discord server with their discord IDs and their roles on the server this file is also stored in the 'files/list-o/' directory

Examples:
- --list
- --list role
- --list online
- --list online role
- --list role member
- --list online offline
- --list my_voice_channel
- --list -o my_file_name

#### dm command

The 'dm' command followed by a role name and a message sends the message to every user who has the specified role. The message can also have an attachment

Example:
	--dm Members Hello world!

#### grant command

The 'grant' command grants roles depending on the attached file. The previously mentioned file has to follow the format of the 'list -o' command.
With the '-r' or '-reset' argument, the bot will remove every role from every user and then it will grant the fiven roles.

#### sondage command

The 'sondage' command sends a survey with the specified question and answers.
This command has a limit of 26 answers.
By using the command 'sondageUnique', you can get the same kind of survey, except the fact that only one answer can be given per user.
The argument '-d' followed by a number 'n' will make this survey last 'n' seconds.
Using the 'sondage' keyword also gives you the id of the survey.

Examples:
- --sondage "my question" "first answer" "second answer" "third answer"  
- --sondageUnique "my question" "first answer" "second answer" "third answer"  
- --sondage -d60 "my question" "first answer" "second answer" "third answer"  
- --sondageUnique -d60 "my question" "first answer" "second answer" "third answer"  

You can get a graph which represents the results of a survey thanks to the command 'result' followed by a survey id. A temporary survey will also upload a graph when it ends.

#### getlogs command

The 'getlogs' commands send you the logs of the bot, which contains the list of commands called when the bot was online

Both the 'grant' command and the 'getlogs' command can only be called by administrators
