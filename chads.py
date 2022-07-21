import discord
from discord.ext import commands
import time as t
import random as rd
import asyncio

from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")

intents = discord.Intents.default()
intents.members = True

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

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur

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

def can_pass(c_id: int, etape: int) -> bool:
    n = rd.randint(0,100)
    if etape == 1:
        return True
    elif etape == 2:
        return n <= 89+c_id
    elif etape == 3:
        return n <= 79 + 2*c_id
    elif etape == 4:
        return n <= 69 + 3*c_id
    elif etape == 5:
        return n <= 59 + 4*c_id
    elif etape == 6:
        return True
    elif etape == 7 or etape == 8:
        return n <= 50*c_id
    elif etape == 9:
        return True
    elif etape == 10:
        return n <= 40 + 5*c_id
    elif etape == 11 or etape == 12:
        return n <= 40 + (1.48**c_id)
    elif etape == 13:
        return n <= 30 + (1.506**c_id)
    elif etape == 14 or etape == 15 or etape == 16:
        return n <= 20 + 1.53**c_id
    elif etape == 17:
        return n <= 10 + 1.53**c_id
    elif etape == 18:
        return n <= 10 + 1.52**c_id
    elif etape == 19:
        return True
    elif etape == 20:
        return True
    elif etape == 190:
        return False

