"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
from functions import *
from discord.utils import get
import json

with open('./config.json', 'r') as f:
	config = json.load(f)

class ListCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	command_brief="Displays a list of users depending on the arguments"
	command_help="Displays a list of users depending on the arguments\nSeveral arguments are allowed:\n"
	command_help+="  - the name of a role, in this case the command only shows the names of the users possessing the specified role\n"
	command_help+="  - a status (online, offline, idle, dnd or invisible), in this case the command only shows the names of the users whose status corresponds to the specified status\n"
	command_help+="  - the name of a voice channel, in this case the command only shows the names of the users currently in the specified channel\n"
	command_help+="  - '-o ' followed by a name, in this case the command will create and upload a file named as specified. This file contains every usernames followed by their IDs and their roles on the server\n"
	command_help+="If the command has none of these arguments, it will simply show the names of every single user of the server\nIn every case, this command ignores bots"
	@commands.command(name="list", help=command_help, brief=command_brief) 
	async def list(self, ctx, *args):
	    """Displays a list of users depending on the arguments
	    Several arguments are allowed:
	    - the name of a role, in this case the command only shows the names of the users possessing the specified role
	    - a status (online, offline, idle, dnd or invisible), in this case the command only shows the names of the users whose status corresponds to the specified status
	    - the name of a voice channel, in this case the command only shows the names of the users currently in the specified channel
	    - '-o ' followed by a name, in this case the command will create and upload a file named as specified. This file contains every usernames followed by their IDs and their roles on the server
	    If the command has none of these arguments, it will simply show the names of every single user of the server
	    In every case, this command ignores bots

	    Parameters
	    ----------
	    ctx: Context
	        The context of the message
	    args: List[str]
	        Every single word following the name of the command
	    """
	    statusList = ['online', 'offline', 'dnd', 'idle', 'invisible']
	    memberList = []
	    memberListRole = []
	    memberListStatus = []
	    memberListChannel = []
	    if len(args) == 0:
	    	for member in ctx.guild.members:
	    		if not member.bot:
	    			memberList.append(member)
	    else:
	    	for arg in args:
	    		# if 'args' contains a role
	    		for role in ctx.guild.roles:
	    			if arg.upper() == role.name.upper():
	    				for member in ctx.guild.members:
	    					for memberRole in member.roles:
	    						if arg.upper() == memberRole.name.upper():
	    							if member not in memberListRole and not member.bot:
	    								memberListRole.append(member)
	    		# if 'args' contains a status
	    		for status in statusList:
	    			for member in ctx.guild.members:
	    				if check_status(member, arg):
	    					if member not in memberListStatus and not member.bot:
	    						memberListStatus.append(member)
	    		# if 'args' contains a voice channel name
	    		for channel in ctx.guild.voice_channels:
	    			if arg.upper() == channel.name.upper():
	    				for member in channel.members:
	    					if member not in memberListChannel and not member.bot:
	    						memberListChannel.append(member)
	    	# list intersections
	    	if len(memberListRole) > 0 and len(memberListStatus) > 0 and len(memberListChannel) > 0:
	    		for member in memberListRole:
	    			if member in memberListStatus and member in memberListChannel:
	    				memberList.append(member)
	    	elif len(memberListRole) > 0 and len(memberListStatus) and len(memberListChannel) == 0:
	    		for member in memberListRole:
	    			if member in memberListStatus:
	    				memberList.append(member)
	    	elif len(memberListRole) > 0 and len(memberListChannel) and len(memberListStatus) == 0:
	    		for member in memberListRole:
	    			if member in memberListChannel:
	    				memberList.append(member)
	    	elif len(memberListChannel) > 0 and len(memberListStatus) and len(memberListRole) == 0:
	    		for member in memberListChannel:
	    			if member in memberListStatus:
	    				memberList.append(member)
	    	elif len(memberListRole) > 0 and len(memberListStatus) == 0 and len(memberListChannel) == 0:
	    		memberList = memberListRole
	    	elif len(memberListStatus) > 0 and len(memberListChannel) == 0 and len(memberListRole) == 0:
	    		memberList = memberListStatus
	    	elif len(memberListChannel) > 0 and len(memberListRole) == 0 and len(memberListStatus) == 0:
	    		memberList = memberListChannel
	    	# if 'args' contains '-o'
	    	if len(args) >= 2 and args[len(args)-2] == '-o':
	    		file = open('./files/list-o/'+args[len(args)-1]+'.txt', 'w+')
	    		roleNameList = []
	    		rows = []
	    		for member in memberList:
	    			for role in member.roles:
	    				roleNameList.append(role.name)
	    			rows.append(pseudo(member)+';'+str(member.id)+';'+','.join(roleNameList))
	    		file.write('\n'.join(rows))
	    		file.close()
	    		return await ctx.send(file=discord.File('./files/list-o/'+args[len(args)-1]+'.txt', filename=args[len(args)-1]))
	    embed = discord.Embed(title=config['prefix']+'list')
	    embed.description = str(len(memberList)) + ' user(s) found \n\n'
	    for member in memberList:
	    	embed.description += pseudo(member) + '\n'
	    try:
	    	await ctx.send(embed=embed)
	    except Exception:
	    	await ctx.send('The list might be too long, consider using\n```'+ctx.message.content+' -o filename```')

def setup(bot):
    bot.add_cog(ListCog(bot))