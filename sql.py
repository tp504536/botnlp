import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def users(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, notepad):
        with self.connection:
            result = self.cursor.execute('INSERT INTO users (user_id, notes) VALUES (?,?)', (user_id, notepad))
            return result

    def count(self,user_id):
        with self.connection:
            result = self.cursor.execute('SELECT COUNT(notes) FROM users WHERE user_id =?', (user_id,)).fetchall()
            print(result)
            return result[0]

    def read(self,user_id):
        with self.connection:
            result = self.cursor.execute('SELECT notes FROM users WHERE user_id =?', (user_id,)).fetchall()
            print(result)
            return result
    # def count_referals(self, user_id):
    #     with self.connection:
    #         #return self.cursor.execute("SELECT COUNT('id') as count FROM 'users' WHERE 'referrer_id' = ?", (user_id,)).fetchone()[0]
    #         result = self.cursor.execute('SELECT user_id FROM users WHERE referrer_id = ?',(user_id,)).fetchall()
    #         return len(result)
    #
    # def get_buildings(self, user_id):
    #     with self.connection:
    #         result = self.cursor.execute('SELECT farm1, farm2, farm3 FROM users WHERE user_id = ?',(user_id,)).fetchall()
    #         return result