async def situation(ctx, sit):
    msg = ""
    if sit == 1:
        msg = "Ptite rando tranquilou jusqu'à la forêt"
        img = discord.File(fp = "/home/container/Pictures/chadroad/chadmontagne.jpg", filename = "image.png")
        p = "Ton Chad a fait une ptite balade pépouze, tu atteins donc **l'étape 2 !**"
        f = p
    
    elif sit == 2:
        msg = "Ton Chad entre dans la forêt, quand soudain un écureuil méchant se dresse sur sa route ! Ton Chad doit lui niquer sa mère ! Va-t-il réussir ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/ecureuil.jpeg", filename = "image.png")
        p = "C'est bon l'écureuil s'est fait niquer sa mère, ton Chad est pas une victime ! Tu arrives à **l'étape 3 !**"
        f = "C'est un peu une victime ton Chad, il s'est fait niquer sa mère par un écureuil, du coup il est mort... Tu restes à l'étape 2"

    elif sit == 3:
        msg = "Tandis que ton Chad marche dans la forêt, il croise Bambi qui a trop le seum de s'être fait buter sa daronne, du coup il veut se venger sur ton Chad ! Va-t-il s'en sortir ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/bambi.jpeg", filename = "image.png")
        p = "Bambi s'est fait péter les genoux il a encore plus le seum, mais au moins tu passes à **l'étape 4 !**"
        f = "Bambi et son seum ont niqué ton Chad, malheureusement il meurt, et tu restes à l'étape 3..."

    elif sit == 4:
        msg = "wesh ya un ours dans la forêt, il veut grailler ton Chad ! Va-t-il péter le cul à l'ours ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/ours.jpg", filename = "image.png")
        p = "Quel goat ce Chad, il a graillé l'ours ! Tu passes à **l'étape 5 !**"
        f = "L'ours avait vraiment la dalle, il a mangé ton Chad... tu restes à l'étape 4, pas de bol"

    elif sit == 5:
        msg = "Ton Chad arrive devant une rivière, quand un crabe surgit d'entre deux pierres ! Ton Chad va-t-il péter le crabe en deux ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/crabe.jpeg", filename = "image.png")
        p = "Le crabe s'est fait fracasser ses huit pattes, tu passes donc à **l'étape 6 !**"
        f = "Le crabe a pincé les couilles de ton Chad et il en est mort, tu restes donc à l'étape 5..."

    elif sit == 6:
        msg = "Ton Chad doit traverser la rivière, mais il sait pas nager ! Du coup, il va affronter un arbre pour construire un bateau ! Va-t-il vaincre l'arbre ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/arbre.jpeg", filename = "image.png")
        p = "Wow c'est un Chad quand même, il va pas perdre un 1v1 contre un arbre wsh... Tu passes à **l'étape 7 !**"
        f = p

    elif sit == 7:
        msg = "Pendant que ton Chad traverse la rivière, un requin l'attaque pour le faire couler ! Bizarre la rivière un peu... Ton Chad va-t-il réussir à défendre son bateau ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/requin.jpeg", filename = "image.png")
        p = "Ton Chad a courageusement défendu son navire ! Tu passes à **l'étape 8 !**"
        f = "Le requin a graillé ton Chad, tu restes à l'étape 7..."
    
    elif sit == 8:
        msg = "Ton Chad a traversé la rivière, mais une horde de flamands roses l'attaque ! Va-t-il manger du flamand rose ce soir ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/flamands_roses.jpeg", filename = "image.png")
        p = "C'est bon wesh c'est des flamands roses, un peu de respect pour ton Chad quand même, tu passes à **l'étape 9 !**"
        f = "C'est les flamands roses qui vont manger du Chad ce soir... tu restes à l'étape 8"

    elif sit == 9:
        msg = "Ton Chad a passé la rivière, maintenant il doit traverser un ravin. POur le moment c'est ez :sunglasses:"
        img = discord.File(fp = "/home/container/Pictures/chadroad/ravin.jpeg", filename = "image.png")
        p = "Tranquille il traverse le ravin ! Tu passes à **l'étape 10 !**"
        f = p

    elif sit == 10:
        msg = "Pour traverser le ravin, ton Chad doit passer sur un pont de corde qui pourrait casser à tout instant ! Va-t-il réussir sans finir en chadatouille (ratatouille de chad) en bas du ravin ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/pont.jpeg", filename = "image.png")
        p = "Ton Chad a cavalé vers l'autre côté comme Pierre Ménès vers le McDo ! Tu passes à **l'étape 11 !**"
        f = "Ton Chad a pas couru assez vite, le pont s'est écroulé... tu restes à l'étape 10"

    elif sit == 11:
        msg = "Ton Chad a traversé le pont, mais un terrible scorpion mortel l'attaque ? Va-t-il niquer sa mère au scorpion ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/scorpion.jpeg", filename = "image.png")
        p = "Le scorpion est aplati sous un pied de Chad, et tu passes à **l'étape 12 !**"
        f = "Le scorpion a piqué ton Chad et il a succombé... tu restes à l'étape 11"

    elif sit == 12:
        msg = "Ton Chad a vaincu le scorpion, mais pour sortir du ravin, il doit escalader une paroi de pierre ! Va-t-il réussir sans tomber ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/paroi.jpg", filename = "image.png")
        p = "Ton Chad a grimpé le mur comme s'il était Spiderman, tu passes à **l'étape 13 !**"
        f = "Ton Chad s'est misérablement éclaté sur le sol en bas du mur... tu restes à l'étape 12"

    elif sit == 13:
        msg = "Ton Chad est maintenant dans une forêt enneigée, et il se caille le cul ! Va-t-il survivre au froid ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/foret.jpeg", filename = "image.png")
        p = "L'idée de se savoir aussi proche du but a réchauffé le cœur de ton Chad, et il a résisté au froid ! Tu passes à **l'étape 14 !**"
        f = "Malheureusemen, ton Chad a vu ses couilles rétrécir à cause du froid, et il en est mort de désespoir... Tu restes à l'étape 13"

    elif sit == 14:
        msg = "Pendant que ton Chad traverse la forêt enneigée, un puma le défie dans un octogone ! Ton Chad va-t-il battre le puma comme McGregor ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/puma.jpeg", filename = "image.png")
        p = "Ton Chad a mis le puma KO d'un coup spécial de la couille gauche, tu passes à **l'étape 15 !**"
        f = "Le puma a mis ton Chad KO d'un coup spécial de sa couille droite, tu restes à l'étape 14..."

    elif sit == 15:
        msg = "Tu te sens trop frais d'être arrivé jusqu'ici, donc ton Chad doit construire un traîneau pour transporter ton ego ! Va-t-il construire un traîneau suffisamment résistant ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/traineau.jpeg", filename = "image.png")
        p = "Ton Chad a réussi à contruire un traîneau grâce à ses skills innées en menuiserie ! Tu passes à **l'étape 16 !**"
        f = "Malheureusement, t'avais trop pris la grosse tête pour que ton ego soit transportable, tu restes à l'étape 15..."

    elif sit == 16:
        msg = "Pour sortir de la forêt enneigée, ton Chad doit escalader une cascade gelée ! Ses doigts musclés vont-ils le mener en haut ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/cascade.jpeg", filename = "image.png")
        p = "Ton Chad a pensé à la légendaire Musique des Chads pour se donner du courage, et il a grimpé jusqu'au sommet ! Tu passes à **l'étape 17 !**"
        f = "Ton Chad a glissé et s'est empalé sur une stalagmite de glace, tu restes à l'étape 16..."

    elif sit == 17:
        msg = "Un alien attaque ton Chad, car il a peur que quelqu'un qui devienne un Chad Suprême ! Ton Chad va-t-il prouver sa supériorité chadesque ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/alien.jpeg", filename = "image.png")
        p = "Le charisme de ton Chad a suffit à faire fuir l'alien ! Tu passes à **l'étape 18 !**"
        f = "L'alien a sorti sa bite extraterrestre pour soulever ton Chad... tu restes à l'étape 17"

    elif sit == 18:
        msg = "Une armée de Chads zombies qui ont échoué à cette étape attaquent ton Chad ! Va-t-il surpasser leur seum ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/zombies.jpeg", filename = "image.png")
        p = "Ton Chad a vaincu cette armée d'anciens Chads qui avaient trop la rage ! Tu passes à **l'étape 19 !**"
        f = "Ton Chad va aller grossir les rangs de l'armée de zombies... tu restes à l'étape 18"

    elif sit == 19:
        msg = "Ton Chad arrive à l'entrée du Temple Suprême des Chads, et un garde lui demande de chanter la chanson des Chads ! Aide-le en faisant la commande qui joue la musique le plus vite possible !"
        img = discord.File(fp = "/home/container/Pictures/chadroad/chad.png", filename = "image.png")
        p = "Tu as été assez rapide et ton Chad a pu chanter la chanson ! Tu passes à **l'étape 20 !**"
        f = "Tu as été trop lent à aider ton Chad, le garde l'a zigouillé... tu restes à l'étape 19"

    elif sit == 20:
        msg = "Ton Chad est entré dans le Temple Suprême des Chads, et les dieux s'apprêtent à juger si tu es apte à devenir un Chad Suprême et si tu mérites la Médaille des Chads ! Vas-tu mériter cet honneur ?"
        img = discord.File(fp = "/home/container/Pictures/chadroad/temple.jpeg", filename = "image.png")
        p = "Les dieux on tjugé que tu avais mérité la Médaille des Chads ! Tu es désormais un Chad Suprême ! gg à toi mon reuf ! Tu peux faire `k.getmedal` pour obtenir ta médaille !"
        f = p



    embed = discord.Embed(description = msg, color = bleu)
    embed.set_image(url="attachment://image.png")
    await ctx.send(file = img, embed = embed)

        

    return p, f




