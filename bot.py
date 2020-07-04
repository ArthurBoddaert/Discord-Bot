"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from functions import *
import json

with open('./config.json', 'r') as f:
	config = json.load(f)

bot = commands.Bot(command_prefix=config['prefix'])

log = [] # not used for the moment

# ****************************************************************************
# events
# ****************************************************************************

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user.name} - {bot.user.id}')
	return

@bot.event
async def on_command(ctx):
	print(f'Command {ctx.command.name} called by {ctx.message.author}')
	log.append(f'Command {ctx.command.name} called by {ctx.message.author}')
	return

@bot.event
async def on_message(message):   
	await bot.process_commands(message) # necessary to keep both use on_message() and commands
    
@bot.event
async def on_reaction_add(reaction, user):
	# ***** '--sondage' command with a single answer per user *****
	if len(reaction.message.embeds) > 0:
		embed = reaction.message.embeds[0]
		if embed.title == config['prefix']+'sondageUnique':
			if not user.bot:
				# si 'user' réagit et qu'il a déjà réagi au paravant, on supprime ses anciennes réactions
				for react in reaction.message.reactions:
					if react != reaction:
						async for usr in react.users():
							if usr.name == user.name:
								await react.remove(usr)

@bot.event
async def on_message_delete(message):
	if len(message.embeds) > 0:
		if 'sondage' in message.embeds[0].title:
			embed = discord.Embed(author=message.author)
			embed.description = ' '
			for reaction in message.reactions:
				embed.description += '\n' + reaction.emoji + ' : ' + str(reaction.count) + ' answer(s)'
			await message.channel.send(embed=message.embeds[0])
			await message.channel.send(embed=embed)
			create_diagram(message, str(message.id))
			image = discord.File('./files/sondage/'+str(message.id)+'.png', filename=str(message.id)+'.png')
			await message.channel.send(file=image)
			
	# ***********************************************************

# ****************************************************************************
# commands
# ****************************************************************************

bot.load_extension('cogs.rolelist')
bot.load_extension('cogs.list')
bot.load_extension('cogs.dm')
bot.load_extension('cogs.grant')
bot.load_extension('cogs.sondage')
bot.load_extension('cogs.version')
bot.load_extension('cogs.poll')

@bot.command(name='getlogs', hidden=True)
async def getlogs(ctx):
	"""
	Sends the command logs to the author

	Parameters
	----------
    ctx: Context
        The context of the message
	"""
	if isAdministrator(ctx.message.author, ctx.message.guild):
		file = open('./files/logs/logs.txt', 'w+')
		file.write('\n'.join(log))
		file.close()
		return await ctx.message.author.send(file=discord.File('./files/logs/logs.txt', filename='logs'))

# ****************************************************************************
# main
# ****************************************************************************

def main():
	bot.run(config['token'])

if __name__ == '__main__':
	main()