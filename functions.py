"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands
import pandas as pandas
import matplotlib.pyplot as plot
import discord.utils

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
            print("problème")
            return member.display_name
        else:
            print(member.display_name)
            return member.nick

        
    return

def check_status(member, status):
    """Checks the member's status

    Parameters
    ----------
    member: Member
        The targeted discord member
    status: str 
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

def isAdministrator(user, guild):
    """Checks if a user is administrator in a given guild

    Parameters
    ----------
    user: User
        the targeted user
    guild: Guild
        the targeted guild

    Returns
    -------
    True
        If the user is an administrator
    False
        If the user isn't an administrator
    """
    if user in guild.members:
        member = guild.get_member(user.id)
        if member.top_role.permissions.administrator:
            return True
    return False

def regional_indicator(character):
    """Gives the unicode string of a given character

    Parameters
    ----------
    Returns
    -------
    False
        If the character isn't correct
    Unicode string
        The unicode string corresponding to the character if it is correct
    """
    if character == 'a':
        return '\U0001F1E6'
    if character == 'b':
        return '\U0001F1E7'
    if character == 'c':
        return '\U0001F1E8'
    if character == 'd':
        return '\U0001F1E9'
    if character == 'e':
        return '\U0001F1EA'
    if character == 'f':
        return '\U0001F1EB'
    if character == 'g':
        return '\U0001F1EC'
    if character == 'h':
        return '\U0001F1ED'
    if character == 'i':
        return '\U0001F1EE'
    if character == 'j':
        return '\U0001F1EF'
    if character == 'k':
        return '\U0001F1F0'
    if character == 'l':
        return '\U0001F1F1'
    if character == 'm':
        return '\U0001F1F2'
    if character == 'n':
        return '\U0001F1F3'
    if character == 'o':
        return '\U0001F1F4'
    if character == 'p':
        return '\U0001F1F5'
    if character == 'q':
        return '\U0001F1F6'
    if character == 'r':
        return '\U0001F1F7'
    if character == 's':
        return '\U0001F1F8'
    if character == 't':
        return '\U0001F1F9'
    if character == 'u':
        return '\U0001F1FA'
    if character == 'v':
        return '\U0001F1FB'
    if character == 'w':
        return '\U0001F1FC'
    if character == 'x':
        return '\U0001F1FD'
    if character == 'y':
        return '\U0001F1FE'
    if character == 'z':
        return '\U0001F1FF'
    return False

def create_diagram(message, name):
    """Creates and saves a diagram

    Parameters
    ----------
    message: discord.Message
        A message object with reactions
    name: str
        File name
    """
    if isinstance(message, discord.Message):
        voteList = []
        index = []
        for reaction in message.reactions:
            voteList.append(reaction.count)
            index.append(chr(97+message.reactions.index(reaction)))
        data = {
            "Votes":voteList
        }
        dataFrame = pandas.DataFrame(data=data, index=index)
        dataFrame.plot.bar(rot=15, title=name)
        plot.savefig('./files/sondage/'+name+'.png')