# COMMANDES

class CommandsChads(commands.Cog):

    def __init__(self, bot, version) -> None:
        self.bot = bot
        self.version = version

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
                        txt += f"{chads_ranks[chad_id]} : **{chads_names[chad_id]}** x{chad_number}\n\n"
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
                        txt += f"{chads_ranks[chad_id]} : **{chads_names[chad_id]}** x{chad_number}\n\n"
                embed.add_field(name = f"Chads de {member.name}", value = txt)
                await ctx.send(embed = embed)


    @commands.command(aliases = ['topcoll', 'topcols', 'topcolls'])
    async def topcol(self, ctx, opt: str = None):
        lb = database_handler.lb_chadscore()
        if opt == 'g':
            msg = f""
            for i in range(len(lb)):
                u = self.bot.get_user(lb[i][0])
                msg += f"**{i+1}.** {u.name}, {lb[i][1]} chadscore\n\n"
            embed = discord.Embed(title = f"Classement général des collections", description = msg, color = bleu)
            await ctx.send(embed = embed)
        elif opt == None:
            msg = f""
            for i in range(len(lb)):
                user = ctx.guild.get_member(lb[i][0])
                if user != None:
                    msg += f"**{i+1}.** {u.name}, {lb[i][1]} chadscore\n\n"
            embed = discord.Embed(title = f"Classement des collections de {ctx.guild.name}", description = msg, color = bleu)
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
    
    @commands.command(aliases = ['gc'])
    @commands.cooldown(2,86400, commands.BucketType.user)
    async def getchad(self, ctx):
        nbe = rd.randint(1,373)
        result = database_handler.get_collection(ctx.author.id)
        if nbe <= 100:
            c_id = 1

        elif nbe <= 180:
            c_id = 2

        elif nbe <= 240:
            c_id = 3

        elif nbe <= 290:
            c_id = 4

        elif nbe <= 320:
            c_id = 5

        elif nbe <= 340:
            c_id = 6

        elif nbe <= 355:
            c_id = 7

        elif nbe <= 365:
            c_id = 8

        elif nbe <= 370:
            c_id = 9

        elif nbe <= 372:
            c_id = 10

        if has_chad_bis(result, c_id) == False:
            database_handler.add_new_chad(ctx.author.id, c_id)
            file = discord.File(str(chads_adresses[c_id]))
            await ctx.send(f"gg ! t'as débloqué le **Chad de rang {c_id}** !", file = file)
            
        else:
            database_handler.add_chad(ctx.author.id, c_id, 1)
            await ctx.send(f"t'as gagné un chad de rang {c_id} !")
                
    @commands.command()
    async def upgrade(self, ctx, *, rank):
        member = ctx.author
        rank = int(rank)
        collection = database_handler.get_collection(member.id)
        if has_chad(collection, rank):
            pos = chad_pos(collection, rank)
            if collection[pos][1] > 10:
                database_handler.upgrade_chad(member.id, rank)
                if has_chad(collection, rank+1):
                    database_handler.add_chad(member.id, rank + 1, 1)
                else:
                    database_handler.add_new_chad(member.id, rank + 1)
                await ctx.send(f"bien joué ! chad amélioré au rang {rank+1} !")
            else:
                await ctx.send("t'en a pas assez dsl, il t'en faut au moins 11")
        else:
            await ctx.send("t'as pas ce chad dsl")

    @getchad.error
    async def getchad_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("cette commande est dispo que 2 fois par jour dsl")

    @commands.command()
    async def chadsong(self, ctx):
        file = discord.File("/home/container/Pictures/chads/chadsong.mp4")
        await ctx.send(file = file)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def chadtips(self, ctx):
        if database_handler.is_finished(ctx.author.id) == False:
            c_ad = rd.choice(chads_random)
            msg = rd.choice(chads_tips)
            embed = discord.Embed(description = msg, color = bleu)
            file = discord.File(fp = c_ad, filename = "image.png")
            embed.set_image(url="attachment://image.png")
            await ctx.send(file=file, embed=embed)
        else:
            await ctx.send("t'es déjà un gigachad, tu as fini la route des Chads :sunglasses:")

    @chadtips.error
    async def chadtips_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Tu as eu ton conseil du jour, la patience fait partie des qualités d'un chad")

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

    
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    async def avance(self, ctx):
        user = ctx.author
        try:
            if database_handler.is_started(user.id):

                if not database_handler.is_finished(user.id):

                    def checkMessage(message):
                        return message.author == user and ctx.message.channel == message.channel

                    await ctx.send("Quel rang de chad choisis-tu pour tenter de passer à l'étape suivante ?")
                    c_id = await self.bot.wait_for("message", timeout = 20, check = checkMessage)
                    c_id = int(c_id.content)

                    coll = database_handler.get_collection(user.id)

                    if has_chad(coll, c_id):
                        
                        etape_act = database_handler.get_etape(user.id)[0][0]

                        # Choix de l'action en fonction de l'étape

                        p, f = await situation(ctx, etape_act)
                        
                        if etape_act == 19:
                            await ctx.send("Vite, fais la commande qui joue la musique des Chads !")
                            cmd = await self.bot.wait_for("message", timeout = 10, check = checkMessage)

                            if cmd.content != "k.chadsong":
                                etape_act = 190
                        
                        await asyncio.sleep(3)
                        
                        if can_pass(c_id, etape_act):
                            await ctx.send(p)
                            database_handler.up_etape(user.id)
                        else:
                            await ctx.send(f)
                            database_handler.add_chad(user.id, c_id, -1)
                            
                    else:
                        await ctx.send("Tu n'as pas ce Chad dsl")
                        await self.avance.reset_cooldown(ctx)
                else:
                    await ctx.send("Tu as déjà fini la Route des Chads :sunglasses:")
            else:
                await ctx.send("fais `k.start` pour pouvoir jouer la route des chads !")
                await self.avance.reset_cooldown(ctx)
        except:
            await self.avance.reset_cooldown(ctx)

    @commands.command()
    async def getmedal(self, ctx):
        if database_handler.is_finished(ctx.author.id):
            file = discord.File("/home/container/Pictures/chadroad/medal.png")
            await ctx.send("Voilà ta médaille :", file = file)
        else:
            await ctx.send("Tu n'as pas encore gagné la médaille des Chads dsl")

    @avance.error
    async def avance_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("tu peux avancer d'une seule étape par jour mon reuf, ton chad doit se reposer")
    

    @commands.command(aliases = ['lb'])
    @commands.guild_only()
    async def leaderboard(self, ctx, arg = None):
        guild = ctx.guild
        lb = database_handler.leaderboard()

        if arg == "g" or arg == "global":
            txt = f""
            for i in range(11):
                user = self.bot.get_user(lb[i][0])

                if lb[i][1] == 21 or lb[i][1] == 0:
                    txt = txt + f"**{user.name} **est devenu un Chad Suprême :sunglasses:\n\n"
                else:
                    txt = txt + f"**{user.name} :** étape {lb[i][1]}\n\n"

            embed = discord.Embed(title = "Classement de la Route des Chads", color = bleu, description = txt)
            await ctx.send(embed = embed)

        elif arg == None:
            txt = f""
            for i in range(11):
                user = guild.get_member(lb[i][0])
                if user != None:
                    if lb[i][1] == 21 or lb[i][1] == 0:
                        txt = txt + f"**{user.name} **est devenu un Chad Suprême :sunglasses:\n\n"
                    else:
                        txt = txt + f"**{user.name} :** étape {lb[i][1]}\n\n"
            embed = discord.Embed(title = f"Classement de la Route des Chads dans {guild.name}", color = bleu, description = txt)
            await ctx.send(embed = embed)
        
        else:
            await ctx.send("Cet argument n'est pas reconnu")

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
                    boutons = [
                        create_button(style=ButtonStyle.blue, label = "azy letsgo", custom_id='1'),
                        create_button(style=ButtonStyle.blue, label="nan nsm", custom_id='2')
                    ]
                    action_row_buttons = create_actionrow(*boutons)

                    channel2 = await member2.create_dm()
                    embed = discord.Embed(title = "", color = bleu, description = f"veux tu donner un chad de **rang {chad_asked}** et recevoir un chad de **rang {chad_given}** de la part de **{member.name} **?\n\nréponds par `oui` pour accepter, et réponds n'importe quoi pour refuser")
                    embed.set_footer(text = "tu as 5 minutes pour répondre")

                    msg = await channel2.send(embed = embed, components = [action_row_buttons])

                    await ctx.send(f"j'ai envoyé un dm à {member2.name} pour savoir s'il veut échanger, jte dm bientôt pour te dire s'il accepte ou pas", delete_after = 10)

                    def check_buttons(m):
                        return m.origin_message.id == msg.id

                    confirmation = await wait_for_component(self.bot, components = action_row_buttons, check = check_buttons, timeout = 300)
                    
                    await confirmation.defer(ignore=True)
            
                    if confirmation.custom_id == "1":
                        # On ajoute les chads
                        if has_chad(member2_col, chad_given):
                            database_handler.add_chad(member2.id, chad_given)
                        else:
                            database_handler.add_new_chad(member2.id, chad_given)
                        
                        if has_chad(member_col, chad_asked):
                            database_handler.add_chad(member.id, chad_asked)
                        else:
                            database_handler.add_new_chad(member.id, chad_asked)

                        # On retire les chads
                        database_handler.remove_chad(member.id, chad_given)
                        database_handler.remove_chad(member2.id, chad_asked)
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
    