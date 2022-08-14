# gestion discord
import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *

# autres modules
import time as t
import random as rd
import re
from datetime import timedelta
import traceback
import sys
import os

# imports cogs
import commandes_troll
from commandes_troll import CommandesTroll
from commandes_admin import CommandesAdmin
from commandes_base import CommandesBase
from chads import CommandsChads
from chads2 import CommandsChads2
from token_k import token_kowalsky
from version_k import version

# database
from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")

# gestion discord 2
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = "k.", intents = intents)
bot.remove_command("help")
slash = SlashCommand(bot)

# démarrage du bot

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
    a1 = discord.Activity(name = f"{len(bot.guilds)} serveurs", type = discord.ActivityType.watching)
    a2 = discord.Activity(name = f"k.help", type = discord.ActivityType.playing)
    a3 = discord.Activity(name = f"k.invite | k.support", type = discord.ActivityType.playing)
    activities = [a1, a2, a3]
    await bot.change_presence(activity=rd.choice(activities))

# Boucle de redémarrage des cogs
@tasks.loop(seconds = 50)
async def check_restart_cogs():
    if t.localtime(t.time())[3] == 0:
        if t.localtime(t.time())[4] == 0:
            restart_cogs.start()
            check_restart_cogs.stop()

@tasks.loop(hours=24)
async def restart_cogs():
    bot.reload_extension('commandes_bases')
    bot.reload_extension('commandes_admin')
    bot.reload_extension('commandes_troll')
    bot.reload_extension('chads')
    bot.reload_extension('chads2')
    channel = bot.get_channel(logs_channel_id)
    await channel.send("restart cogs :green_circle:")




#----------------| INFOS |-----------------#

# Liste des commandes désactivables :
liste_commandes = commandes_troll.liste_commandes

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
        bot.reload_extension('commandes_base')
        bot.reload_extension('commandes_admin')
        bot.reload_extension('commandes_troll')
        bot.reload_extension('chads')
        channel = bot.get_channel(logs_channel_id)
        await channel.send("restart cogs :green_circle:")



# Activation / désactivation de commandes
@bot.command()
@commands.has_permissions(administrator = True)
async def activo(ctx, command_name):
    command_id = liste_commandes[command_name]
    database_handler.on(ctx.guild.id, command_id)
    # création de l'embed
    embed = discord.Embed(title = "Commande activée mon reuf :white_check_mark:", color = vert)
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(administrator = True)
async def desactivo(ctx, command_name):
    command_id = liste_commandes[command_name]
    database_handler.off(ctx.guild.id, command_id)
    # création de l'embed
    embed = discord.Embed(title = "Commande désactivée mon reuf :white_check_mark:", color = vert)
    await ctx.send(embed = embed)

@bot.command()
async def check(ctx, command_name):
    result = check_command(ctx.guild.id, command_name)
    if result == True:
        embed = discord.Embed(title = "Ici c'est activé :sunglasses:", color = bleu)
        await ctx.send(embed = embed)
    else:
        embed = discord.Embed(title = "Ici c'est désactivé :pensive:", color = bleu)
        await ctx.send(embed = embed)


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
            await ctx.send(embed = embed10)
            l = traceback.format_exception(type(error), error, error.__traceback__)
            msg = "`"
            for i in l:
                msg += i
            channel = bot.get_channel(errors_channel_id)
            msg += "`"
            await channel.send(msg)
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



bot.load_extension("commandes_base")
bot.load_extension("commandes_admin")
bot.load_extension("commandes_troll")
bot.load_extension("chads")
bot.load_extension("chads2")
bot.run(token_kowalsky)



