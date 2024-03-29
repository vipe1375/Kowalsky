import os
import sqlite3

l = [5, 6, 7, 12, 19, 25, 37, 75, 124, 373]

def get_chadscore(result):
    chadscore = 0
    for i in range(len(result)):
        chadscore += result[i][0] * result[i][1] * l[result[i][0]-1] #rang du chad * nombre * valeur
    return chadscore


class DatabaseHandler():
    def __init__(self, database_name : str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row


    # ------------- Clear ----------------#

    def edit_clear_status(self, guild_id: int, value: bool = False):
        cursor = self.con.cursor()
        if self.get_clear_status(guild_id) == 0:
            query = "INSERT INTO Clear(status, guild_id) VALUES (?, ?);"
        else:
            query = "UPDATE Clear SET status = ? WHERE guild_id = ?;"
        cursor.execute(query, (value, guild_id))
        self.con.commit()
        cursor.close

    def get_clear_status(self, guild_id: int):
        cursor = self.con.cursor()
        query = f"SELECT status FROM Clear WHERE guild_id = {guild_id};"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        if result != None:
            result = dict(result)
            if result['status'] == 0:
                return False
            elif result['status'] == 1:
                return True
        else:
            return 0



    # ------------ Updates -------------- #

    def setup(self):
        cursor = self.con.cursor()
        query = f"CREATE TABLE Updates (guild_id INTEGER NOT NULL UNIQUE, channel_id INTEGER NOT NULL);"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def is_following(self, guild_id):
        cursor = self.con.cursor()
        query = f"SELECT guild_id FROM Updates WHERE {guild_id} = guild_id;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        result = list(map(list, result))
        if result == [] or result == [[]]:
            return False
        else:
            return True

    def add_channel(self, guild_id, channel_id):
        cursor = self.con.cursor()
        query = f"INSERT INTO Updates(guild_id, channel_id) VALUES (?, ?)"
        cursor.execute(query, (guild_id, channel_id))
        self.con.commit()
        cursor.close()

    def delete_channel(self, guild_id):
        cursor = self.con.cursor()
        query = f"DELETE FROM Updates WHERE guild_id = {guild_id};"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def get_channels(self):
        cursor = self.con.cursor()
        query = "SELECT channel_id FROM Updates"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        result = list(map(list, result))
        return result

        
    # ------------ Activation/désactivation de commandes -----------#

    def on(self, guild_id : int, command_id : int):
        if self.get_command(guild_id, command_id) == []:
            cursor = self.con.cursor()
            query = f"INSERT INTO Commands(guild_id, command_id) VALUES (?, ?)"
            cursor.execute(query, (guild_id, command_id))
            self.con.commit()
            cursor.close()
            
        else:
            cursor = self.con.cursor()
            query = f"UPDATE Commands SET activated = 1 WHERE guild_id = {guild_id} AND command_id = {command_id};"
            cursor.execute(query)
            self.con.commit()
            cursor.close()
            
    def off(self, guild_id, command_id):
        if self.get_command(guild_id, command_id) == []:
            cursor = self.con.cursor()
            query = f"INSERT INTO Commands(guild_id, command_id, activated) VALUES (?, ?, ?)"
            cursor.execute(query, (guild_id, command_id, 0))
            self.con.commit()
            cursor.close()
            
        else:
            cursor = self.con.cursor()
            query = f"UPDATE Commands SET activated = 0 WHERE guild_id = {guild_id} AND command_id = {command_id};"
            cursor.execute(query)
            self.con.commit()
            cursor.close()
        
    def get_command(self, id_guild, id_command):
        cursor = self.con.cursor()
        query = f"SELECT activated FROM Commands WHERE {id_guild} = guild_id AND {id_command} = command_id;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result




#-------------------- Chadscore -----------------------#

    def get_chadscore(self, user_id):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Chadscore WHERE user_id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result

    def lb_chadscore(self):
        cursor = self.con.cursor()
        query = f"SELECT * FROM Chadscore ORDER BY chadscore DESC;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def update_chadscore(self, user_id):
        cursor = self.con.cursor()
        query = f"SELECT chad_id, number FROM Collection WHERE user_id = {user_id} ORDER BY chad_id ASC ;"
        cursor.execute(query)
        result = cursor.fetchall()
        
        new_chadscore = get_chadscore(result)

        if self.get_chadscore(user_id) == None:
            query2 = f"INSERT INTO Chadscore(user_id, chadscore) VALUES ({user_id}, {new_chadscore});"
        else:
            query2 = f"UPDATE Chadscore SET chadscore = {new_chadscore} WHERE user_id = {user_id};"
        cursor.execute(query2)
        self.con.commit()
        cursor.close()


#-------------------- Chads -----------------------#
    
    
    def get_collection(self, user_id):
        cursor = self.con.cursor()
        query = f"SELECT chad_id, number FROM Collection WHERE user_id = {user_id} ORDER BY chad_id ASC ;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        if result == None:
            return None
        else:
            result = list(map(list, result))
            
            return result

    def add_new_chad(self, user_id, chad_id):
        cursor = self.con.cursor()
        query =f"INSERT INTO Collection (chad_id, user_id) VALUES (?, ?);"
        cursor.execute(query, (chad_id, user_id))
        self.con.commit()
        cursor.close()

    def add_chad(self, user_id, chad_id, number):
        cursor = self.con.cursor()
        query = f"UPDATE Collection SET number = number + {number} WHERE user_id = {user_id} AND chad_id = {chad_id};"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def upgrade_chad(self, user_id, chad_id):
        cursor = self.con.cursor()
        query = f"UPDATE Collection SET number = number - 5 WHERE user_id = {user_id} AND chad_id = {chad_id};"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def full_collection(self, user_id):
        cursor = self.con.cursor()
        query = f"SELECT chad_id FROM Collection WHERE user_id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        if result == [] or result == None:
            return False
        else:
            result = list(map(list, result))
            return len(result) == 10

    def remove_chad(self, user_id, chad_id):
        cursor = self.con.cursor()
        query = f"UPDATE Collection SET number = number - 1 WHERE user_id = {user_id} AND chad_id = {chad_id};"
        cursor.execute(query)
        self.con.commit()
        cursor.close()




        
# ------------------- Route des Chads ----------------- #

    def is_started(self, user_id):
        cursor = self.con.cursor()
        query = f"SELECT etape FROM Chadroad WHERE user_id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(map(list, result))
        return result != []

    def get_etape(self, user_id):
        cursor = self.con.cursor()
        query = f"SELECT etape, dead_chads, is_finished FROM Chadroad WHERE user_id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(map(list, result))
        return result

    def new_etape(self, user_id):
        cursor = self.con.cursor()
        query =f"INSERT INTO Chadroad (user_id) VALUES ({user_id});"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def up_etape(self, user_id):
        cursor = self.con.cursor()
        if self.get_etape(user_id)[0][0] == 20:
            query =f"UPDATE Chadroad SET etape = etape + 1, is_finished = 1 WHERE user_id = {user_id};"
        else:
            query =f"UPDATE Chadroad SET etape = etape + 1 WHERE user_id = {user_id};"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def is_finished(self, user_id):
        result = self.get_etape(user_id)
        if result is not None:
            return result[0][0] == 21 or result[0][0] == 0
        else:
            return False

    def leaderboard(self):
        cursor = self.con.cursor()
        query = f"SELECT user_id, etape FROM Chadroad ORDER BY etape DESC;"
        cursor.execute(query)
        result = cursor.fetchall()
        result = list(map(list, result))
        return result

    def set_finishers(self):
        cursor = self.con.cursor()
        query = f"UPDATE Chadroad SET etape = 21, is_finished = 1 WHERE etape = 0;"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    
# ------------------ Testmod --------------#

    def check_testmod(self):
        cursor = self.con.cursor()
        query = f"SELECT is_on_testmod FROM Testmod;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        result = list(map(list, result))
        return result


    def testmod_on(self):
        cursor = self.con.cursor()
        query = "UPDATE Testmod SET is_on_testmod = 1;"
        cursor.execute(query)
        self.con.commit()
        cursor.close()

    def testmod_off(self):
        cursor = self.con.cursor()
        query = "UPDATE Testmod SET is_on_testmod = 0;"
        cursor.execute(query)
        self.con.commit()
        cursor.close()




