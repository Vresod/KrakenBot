import discord
import random
import os
import json
from asyncio import sleep as asyncsleep
from discord.ext import commands

##################
####  TOKEN   ####
####  LOADING ####
##################
with open("tokenfile", "r") as tokenfile:
    TOKEN = tokenfile.read()

##################
####  GENERIC ####
####  LOADING ####
##################
client = commands.Bot(command_prefix="k!")
client.remove_command('help')
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

#################
####  EVENT  ####
#################


@client.event
async def on_ready():
    print("The Kraken has awaken")
    game = discord.Game("in the ocean")
    await client.change_presence(status=discord.Status.online, activity=game)
    print(
        f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")


DMsEnabled = True


@client.event
async def on_member_join(member):
    if(DMsEnabled == False):
        return
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
async def poll(ctx, *criterion):
    embed = discord.Embed(
        title="Poll",
        description=f"{empty_string.join(criterion)}"
    )
    msg = await ctx.send(embed=embed)
    emojis = [u"\U0001F44D", u"\U0001F937", u"\U0001F44E"]
    for emoji in emojis:
        await msg.add_reaction(emoji)


@client.command()
async def pfp(ctx, user_for_avatar: str = None):
    avatar_user = ctx.author if len(
        ctx.message.mentions) == 0 else ctx.message.mentions[0]
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
    DMsEnabled = False


@client.command()
async def enableDM(ctx):
    warn_embed = discord.Embed(
        title="WARNING!",
        description="Kraken will NOW DM everyone who joins this guild"
    )
    await ctx.send(embed=warn_embed)
    DMsEnabled = True

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

@client.command()
async def echo(ctx,*text):
    await ctx.send(f"{empty_string.join(text)}")
    await ctx.message.add_reaction(u"\U00002705")
    await asyncsleep(3)
    await ctx.message.delete()

###########
# RUN BOT #
###########
client.run(TOKEN, bot=True)
