"""
This is basically kraken.py but without DM'ing people once they join
It's handy for when it gets annoying.
"""

# Imports
import discord
import random
import os
import json
from discord.ext import commands


# token loading
# load the token
with open("tokenfile","r") as tokenfile:
    TOKEN = tokenfile.read()


# Loading all the bots information
# this includes the help file (help.json) and
# the prefix of the bot
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


# Events
# Usually discord bots handle certain events
# when certain things happen
# such as a member joining, or a member leaving.

# here we are ONLY going to put the on_ready
# which is basically when the bot is ready

@client.event
async def on_ready():
    print("The Kraken has awaken, and will not disturb")
    game = discord.Game("without interrupting you")
    await client.change_presence(status=discord.Status.online, activity=game)


# Commands
# what gets run in the discord chat channels are basically these things

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
async def enableDM(ctx):
    warn_embed = discord.Embed(
        title="WARNING!",
        description="Kraken will NOW DM everyone who joins this guild"
    )
    await ctx.send(embed=warn_embed)
    os.system("bash enableDM.sh") # run a shell script
    
@client.command()
async def disableDM(ctx):
    await ctx.send("....you can't re-disable something, try `k!enableDM`")



# here we can run the bot using our token
client.run(TOKEN, bot=True)