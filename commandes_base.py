import discord
from discord.ext import commands
import time as t
import random as rd
#from discord_slash import ButtonStyle, SlashCommand
#from discord_slash.utils.manage_components import *
from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")

intents = discord.Intents.default()
intents.members = True

from version_k import version

def is_vipe(id):
    return id == 691380397673545828

def setup(bot):
    bot.add_cog(CommandesBase(bot))


# ------------------- COMMANDES ---------------#

class CommandesBase(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #self.version = version

    @commands.command()
    async def help(self, ctx, *, theme = None):
        # Aide générale
        if theme == None:
            file = discord.File("/home/container/Pictures/kowalsky_lunettes.png", filename = "kowalskypp.png")
            msg = """> `help` : tsais la commande de base pour l'aide
            > `help troll` : là c'est pour afficher les commandes stylées :sunglasses:
            > `help chad` : affiche l'aide pour les chads
            > `serverinfo` : affiche des infos sur le serv mais on s'en fout
            > `say <truc>` : ça dit le truc
            > `support` : envoie le lien du serveur d'aide
            > `invite` : envoie un lien d'invitation du bot
            > `ping` : affiche la latence du bot
            > `suggestion` : envoie une suggestion aux devs (ne fonctionne qu'en dm avec le bot)
            > `activo <commande>` : active la commande sur le serveur (commandes désactivables : csc, randomping, ph, tg, fonction quoi/feur, saydm, haagrah, ratio, sus, cheh, flop, nwar, con, masterclass)
            > `desactivo <commande>` : désactive la commande sur le serveur (mêmes commandes que `activo`)"""
            embed = discord.Embed(title = "**Aide de Kowalsky**", color = bleu)
            embed.set_thumbnail(url = "attachment://kowalskypp.png")
            embed.add_field(name = "Important", value = "<exemple> = argument requis, (exemple) = argument optionnel", inline = False)
            embed.add_field(name = "Commandes", value = msg, inline = False)
            embed.set_footer(text = "version actuelle : " + version)
            await ctx.send(embed = embed, file = file) 

        # Aide troll
        elif theme == "troll":
            file = discord.File("/home/container/Pictures/kowalsky_lunettes.png", filename = "kowalskypp.png")

            embed = discord.Embed(title = "**Commandes stylées :sunglasses:**", color = bleu)
            msg = """> `tg <membre>`
            > `coucou`
            > `ph`
            > `randomping`
            > `matchup`
            > `stylé`
            > `csc`
            > `haagrah`
            > `random`
            > `sus`
            > `cheh`
            > `ratio`
            > `flop`
            > `nwar`
            > `k`
            > `con`
            > `masterclass`
            et d'autres qui arrivent :sunglasses:"""
            embed.set_thumbnail(url = "attachment://kowalskypp.png")
            embed.add_field(name = "Important", value = "<exemple> = argument requis, (exemple) = argument optionnel\n\nPas d'infos sur ce que font les commandes, à vous de le découvrir", inline = False)
            embed.add_field(name = "Commandes", value = msg, inline = False)
            embed.set_footer(text = "version actuelle : " + version)
            await ctx.send(embed = embed, file = file)

        # Aide chads
        elif theme == "chad" or theme == "chads":
            file = discord.File("/home/container/Pictures/kowalsky_lunettes.png", filename = "kowalskypp.png")
            embed = discord.Embed(title = "Aide chads", color = bleu)
            embed.set_thumbnail(url = "attachment://kowalskypp.png")
            msg = """> `collection` : affiche ta collection de Chads
            > `getchad` : récupère tes deux Chads du jour ! slowmode: 1j
            > `mychad <rang>` : affiche le Chad du rang en question
            > `upgrade <rang>` : si t'as plus de 5 Chads de ce rang, il s'améliore au rang d'au-dessus
            > `trade <mention>` : permet d'échanger un Chad avec le mec mentionné
            > `chadsong` : joue la douce mélodie des gigachads pour satisfaire tes tympans
            > `chadtips` : affiche un conseil pour devenir un gigachad

            > `routedeschads` : affiche des infos sur la Route des Chads
            > `start` : permet de démarrer la Route des Chads
            > `avance` : une fois par jour, avance dans ta Route des Chads
            > `leaderboard` : affiche les différents classements du bot
            """
            embed.add_field(name = "Présentation", value = "Le Chad Game est un jeu de collection de chads, avec 10 rangs de chads différents, tous plus rares les uns que les autres !\n\nLe but, c'est de tous les avoir, jpense t'avais compris", inline = False)
            embed.add_field(name = "Commandes", value = msg)
            embed.set_footer(text = "version actuelle : " + version)
            await ctx.send(embed = embed, file = file)

    @commands.command()
    async def post(self, ctx, *, msg):
        if is_vipe(ctx.author.id):
            channels = database_handler.get_channels()
            msg = str(msg + "\n\n disponible à partir de minuit")
            embed = discord.Embed(title = "Mise à jour", color = bleu, description = msg)
            embed.set_footer(text = f"version actuelle : {version}")
            for i in channels:
                try:
                    chan = self.bot.get_channel(i[0])
                    await chan.send(embed = embed)
                except:
                    pass
            await ctx.send("message posté")
        else:
            await ctx.send("t'as pas le droit dsl")
    
    # Suggestion :

    @commands.command()
    @commands.dm_only()
    async def suggestion(self, ctx, *, texte = None):
        channel = self.bot.get_channel(944564263652057158)

        def checkMessage(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel

        if texte == None:
            await ctx.send(f"{ctx.author.mention}, quel est le contenu de ta suggestion ? Réponds 'cancel' pour annuler")
            texte = await self.bot.wait_for("message", timeout = 60, check = checkMessage)

            embed = discord.Embed(title = "Ta suggestion a été envoyée !", color = 0x2BE4FF)
            await ctx.send(embed = embed)
            await channel.send(f"suggestion de {ctx.author.name} : {texte.content}")

        elif texte == "cancel" or texte == "Cancel":
            await ctx.send("Commande annulée")
        else:
            embed = discord.Embed(title = "Ta suggestion a été envoyée !", color = 0x2BE4FF)
            await ctx.send(embed = embed)
            await channel.send(f"suggestion de {ctx.author.name} : {texte}")



    # Bot info :

    @commands.command(aliases = ['infobot'])
    async def botinfo(self, ctx):
        txt = """**Développeur :** c'est vipe le bg

        **Création :** janvier 2022 ambiance covid

        **Premiers testeurs :** les bg de CRFR bis, vous savez qui vous êtes

        **Graphistes officiels :** dori et zamass, merci à eux

        **Chad Kings :** Nayde fut le premier à réunir les 10 chads, near et pépito furent les premiers à atteindre le Temple des Chads.

        **Information importante :** le bot est extrêmement raciste"""
        embed = discord.Embed(title = "Infos sur le bot", color = bleu, description = txt)
        embed.set_footer(text = "version actuelle : " + version)
        await ctx.send(embed = embed)


    # Ping:
    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        ping = int(self.bot.latency*1000)
        if ping <= 50:
            msg = "||ça bombarde youhou||"
        elif ping <= 100:
            msg = "||on lag un peu mais oklm||"
        else:
            msg ="||wtf c'est quoi ce lag jsuis sur neptune ou quoi||"
        await ctx.send(f"Latence : {ping} ms {msg}")


     # Serverinfo :

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        server = ctx.guild
        nbTextChans = len(server.text_channels)
        if nbTextChans == 1:
            txtTextChans = "1 salon écrit"
        else:
            txtTextChans = f"{nbTextChans} salons écrits"
        nbVoiceChans = len(server.voice_channels)
        if nbVoiceChans == 1:
            txtVoiceChans = f"1 salon vocal"
        else:
            txtVoiceChans = f"{nbVoiceChans} salons vocaux"
        servDescription = server.description
        nbMembres = server.member_count
        nom = server.name

        #Création de l'embed:
        embed = discord.Embed(title = f"**Informations de {server.name}**", color = bleu)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.add_field(name = "Membres", value = nbMembres, inline = False)
        embed.add_field(name = "Salons textuels", value = txtTextChans, inline = False)
        embed.add_field(name = "Salons vocaux", value = txtVoiceChans, inline = False)
        await ctx.send(embed = embed)


    # Say :

    @commands.command()
    async def say(self, ctx, *, texte):
        await ctx.message.delete()
        if texte == "@everyone":
            await ctx.send("nan c pa koul")
        else:

            await ctx.send(texte)


    # Rate :

    @commands.command()
    async def rate(self, ctx, *texte):
        note = rd.randint(0,10)
        texte2 = " ".join(texte)
        await ctx.send(f"Je note `{texte2}` {note}/10")





    # Support :

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(title = "tiens stv ya un serveur d'aide", color = bleu, description = "[clique ici mon reuf](https://discord.gg/f2xBTAxB6W)")
        await ctx.send(embed = embed)


    # Invite :

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title = "Tu veux m'ajouter à un serveur ?", color = bleu, description = "[clique ici mon reuf](https://discord.com/api/oauth2/authorize?client_id=926864538681368626&permissions=8&scope=bot)")
        await ctx.send(embed = embed)


    # Update:

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def update(self, ctx, y = None, channel: discord.TextChannel = None):

        def checkMessage(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel

        if y == None:
            embed = discord.Embed(color = bleu)
            embed.add_field(name = "Mises à jour", value = """`k.update follow <salon>` -> permet de recevoir un message dans un salon à chaque maj

`k.update unfollow` -> arrête de suivre les mises à jour

Vous ne pouvez suivre les mises à jour que dans un salon par serveur""")
            await ctx.send(embed = embed)
        elif y == "follow":
            if database_handler.is_following(ctx.guild.id):
                await ctx.send("Ce serveur suit déjà les mises à jour")
            else:
                database_handler.add_channel(ctx.guild.id, channel.id)
                await ctx.send(f"Les mises à jour du bot seront publiées dans {channel.mention} !")

        elif y == "unfollow":
            database_handler.delete_channel(ctx.guild.id)
            await ctx.send('Les mises à jour ne seront plus publiées dans ce serveur')






    """
    @commands.command()
    async def trade(self, ctx, member2 : discord.Member):

        guild = ctx.guild
        member = ctx.author
        if member != member2:
            def checkMessage(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel

            def checkMessage2(message):
                return member == ctx.author

            await ctx.send(f"tu veux donner un chad de quel rang à **{member2.name}** ?")
            chad_given = await self.bot.wait_for("message", timeout = 20, check = checkMessage)
            chad_given = int(chad_given.content)
            if chad_given > 10 or chad_given < 1:
                await ctx.send("ce rang de chad n'existe pas")
                return

            await ctx.send("tu veux recevoir un chad de quel rang ?")
            chad_asked = await self.bot.wait_for("message", timeout = 20, check = checkMessage)
            chad_asked = int(chad_asked.content)
            if chad_asked > 10 or chad_asked < 1:
                await ctx.send("ce rang de chad n'existe pas")
                return

            member_col = database_handler.get_collection(member.id)
            member2_col = database_handler.get_collection(member2.id)
            if has_chad(member_col, chad_given) and has_chad(member2_col, chad_asked):
                pos1 = chad_pos(member_col, chad_given)
                pos2 = chad_pos(member2_col, chad_asked)

                if (member_col[pos1][1] > 1) and (member2_col[pos2][1] > 1):
                    channel2 = await member2.create_dm()
                    embed = discord.Embed(title = "", color = bleu, description = f"veux tu donner un chad de **rang {chad_asked}** et recevoir un chad de **rang {chad_given}** de la part de **{member.name} **?\n\nréponds par `oui` pour accepter, et réponds n'importe quoi pour refuser")
                    embed.set_footer(text = "tu as 5 minutes pour répondre")
                    await channel2.send(embed = embed)

                    confirmation = await self.bot.wait_for('message', timeout = 300, check = checkMessage2)
                    confirmation = str(confirmation.content)
                    confirmation.lower()

                    await ctx.send(f"j'ai envoyé un dm à {member2.name} pour savoir s'il veut échanger, jte dm bientôt pour te dire s'il accepte ou pas", delete_after = 10)

                    if confirmation == "oui":
                        database_handler.remove_chad(member2.id, chad_asked)
                        if has_chad(member2_col, chad_given):
                            database_handler.add_chad(member2.id, chad_given)
                        else:
                            database_handler.add_new_chad(member2.id, chad_given)

                        database_handler.remove_chad(member.id, chad_given)
                        if has_chad(member_col, chad_asked):
                            database_handler.add_chad(member.id, chad_asked)
                        else:
                            database_handler.add_new_chad(member.id, chad_asked)
                        channel = await member.create_dm()
                        await channel.send(f"échange réussi ! {member2.name} t'a bien donné un chad de rang {chad_asked}, et tu as donné un chad de rang {chad_given} !")
                        await channel2.send(f"échange réussi ! {member.name} t'a bien donné un chad de rang {chad_given}, et tu as donné un chad de rang {chad_asked} !")

                    else:

                        channel = await member.create_dm()
                        await channel.send(f"échange refusé par {member2.name}")
                        await channel2.send(f"échange refusé")
                else:
                    await ctx.send("Vous avez pas assez de chads dsl")
            else:
                await ctx.send("vous avez pas les bons chads dsl")
        else:
            await ctx.send("ben bien sûr fais des échanges tout seul")
    """






# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur
