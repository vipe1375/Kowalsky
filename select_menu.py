import discord
from discord.ext import commands
from discord.ui import button, View, Button

from database_handler_k import DatabaseHandler

db_handler = DatabaseHandler("database_kowalsky.db")

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur

class choose_leaderboard(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Classement des collections - serveur", value='0'),
            discord.SelectOption(label="Classement des collections - général", value='1'),
            discord.SelectOption(label="Classement de la Route des Chads - serveur", value='2'),
            discord.SelectOption(label="Classement de la Route des Chads - général", value='3')
        ]
        super().__init__(placeholder="Choisissez un joueur",max_values=1,min_values=1,options=options)


    async def callback(self, itr: discord.Interaction):
        
        if self.values[0] == '0':
            await self.topcol(itr, db_handler.lb_chadscore())
        elif self.values[0] == '1':
            await self.topcol(itr, db_handler.lb_chadscore(), 'g')
        elif self.values[0] == '2':
            await self.create_leaderboard(itr, db_handler.leaderboard())
        elif self.values[0] == '3':
            await self.create_leaderboard(itr, db_handler.leaderboard(), 'g')


    async def create_leaderboard(self, itr: discord.Interaction, lb, arg = None):   

        if arg == "g" or arg == "global":
            txt = f""
            for i in range(11):
                user = self.bot.get_user(lb[i][0])

                if lb[i][1] == 21 or lb[i][1] == 0:
                    txt = txt + f"**{user.name} **est devenu un Chad Suprême :sunglasses:\n\n"
                else:
                    txt = txt + f"**{user.name} :** étape {lb[i][1]}\n"

            embed = discord.Embed(title = "Classement de la Route des Chads", color = bleu, description = txt)
            await itr.response.send_message(embed = embed)

        elif arg == None:
            txt = f""
            for i in range(11):
                user = itr.guild.get_member(lb[i][0])
                if user != None:
                    if lb[i][1] == 21 or lb[i][1] == 0:
                        txt = txt + f"**{user.name} **est devenu un Chad Suprême :sunglasses:\n\n"
                    else:
                        txt = txt + f"**{user.name} :** étape {lb[i][1]}\n"
            embed = discord.Embed(title = f"Classement de la Route des Chads dans {itr.guild.name}", color = bleu, description = txt)
            await itr.response.send_message(embed = embed)

        else:
            await itr.response.send_message("Cet argument n'est pas reconnu")

    async def topcol(self, itr: discord.Interaction, lb, opt: str = None):
        author_in_top = False

        # Classement général
        if opt == 'g':
            msg = f""

            for i in range(10):
                u = self.bot.get_user(lb[i][0])
                if u != None:
                    if u.id == itr.user.id:
                        msg += f":blue_circle: **{i+1}.** {u.name}, {lb[i][1]} chadscore \n"
                        author_in_top = True
                    else:
                        msg += f"**{i+1}.** {u.name}, {lb[i][1]} chadscore\n"

            if not author_in_top:
                for i in range(10, len(lb)):
                    u = self.bot.get_user(lb[i][0])
                    if u == itr.user:
                        msg += f"...\n:blue_circle: **{i+1}.** {u.name}, {lb[i][1]} chadscore "
                        break

            embed = discord.Embed(title = f"Classement général des collections", description = msg, color = bleu)
            await itr.response.send_message(embed = embed)
        
        # Classement par serveur
        elif opt == None:
            y = 0
            
            msg = f""
            for i in range(len(lb)):
                if y < 10:
                    user = itr.guild.get_member(lb[i][0])
                    if user != None:
                        if user == itr.user:
                            msg += f":blue_circle: **{y+1}.** {user.name}, {lb[i][1]} chadscore \n"
                            author_in_top = True
                        else:
                            msg += f"**{y+1}.** {user.name}, {lb[i][1]} chadscore\n"
                        y += 1
                else:
                    
                    break


            if not author_in_top:
                for j in range(i, len(lb)):
                    u = itr.guild.get_member(lb[j][0])
                    if u != None:
                        if u == itr.user:
                            msg += f"...\n\n:blue_circle: **{y+1}.** {u.name}, {lb[j][1]} chadscore"
                            break
                        else:
                            y += 1

            embed = discord.Embed(title = f"Classement des collections de {itr.guild.name}", description = msg, color = bleu)
            await itr.response.send_message(embed = embed)


class SelectView(View):
    def __init__(self, bot, msg, timeout = None):
        super().__init__(timeout=timeout)
        self.add_item(choose_leaderboard(msg, bot))