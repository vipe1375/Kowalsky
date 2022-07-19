import discord
from discord.ext import commands

from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur

def is_vipe(id):
    return id == 691380397673545828

class CommandesAdmin(commands.Cog):
    def __init__(self, bot: commands.Bot, version):
        self.bot = bot
        self.version = version

    # Testmod
        
    @commands.command()
    async def testmod(self, ctx, *, oe):
        if ctx.author.id == 691380397673545828:
            if oe == "on":
                database_handler.testmod_on()
                await ctx.send("on")
            elif oe == "off":
                database_handler.testmod_off()
                await ctx.send("off")
            elif oe == "check":
                result = database_handler.check_testmod()
                await ctx.send(f"{result[0][0]}")  

    @commands.command()
    async def setup_update_db(self, ctx):
        database_handler.setup()


    @commands.command()
    async def post(self, ctx, *, msg):
        if is_vipe(ctx.author.id):
            channels = database_handler.get_channels()
            msg = str(msg + "\n\n disponible à partir de minuit")
            embed = discord.Embed(title = "Mise à jour", color = bleu, description = msg)
            embed.set_footer(text = f"version actuelle : {self.version}")
            for i in channels:
                chan = self.bot.get_channel(i[0])
                await chan.send(embed = embed)
            await ctx.send("message posté")
        else:
            await ctx.send("t'as pas le droit dsl")

    
    @commands.command()
    async def admin(self, ctx):
        if is_vipe(ctx.author.id):
            channel = self.bot.get_channel(971870035624726628)
            for g in self.bot.guilds:
                await channel.send(g.name)
            await ctx.send(len(self.bot.guilds))

    @commands.command()
    async def getinvite(self, ctx, *, guild_name):
        if is_vipe(ctx.author.id):
            channel = self.bot.get_channel(971870035624726628)
            for g in self.bot.guilds:
                if g.name == guild_name:
                    c = g.channels[0]
                    i = await c.create_invite()
                    await ctx.send(i.url)
                    return

            await channel.send("pas trouvé")
            