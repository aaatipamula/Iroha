![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

# Iroha

A discord bot that searches for anime.

Made using the [discord.py](https://discordpy.readthedocs.io/en/stable/) framework, and the [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs/)

# About

I use Discord often and occasionally I like to pull up information about an anime to display, I wrote this bot to make finding and displaying info on anime accessible right from discord. 

The bot uses the [AniList API](https://anilist.gitbook.io/anilist-apiv2-docs/) as the other APIs I found didn't give me the query results I was looking for. I would have use the MyAnimeList API however because firstly it required an Oauth2.0 flow that I felt was uncessary, and secondly because the API is in Beta I decided against using it.

## Commands

This bot is currently under development but here are a few of the commands:

- search: searches for anime given a query string, optionally you can specify what type of media you are looking for
- seasonal: sends the top seasonal anime for a given season and year. It defaults to the current season and year and 3 results displayed

# Deployment

## Docker

The project can be deployed by navigating to the root folder of the project and running the `./src/setup.py` file to generate the `.env` file. 

It can also be generated manually using the following format:
```sh
TOKEN="token"
DUMP_CHANNEL=123456
COMMAND_PREFIX="command_prefix"
ABOUT_ME="about_me"
```

From there the Docker Image can be created and run by running:
```bash
./scripts/dockerstart.sh iroha
```

Alternatively you can run the two following commands manually: 
```bash
sudo docker build -t iroha -f ./scripts/Dockerfile .
sudo docker run -it --name iroha -d $1
```

