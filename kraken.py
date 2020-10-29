#!/usr/bin/env python3

# Imports used for kraken bot to work properly

# hello im torvalds and i approve this message
import discord
import random
import os
import json
import praw
from asyncio import sleep as asyncsleep
from discord.ext import commands
from subprocess import check_output
from sys import argv as cliargs
from datetime import datetime

### Variables

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

with open("disable_DM_checks.json", "r+") as dm_checks:
	dmJSON = json.loads(dm_checks.read())
dmembed = discord.Embed(title="DM on join")

# praw
reddit = praw.Reddit("bot")

#for foo in dmJSON:
#	fieldEnabled = ""
#	print(foo)
#	for checks in dmJSON[foo]:
#		print(checks)
#		# i have a solution
#		dmSW = dmJSON
#		if dmJSON[foo][checks] == 1:
#			print("fuck you")
#		elif dmJSON[foo][checks] == 0:
#			print("FUCK YOU")
#	fieldEnabled += f"**{dmSW}\n"
#	list_dm.append(fieldEnabled)
#	dmembed.add_field(
#		name="test", value=dmSW)

# Changelog code.
# this little snippet gets the 5 latest commits of this repo
# and puts them in an embed
out = check_output("git log -25 --pretty=%s|%h".split(" "))
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

with open("interjection","r") as interjection_raw: interjection = interjection_raw.read()
with open("LICENSE","r") as license_raw: license = license_raw.read()

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
	for guild in client.guilds:
		print(f"In guild: {guild.name}") 
	
# variable for if DMs are enabled or not
DMsEnabled = True


# This event checks whether or not
# DMsEnabled is true or false
# if it is, then it can dm everyone who joins it
# if it isn't then it wont do anything
@client.event
async def on_member_join(member):
	if str(member.guild.id) in dmJSON: # detect if theres a value set for
		if not dmJSON[str(member.guild.id)]: # if its set to not DM members of the guild
			return
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, I am the kraken.'
	)

@client.event
async def on_guild_join(guild):
	print(f"Joined guild: {guild.name}")
# on message event

# save me from this nightmare
# please help me
@client.event
async def on_message(message):
	if "carl bot is better" in message.content:
		msg = await message.channel.send("carl bot is ***bloat***")
		await msg.add_reaction(u"\U0001F44D")
	await client.process_commands(message)

#####################
####  COMAMANDS  ####
#####################

# like a ping command, but for kraken, and is also kraken
# based
@client.command()
async def kraken(ctx):
	krakenMsg = "I am the one, the only kraken" if client.user.id == 748960748935446588 else "Im fake kraken"
	await ctx.send(krakenMsg)

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
	if ctx.message.mention_everyone:
		for user in ctx.guild.members:
			avatar_users.append(user)
	else:
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
	dmJSON[str(ctx.guild.id)] = False
	prefixesfile = open("disable_DM_checks.json","w")
	prefixesfile.write(json.dumps(dmJSON))
	prefixesfile.close()
	warn_embed = discord.Embed(
		title="WARNING!",
		description="Kraken will NOW STOP DMing everyone who joins this guild"
	)
	await ctx.send(embed=warn_embed)	


