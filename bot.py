"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands

BOT_PREFIX = '--'
TOKEN=''
bot = commands.Bot(command_prefix=BOT_PREFIX)

log = []

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

command_brief="Displays a list of the existing roles"
command_help="Displays a list of the existing roles"
@bot.command(name="rolelist", help=command_help)
async def rolelist(ctx, *args):
    """Displays a list of the existing roles

    Parameters
    ----------
    ctx: Context
        The context of the message
    args: List[str]
        Every single word following the name of the command
    """
    embed = discord.Embed(title="--rolelist")
    text = ""
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            text += role.name + "\n"
    embed.description = text
    await ctx.send(embed=embed)

command_brief="Displays a list of users depending on the arguments"
command_help="Displays a list of users depending on the arguments\nSeveral arguments are allowed:\n"
command_help+="  - the name of a role, in this case the command only shows the names of the users possessing the specified role\n"
command_help+="  - a status (online, offline, idle, dnd or invisible), in this case the command only shows the names of the users whose status corresponds to the specified status\n"
command_help+="  - the name of a voice channel, in this case the command only shows the names of the users currently in the specified channel\n"
command_help+="  - '-o ' followed by a name, in this case the command will create and upload a file named as specified. This file contains every usernames followed by their IDs and their roles on the server\n"
command_help+="If the command has none of these arguments, it will simply show the names of every single user of the server\nIn every case, this command ignores bots"
@bot.command(name="list", help=command_help, brief=command_brief) 
async def list(ctx, *args):
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
    embed = discord.Embed(title="--list")
    text = ""
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
        if args[0] == "-o" and len(args) == 2:
            memberRoles = ""
            file = open("./files/list-o/"+args[1]+".txt", "w+")
            for member in ctx.guild.members:
                memberRoles = ""
                for role in member.roles:
                    memberRoles += role.name
                    if not role == member.roles[(len(member.roles)-1)]:
                        memberRoles += ","
                file.write(pseudo(member)+":"+str(member.id)+":"+memberRoles+"\n")
            file.close()
            return await ctx.send(file=discord.File("./files/list-o/"+args[1]+".txt", filename=args[1]))
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
        text += pseudo(memberListItem) + "\n"
    embed.description = text;
    return await ctx.send(embed=embed)


@bot.command(name="dm")
async def dmall(ctx, role_arg, *args):
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

# ****************************************************************************
# ****************************************************************************
# ****************************************************************************

def pseudo(member):
    """Checks if the member has a nickname or not

    Parameters
    ----------
    member: Member
        The targeted discord member

    Returns
    -------
    The member's username
        If the member has no nickname on the server
    The member's nickname
        If the member has a nickname on the server
    Nothing
        If the parameter isn't a Member
    """
    if isinstance(member, discord.Member):
        if member.nick is None:
            return member.name
        else:
            return member.nick
    return

def check_statut(member, status):
    """Checks the member's status

    Parameters
    ----------
    member: Member
        The targeted discord member
    statut:
        The targeted status

    Returns
    -------
    True
        If the user's status corresponds to the specified status
    False
        If the user's status doesn't corresponds to the specified status or if the parameter isn't a Member
    """
    if isinstance(member, discord.Member) and isinstance(status, str):
        if status.upper() == "ONLINE":
            if member.status == discord.Status.online:
                return True
        if status.upper() == "OFFLINE":
            if member.status == discord.Status.offline:
                return True
        if status.upper() == "IDLE":
            if member.status == discord.Status.idle:
                return True
        if status.upper() == "DND":
            if member.status == discord.Status.dnd:
                return True
        if status.upper() == "INVISIBLE":
            if member.status == discord.Status.invisible:
                return True
    return False

# ****************************************************************************
# main
# ****************************************************************************

def main():
	bot.run(TOKEN)

if __name__ == '__main__':
	main()