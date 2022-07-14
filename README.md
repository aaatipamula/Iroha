# Python Discord Bot Framework

This repo aims to provide a simple bot framework for easily starting up a discord.py project

## Project Info

**Author**: Aniketh Aatipamula <br>
**Project Start Date**: July 8, 2022 <br>
**Contributors**: N/A <br> 

**Project Origin**: This project started as a way to get future projects and or other projects started faster as it sets up a lot of the basic framework that one would need to make a discord.py bot. <br>

**Project Description**: The project uses a simple framework that simply sets up the bot for commands. The `embeds.py` file contains functions that create simple embeds and a help command. Parameters and the help command are easily configureable through the .json files. Scripts to host the bot on a docker container are also included in the /scripts folder. 

## Project Notes

**Module Dependencies**: This project requires that a handful of non-standard python modules be installed. <br>
This includes:
- discord.py
<br>

## Running This Project 

**Inital Setup** <br> 
Assuming you have [**git**](https://git-scm.com/) installed on your client, clone the repo by running the following command in your terminal:

```
git clone https://github.com/aaatipamula/discordpy-bot-framework
``` 

This will create a folder named `discordpy-bot-framework` in your working directory. Navigate into that directory in your terminal and run `python3 ./src/setup.py` This will ask you for a handful of items including a Discord channel in a server that you would not mind the bot dumping messages in, and the bot token. This will generate a data.json file that you can always edit to update any values that you may want to change <br>

**Channel Id and User Id** <br>
If you don't know how to get channel and user id's refer to [this](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) discord faq. <br>


**Bot Token** <br>
You can create a bot token by going to https://discord.com/developers/applications signing in, hitting `New Application` and typing in what you want the bot to be named. From there go to the `Bot` tab and hit `Add Bot` and hit `Yes`. If your token is displayed copy that and put it into the required field. If not you can reset your token and copy it in. The token only appears once before you cannot see it again so make sure to copy it down somewhere. <br><br>

**About Me** <br>
This should be a short and concise description of what your bot does. This can always be edited in the data.json file.

**Commands.json** <br>
Syntax for the json objects is as follows: 
```json
{
    "command-title":[
        "(*arg1*, *arg2*, *argx*...)",
        "Short-explination-of-command",
        "Explination of each argument" 
    ]
}
```

You may format each item in the key pair list how you would like but as an example I have my perffered format below:

```json
"dm":[
    "(*user*, *message*)",
    "This command DM's a specific user a message of your choice.", 
    "This command excepts two arguments, *user* and *message*.\n\n*user* can either be a mention of the user, or the users name, if they are already added to the dictionary.\n\n*message* has to be put in quotation marks if more than one word, emotes can be used if the bot is in the same server as the emotes origin."
],

```

If you command has no arguments and no need for explination of them you can format them as shown below: 

```json
"ping":[
    "",
    "Sends 'pong' along with the bot's ping in milliseconds.",
    "\u200b"
],
```
<br>

## Hosting the Project

**Hosting With Docker (Recommended)** <br>
Make sure you have Docker installed on your client, you can install it [here](https://docs.docker.com/get-docker/). <br><br>
If you're hosting this bot on a Linux machine, or even OSX, you can run the configuration file located in `./scripts/dockerstart.sh` to create the image and run it. Use the following command in the root directory of the project to do so:

```bash
sudo /bin/sh -c './scripts/dockerstart.sh foo'
```
*Note that foo can be replaced with any name you want for the docker image/container* <br><br>
If you're hosting this container on a Windows machine you can use the docker file located at `/scripts/Dockerfile` and you can use the same commands as in the `/scripts/dockerstart.sh` file without the *sudo* prefix. The commands are listed below: 
```bash
docker build -t bot -f ./scripts/Dockerfile . 
docker run -it --name bot -d bot
```

Finally you can start the bot up by running the following command (Dropping the *sudo* prefix for a Windows machine):

```bash
sudo docker exec -it -d bot python3 ./src/apcsp_bot.py
```
<br>

**Hosting Bare Metal (Without Container)**<br>
Although not recommended, you can host the bot without a container by simply running the python script in the background.<br>

This can be done in Linux/OSX with:
```bash
python3 ./src/apcsp_bot.py &

or 

nohup python3 ./src/apcsp_bot.py
``` 
<br>

This may also be acheived on a Windows machine by creating a Windows service, however I do not have experience with this and you will have to find a source to help you achieve this. Windows does however have [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) which allows you to host a Linux OS on your Windows machine.
