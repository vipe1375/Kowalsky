# imports discord :
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True

# imports autres modules
import time as t
import random as rd
import os
import traceback

# Database:
from database_handler_k import DatabaseHandler
database_handler = DatabaseHandler("database_kowalsky.db")

async def setup(bot):
    await bot.add_cog(CommandesTroll(bot))

# ------------ INFOS ---------------- #

listeOof = os.listdir('/home/container/Pictures/oof')

listeMU = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

listeCSC = os.listdir('/home/container/Pictures/csc')

liste_random_pics = os.listdir('/home/container/Pictures/random')

liste_random_words = ["guingamp",
                     "sheesh",
                     "zizi",
                     "ekip",
                     "qui veut la paix prépare la guerre",
                     "assinus assinum fricat",
                     "un grand sage a un jour dit : 'tu comprendras que la violence ne règle pas tout quand t'auras un moustique sur les couilles'",
                     "YIIIHH QUAND TON BANGALA EST BIEN DRESSER 😭😭😭⚔️⚔️⚔️⚔️🏴‍☠️🏴‍☠️🏴‍☠️🚨🚨👎🏼👎🏼👎🏼🥶🥶🥶🥶🥶🥶🥶NONNN C'EST CHAUD SURTOUT QUAND TON JOGGING BAAD GRIS🥶🥶🥶🥶🥶🥶🥶🥶🥶😭😭😭🏴‍☠️🏴‍☠️🏴‍☠️⚔️⚔️⚔️👎🏼👎🏼👎🏼🔥🔥🔥TSAI LE MEC QUI MET PAS DE CALECON'ZER😭😭😭😭😭🥶🥶🥶🥶😎😎😎👎🏼👎🏼👎🏼⚔️⚔️⚔️🏴‍☠️🏴‍☠️🏴‍☠️🏴‍☠️💀💀💀💀",
                     "https://www.caca.com",
                     "J’vien de tomber sur le jeune homme 🤣🤣🤣🤣🏴‍☠️🏴‍☠️Il a mis Un RÉGULAR COUPE SKINNY SECTION JAVELOT😹SECTION POINTE🤣🤣Matte la paire de godasse🤌🤌😹C’EST MÊME PLUS DES GODASSE C’EST DES GROLES 😹😹LE RACLOS EST STRESSÉ😈😈😭😭",
                     "discussions entre maes et penaldo :- hola maes cafew a qui sert ton million si tu prend perpete ?😆🥺🥵🥵🥶- million liberté tu connais😱💸🥳🤙🤙-no no penalty no goal cafeww😡😡😊🥵🤙🤙-masterfraude penaldo🥶🤣🤣😹🤙🤙",
                     "@booba dit leurs 🤣🤣🤣😂😂 #LaPiraterieNestJamaisFini #ElleNeSeFiniraDailleursJamais 🏴‍☠️🏴‍☠️🏴‍☠️ #ChakalMonteDansABord #OnMangePas #Piranha 🙌🏼🙌🏼🙌🏼🙌🏼🏴‍☠️🏴‍☠️Ici on emploi Les termes Chakal ✊🏼✊🏼😂😂😂🤣🤣 Dit leurs Duc’zer Imre chakou #QuiVaMarreter #PasLa5G",
                     "kestia tu veux veux commenter🔥🔥🤣😏🤣😏🥶hehehehe😂🤣🤣😂🤣😂kestya ?😏😂😏😂 mé kestya aaa😏😂😏😂pq tu v...tia le démon comme ça🥶😏🤣🥶😏🤣trankil🥶🥶🥶tia jamais v’u un bg ou quoi🔥🥶😏🤣🔥🥶😂🤣hein🤣🥶😂",
                     "Super Idol的笑容 都没你的甜 八月正午的阳光 都没你耀眼 热爱 105 °C的你 滴滴清纯的蒸馏水",
                     "Le contre son camp 🤣🤣🤣🏴‍☠️🏴‍☠️🏴‍☠️🙏 🏴‍☠️🤣🤣🤣🤣 tchoinzer qui se moque du trottoirzer ou comment 🤣🤣🤣🏴‍☠️🏴‍☠️🏴‍☠️🏴‍☠️🙏 s'agit de marquer dans les bons buts 🤣🤣🏴‍☠️🏴‍☠️ amenez moi un ratpi du navire qu'il leur montre 🥶🥶🤣🤣   bon qu'a te dénoncer duc !!⛏⛏⛏⛏ #merciimrepourlestravaux🏴‍☠️🏴‍☠️",
                     "CONVERSATION ENTRE MESSI ET MBAPPE DANS LE MATCH Mbappe : « Hola pessi et ca fais goaaal cafeww 🤣🤣🕺🕺 »  Messi : « nah nah noisette chakal 😅😅 »  Mbappe : « pessi cabron es hora de comer 🤣🤣👊 »  Messi : « noisette 🥜 masterclass cafeww 🤣🤣🕺🔥🕺🔥🔥 »",
                     "Red sus. Red suuuus. I said red, sus, hahahahaha. Why arent you laughing? I just made a reference to the popular video game 'Among Us'! How can you not laugh at it? Emergeny meeting! Guys, this here guy doesnt laugh at my funny Among Us memes! Lets beat him to death! Dead body reported! Skip! Skip! Vote blue! Blue was not an impostor. Among us in a nutshell hahahaha. What?! Youre still not laughing your ass off? I made SEVERAL funny references to Among Us and YOU STILL ARENT LAUGHING??!!! Bruh. Ya hear that? Wooooooosh. Whats woooosh? Oh, nothing. Just the sound of a joke flying over your head. Whats that? You think im annoying? Kinda sus, bro. Hahahaha! Anyway, yea, gotta go do tasks. Hahahaha!",
                     "O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA",
                     "Yeeeeee 🥶🥶🥶🥶 le boug a qualifié les term zer 🤣🤣🤣🤣🤣🤣🤣🤣🤣 🥵🥵🥵🥵🥵🤣🤣🤣🤣🤙🤙🤙🤙 à bon entendeur bien sûr 😎😎😎😎",
                     """Yes sir
You already know this is based on a true story
The story of how I’ve shit my pants in real life
Among us
Yes
Shit my pants

I shitted in my pants, yes
I shitted in my pants (Woah)
I am for real
Never meant to make my booty shit
I apologize I shit my pants

I shitted in my pants
I am for real
Never meant to make my booty shit
I apologize I shit my pants

I’m gonna go to the bathroom because I shit my pants
I’m gonna pull down my pants and I’m not gonna wipe it cause I can
I feel the diarrhea spreading down my legs going down through my toenails

People only talk because they don’t know the pain
The pain of shitting your pants
Diarrhеa going through your legs
I don’t wanna wipe my ass no more
It’s too latе
The diarrhea got to my knee and my legs
What the fuck

I shitted in my pants (Woah)
I am for real
Never meant to make my booty shit
I apologize I shit my pants

I shitted in my pants (Woah)
I am for real
Never meant to make my booty shit
I apologize I shit my pants

I shitted in my pants (Woah)
I am for real
Never meant to make my booty shit
I apologize I shit my pants

Me and my booty
Got special things going on
You say that’s dirty
I’m asking what the fuck is wrong
I’m broke no money
The big booty is on the run
You can suck on dick
But you can’t print dicks on booty

Shitted in my pants
People ask me how I shitted my pants
I say you gotta pull down your pants
Let that shit drop
Then pick it up with your hands
Pull up your pants
Then you put that shit inside your mouth
Oh man

I shitted in my pants
They ask me did you really shit your pants though?
Hell yeah
I love shitting my pants
It feels good when the diarrhea is going down my ass goddamn

I shitted in my pants (Woahoah)
I am for real
Never meant to make my booty shit
I apologize I shit my pants

I shitted in my pants (Woah)
I am for real
Never meant to make my booty shit
I apologize I shit my pants


So amazing (Shitted my pants)""",

"It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just😐a😆sussy🖤baka😫and🥵it😱can🤯not🤭be😵that🤖bad💀I’m😈feeling😷like👅imposter👾I😲 might🥶just😩be❤️a🎊monster🤡It’s😦just"]

