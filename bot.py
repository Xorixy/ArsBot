# bot.py
import os

import discord
from dotenv import load_dotenv

import random


async def roll_stress(num, modifier, botch, user, channel):
    message = ''
    try:
        num = int(num)
        if num < 1:
            await channel.send("Error: number of dice must be a positive integer")
            return
    except:
        await channel.send("Error: number of dice must be a positive integer")
        return
    try:
        modifier = int(modifier)
    except:
        await channel.send("Error: modifier must be an integer")
        return
    try:
        botch = int(botch)
        if botch < 1:
            await channel.send("Error: number of botch dice must be a positive integer")
            return
    except:
        await channel.send("Error: number of botch dice must be a positive integer")
        return
    botch_string = f'{botch} botch dice'
    if botch == 1:
        botch_string = f'1 botch die'
    if num == 1:
        message += f"{user} rolling 1 stress die with modifier {modifier} and {botch_string}\n"
    else:
        message += f"{user} rolling {num} stress dice with modifier {modifier} and {botch_string}\n"
    for _ in range(num):
        roll = random.randrange(10)
        if roll == 0:
            botches = 0
            for __ in range(botch):
                if random.randrange(10) == 0:
                    botches += 1
            if botches == 0:
                message += f"{user} rolled a stress die: 0 + {modifier} = {modifier} (0/{botch} botches)\n"
            else:
                message += f"{user} rolled a stress die: botched ({botches}/{botch} botches)\n"
        elif roll == 1:
            multiplier = 1
            n_explode = 0
            while(roll == 1):
                multiplier *= 2
                n_explode += 1
                roll = random.randrange(10) + 1
            message += f"{user} rolled a stress die: {roll}\\*{multiplier} + {modifier} = {roll*multiplier + modifier} ({n_explode} exploding dice)\n"
        else:
            message += f"{user} rolled a stress die: {roll} + {modifier} = {roll + modifier}\n"
    if len(message) > 2000:
        message = "Error: Message over character limit"
    await channel.send(message)

async def roll_normal(num, modifier, user, channel):
    message = ''
    try:
        num = int(num)
        if num < 1:
            await channel.send("Error: number of dice must be a positive integer")
            return
    except:
        await channel.send("Error: number of dice must be a positive integer")
        return
    try:
        modifier = int(modifier)
    except:
        await channel.send("Error: modifier must be an integer")
        return
    if num == 1:
        message += f"{user} rolling 1 normal die with modifier {modifier}\n"
    else:
        message += f"{user} rolling {num} normal dice with modifier {modifier}\n"
    for _ in range(num):
        roll = random.randrange(10) + 1
        message += f"{user} rolled a normal die: {roll} + {modifier} = {roll + modifier}\n"
    if len(message) > 2000:
        message = "Error: Message over character limit"
    await channel.send(message)

async def roll_botch(botch, user, channel):
    message = ''
    try:
        botch = int(botch)
        if botch < 1:
            await channel.send("Error: number of botch dice must be a positive integer")
            return
    except:
        await channel.send("Error: number of botch dice must be a positive integer")
        return
    if botch == 1:
        message += "{user} rolling 1 botch die\n"
    else:
        message += f"{user} rolling {botch} botch dice\n"
    botches = 0
    for __ in range(botch):
        if random.randrange(10) == 0:
            botches += 1
    if botches == 0:
        message += f"{user} did not botch (0/{botch} botches)\n"
    else:
        message += f"{user} botched ({botches}/{botch} botches)\n"
    if len(message) > 2000:
        message = "Error: Message over character limit"
    await channel.send(message)

async def parse_stress(parts, user, channel):
    num = 1
    modifier = None
    botch = None
    if len(parts) == 0:
        await roll_stress(1, 0, 1, user, channel)
        return
    message = "".join(parts)
    num_integers = 0
    for char in message:
        if char.isdigit():
            num_integers += 1
        else:
            break
    if num_integers != 0:
        try:
            num = int(message[0:num_integers])
        except:
            await channel.send("Something went wrong, could not parse stress roll")
            return
    message = message[num_integers:]
    while(modifier is None or botch is None):
        if len(message) == 0:
            break
        if message[0] == 'b':
            if botch is not None:
                break
            message = message[1:]
            botch_integers = 0
            for char in message:
                if char.isdigit():
                    botch_integers += 1
                else:
                    break
            if botch_integers != 0:
                try:
                    botch = int(message[0:botch_integers])
                except:
                    await channel.send("Something went wrong, could not parse stress roll")
                    return
            else:
                botch = 1
            message = message[botch_integers:]
        elif message[0] == '+' or message[0] == '-':
            if modifier is not None:
                break
            modifier_total = 0
            while len(message) > 0 and (message[0] == '+' or message[0] == '-'):
                modifier_integers = 0
                sign = message[0]
                message = message[1:]
                for char in message:
                    if char.isdigit():
                        modifier_integers += 1
                    else:
                        break
                if modifier_integers != 0:
                    try:
                        modifier_total += int(sign + message[0:modifier_integers])
                    except:
                        await channel.send("Something went wrong, could not parse stress roll")
                        return
                else:
                    modifier_total += 0
                message = message[modifier_integers:]
            modifier = modifier_total
        else:
            break
    if botch is None:
        botch = 1
    if modifier is None:
        modifier = 0
    await roll_stress(num, modifier, botch, user, channel)

async def parse_normal(parts, user, channel):
    num = 1
    modifier = None
    if len(parts) == 0:
        await roll_normal(1, 0, user, channel)
        return
    message = "".join(parts)
    num_integers = 0
    for char in message:
        if char.isdigit():
            num_integers += 1
        else:
            break
    if num_integers != 0:
        try:
            num = int(message[0:num_integers])
        except:
            await channel.send("Something went wrong, could not parse normal roll")
            return
    message = message[num_integers:]
    if len(message) != 0 and (message[0] == '+' or message[0] == '-'):
        modifier_total = 0
        while len(message) > 0 and (message[0] == '+' or message[0] == '-'):
            modifier_integers = 0
            sign = message[0]
            message = message[1:]
            for char in message:
                if char.isdigit():
                    modifier_integers += 1
                else:
                    break
            if modifier_integers != 0:
                try:
                    modifier_total += int(sign + message[0:modifier_integers])
                except:
                    await channel.send("Something went wrong, could not parse stress roll")
                    return
            else:
                modifier_total += 0
            message = message[modifier_integers:]
        modifier = modifier_total
    else:
        modifier = 0
    await roll_normal(num, modifier, user, channel)

async def parse_botch(parts, user, channel):
    botch = 1
    modifier = None
    if len(parts) == 0:
        await roll_botch(1, user, channel)
        return
    message = "".join(parts)
    botch_integers = 0
    for char in message:
        if char.isdigit():
            botch_integers += 1
        else:
            break
    if botch_integers != 0:
        try:
            botch = int(message[0:botch_integers])
        except:
            await channel.send("Something went wrong, could not parse normal roll")
            return
    await roll_botch(botch, user, channel)

async def parse_message(msg, user, channel):
    if (len(msg) == 0):
        return
    parts = str(msg).split()
    if parts[0] == "/s":
        await parse_stress(parts[1:], user, channel)
    elif parts[0] == "/r":
        await parse_normal(parts[1:], user, channel)
    elif parts[0] == "/b":
        await parse_botch(parts[1:], user, channel)







load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = message.channel
    user_message = str(message.content)
    await parse_message(user_message, username, channel)

client.run(TOKEN)
