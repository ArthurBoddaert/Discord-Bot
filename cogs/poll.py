"""
Created By : Delepoulle Samuel and Deloison Clément
"""

import discord as discord
from discord.ext import commands
from discord.utils import get
from functions import *
import discord.utils
import json


with open('./config.json', 'r') as f:
    config = json.load(f)
    
bot = commands.Bot(command_prefix=config['prefix'])
user = discord.Client()

class PollCog(commands.Cog):

    def __init__(self, bot):
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
            # get file lines
            for destinataire in destinataires:
                f = open('./files/poll/'+pseudo(destinataire)+'_answers.txt', "w")
                answer.append('Poll Answer for user '+pseudo(destinataire)+' :\n')
                await destinataire.send('A poll has been issued for you, please answer correctly to the following questions :')
                for line in fileLines:
                    # dm targets 
                    await destinataire.send(content=line)
                    
                    #wait reply
                    try:
                        msg = await self.bot.wait_for('message', check=lambda message: not message.author.bot, timeout=60)
                        answer.append('Question : '+str(line)+'\nAnswer : '+msg.content+'\n')
                    except TimeoutError: 
                        return await message.channel.send("Timed out, try again.")
                    
                    await destinataire.send('Ok, Answer registered\n')
                await destinataire.send('**Poll is finished, thanks for answering**')    
                # write results
                f.write('\n'.join(answer))
                f.close()
                # dm author result file 
                answers = discord.File('./files/poll/'+pseudo(destinataire)+'_answers.txt', filename=""+pseudo(destinataire)+"_answers.txt")    
                await ctx.message.author.send("User "+pseudo(destinataire)+" has finished answering the poll : ", file=answers)
        else:
            return await ctx.message.author.send('You do not have the permissions to use this command')

def setup(bot):
    bot.add_cog(PollCog(bot))