import discord
from datetime import datetime
from discord.ext import commands
from dbh_bet import DatabaseHandlerBet
from discord.ui import View

dbh = DatabaseHandlerBet("db_bet.db")

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur








class BetSelectView(View):
    def __init__(self, bot, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(ChooseActiveEvent(bot))
        self.add_item(ChooseInactiveEvent(bot))


class ChooseActiveEvent(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        result = dbh.get_active_events()
        options = [discord.SelectOption(label = result[i][1], value = str(result[i][0])) for i in range(len(result))]
        if len(options) < 1:
            options.append(discord.SelectOption(label = "pas d'event actif", value = "-1"))
        super().__init__(placeholder="Liste des events actifs",max_values=1,min_values=1,options=options)

    async def callback(self, itr: discord.Interaction):
        event = dbh.get_event_by_id(int(self.values[0]))

class ChooseInactiveEvent(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        result = dbh.get_inactive_events()
        options = [discord.SelectOption(label = result[i][1], value = str(i)) for i in range(len(result))]
        if len(options) < 1:
            options.append(discord.SelectOption(label = "pas d'event inactif", value = "-1"))
        super().__init__(placeholder="Liste des events inactifs",max_values=1,min_values=1,options=options)



async def setup(bot):
    await bot.add_cog(Bet(bot))




# commandes :
# listage des events en cours/planifiés ? menu select pour agir sur un event
# créer un event (nom/date)
# entrer les résultats


class Bet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def bet(self, ctx: commands.Context, param: str = "active"):

        if param == "active":
            await ctx.send("choisis ton event !", view=BetSelectView(self.bot))

        elif param == "create":
            msg = f"Pour créer ton event de pari, envoie un message **__sous cette forme :__**\n\n`nom date_de_fin option_1 option_2`\n\n`nom` -> le nom de l'event\n`date_de_fin` -> date de fin des votes/début de l'event **sous la forme** `heure/jour/mois` (sans le chiffre 0 au début, genre janvier c'est 1 pas 01)\n`option_1`-> le nom de la première option de vote\n`option_2` -> pareil"
            embed = discord.Embed(title = "Création d'un event de pari", color = bleu, description=msg)
            await ctx.send(embed = embed)
            def check(message):
                return True
            message = await self.bot.wait_for('message', check=check)
            r = message.content
            r1 = r.split()

            if len(r1) != 4:
                await ctx.send("format invalide, recommence la commande stp")
                return
            
            label = r1[0]
            date = r1[1]
            option_1 = r1[2]
            option_2 = r1[3]

            #mise en forme de la date
            formated_date = date.split("/")
            hour = int(formated_date[0])
            day = int(formated_date[1])
            month = int(formated_date[2])

            today = datetime.today()
            if today.month < month:
                year = today.year
            elif today.month == month:
                if day < today.day:
                    year = today.year + 1
                else:
                    year = today.year
            else:
                year = today.year
            try:
                time = datetime(year, month, day, hour=hour)
            except TypeError as e:
                await ctx.send(f"ton format de date est pas valide, recommence la commande {e}")
                return
            formated_time = int(time.strftime("%Y%m%d%H"))
            dbh.create_event(label, formated_time, option_1, option_2)
    