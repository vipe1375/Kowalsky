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

# imports cogs
import commandes_troll
import commandes_base
import chads
import commandes_admin
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
    bot.reload_extension('CommandesBase')
    bot.reload_extension('CommandesAdmin')
    bot.reload_extension('CommandesTroll')
    bot.reload_extension('CommandsChads')



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

# Fonctions aide goulag

async def getGoulagRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Goulag":
            return role
    return await createGoulagRole(ctx)

async def createGoulagRole(ctx):
    goulagRole = await ctx.guild.create_role(name = "Goulag")
    return goulagRole


# ----------COMMANDES---------#

# Help :

@bot.command(aliases = ['aide'])
async def help(ctx, *, theme = None):
    # Aide générale
    if theme == None:
        file = discord.File("/home/container/Pictures/kowalsky_lunettes.png", filename = "kowalskypp.png")
        embed = discord.Embed(title = "**Aide de Kowalsky**", color = bleu)
        embed.set_thumbnail(url = "attachment://kowalskypp.png")
        embed.add_field(name = "Important", value = "[exemple] = argument requis, (exemple) = argument optionnel", inline = False)
        embed.add_field(name = "k.help", value = "tsais la commande de base", inline = False)
        embed.add_field(name = "k.help troll", value = "là c les commandes stylées :sunglasses:", inline = False)
        embed.add_field(name = "k.help chad", value = "affiche l'aide pour les chads", inline = False)
        embed.add_field(name = "k.serverinfo", value = "des infos sur le serv mais on s'en fout", inline = False)
        embed.add_field(name = "k.say [truc]", value = "il dit le truc", inline = False)
        embed.add_field(name = "k.support", value = "envoie le lien du serveur d'aide", inline = False)
        embed.add_field(name = "k.invite", value = "envoie un lien d'invitation du bot", inline = False)
        embed.add_field(name = "k.ping", value = "affiche la mention du bot")
        embed.add_field(name = "k.suggestion", value = "envoie une suggestion concernant le bot (ne fonctionne que dans les dm du bot)")
        embed.add_field(name = "k.activo [command]", value = "active la commande sur le serveur (permissions : admin, commandes désactivables : csc, randomping, ph, tg, fonction quoi/feur, saydm, haagrah, ratio, sus, cheh, flop, nwar)", inline = False)
        embed.add_field(name = "k.desactivo [command]", value = "désactive la commande (mêmes commandes que activo, permissions : admin)", inline = False)
        embed.set_footer(text = "version actuelle : " + version)
        await ctx.send(embed = embed, file = file)

    # Aide troll
    elif theme == "troll":
        file = discord.File("/home/container/Pictures/kowalsky_lunettes.png", filename = "kowalskypp.png")

        embed = discord.Embed(title = "**Commandes stylées :sunglasses:**", color = bleu)
        embed.set_thumbnail(url = "attachment://kowalskypp.png")
        embed.add_field(name = "Important", value = "[exemple] = argument requis, (exemple) = argument optionnel\n\nPas d'infos sur ce que font les commandes, à vous de le découvrir", inline = False)
        embed.add_field(name = "Commandes", value = "\nk.tg [membre]\n\nk.coucou\n\nk.ph\n\nk.randomping\n\nk.matchup ou k.mu\n\nk.stylé\n\nk.csc\n\nk.haagrah\n\nk.random\n\nk.sus\n\nk.cheh\n\nk.flop\n\nk.nwar\n\nk.k\n\net d'autres qui arrivent...", inline = False)
        embed.set_footer(text = "version actuelle : " + version)
        await ctx.send(embed = embed, file = file)

    # Aide chads
    elif theme == "chad" or theme == "chads":
        file = discord.File("/home/container/Pictures/kowalsky_lunettes.png", filename = "kowalskypp.png")
        embed = discord.Embed(title = "Aide chads", color = bleu)
        embed.set_thumbnail(url = "attachment://kowalskypp.png")
        embed.add_field(name = "Présentation", value = "Le Chad Game est un jeu de collection de chads, avec 10 rangs de chads différents, tous plus rares les uns que les autres !\n\nLe but, c'est de tous les avoir, jpense t'avais compris", inline = False)
        embed.add_field(name = "k.collection", value = "Affiche ta collection de chads", inline = False)
        embed.add_field(name = "k.getchad", value = "Obtiens ton chad du jour ! slowmode : 1j", inline = False)
        embed.add_field(name = "k.mychad [rang du chad]", value = "affiche le chad du rang en question si tu l'as", inline = False)
        embed.add_field(name = "k.upgrade [rang]", value = "Si t'as plus de 5 chads de ce rang, tu perds 5 chads de ce rang et t'en gagne 1 du rang d'au-dessus", inline = False)
        #embed.add_field(name = "k.trade [membre avec qui échanger]", value = "permet d'échanger des chads avec quelqu'un dautre (si vous avez les chads que vous proposez bien entendu)")
        embed.add_field(name = "k.chadsong", value = "joue la douce mélodie des gigachads afin de satifaire vos tympans", inline = False)
        embed.add_field(name = "k.chadtips", value = "affiche un conseil pour devenir un gigachad", inline = False)
        embed.add_field(name = "k.topcol", value = "affiche un classement des collections des membres du serveur (faites `k.topcol g` pour avoir le classement général)", inline = False)
        embed.add_field(name = "k.start", value = "démarre ta Route des Chads", inline = False)
        embed.add_field(name = "k.avance", value = "avance dans ta Route des Chads ! slowmode : 1j", inline = False)
        embed.add_field(name = "k.routedeschads", value = "affiche des infos sur la Route des Chads", inline = False)
        embed.add_field(name = "k.leaderboard/k.lb",value = "affiche un classement de la route des chads dans le serveur (faites `k.lb g` pour afficher le classement général)", inline = False)
        embed.set_footer(text = "version actuelle : " + version)
        await ctx.send(embed = embed, file = file)


@bot.command()
async def restart(ctx):
    if commandes_admin.is_vipe(ctx.author.id):
        bot.reload_extension('CommandesBase')
        bot.reload_extension('CommandesAdmin')
        bot.reload_extension('CommandesTroll')



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



bot.add_cog(commandes_base.CommandesBase(bot))
bot.add_cog(commandes_troll.CommandesTroll(bot))
bot.add_cog(chads.CommandsChads(bot))
bot.add_cog(commandes_admin.CommandesAdmin(bot))
bot.run(token_kowalsky)



