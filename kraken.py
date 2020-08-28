import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

################
####  ENV   ####
####  VARS  ####
################
load_dotenv()
TOKEN = os.getenv('TOKEN_AUTH')

client = commands.Bot(command_prefix="k!")
#################
####  EVENT  ####
#################

@client.event
async def on_ready():
    print("The Kraken has awaken")
    game = discord.Game("in the ocean")
    await client.change_presence(status=discord.Status.idle, activity=game)



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I am the kraken.'
    )


#####################
####  COMAMANDS  ####
#####################

@client.command()
async def kraken(ctx):
    await ctx.send("I am the one, the only kraken")


@client.command()
async def rollDice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@client.command()
async def poll(ctx, criterion):
    embed = discord.Embed(
            title="Poll",
            description=f"{criterion}"
        )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(u"\U0001F44D")
    await msg.add_reaction(u"\U0001F937")
    await msg.add_reaction(u"\U0001F44E")

@client.command()
async def pfp(ctx):
    await ctx.send(file=discord.File('kraken.png'))

@client.command()
async def disableDM(ctx):
    os.system("python krakenNoDM.py")



client.run(TOKEN, bot=True)
