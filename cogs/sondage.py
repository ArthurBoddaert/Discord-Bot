"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from functions import *
import discord.utils
import json

with open('./config.json', 'r') as f:
	config = json.load(f)

class SondageCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	command_brief = "Sends an embed message with a given question and its answers"
	command_help = command_brief + "\n" + "The reactions corresponding to the answers are automaticaly generated" + "\n" + "This command has a limit of 24 answers"
	@commands.command(name="sondage",aliases=['sondageUnique'] , brief=command_brief, help=command_help)
	async def sondage(self, ctx, *args):
		"""Sends an embed message with a given question and its answers
		The reactions corresponding to the answers are automaticaly generated
		This command has a limit of 26 answers
		The argument '-d' and a number 'n' makes the survey last 'n' seconds
		calling the command with the keyword 'sondageUnique' limits the number of answers per user to 1

		Parameters
		----------
		ctx: Context
	        The context of the message
	    args: List[str]
	        Every single word following the name of the command
		"""
		arguments = list(args)
		delay = 0
		await ctx.message.delete()
		if arguments[0].startswith('-d'):
			delay = float(arguments[0][2:])
			arguments.pop(0)
		if ctx.message.content.startswith(config['prefix']+'sondageUnique'):
			embed = discord.Embed(title=config['prefix']+'sondageUnique')
		else:
			embed = discord.Embed(title=config['prefix']+'sondage')
		embed.description = "**" + arguments[0] + "**" + "\n"
		reactionList = []
		for i in range(len(arguments)):
			reactionList.append("regional_indicator_"+chr(i+96))
		for answer in arguments:
			if answer != arguments[0]:
				embed.description += "\n" + ":" + reactionList[arguments.index(answer)] + ": :" + answer;
		message = await ctx.send(embed=embed)
		if delay == 0:
			await ctx.send('```Survey ID : '+str(message.id)+'```')
		for reaction in reactionList:
			if reaction != reactionList[0]:
				await message.add_reaction(regional_indicator(chr(96+reactionList.index(reaction))))
		if delay > 0:
			await message.delete(delay=delay)

	command_brief = "Sends a graph which corresponds to the results of a survey"
	command_help = command_brief + "\n" + "The survey id is given when the 'sondage' command is called" + "\n" + "In case you use the 'sondageUnique' keyword, the survey id isn't sent but a graph is uploaded at the end of the timer"
	@commands.command()
	async def result(self, ctx, survey_id, brief=command_brief, help=command_help):
		"""Uploads a graph corresponding to a survey

		Parameters
		----------
		ctx: Context
			The context of the message
		survey_id: str
			The id of the survey
		"""
		try:
			create_diagram(await ctx.channel.fetch_message(int(survey_id)), survey_id)
			image = discord.File('./files/sondage/'+survey_id+'.png', filename=survey_id+'.png')
			await ctx.send(file=image)
		except:
			await ctx.send('Message not found')

async def setup(bot):
	await bot.add_cog(SondageCog(bot))
