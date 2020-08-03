import sqlite3


class MusicDao:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def find_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music').fetchall()

    def find_by_id(self, row_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music WHERE id = ?', (row_id,)).fetchone()

    def count_rows(self):
        with self.connection:
            return self.cursor.execute('SELECT COUNT(*) FROM music').fetchone()[0]

    def add(self, file_id, name):
        with self.connection:
            self.cursor.execute('INSERT INTO music(file_id, name) VALUES (?, ?)', (file_id, name))

    def close(self):
        self.connection.close()
