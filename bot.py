import os

import discord
from dotenv import load_dotenv
from discord import app_commands

# import requests
# from bs4 import BeautifulSoup
import pandas as pd
# import jpype
import subprocess

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD_NAME')
PREFIX = "-"
PREFIXES = ""

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    await tree.sync(guild=discord.Object(id=guild.id))
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # await client.change_presence(activity=discord.Game("Journey of the Prairie King"))

@tree.command(
    name="retrieve",
    description="retrieves password from the password manager",
    guild=discord.Object(id=1028609871937032202)
)
async def retrieve(interaction, index : str):
    args = "1\n" + index + "\n4\n"
    read, write = os.pipe()
    os.write(write, args.encode())
    os.close(write)

    proc = subprocess.Popen(['java','-jar', '../password-manager/src/manager.jar'], stdin=read, stdout=subprocess.PIPE)

    while True:
        line = proc.stdout.readline()
        if line == b'Enter the index or the name of the website you wish to retrieve the password of: \r\n':
            pw = proc.stdout.readline()
            await interaction.response.send_message(pw.decode(), delete_after=30)
            return
        if not line:
            break
    return

@tree.command(
    name="catalog",
    description="prints the available passwords from the password manager",
    guild=discord.Object(id=1028609871937032202)
)
async def catalog(interaction):
    pws = pd.read_csv('../password-manager/src/list.txt', dtype = str, sep = ' ')
    column = pws.columns[0]
    pws = pws.iloc[:, 0].tolist()
    pws.insert(0, column)
    
    rets = []
    i = 1
    curret = ""
    for website in pws:
        cur = str(i) + ': ' + website
        curret += '`' + fill_message(cur,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') + '`,'
        i += 1
        if i-1 % 4 == 0:
            curret = curret[:len(curret)-1]
            curret += "\n"
        if len(curret) > 1950:
            rets.append(curret)
            curret = ""
    # print(rets)
    await interaction.response.send_message("Here's a list of passwords: \n")
    for ret in rets:
        await interaction.followup.send(ret)
    return

def fill_message(value, message):
    ret = value
    for i in range(len(message)-len(value)):
        ret += " "
    return ret

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(message.content)
    if not message.content.startswith(PREFIX):
        return
    command = message.content[1:]
    
    if command.lower().startswith("pw"):
        args = command[len("pw "):]
        args += " 4\n"
        args = args.replace(" ","\n")
        read, write = os.pipe()
        os.write(write, args.encode())
        os.close(write)

        proc = subprocess.Popen(['java','-jar', '../password-manager/src/manager.jar'], stdin=read, stdout=subprocess.PIPE)
        
        # subprocess.call(['java', '-jar', '../password-manager/src/password_manager.jar'], stdin=read)
        while True:
            line = proc.stdout.readline()
            if line == b'Enter the index or the name of the website you wish to retrieve the password of: \r\n':
                pw = proc.stdout.readline()
                await message.channel.send(pw.decode(), delete_after=30)
                return
            if not line:
                break
        return
    elif command.lower().startswith("r"):
        pws = pd.read_csv('../password-manager/src/list.txt', dtype = str, sep = ' ')
        column = pws.columns[0]
        pws = pws.iloc[:, 0].tolist()
        pws.insert(0, column)
        
        rets = []
        i = 1
        curret = ""
        for website in pws:
            cur = str(i) + ': ' + website
            curret += '`' + fill_message(cur,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') + '`,'
            i += 1
            if i-1 % 4 == 0:
                curret = curret[:len(curret)-1]
                curret += "\n"
            if len(curret) > 1950:
                rets.append(curret)
                curret = ""
        # print(rets)
        await message.channel.send("Here's a list of passwords: \n")
        for ret in rets:
            await message.channel.send(ret)
        return
    else:
        await message.channel.send("Unknown command: " + command)

client.run(TOKEN)