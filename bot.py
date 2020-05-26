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

# ****************************************************************************
# commands
# ****************************************************************************

bot.load_extension('cogs.rolelist')
bot.load_extension('cogs.list')
bot.load_extension('cogs.dm')
bot.load_extension('cogs.grant')
bot.load_extension('cogs.sondage')

# ****************************************************************************
# main
# ****************************************************************************

def main():
	bot.run(config['token'])

if __name__ == '__main__':
	main()