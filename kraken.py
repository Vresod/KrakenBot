import discord
import random
import os
import json
from discord.ext import commands
import asyncio

##################
####  TOKEN   ####
####  LOADING ####
##################
with open("tokenfile","r") as tokenfile:
    TOKEN = tokenfile.read()

##################
####  GENERIC ####
####  LOADING ####
##################
client = commands.Bot(command_prefix="k!")
client.remove_command('help')
with open("help.json","r") as helpfile:
    jsonhelp = json.loads(helpfile.read())
empty_string = " "
help_embed = discord.Embed(title="Help")
help_message_list = []
for category in jsonhelp:
    field_text = ""
    for command in jsonhelp[category]:
        syntax = jsonhelp[category][command]["syntax"]
        usage = jsonhelp[category][command]["usage"]
        field_text += f"**{command}**: k!{command} {empty_string.join(syntax)}\n*{usage}*\n"
    help_message_list.append(field_text)
    help_embed.add_field(name=category,value=help_message_list[len(help_message_list) - 1])

#################
####  EVENT  ####
#################

@client.event
async def on_ready():
    print("The Kraken has awaken")
    game = discord.Game("in the ocean")
    await client.change_presence(status=discord.Status.online, activity=game)



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
    emojis = [u"\U0001F44D", u"\U0001F937", u"\U0001F44E"]
    for emoji in emojis:
        await msg.add_reaction(emoji)

@client.command()
async def pfp(ctx,user_for_avatar: str = None):
    avatar_user = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
    pfp_url = str(avatar_user.avatar_url)
    embed = discord.Embed(title=avatar_user.name)
    embed.set_image(url=pfp_url)
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    await ctx.send(embed=help_embed)

@client.command()
async def git(ctx):
    # this command shows all the git info
    # needed
    git_embed = discord.Embed(
        title="Git Repository",
        description="https://github.com/AVCADO/KrakenBot"
    )
    await ctx.send(embed=git_embed)


@client.command()
async def disableDM(ctx):
    warn_embed = discord.Embed(
        title="WARNING!",
        description="Kraken will NOW STOP DMing everyone who joins this guild"
    )
    await ctx.send(embed=warn_embed)
    os.system("bash disableDM.sh") # run a shell script
    
@client.command()
async def enableDM(ctx):
    await ctx.send("....you can't re-enable something, try `k!disableDM`")
    return


###########
# RUN BOT #
###########
client.run(TOKEN, bot=True)
