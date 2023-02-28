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
        cursor = self.con.cursor()
        query = f"INSERT INTO Events(label, time, option_1, option_2) VALUES (?, ?, ?, ?);"
        cursor.execute(query, (name, time, option_1, option_2))
        self.con.commit()
        cursor.close()

    def delete_event(self, id):
        pass

    def get_active_events(self):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Events WHERE status = 1;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def get_inactive_events(self):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Events WHERE status = 0;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    def get_event_by_id(self, id):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Events WHERE id = {id};"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result

    