import discord
from discord.ext import commands
import time as t
import random as rd
import asyncio
from PIL import Image

from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")

from select_menu import SelectView, choose_leaderboard
from buttons import trade_buttons

intents = discord.Intents.default()
intents.members = True


async def setup(bot):
    await bot.add_cog(CommandsChads(bot))

# INFOS
chads_adresses = {1: "/home/container/Pictures/chads/chad_1.jpg",
                 2: "/home/container/Pictures/chads/chad_2.jpeg",
                 3: "/home/container/Pictures/chads/chad_3.jpg",
                 4: "/home/container/Pictures/chads/chad_4.jpg",
                 5: "/home/container/Pictures/chads/chad_5.jpeg",
                 6: "/home/container/Pictures/chads/chad_6.jpeg",
                 7: "/home/container/Pictures/chads/chad_7.jpg",
                 8: "/home/container/Pictures/chads/chad_8.jpg",
                 9: "/home/container/Pictures/chads/chad_9.jpg",
                 10: "/home/container/Pictures/chads/chad_10.png"}

chads_ranks = {1: "Chad de rang 1",
              2: "Chad de rang 2",
              3: "chad de rang 3",
              4: "Chad de rang 4",
              5: "Chad de rang 5",
              6: "Chad de rang 6",
              7: "Chad de rang 7",
              8: "Chad de rang 8",
              9: "Chad de rang 9",
              10: "Chad de rang 10"}

chads_names = {1: "Chad",
              2: "Superchad",
              3: "Megachad",
              4: "Gigachad",
              5: "Alphachad",
              6: "Sismachad",
              7: "Suprachad",
              8: "Ultrachad",
              9: "Cosmic Chad",
              10: "vipe"}

chads_random = ["/home/container/Pictures/random_chads/chad1.png",
"/home/container/Pictures/random_chads/chad2.jpeg",
"/home/container/Pictures/random_chads/chad3.jpeg",
"/home/container/Pictures/random_chads/chad4.jpeg",
"/home/container/Pictures/random_chads/chad5.jpeg",
"/home/container/Pictures/random_chads/chad6.jpeg",
"/home/container/Pictures/random_chads/chad7.jpeg",
"/home/container/Pictures/random_chads/chad8.jpeg",
"/home/container/Pictures/random_chads/chad9.jpeg",
"/home/container/Pictures/random_chads/chad10.jpeg"]

chads_tips = [
    "tip n°1: *sommeil = perte de temps*",
    "tip n°2: *ne sois pas un beta simp*",
    "tip n°3: *n'écoute que la musique des giga chads*",
    "tip n°4: *mange du gravier pour entraîner ton estomac*",
    "tip n°5: *entraîne toi à boire ton urine pour la fin du monde*",
    "tip n°6: *n'argumente jamais, c'est aux autres de te comprendre*",
    "tip n°7: *ne doute jamais*",
    "tip n°8: *ne garde dans ton entourage que des giga chads, sépare toi de tous les autres*",
    "tip n°9: *ne regarde pas de porno*",
    "tip n°10: *affronte un ours à mains nues tous les matins pour te réveiller*",
    "tip n°11: *ne vas plus aux toilettes pour chier car toilettes = perte de temps*",
    "tip n°12: *mange du poney*",
    "tip n°13: *ajoute ce bot partout où tu peux afin de répandre les conseils chadiques partout*",
    "tip n°14: *fais 200 pompes par heure*",
    "tip n°15: *porte ta voiture pour aller travailler car voiture = facilité = pas chad*",
    "tip n°17: *prends la place du chauffeur quand tu prends le bus car chauffeur = facilité = pas chad*",
    "tip n°18: *chie sur ta table en cours pour montrer ta domination*",
    "tip n°18: *n'achète pas de viande, élève puis tue puis coupe puis fais cuire une vache*",
    "tip n°19: *ne joue pas méga chevalier*",
    "tip n°20: *fais du sport à chaque fois que tu ne fais pas de sport*",
    "tip n°21: chat > chien car 'chat' ressemble à 'chad'",
    "tip n°22: n'adopte pas un animal mais deviens son ami, car relation de supériorité envers les animaux = pas chad"
]

