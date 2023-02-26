# gestion discord
import discord
from discord.ext import commands, tasks
from discord.utils import get

# autres modules
import time as t
import random as rd
import re
from datetime import timedelta
import traceback
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# imports cogs
import commandes_troll
from commandes_troll import CommandesTroll
from commandes_admin import CommandesAdmin
from commandes_base import CommandesBase
from chads import CommandsChads
from chads2 import CommandsChads2
from version_k import version

# database
from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")
token_k = os.getenv("token_kowalsky")

# gestion discord 2
intents = discord.Intents.all()
intents.members = True


# démarrage du bot

class KBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="k.", intents = intents, application_id = 926864538681368626)

    async def setup_hook(self) -> None:
        await self.load_extension("commandes_base")
        await self.load_extension("commandes_admin")
        await self.load_extension("commandes_troll")
        await self.load_extension("chads")
        await self.load_extension("chads2")

bot = KBot()
bot.remove_command('help')

@bot.event
async def on_ready():
    channel = bot.get_channel(logs_channel_id)

    await channel.send("restart")
    change_status.start()
    check_restart_cogs.start()

    database_handler.set_finishers()

    print("\nchuis prêt mon reuf lets gooo, heure : ", str(str(t.localtime(t.time())[3]) + 'h' + str(t.localtime(t.time())[4])), ", version : ", version,"\n")


# Boucle de changement de statut
@tasks.loop(seconds = 10)
async def change_status():
    await bot.change_presence(activity=rd.choice([discord.Activity(name = f"{len(bot.guilds)} serveurs", type = discord.ActivityType.watching), discord.Activity(name = f"k.help", type = discord.ActivityType.playing), discord.Activity(name = f"k.invite | k.support", type = discord.ActivityType.playing)]))

# Boucle de redémarrage des cogs
@tasks.loop(seconds = 50)
async def check_restart_cogs():
    if t.localtime(t.time())[3] == 0:
        if t.localtime(t.time())[4] == 0:
            restart_cogs.start()
            check_restart_cogs.stop()

@tasks.loop(hours=24)
async def restart_cogs():
    channel = bot.get_channel(logs_channel_id)
    msg = await channel.send(":orange_circle: restarting...")
    await bot.reload_extension('commandes_base')
    await bot.reload_extension('commandes_admin')
    await bot.reload_extension('commandes_troll')
    await bot.reload_extension('chads')
    await bot.reload_extension('chads2')
    
    await msg.edit(content=":green_circle: restart cogs ")




#----------------| INFOS |-----------------#

# Liste des commandes désactivables :
liste_commandes = {'quoi': 1, 'feur': 1, 'tg' : 2, 'ph' : 3, 'randomping' : 4, 'csc' : 5, 'saydm' : 6, 'haagrah' : 7, 'ratio': 8, 'sus': 9, 'cheh': 10, 'flop': 11, 'nwar': 12, 'con': 13, 'masterclass': 14}

# Couleurs :
bleu = 0x2BE4FF       #Normal
vert = 0x00FF66       #Unban/unmute/free
rouge = 0xFF2525      #Ban/mute/goulag
orange = 0xFFAA26     #Erreur

# id des channels:
logs_channel_id = 971870035624726628
errors_channel_id = 1004319125587378186


# ------------ FONCTIONS ------------ #

def is_vipe(id):
    return id == 691380397673545828

# Commande activée/désactivée
def check_command(guild_id, command_name):
    command_id = liste_commandes[command_name]
    result = database_handler.get_command(guild_id, command_id)
    if result == []:
        return True
    else:
        value = list(result[0])
        if value[0] == 1:
            return True
        else:
            return False

# Vérification de la hiérarchie des rôles

def check_hierarchy(member1 : discord.Member, member2 : discord.Member) -> bool:
    if member2.top_role <= member1.top_role:
        return False
    return True


# ----------COMMANDES---------#



