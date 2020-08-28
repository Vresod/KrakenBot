import discord
import random
import os
from discord.ext import commands
import asyncio

##################
####  TOKEN   ####
####  LOADING ####
##################
with open("tokenfile","r") as tokenfile:
    TOKEN = tokenfile.read()

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
async def pfp(ctx,user_for_avatar: str = None):
    avatar_user = ctx.author if user_for_avatar == None else ctx.message.mentions[0]
    pfp_url = str(avatar_user.avatar_url)
    embed = discord.Embed(title=avatar_user.name)
    embed.set_image(url=pfp_url)
    await ctx.send(embed=embed)

@client.command()
async def disableDM(ctx):
    os.system("python krakenNoDM.py")



client.run(TOKEN, bot=True)
