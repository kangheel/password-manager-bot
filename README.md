# Password Manager Bot
a Discord bot that works alongside [Password manager](https://github.com/kangheel/password-manager/tree/main) to be able your password manager from your phone or another device.

## Dependencies
- [Password manager](https://github.com/kangheel/password-manager/tree/main)
- python3
  - After intalling python3, run the following command for the dependencies 'pip install 'package-name'
    - discord.py
    - dotenv
    - pandas 

Functionalities of Password Manager Bot:
- /catalog
  - Prints the indices of your passwords
- /retrieve index
  - Prints the password corresponding to your index

## How to run your own fork of the bot
1. Prerequisites: python3, discord.py, dotenv, pandas
   - install python3 first then run the following command for the packages
   - pip install 'package-name'
3. Download the files and [Password manager](https://github.com/kangheel/password-manager/tree/main)
4. Make sure your files are within the same directory
   - i.e. 'parent_dir/password-manager/' and 'parent_dir/password-manager-bot/'
6. Generate your discord bot and token
7. Make a .env file in your directory with the following two lines
   - BOT_TOKEN = 'your-bot-token'
   - GUILD_NAME = 'your-guild-name'
8. Run 'bot.py' and the bot should be up and running!
