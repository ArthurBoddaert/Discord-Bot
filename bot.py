"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from functions import *

BOT_PREFIX = '--'
TOKEN=''
bot = commands.Bot(command_prefix=BOT_PREFIX)

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
	print(f'Command {ctx.command.name} called by {pseudo(ctx.message.author)}')
	log.append(f'Command {ctx.command.name} called by {pseudo(ctx.message.author)}')
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

# ****************************************************************************
# main
# ****************************************************************************

def main():
	bot.run(TOKEN)

if __name__ == '__main__':
	main()