liste_sus = os.listdir('/home/container/Pictures/sus')


liste_choix = [liste_random_words, liste_random_pics]

liste_commandes = {'quoi': 1, 'feur': 1, 'tg' : 2, 'ph' : 3, 'randomping' : 4, 'csc' : 5, 'saydm' : 6, 'haagrah' : 7, 'ratio': 8, 'sus': 9, 'cheh': 10, 'flop': 11, 'nwar': 12, 'con': 13, 'masterclass': 14, 'tts':15}


liste_gifs = ["https://tenor.com/view/dancing-black-big-gif-20472579",
"https://tenor.com/view/dance-move-black-gif-18553004",
"https://tenor.com/view/black-man-dance-happy-dance-gif-15340006",
"https://tenor.com/view/laugh-dance-black-kid-get-it-killing-it-gif-10743055",
"https://tenor.com/view/black-dance-black-twerk-gif-20765436"]

liste_cons = [
    "t'es pas le couteau le plus aiguisé du tiroir",
    "si on mettait tous les idiots du village dans un village, tu serais quand même l'idiot du village",
    "t'es pas le mec le plus con du monde, mais t'as vraiment intérêt à ce qu'il meure pas",
    "on est tous le con de quelqu'un d'autre, mais toi ça fait l'unanimité",
    "si la connerie se mesurait, tu servirais de mètre étalon",
    "t'es pas la truite la plus oxygénée du ruisseau",
    "t'es pas le crayon le mieux taillé de la trousse",
    "t'es pas la chips a plus croquante du paquet",
    "t'es pas le pingouin qui glisse le plus loin",
    "t'es pas le castor le plus utile au barrage",
    "t'es con comme une valise sans poignée",
    "t'as pas inventé la poudre mais tu devais pas être loin quand elle a explosé",
    "si les cons volaient tu serais chef d'escadrille",
    "si on mettait les cons sur orbite t'aurais pas fini de tourner",
    "t'es pas le chocapic le plus fort en chocolat",
    "t'es pas le lampadaire le plus lumineux de la rue",
    "t'es pas la pierre la plus moussue qui roule"
]

