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

    # def count(self,user_id):
    #     with self.connection:
    #         result = self.cursor.execute('SELECT COUNT(notes) FROM users WHERE user_id =?', (user_id,)).fetchall()
    #         print(result)
    #         return result[0]

    def message(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT notes,date FROM users WHERE user_id = ?', (user_id,)).fetchall()
            return result

    def read(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT notes FROM users WHERE user_id =?', (user_id,)).fetchall()
            return result

    def add_date(self, date, user_id):
        with self.connection:
            result = self.cursor.execute('UPDATE users SET date = ? WHERE user_id = ?', (date, user_id))
            return result

    def delet(self, user_id):
        with self.connection:
            result = self.cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            return result
    def time(self):
        with self.connection:
            result = self.cursor.execute('SELECT date FROM users').fetchall()
            return result


    def date_2_1(self):
        """Получаем всех пользователей count 1"""
        with self.connection:
            return self.cursor.execute("SELECT user_id,notes FROM users WHERE date = strftime('%Y-%m-%d %H:%M', 'now','localtime')").fetchall()
