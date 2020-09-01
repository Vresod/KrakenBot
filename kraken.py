#!/usr/bin/env python3

# Imports used for kraken bot to work properly
import discord
import random
import os
import json
from asyncio import sleep as asyncsleep
from discord.ext import commands
from subprocess import check_output
from sys import argv as cliargs
from datetime import datetime

t0 = datetime.now()

prefix = ""
for parameter in cliargs:
    if parameter == "-p":
        prefix = cliargs[cliargs.index(parameter) + 1]
    elif parameter.startswith("--prefix"):
        x = parameter.split("=")
        prefix = x[1]
prefix = "k!" if prefix == "" else prefix 
print(f"prefix:{prefix}")

##################
####  TOKEN   ####
####  LOADING ####
##################

# Here we just load the token
with open("tokenfile", "r") as tokenfile:
    TOKEN = tokenfile.read()

##################
####  GENERIC ####
####  LOADING ####
##################

# Set prefix
client = commands.Bot(command_prefix=prefix)

# Remove help command
client.remove_command('help')

# Help command specification
# (declaring everything needed for the help command)
with open("help.json", "r") as helpfile:
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
    help_embed.add_field(
        name=category, value=help_message_list[len(help_message_list) - 1])


# Changelog code.
# this little snippet gets the 5 latest commits of this repo
# and puts them in an embed
out = check_output("git log -5 --pretty=%s|%h".split(" "))
log = out.decode("utf-8").split("\n")
log.remove('')
logs = []
for cmessage in log:
    logs.append(cmessage.split("|"))
logmsg = ""
for commitpair in logs:
    logmsg += f"[{commitpair[0]}](https://github.com/AVCADO/KrakenBot/commit/{commitpair[1]})\n"

embed_change = discord.Embed(
    title="Changelog",
    description=logmsg
)

#################
####  EVENT  ####
#################


# This event triggers when the bot is ready
# It sends a message to the console saying that the bot has awoken
# and also sends the invite link
@client.event
async def on_ready():
    print("The Kraken has awaken")
    game = discord.Game("in the ocean")
    await client.change_presence(status=discord.Status.online, activity=game)
    print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")

# variable for if DMs are enabled or not
DMsEnabled = True


# This event checks whether or not
# DMsEnabled is true or false
# if it is, then it can dm everyone who joins it
# if it isn't then it wont do anything
@client.event
async def on_member_join(member):
    if DMsEnabled == False:
        return
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I am the kraken.'
    )


#####################
####  COMAMANDS  ####
#####################

# like a ping command, but for kraken, and is also kraken
# based
@client.command()
async def kraken(ctx):
    await ctx.send("I am the one, the only kraken")

