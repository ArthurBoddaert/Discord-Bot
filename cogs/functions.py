"""
Created By : Delepoulle Samuel and Boddaert Arthur
"""

import discord as discord
from discord.ext import commands

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