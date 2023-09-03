"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from functions import *
import json

with open('./config.json', 'r') as f:
	config = json.load(f)

class RolelistCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="rolelist", help="Displays a list of the existing roles")
	async def rolelist(self, ctx, *args):
	    """Displays a list of the existing roles

	    Parameters
	    ----------
	    ctx: Context
	        The context of the message
	    args: List[str]
	        Every single word following the name of the command
	    """
	    roleList = []
	    embed = discord.Embed(title=config['prefix']+"rolelist")
	    text = ""
	    for role in ctx.guild.roles:
	        if role.name != "@everyone":
	        	roleList.append(role.name)
	    roleList.reverse()
	    text = '\n'.join(roleList)
	    embed.description = text
	    await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RolelistCog(bot))