# enables dms
@client.command()
async def enableDM(ctx):
	dmJSON[str(ctx.guild.id)] = True
	prefixesfile = open("disable_DM_checks.json","w")
	prefixesfile.write(json.dumps(dmJSON))
	prefixesfile.close()
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
	logmsg = ""
	global logs
	logs = logs[:num]
	for commitpair in logs:
		logmsg += f"[{commitpair[0]}](https://github.com/AVCADO/KrakenBot/commit/{commitpair[1]})\n"
	if len(logmsg) > 2048:
		logmsg = "message too long; go to [https://github.com/AVCADO/KrakenBot/commits/master](https://github.com/AVCADO/KrakenBot/commits/master)" # replace with upstream url
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
	await ctx.send(" ".join(text).upper())

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
# reddit stuff
@client.command()
async def redditbrowse(ctx, sub, limit: int = 5, sublist = "hot"): # a lot of this code was ripped straight from Vresod/reddit-bot
	subreddit = reddit.subreddit(sub)
	number = 1
	if sublist == "hot":
		listing = subreddit.hot
	elif sublist == "top":
		listing = subreddit.top
	elif sublist == "new":
		listing = subreddit.new
	elif sublist == "random":
		listing = subreddit.random_rising
	elif sublist == "rising":
		listing = subreddit.rising
	elif sublist == "controversial":
		listing = subreddit.controversial
	stickiedposts = 0
	for stickytest in listing(limit=2):
		if(stickytest.stickied):
			stickiedposts += 1
	for submission in listing(limit=limit + stickiedposts):
		if(submission.stickied):
			continue
		if submission.is_self:
			if(len(submission.selftext) > 2048): # dealing with the limit on embedded text
				content = submission.selftext[:2045] + "..."
			else:
				content = submission.selftext
		else:
			try:
				is_gallery = submission.is_gallery
			except:
				is_gallery = False
			if not is_gallery:
				content = submission.url
			else:
				content = "Gallery posts are currently not supported. Use the above link to view the post on reddit."
		if submission.over_18 and not ctx.channel.is_nsfw():
			await ctx.send("NSFW post and non-nsfw channel. try again in nsfw channel")
			continue
		else:
			if len(submission.title) > 256:
				san_title = submission.title[:253] + "..."
			else:
				san_title = submission.title
			embed = discord.Embed(
					title=san_title,
					url=submission.shortlink
			)
			embed.set_footer(text=f"posted by u/{submission.author}")
			if submission.is_self or is_gallery:
				embed.description = content
			else:
				embed.set_image(url=content)
		await ctx.send(f"{ordinal(number)} {sublist} post from r/{submission.subreddit}:",embed=embed)
		number += 1

@client.command()
async def addemoji(ctx,*emojiname):
	failureEmbed = discord.Embed(title="Mission Failed",description="We\'ll get em\' next time.")
	if(not ctx.message.author.permissions_in(ctx.channel).manage_emojis):
		await ctx.send(embed=failureEmbed)
		return
	if len(ctx.guild.emojis) >= ctx.guild.emoji_limit:
		await ctx.send("The emoji limit is full. Remove some emojis and try again.")
		return
	if len(ctx.message.attachments) == 0:
		await ctx.send("You need to provide an image.")
		return
	real_emojiname = "_".join(emojiname)
	custom_emoji = await ctx.guild.create_custom_emoji(name=real_emojiname,image=await ctx.message.attachments[0].read())
	await ctx.send(f"<:{custom_emoji.name}:{custom_emoji.id}> added as :{custom_emoji.name}:. enjoy!")

@client.command()
async def echoas(ctx,person,*text):
	msg = " ".join(text)
	imitated = ctx.message.mentions[0]
	avatar = await imitated.avatar_url_as(format="png").read()
	confirm_message = await ctx.send(f"imitating {ctx.message.mentions[0].name}: {msg}")
	hook = await ctx.channel.create_webhook(name=imitated.display_name,avatar=avatar)
	await ctx.message.add_reaction(u"\U00002705")
	await hook.send(f"{msg}")
	await hook.delete()
	await asyncsleep(3)
	await confirm_message.delete()

@client.command()
async def interject(ctx):
	await ctx.send(interjection)

@client.command()
async def license(ctx):
	await ctx.send(license)

@client.command()
async def iscringe(ctx):
	async for message in ctx.channel.history(limit=2):
		if(message == ctx.message):
			continue
		previous_message = message
	await ctx.send(f"saying \"{previous_message.content}\" is cringe")

###########
# RUN BOT #
###########

# finally, we can run the bot.
client.run(TOKEN, bot=True)
