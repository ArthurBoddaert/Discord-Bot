"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from functions import *
import discord.utils

class SondageCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	command_brief = "Sends an embed message with a given question and its answers"
	command_help = command_brief + "\n" + "The reactions corresponding to the answers are automaticaly generated" + "\n" + "This command has a limit of 24 answers"
	@commands.command(name="sondage", brief=command_brief, help=command_help)
	async def sondage(self, ctx, *args):
		"""Sends an embed message with a given question and its answers
		The reactions corresponding to the answers are automaticaly generated
		This command has a limit of 24 answers

		Parameters
		----------
		ctx: Context
	        The context of the message
	    args: List[str]
	        Every single word following the name of the command
		"""
		embed = discord.Embed(title='--sondage', author=ctx.message.author)
		argSentence = " ".join(args)
		argList = argSentence.split('|')
		embed.description = "**" + argList[0] + "**" + "\n"
		reactionList = []
		for i in range(len(argList)):
			reactionList.append("regional_indicator_"+chr(i+96))
		for answer in argList:
			if answer != argList[0]:
				embed.description += "\n" + ":" + reactionList[argList.index(answer)] + ": :" + answer;
		message = await ctx.send(embed=embed)
		for reaction in reactionList:
			if reaction != reactionList[0]:
				await message.add_reaction(regional_indicator(chr(96+reactionList.index(reaction))))

def setup(bot):
	bot.add_cog(SondageCog(bot))