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
	    embed = discord.Embed(title=config['prefix']+'list')
	    text = ""
	    textList = []
	    memberList = []
	    memberListRole = []
	    memberListStatut = []
	    statusList = ["ONLINE", "OFFLINE", "IDLE", "DND", "INVISIBLE"]
	    statusArgList = []
	    # no parameter
	    if len(args) == 0:
	        for member in ctx.guild.members:
	            if not member.bot:  
	                memberList.append(member)
	    else:
	    	# upload role file
	        if (args[0] == "-o" and len(args) == 2) or (args[1] == "-o" and len(args) == 3):
	            memberRoles = ""
	            targetRole = get(ctx.guild.roles, name='@everyone')
	            if len(args) == 2:
	            	file = open("./files/list-o/"+args[1]+".txt", "w+")
	            else:
	            	for role in ctx.guild.roles:
	            		if role.name.upper() == args[0].upper():
	            			targetRole = role
	            	file = open("./files/list-o/"+args[2]+".txt", "w+")
	            for member in ctx.guild.members:
	                memberRoles = ""
	                for role in member.roles:
	                    memberRoles += role.name
	                    if not role == member.roles[(len(member.roles)-1)]:
	                        memberRoles += ","
	                if len(args) == 2:
	                	memberList.append(pseudo(member)+':'+str(member.id)+':'+memberRoles)
	                else:
	                	if isinstance(targetRole, discord.Role):
	                		if targetRole in member.roles:
	                			print(targetRole.name)
	                			memberList.append(pseudo(member)+':'+str(member.id)+':'+memberRoles)	                		
	            file.write('\n'.join(sorted(memberList)))
	            file.close()
	            if len(args) == 2:
	            	return await ctx.send(file=discord.File("./files/list-o/"+args[1]+".txt", filename=args[1]))
	            else:
	            	return await ctx.send(file=discord.File("./files/list-o/"+args[2]+".txt", filename=args[2]))
	        # with a status
	        for arg in args:
	            if arg.upper() in statusList:
	                statusArgList.append(arg)
	                for member in ctx.guild.members:
	                    if check_statut(member, arg):
	                        if member not in memberListStatut and not member.bot:
	                            memberListStatut.append(member)

	        # with a role
	        for arg in args:
	            for role in ctx.guild.roles:
	                if role.name.upper() == arg.upper():
	                    for member in ctx.guild.members:
	                        if role in member.roles:
	                            if member not in memberListRole and not member.bot:
	                                memberListRole.append(member)

	        # voice channel as a parameter
	        for arg in args:
	            for voice_channel in ctx.guild.voice_channels:
	                if voice_channel.name.upper() == arg.upper():
	                    for member in voice_channel.members:
	                        if member not in memberList and not member.bot:
	                            memberList.append(member)

	    if len(memberListRole) > 0 and len(memberListStatut) > 0:
	        for item in memberListRole:
	            if item in memberListStatut:
	                memberList.append(item)
	    else:
	        if len(memberListRole) > 0:
	            memberList = memberListRole
	        if len(memberListStatut) > 0:
	            memberList = memberListStatut
	    text = str(len(memberList)) + " personnes trouvées" + "\n \n"
	    for memberListItem in memberList:
	    	textList.append(pseudo(memberListItem))
	    text = '\n'.join(sorted(textList))
	    embed.description = text;
	    return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ListCog(bot))