# this command is basically making you able to roll some die
# example:
# k!rollDice 3 3
@client.command()
async def rollDice(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# Want to make a poll?
# Well now you can.
# Here's an example:
# k!poll do you want soup?
@client.command()
async def poll(ctx, *criterion):
    embed = discord.Embed(
        title="Poll",
        description=f"{empty_string.join(criterion)}"
    )
    msg = await ctx.send(embed=embed)
    emojis = [u"\U0001F44D", u"\U0001F937", u"\U0001F44E"]
    for emoji in emojis:
        await msg.add_reaction(emoji)

# profile picture command
@client.command()
async def pfp(ctx, *user_for_avatar):
    avatar_users = []
    pfp_urls = []
    for user in ctx.message.mentions:
        avatar_users.append(user)
    #avatar_user = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
    avatar_users = [ctx.author] if len(avatar_users) == 0 else avatar_users
    for user in avatar_users:
        pfp_urls.append(str(user.avatar_url_as(format="png")))
    for url in pfp_urls:
        embed = discord.Embed(title=avatar_users[pfp_urls.index(url)].name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

# help command
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



# disables dms
@client.command()
async def disableDM(ctx):
    if DMsEnabled == False: 
        return
    else:
        warn_embed = discord.Embed(
            title="WARNING!",
            description="Kraken will NOW STOP DMing everyone who joins this guild"
        )
        await ctx.send(embed=warn_embed)    


# enables dms
@client.command()
async def enableDM(ctx):
    if DMsEnabled == True:
        return
    else:
        warn_embed = discord.Embed(
            title="WARNING!",
            description="Kraken will NOW DM everyone who joins this guild"
        )
        await ctx.send(embed=warn_embed)

# kicks the user specified and also dm's them
@client.command()
async def kick(ctx,user,reason = None):
    successEmbed = discord.Embed(title="Kick",description=f"kicked {ctx.message.mentions[0].mention}\nServer:{ctx.guild.name}\nReason: {reason}")
    failureEmbed = discord.Embed(title="Failed to kick",description="You do not have the correct permissions to kick.")
    if(not ctx.message.author.permissions_in(ctx.channel).kick_members):
        await ctx.send(embed=failureEmbed)
        return
    await ctx.message.mentions[0].create_dm()
    await ctx.message.mentions[0].dm_channel.send(embed=successEmbed)
    await ctx.message.mentions[0].kick(reason=f"{reason}")
    await ctx.send(embed=successEmbed)


# bans the user and also dm's them
@client.command()
async def ban(ctx,user,reason = None):
    successEmbed = discord.Embed(title="Ban",description=f"banned {ctx.message.mentions[0].mention}\nServer: {ctx.guild.name}\nReason: {reason}")
    failureEmbed = discord.Embed(title="Failed to ban",description="You do not have the correct permissions to ban.")
    if(not ctx.message.author.permissions_in(ctx.channel).ban_members):
        await ctx.send(embed=failureEmbed)
        return
    await ctx.message.mentions[0].create_dm()
    await ctx.message.mentions[0].dm_channel.send(embed=successEmbed)
    await ctx.message.mentions[0].ban(reason=f"{reason}")
    await ctx.send(embed=successEmbed)

# echos what the user said
# deletes the command after 3 seconds
@client.command()
async def echo(ctx,*text):
    await ctx.send(f"{empty_string.join(text)}")
    await ctx.message.add_reaction(u"\U00002705")
    await asyncsleep(3)
    await ctx.message.delete()


# the changelog command.
@client.command()
async def changelog(ctx, num=5):
    out = check_output(f"git log -{num} --pretty=%s|%h".split(" "))
    log = out.decode("utf-8").split("\n")
    log.remove('')
    logs = []
    for cmessage in log:
        logs.append(cmessage.split("|"))
    logmsg = ""
    for commitpair in logs:
        logmsg += f"[{commitpair[0]}](https://github.com/AVCADO/KrakenBot/commit/{commitpair[1]})\n"
    if len(logmsg) > 2048:
        logmsg = "message too long; go to [https://github.com/AVCADO/KrakenBot/commits/master](https://github.com/AVCADO/KrakenBot/commits/master)"
    embed_change = discord.Embed(
        title="Changelog",
        description=logmsg
    )
    await ctx.send(embed=embed_change)


# uptime command
@client.command()
async def uptime(ctx):
    uptim = datetime.now() - t0
    str_uptim = str(uptim).split(".")
    time_embed = discord.Embed(
        title="Uptime",
        description=f"**{str_uptim[0]}**"
    )
    await ctx.send(embed=time_embed)

# converts text from latin alphabet to emoji
@client.command()
async def emojify(ctx,*text):
    str_text = " ".join(text).lower()
    emojified_text = ""
    for letter in str_text:
        if not letter in list("abcdefghijklmnopqrstuvwxyz"):
            emojified_text += f"{letter}"
            continue
        emojified_text += f":regional_indicator_{letter.lower()}:"
    await ctx.send(emojified_text)

# inserts clap emojis between every word
@client.command()
async def clapify(ctx, *text):
    if len(text) == 1:
        str_text = "".join(text)
        str_text = f"{str_text} :clap:"
    else:
        str_text = " :clap: ".join(text)
    await ctx.send(str_text)

# converts normal text to UPPERCASE TEXT
@client.command()
async def uppercaseify(ctx, *text):
    await ctx.send("".join(text).upper())

###########
# RUN BOT #
###########

# finally, we can run the bot.
client.run(TOKEN, bot=True)
