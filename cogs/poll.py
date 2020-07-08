"""
Created By : Delepoulle Samuel and Deloison Clément
"""

import discord as discord
from discord.ext import commands
from discord.utils import get
from functions import *
from threading import Thread
import discord.utils
import json


with open('./config.json', 'r') as f:
    config = json.load(f)
    
bot = commands.Bot(command_prefix=config['prefix'])
user = discord.Client()

class PollCog(commands.Cog):

    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot
        
    @commands.command(name="poll")
    async def poll(self, ctx, role_arg, *args):

        # permisson for command
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

            # get poll file
            attachedFile = await ctx.message.attachments[0].to_file()
            file = attachedFile.fp
            fileText = file.read().decode("utf-8")
            fileLines = fileText.split('\n')
            answer = []
            poll = []
            poll_id = str(ctx.message.id)
            
            #generate answers file
            f = open('./files/poll/'+poll_id+'_answers.csv', "w+")
            
            # get targets
            for destinataire in destinataires:
                await destinataire.send('A poll has been issued for you by'+pseudo(ctx.message.author)+', please answer correctly to the following questions :')
                # get file lines
                for row in fileLines:
                    # dm targets 
                    try:
                        await destinataire.send(content=row)
                        #wait reply
                        try:
                            msg = await self.bot.wait_for('message', check=lambda message: not message.author.bot, timeout=60)
                            answer.append('"'+msg.content+'"')
                        except TimeoutError: 
                            return await message.channel.send("Timed out, try again.")
                        
                        await destinataire.send('Ok, Answer registered\n')
                    except : 
                        print("Empty line")
                await destinataire.send('**Poll is finished, thanks for answering**')    
                # write results
                poll.append(pseudo(destinataire)+';'+str(destinataire.id)+';'+','.join(answer))
                answer[:] = []
            f.write('\n'.join(sorted(poll, key=lambda v: v.upper())))
            f.close() 
            
            # dm author result file 
            answers = discord.File('./files/poll/'+poll_id+'_answers.csv', filename=''+poll_id+'_answers.csv')
            await ctx.message.author.send("All users have finished answering the poll.\n Answers file", file=answers)
        else:
            return await ctx.message.author.send('You do not have the permissions to use this command')

def setup(bot):
    bot.add_cog(PollCog(bot))