liste_masterclass = os.listdir('/home/container/Pictures/masterclass')

liste_sons = os.listdir('/home/container/Sounds')

# Couleurs :

bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur



# ------------ FONCTIONS ------------ #

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

def is_vipe_or_bot(id):
    return id == 691380397673545828 or id == 926864538681368626




class CommandesTroll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @commands.command()
    async def tts(self, ctx: commands.Context, sound: str = None):
        if check_command(ctx.guild.id, 'tts'):

            if ctx.author.voice == None:
                await ctx.send("Tu n'es pas dans un salon vocal")
                return
            else:
                voice_channel = ctx.author.voice.channel
                
                
            if sound == None:
                sound_path = rd.choice(liste_sons)
                await ctx.send('mets un nom de son bro')
                return
            else:
                sound_name = f"{sound}.mp3"
                if sound_name not in liste_sons:
                    await ctx.send('ce son existe pas bro')
                    
                else:
                    sound_path = f"/home/container/Sounds/{sound}.mp3"
            try:
                voc = await voice_channel.connect()
            except:
                await ctx.send("je parle là attends que j'aie fini stp")
                return
            voc.play(discord.FFmpegPCMAudio(source=sound_path))
            while voc.is_playing():
                t.sleep(0.1)
            await voc.disconnect()
        else:
            await ctx.send("Cette commande est désactivée ici :pensive:")


    @commands.command()
    async def masterclass(self, ctx):
        if check_command(ctx.guild.id, 'masterclass'):
            ad = f"/home/container/Pictures/masterclass/{rd.choice(liste_masterclass)}"
            file = discord.File(ad)
            await ctx.send(file = file)
        else:
            await ctx.send('Cette commande est désactivée ici')


    @commands.command(aliases = ['tcon'])
    async def con(self, ctx, member: discord.Member = None):
        if check_command(ctx.guild.id, 'con'):
            if member != None:
                if is_vipe_or_bot(member.id):
                    await ctx.send("nan c'est toi t'es con")
                elif member == ctx.author:
                    await ctx.send("nooon t'es pas con bebou aie confiance en toi :pleading_face::heart::heart:")
                else:
                    await ctx.send(f"{rd.choice(liste_cons)} {member.mention}")
            else:
                await ctx.send(rd.choice(liste_cons))
        else:
            await ctx.send('Cette commande est désactivée ici :x:')
            

    @commands.command()
    async def k(self, ctx):
        await ctx.message.delete()
        await ctx.send("caca :poop:")

    @commands.command()
    @commands.guild_only()
    async def nwar(self, ctx):
        if check_command(ctx.guild.id, 'nwar'):
            await ctx.send(rd.choice(liste_gifs))
        else:
            await ctx.send("Cette commande est désactivée ici :x:")


    # cheh:

    @commands.command()
    @commands.guild_only()
    async def cheh(self, ctx, member: discord.Member = None):
        validation = check_command(ctx.guild.id, 'cheh')
        if validation:
            if member == None:
                await ctx.send("t'as trop la rage + cheh + fail + t'es adopté :joy_cat::joy_cat::joy_cat::moyai::moyai::moyai:")
            else:
                await ctx.send(f"t'as trop la rage {member.mention} + cheh + fail + t'es adopté :joy_cat::joy_cat::joy_cat::moyai::moyai::moyai:")
        else:
            await ctx.send("cette commande est désactivée ici :pensive:")


    # Random:

    @commands.command()
    async def random(self, ctx):
        choix_theme = rd.choice(liste_choix)
        if choix_theme == liste_random_pics:
            file = discord.File('/home/container/Pictures/random/'+rd.choice(liste_random_pics))
            await ctx.send(file = file)
        else:
            content = rd.choice(choix_theme)
            await ctx.send(content)


    # Haagrah

    @commands.command(aliases = ['oof'])
    @commands.guild_only()
    async def haagrah(self, ctx):
        validation = check_command(ctx.guild.id, 'haagrah')
        if validation == True:
            file = discord.File('/home/container/Pictures/oof/'+rd.choice(listeOof))
            await ctx.send(file=file)
        else:
            await ctx.send("Cette commande est désactivée ici :x:")



    # TG :

    @commands.command()
    @commands.guild_only()
    async def tg(self, ctx, member : discord.Member):
        validation = check_command(ctx.guild.id, 'tg')
        if validation == True:
            await ctx.message.delete()
            if member == ctx.author:
                await ctx.send("t limite con toi")
            elif is_vipe_or_bot(member.id):
                await ctx.send(f"non toi tg {ctx.author.mention}")
            else:
                listeTG = [f"ta gueule {member.mention} tout le monde s'en blc de toi et d'ailleurs t'es adopté",
                   f"tsais {member.mention} des fois c'est pas nécessaire de parler, surtout si c'est pour dire ça",
                   f"eh {member.mention} tsais quoi ftg on s'en branle",
                   f"cher {member.mention}, auriez-vous l'obligeance de garder le silence",
                   f"{member.mention}, ta encore perdu une occasion de te taire",
                   f"{member.mention} azy fais nous un freestyle s/o les muets"]
                await ctx.send(rd.choice(listeTG))
        else:
            await ctx.send("Cette commande est désactivée ici :x:")


    # ph :

    @commands.command()
    @commands.guild_only()
    async def ph(self, ctx):
        validation = check_command(ctx.guild.id, 'ph')
        if validation == True:
            await ctx.message.delete()
            await ctx.send("https://www.pornhub.com")
        else:
            await ctx.send("Cette commande est désactivée ici :x:")


    # coucou :

    @commands.command(aliases = ["salut", "bonjour"])
    async def coucou(self, ctx):
        await ctx.send("salut mon reuf")


    # saydm :

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1,120, commands.BucketType.user)
    async def saydm(self, ctx, member : discord.Member, *, message : str):
        validation = check_command(ctx.guild.id, 'saydm')
        if validation == True:
            await ctx.message.delete()
            dmchannel = await member.create_dm()
            await dmchannel.send(f"{message}")
            await ctx.send("`c'est envoyé mon reuf`", delete_after = 5)

    @saydm.error
    async def saydm_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"doucement wsh, tu pourras refaire cette commande dans {int(error.retry_after)} secondes")



    # Randomping :

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.member)
    @commands.guild_only()
    async def randomping(self, ctx):
        validation = check_command(ctx.guild.id, 'randomping')
        if validation == True:
            await ctx.message.delete()
            members = ctx.guild.members
            ping = rd.choice(members)
            await ctx.send(f"{ping.mention}")
        else:
            await ctx.send("Cette commande est désactivée ici :x:")

    @randomping.error
    async def randomping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"doucement wsh, tu pourras refaire cette commande dans {int(error.retry_after)} secondes")



    # Racism :

    @commands.command(aliases = ['racism', 'raciste', 'racisme'])
    @commands.guild_only()
    async def racist(self, ctx):
        await ctx.message.delete()
        await ctx.send("le racisme c pas bien :pensive::pensive::pensive::pensive: faut aimer les autres même s'ils sont noirs ou arabes :smiling_face_with_3_hearts::smiling_face_with_3_hearts::smiling_face_with_3_hearts::smiling_face_with_3_hearts::smiling_face_with_3_hearts:")


    # MU :

    @commands.command(aliases = ['matchup'])
    async def mu(self, ctx):
        mu = rd.choice(listeMU)
        if mu <= 30:
            await ctx.send("il a un hc  moi jdis "+ str(100-mu) + "-" + str(mu) + " pour lui")
        elif mu >= 70:
            await ctx.send("là frr c'est freewin t'as "+ str(mu) + "-" + str(100-mu))
        else:
            await ctx.send("ça passe c'est un "+ str(mu) + "-" + str(100-mu) + " chill en vrai")


    # Stylé :

    @commands.command()
    async def stylé(self, ctx):
        await ctx.send("de ouf :sunglasses:")


    # csc :

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def csc(self, ctx):
        validation = check_command(ctx.guild.id, 'csc')
        if validation == True:
            await ctx.message.delete()
            file = discord.File('/home/container/Pictures/csc/'+rd.choice(listeCSC))
            await ctx.send(file=file)
        else:
            await ctx.send("Cette commande est désactivée ici :x:")

    @csc.error
    async def csc_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"doucement wsh, tu pourras refaire cette commande dans {int(error.retry_after)}")


    # ratio:

    @commands.command()
    @commands.guild_only()
    async def ratio(self, ctx, user: discord.Member = None):
        validation = check_command(ctx.guild.id, 'ratio')
        if validation:
            if user == None:
                await ctx.send("ratio généralisé :cold_face::cold_face::cold_face::cold_face::moyai::moyai::moyai::moyai::fire::fire::fire:")

            elif is_vipe_or_bot(user.id):
                msg = await ctx.send(f"contre ratio {ctx.author.mention} + flop + adoption :cold_face::cold_face::cold_face::cold_face::moyai::moyai::moyai::moyai::sunglasses::sunglasses::sunglasses::sunglasses:")
                await msg.add_reaction("❤️")


            elif user == ctx.author:
                await ctx.send("le boug s'auto-ratio quoi :cold_face::cold_face::cold_face::cold_face::moyai::moyai::moyai::moyai:")

            else:
                msg = await ctx.send(f"L + ratio {user.mention} :cold_face::cold_face::cold_face::cold_face::moyai::moyai::moyai::moyai::sunglasses::sunglasses::sunglasses::sunglasses:")
                await msg.add_reaction("❤️")


    @commands.command()
    @commands.guild_only()
    async def flop(self, ctx):
        validation = check_command(ctx.guild.id, 'flop')
        if validation:
            file = discord.File("/home/container/Pictures/grenouille.jpeg")
            await ctx.send("flop + contre ratio + grenouille de la honte :fire::fire::fire::sunglasses::sunglasses::sunglasses::cold_face::cold_face::cold_face:", file = file)


    # sus:

    @commands.command()
    @commands.guild_only()
    async def sus(self, ctx):
        validation = check_command(ctx.guild.id, 'sus')
        if validation:
            embed = discord.Embed(description = 'sus bro', color = bleu)
            file = discord.File(fp = '/home/container/Pictures/sus/'+rd.choice(liste_sus), filename = "image.png")
            embed.set_image(url="attachment://image.png")
            await ctx.send(file = file, embed = embed)
        else:
            await ctx.send("Cette commande est désactivée ici :pensive:")

    
    # Activation / désactivation de commandes
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def activo(self, ctx, command_name):
        
        command_id = liste_commandes[command_name]
        database_handler.on(ctx.guild.id, command_id)
        # création de l'embed
        embed = discord.Embed(title = "Commande activée mon reuf :white_check_mark:", color = vert)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def desactivo(self, ctx, command_name):
        
        command_id = liste_commandes[command_name]
        database_handler.off(ctx.guild.id, command_id)
        # création de l'embed
        embed = discord.Embed(title = "Commande désactivée mon reuf :white_check_mark:", color = vert)
        await ctx.send(embed = embed)

    @commands.command()
    async def check(self, ctx, command_name):
        result = check_command(ctx.guild.id, command_name)
        if result == True:
            embed = discord.Embed(title = "Ici c'est activé :sunglasses:", color = bleu)
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = "Ici c'est désactivé :pensive:", color = bleu)
            await ctx.send(embed = embed)