actions = ["mange", "bois", "urine", "casse", "explose", "chie", "construis", "cuisine", "regarde", "suce", "lèche", "baise", "sois"]
sujets = ["un gay (no offense les lgbt)", "ton père", "ta mère", "ta sœur", "ton chat", "un ours", "un requin", "du gravier", "une pierre", "de la cocaïne", "une fusée", "Kim Jong Un", "du caca"]
compléments = ["tous les matins", "7 fois par jour", "à Noël", "pour dénazifier l'Ukraine", "pour prouver ta supériorité", "quand tu as faim", "au lieu de te pignouf", "aux toilettes", "à l'école", "devant des enfants", "pendant que tu dors"]

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur

emojis_chads = {1 : "<:chad1:975871604368228372>",
2 : "<:chad2:975872145618001920>",
3 : "<:chad3:975872184427900948>",
4 :"<:chad4:975872815901335573>",
5 : "<:chad5:975873049708605550>",
6 : "<:chad6:975873082294165594>",
7 : "<:chad7:975873206508453948>",
8 : "<:chad8:975873275995508776>",
9 : "<:chad9:975873595995734036>",
10: ""}


# embed avec image :
#file = discord.File(fp = c_ad, filename = "image.png")
#embed.set_image(url="attachment://image.png")

# FONCTIONS



def has_chad(result, index):
    if result == None or result == []:
        return False
    else:
        for i in range(len(result)):
            if result[i][0] == index:
                return result[i][1] > 0
        return False

def has_chad_bis(result, index):
    if result == None or result == []:
        return False
    else:
        for i in range(len(result)):
            if result[i][0] == index:
                return result[i][1] >= 0
        return False

def chad_pos(col, ind):
    for i in range(len(col)):
        if col[i][0] == ind:
            return i

    return None







# COMMANDES

