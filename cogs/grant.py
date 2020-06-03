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

class GrantCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="grant", hidden=True)
	async def grant(self, ctx, *args):
		"""Grants roles corresponding to an attached file
		The file's format must be the same as the 'list -o' output file format

		Parameters
		----------
		ctx: Context
	        The context of the message
	    args: List[str]
	        Every single word following the name of the command
		"""
		logs = []
		targetGuild = ctx.message.guild
		if isAdministrator(ctx.message.author, targetGuild):
			if len(ctx.message.attachments) > 0:
				if len(args) > 0 and (args[0] == '-r' or args[0] == '-reset'):
					for member in targetGuild.members:
						for role in member.roles:
							if role.name != '@everyone' and role.managed == False:
								try:
									await member.remove_roles(role)
									print(f'- Removing the role {role.name}#{role.id} from {member.name}')
									logs.append(f'- Removing the role {role.name}#{role.id} from {member.name}')
								except:
									print(f"- ERROR: can't remove the role {role.name}#{role.id} from {member.name}")
									logs.append(f"- ERROR: can't remove the role {role.name}#{role.id} from {member.name}")
				attachedFile = await ctx.message.attachments[0].to_file()
				file = attachedFile.fp
				fileText = file.read().decode("utf-8")
				fileLines = fileText.split('\n')
				target = None
				oldTarget = None
				for line in fileLines:
					row = line.split(';')
					if len(row) == 3 and ',' in row[2]:
						rolesToGrant = row[2].split(',')
						for member in targetGuild.members:
							if str(member.id) == row[1]:
								if target is not None:
									oldTarget = target
								target = member
						for role in rolesToGrant:
							if role != '@everyone' and get(targetGuild.roles, name=role).managed == False:
								if oldTarget != target and get(targetGuild.roles, name=role) not in target.roles:
									try:
										await target.add_roles(get(targetGuild.roles, name=role))
										print(f'- Giving the role {get(targetGuild.roles, name=role).name}#{get(targetGuild.roles, name=role).id} to {target.name}')
										logs.append(f'- Giving the role {get(targetGuild.roles, name=role).name}#{get(targetGuild.roles, name=role).id} to {target.name}')
									except:
										print(f"- ERROR: can't give the role {get(targetGuild.roles, name=role).name}#{get(targetGuild.roles, name=role).id} from {target.name}")
										logs.append(f"- ERROR: can't give the role {get(targetGuild.roles, name=role).name}#{get(targetGuild.roles, name=role).id} from {target.name}")
				file = open('./files/logs/grantlogs.txt', 'w+')
				file.write('\n'.join(logs))
				file.close()
				return await ctx.message.author.send(file=discord.File('./files/logs/grantlogs.txt', filename='grantlogs'))
			else:
				await ctx.send("No attachment found")
		else:
			return await ctx.message.author.send('You do not have the permissions to use this command')

def setup(bot):
	bot.add_cog(GrantCog(bot))