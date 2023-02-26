import discord
from discord.ext import commands

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur

async def setup(bot):
    await bot.add_cog(Bet(bot))


# commandes :
# listage des events en cours/planifiés ? menu select pour agir sur un event
# créer un event (nom/date)
# entrer les résultats


class Bet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    