class CommandsChads(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def topcol(self, ctx):
        await ctx.send("Maintenant tout est dans la commande `k.lb` mon reuf")

# collection :

    @commands.command(aliases = ['col', 'coll'])
    async def collection(self, ctx, member : discord.Member = None):

        if member == None:
            result = database_handler.get_collection(ctx.author.id)
            if result == None or result == []:
                await ctx.send("t'as pas encore de chads")

            else:
                embed = discord.Embed(title = "", color = bleu)

                txt = ""
                for i in range(len(result)):
                    chad_id = result[i][0]
                    chad_number = result[i][1]
                    if chad_number > 0:
                        txt += f"{chads_ranks[chad_id]} : **{chads_names[chad_id]}** x{chad_number} {emojis_chads[chad_id]}\n"
                embed.add_field(name = "Tes chads", value = txt)
                await ctx.send(embed = embed)


        else:
            result = database_handler.get_collection(member.id)
            if result == None or result == []:
                await ctx.send(f"{member.display_name} n'a pas encore de chads")
            else:
                embed = discord.Embed(title = "", color = bleu)
                txt = ""
                for i in range(len(result)):
                    chad_id = result[i][0]
                    chad_number = result[i][1]
                    if chad_number > 0:
                        txt += f"{chads_ranks[chad_id]} : **{chads_names[chad_id]}** x{chad_number} {emojis_chads[chad_id]}\n"
                embed.add_field(name = f"Chads de {member.name}", value = txt)
                await ctx.send(embed = embed)



    @commands.command()
    async def mychad(self, ctx, index):
        result = database_handler.get_collection(ctx.author.id)
        if result == None or result == []:
            await ctx.send("t'as pas encore de chads")
        else:
            index = int(index)
            if index > 10:
                await ctx.send("ce chad n'existe pas")
            else:
                if has_chad(result, index):
                    file = discord.File(str(chads_adresses[index]))
                    await ctx.send("Voilà ton chad :", file = file)
                else:
                    await ctx.send("t'as pas ce chad dsl")

    

    @commands.command()
    async def upgrade(self, ctx, *, rank):
        member = ctx.author
        rank = int(rank)
        collection = database_handler.get_collection(member.id)
        if has_chad(collection, rank):
            pos = chad_pos(collection, rank)
            if collection[pos][1] > 5:
                database_handler.upgrade_chad(member.id, rank)
                if has_chad(collection, rank+1):
                    database_handler.add_chad(member.id, rank + 1, 1)
                else:
                    database_handler.add_new_chad(member.id, rank + 1)
                await ctx.send(f"bien joué ! chad amélioré au rang {rank+1} !")
                database_handler.update_chadscore(ctx.author.id)
            else:
                await ctx.send("t'en a pas assez dsl, il t'en faut au moins 6")
        else:
            await ctx.send("t'as pas ce chad dsl")


    

    @commands.command()
    async def chadsong(self, ctx):
        file = discord.File("/home/container/Pictures/chads/chadsong.mp4")
        await ctx.send(file = file)

    

    @commands.command()
    async def routedeschads(self, ctx):
        desc = """

        La Route des Chads est la quête ultime de tout être qui prétend au titre de Chad.

        Elle consiste en un voyage jusqu'au sommet de la légendaire Chad Mountain, voyage peuplé de dangers et de mystères. Le voyageur doit passer avec succès les 20 étapes du voyage, afin de pouvoir accéder au sommet de la montagne et ainsi devenir un Chad.

        Tu veux tenter ta chance ? Alors choisis un des Chads de ta collection et fais en sorte qu'il passe les étapes jusqu'au sommet. Si ton Chad parvient à passer à l'étape suivante, tant mieux. Mais si par malheur il n'y parvient pas, alors l'aventure s'arrête pour lui, et ce Chad sera perdu à tout jamais.

        Une fois là-haut, tu auras la Médaille de Chad.

        Bonne chance mon reuf.

        *indice : plus ton Chad est de rang élevé, plus il aura de chances de réussir les étapes.*"""
        embed = discord.Embed(title = "Route des chads", description= desc, color = bleu)
        await ctx.send(embed = embed)


    @commands.command()
    async def start(self, ctx):

        user = ctx.author
        if database_handler.get_etape(user.id) == [] or database_handler.get_etape(user.id) == None:
            database_handler.new_etape(user.id)
            await ctx.send("gg ! Tu viens de commencer la Route des Chads ! Bonne chance ! \n\nAstuce : fais `k.avance` pour tenter de passer à l'étape suivante.")
        else:
            await ctx.send("T'as déjà commencé la Route des Chads")


    
    @commands.command()
    async def getmedal(self, ctx):
        if database_handler.is_finished(ctx.author.id):
            fond = Image.open('Pictures/chadroad/medal.png')
            await ctx.author.avatar.save(f"pp_{ctx.author.id}")
            pp = Image.open(f"pp_{ctx.author.id}")
            file = discord.File("/home/container/Pictures/chadroad/medal.png")
            await ctx.send("Voilà ta médaille :", file = file)
        else:
            await ctx.send("Tu n'as pas encore gagné la médaille des Chads dsl")

    


    @commands.command(aliases = ['lb'])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        
        # Embed avec menu select
        embed1 = discord.Embed(title = "Choix du classement", description = "Choisis le classement à afficher avec le menu en-dessous mon reuf", color = bleu)

        await ctx.send(embed = embed1, view=SelectView(self.bot))

        
    @commands.command()
    async def trade(self, ctx, member2 : discord.Member):

        guild = ctx.guild
        member = ctx.author
        if member != member2:
            def checkMessage(message):
                return message.author == ctx.message.author and ctx.message.channel == message.channel



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

                # DM du second membre

                if (member_col[pos1][1] > 1) and (member2_col[pos2][1] > 1):

                    channel2 = await member2.create_dm()
                    embed = discord.Embed(title = "", color = bleu, description = f"veux tu donner un chad de **rang {chad_asked}** et recevoir un chad de **rang {chad_given}** de la part de **{member.name} **?")
                    embed.set_footer(text = "tu as 5 minutes pour répondre")

                    await ctx.send(f"j'ai envoyé un dm à {member2.name} pour savoir s'il veut échanger, jte dm bientôt pour te dire s'il accepte ou pas", delete_after = 10)

                    await channel2.send(embed = embed, view = trade_buttons(member1=member, member2=member2, member1_col=member_col, member2_col=member2_col, chad_given=chad_given, chad_asked=chad_asked))

                else:
                    await ctx.send("Vous avez pas assez de chads dsl")
            else:
                await ctx.send("vous avez pas les bons chads dsl")
        else:
            await ctx.send("ben bien sûr fais des échanges tout seul")
