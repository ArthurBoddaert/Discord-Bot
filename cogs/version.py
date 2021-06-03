"""
Created By : Delepoulle Samuel and Deloison Clément
"""

import discord as discord
from discord.ext import commands
from discord.utils import get
from functions import *
import json
import re
import os

with open('./config.json', 'r') as f:
    config = json.load(f)

class VersionCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="version", help="Displays the active bot version")
    async def rolelist(self, ctx, *args):
        """Displays the active bot version

        Parameters
        ----------
        ctx: Context
            The context of the message
        args: List[str]
            Every single word following the name of the command
        """
        rows = []
        versionFile = []

        

        # The full version, including alpha/beta/rc tags.
        release = re.sub('^v', '', os.popen('git describe --tag').read().strip())
        # The short X.Y version.
        version = release  

        text = version + "\nGit Repository : https://github.com/ArthurBoddaert/Discord-Bot"
        
        # print(file.read())
        embed = discord.Embed(title=config['prefix']+"version")
        embed.add_field(name="Author:", value=ctx.message.author, inline=False)
        embed.description = text
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(VersionCog(bot))