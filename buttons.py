import discord
from discord.ext import commands
from discord.ui import button, View, Button

from database_handler_k import DatabaseHandler

database_handler = DatabaseHandler("database_kowalsky.db")

# Couleurs :
bleu = 0x2BE4FF #Normal
vert = 0x00FF66 #Unban/unmute/free
rouge = 0xFF2525 #Ban/mute/goulag
orange = 0xFFAA26 #Erreur

def has_chad(result, index):
    if result == None or result == []:
        return False
    else:
        for i in range(len(result)):
            if result[i][0] == index:
                return result[i][1] > 0
        return False

class trade_buttons(View):
    def __init__(self, member1: discord.Member, member2: discord.Member, member1_col, member2_col, chad_given: int, chad_asked: int):
        super().__init__(timeout=None)
        self.member1 = member1
        self.member2 = member2
        self.member1_col = member1_col
        self.member2_col = member2_col
        self.chad_given = chad_given
        self.chad_asked = chad_asked

    @button(label = "azy", emoji='👍')
    async def azy(self, itr: discord.Interaction, button: Button):
        button.disabled = True
        # On ajoute les chads
        if has_chad(self.member2_col, self.chad_given):
            database_handler.add_chad(self.member2.id, self.chad_given, 1)
        else:
            database_handler.add_new_chad(self.member2.id, self.chad_given)

        if has_chad(self.member1_col, self.chad_asked):
            database_handler.add_chad(self.member1.id, self.chad_asked, 1)
        else:
            database_handler.add_new_chad(self.member1.id, self.chad_asked)

        # On retire les chads
        database_handler.remove_chad(self.member1.id, self.chad_given)
        database_handler.remove_chad(self.member2.id, self.chad_asked)
        channel = await self.member1.create_dm()
        await channel.send(f"échange réussi ! {self.member2.name} t'a bien donné un chad de rang {self.chad_asked}, et tu as donné un chad de rang {self.chad_given} !")
        await self.member2.send(f"échange réussi ! {self.member1.name} t'a bien donné un chad de rang {self.chad_given}, et tu as donné un chad de rang {self.chad_asked} !")
        database_handler.update_chadscore(self.member1.id)

        await itr.message.delete()

    @button(label = "nan", emoji = '👎')
    async def nan(self, itr: discord.Interaction, button: Button):
        button.disabled = True
        channel = await self.member1.create_dm()
        await channel.send(f"échange refusé par {self.member2.name}")
        await self.member2.send(f"échange refusé")
        await itr.message.delete()