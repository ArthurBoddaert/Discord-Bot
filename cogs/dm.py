"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from discord.utils import get
from functions import *
import json

with open('./config.json', 'r') as f:
	config = json.load(f)

class DmCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="dm")
	async def dmall(self, ctx, role_arg, *args):
	    """Sends a specified message to all users who have the specified role
	    This command also allows to send an attachment

	    Parameters
	    ----------
	    ctx: Context
	        The context of the message
	    role_arg: str
	        The targeted role
	    args: List[str]
	        Every single word following the name of the command
	    """
	    # specified role
	    if ctx.message.author.top_role >= get(ctx.guild.roles, name=config['role_to_dm']):
		    listRole = []
		    for role in ctx.guild.roles:
		        if role.name.upper() == role_arg.upper():
		            listRole.append(role)
		    # list of every targeted user
		    destinataires = []
		    for member in ctx.guild.members:
		        for role in listRole:
		            if member not in destinataires and role in member.roles and not member.bot:
		                destinataires.append(member)
		    # attachments
		    attachmentList = []
		    for attachment in ctx.message.attachments:
		        attachmentList.append(await attachment.to_file())
		    # send the message to every targeted user
		    for destinataire in destinataires:
		        await destinataire.send(content=" ".join(args), files=attachmentList)
		    return await ctx.message.author.send('"'+' '.join(args)+'"'+' sent to all '+role_arg.upper())
	    else:
	    	return await ctx.message.author.send('You do not have the permissions to use this command')

def setup(bot):
    bot.add_cog(DmCog(bot))