@bot.command()
async def restart(ctx):
    if is_vipe(ctx.author.id):
        channel = bot.get_channel(logs_channel_id)
        msg = await channel.send("restarting cogs... :orange_circle:")
        await bot.reload_extension('commandes_base')
        await bot.reload_extension('commandes_admin')
        await bot.reload_extension('commandes_troll')
        await bot.reload_extension('chads')
        await channel.send("restart cogs :green_circle:")






@bot.command()
async def donneheurefdp(ctx):
    await ctx.send(str(str(t.localtime(t.time())[3]) + 'h' + str(t.localtime(t.time())[4])))







# ------------------| EVENTS |------------------#


# quoi/feur, oui/stiti, non/bril

@bot.listen()
async def on_message(message: discord.Message):
    if not isinstance(message.channel, discord.channel.DMChannel):
        if check_command(message.guild.id, 'feur'):
            if message.author != bot.user:
                message2 = str(message.content)
                message2 = message2.lower()
                out = re.sub(r'[^\w\s]','',message2)
                if out.endswith("quoi") or out.endswith("quoi "):
                    await message.reply("feur")
                elif out.endswith("non") or out.endswith("non "):
                    await message.reply("bril")
                elif out.endswith("oui") or out.endswith("oui "):
                    await message.reply("stiti")

# Gestion des erreurs :

@bot.event
async def on_command_error(ctx, error):
    if database_handler.check_testmod()[0][0] == 0:
        if isinstance(error, commands.MissingRequiredArgument):
            embed1 = discord.Embed(description = "il manque un argument là :x:", color = 0xFFAA26)
            await ctx.send(embed = embed1)
        elif isinstance(error, commands.MissingPermissions):
            embed2 = discord.Embed(description = "nan tu peux pas dsl :x:", color = 0xFFAA26)
            await ctx.send(embed = embed2)
        elif isinstance(error, commands.CommandNotFound):
            embed3 = discord.Embed(description = "Cette commande n'existe pas :x:", color = 0xFFAA26)
            await ctx.send(embed = embed3)
        elif isinstance(error, commands.UserInputError):
            embed4 = discord.Embed(description = "réessaye ça a pas marché là :x:", color = 0xFFAA26)
            await ctx.send(embed = embed4)
        elif isinstance(error, commands.PrivateMessageOnly):
            embed5 = discord.Embed(description = "ça marche que en dm ça :x:", color = 0xFFAA26)
            await ctx.send(embed = embed5)
        elif isinstance(error, commands.NoPrivateMessage):
            embed6 = discord.Embed(description = "ça marche pas en dm dsl :x:", color = 0xFFAA26)
            await ctx.send(embed = embed6)
        elif isinstance(error, commands.BotMissingPermissions):
            embed7 = discord.Embed(description = "g pas les perms pour faire ça :x:", color = 0xFFAA26)
            await ctx.send(embed = embed7)
        elif isinstance(error, commands.MissingRole):
            embed8 = discord.Embed(description = "t'as pas les rôles pour ça dsl :x:", color = 0xFFAA26)
            await ctx.send(embed = embed8)
        elif isinstance(error, commands.CommandOnCooldown):
            pass
        else:
            embed10 = discord.Embed(description = "y'a une erreur mais je sais pas trop quoi :x:", color = orange)
            await ctx.send(embed = embed10, delete_after=5)
            l = traceback.format_exception(type(error), error, error.__traceback__)
            channel = bot.get_channel(errors_channel_id)
            
            for i in l:
                await channel.send(f"`{i}`")
            
    else:

        l = traceback.format_exception(type(error), error, error.__traceback__)
        msg = "Erreur venant du testmod:\n`"
        for i in l:
            msg += i
        channel = bot.get_channel(errors_channel_id)
        msg += "`"
        await channel.send(msg)

        


@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(logs_channel_id)

    await channel.send(f"nouveau serveur : {guild.name}")

print(token_k)
bot.run(token_k)



