import discord as discord
from discord.ext import commands

import json
with open('./config.json', 'r') as f:
	config = json.load(f)

class TempCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def temp(self, ctx, *args):
        
        the_guild = ctx.guild
        category = discord.utils.get(the_guild.categories, name=config['temp_category'])

        if ctx.message.author.guild_permissions.administrator : 
            if args[0] == "--clear" :
                for channel in category.voice_channels :
                        if (len(channel.members) == 0) :
                            await channel.delete()
                return


        await the_guild.create_voice_channel(args[0],category=category)
        return await ctx.send('create new vocal chanel '+args[0]+' in '+str(ctx.guild)+" category = "+str(category))

        
        

def setup(bot):
    bot.add_cog(TempCog(bot))