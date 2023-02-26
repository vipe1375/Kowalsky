import os
import sqlite3


# Fonctionnement :
# on fixe une heure de fin des paris, et les gains sont distribués le lendemain matin à 8h
# on dm chaque participant
# somme minimale : 10


class DatabaseHandlerBet():
    def __init__(self, database_name : str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row


    # Gestion des events
    def create_event(self, name, time, option_1, option_2):
        pass

    def delete_event(self, id):
        pass

    