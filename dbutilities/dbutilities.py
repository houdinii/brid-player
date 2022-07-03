import sqlite3
from datetime import datetime

conn = None


class DBUtilities:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, filename):
        try:
            self.conn = sqlite3.connect(filename)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            return self.conn
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            self.conn = None
            self.cursor = None
            return None

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("The SQLite connection is closed")

    def get_db_connection(self):
        return self.conn

    def get_db_cursor(self):
        return self.cursor

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def create_tables(self):
        create_download_table_query = '''CREATE TABLE bp_Downloads (
                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         download_id TEXT,
                                         filename TEXT,
                                         mimeType TEXT,
                                         filesize INTEGER,
                                         link TEXT,
                                         host TEXT,
                                         host_icon TEXT,
                                         chunks INTEGER,
                                         download TEXT,
                                         streamable INTEGER,
                                         generated TEXT);
                                         '''

        create_detailed_info_table_query = '''CREATE TABLE bp_detailed_info(
                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              download_id TEXT,
                                              filename TEXT,
                                              hoster TEXT,
                                              link TEXT,
                                              type TEXT,
                                              season TEXT,
                                              episode TEXT,
                                              year INTEGER,
                                              duration REAL,
                                              bitrate INTEGER,
                                              size INTEGER,
                                              poster_path TEXT,
                                              backdrop_path TEXT,
                                              baseUrl TEXT,
                                              modelUrl TEXT,
                                              host TEXT
            );'''

        create_available_formats_table_query = '''CREATE TABLE bp_available_formats(
                                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                  download_id TEXT,
                                                  label TEXT,
                                                  extension TEXT
        );'''

        try:
            self.cursor.execute(create_download_table_query)
            self.cursor.execute(create_detailed_info_table_query)
            self.cursor.execute(create_available_formats_table_query)
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as error:
            print("Error while creating table", error)

    def add_download_record(self, record):
        insert_query = '''INSERT INTO bp_Downloads (download_id, filename, mimeType, filesize, link, host, host_icon, chunks, download, streamable, generated)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        print(f"RECORD: {record}")
        print(f"TYPE RECORD: {type(record)}")
        try:
            self.cursor.execute(insert_query, (record['id'], record['filename'], record['mimeType'], record['filesize'], record['link'], record['host'], record['host_icon'], record['chunks'], record['download'], record['streamable'], record['generated']))
            self.conn.commit()
            return True
        except sqlite3.Error as error:
            print("Error while adding record", error)
            return False

    def add_available_formats_record(self, record, download_id):
        insert_query = '''INSERT INTO bp_available_formats (
                          download_id, 
                          label, 
                          extension)
                          VALUES (?, ?, ?);'''

        print(f"RECORD: {record}")
        print(f"TYPE RECORD: {type(record)}")

        try:
            self.cursor.execute(insert_query, (
                                    download_id,
                                    record['label'],
                                    record['extension']))
            self.conn.commit()
            return True
        except sqlite3.Error as error:
            print("Error while adding record", error)
            return False

    def add_detailed_info_record(self, record, download_id):
        insert_query = '''INSERT INTO bp_detailed_info (
                          download_id, 
                          filename, 
                          hoster, 
                          link, 
                          type, 
                          season, 
                          episode, 
                          year, 
                          duration, 
                          bitrate, 
                          size, 
                          poster_path, 
                          backdrop_path, 
                          baseUrl, 
                          modelUrl, 
                          host)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

        print(f"RECORD: {record}")
        print(f"TYPE RECORD: {type(record)}")

        try:
            self.cursor.execute(insert_query, (
                                    download_id,
                                    record['filename'],
                                    record['hoster'],
                                    record['link'],
                                    record['type'],
                                    record['season'],
                                    record['episode'],
                                    record['year'],
                                    record['duration'],
                                    record['bitrate'],
                                    record['size'],
                                    record['poster_path'],
                                    record['backdrop_path'],
                                    record['baseUrl'],
                                    record['modelUrl'],
                                    record['host']))
            self.conn.commit()
            return True
        except sqlite3.Error as error:
            print("Error while adding record", error)
            return False

    def delete_download_record(self, download_id):
        # TODO: delete all records with the same download_id in ALL TABLES
        delete_query = f"DELETE FROM bp_Downloads WHERE download_id = '{download_id}'"
        try:
            self.cursor.execute(delete_query)
            self.conn.commit()
            return True
        except sqlite3.Error as error:
            print("Error while deleting record", error)
            return False

    def query_db(self, table, query, columns="*"):
        query_query = f"SELECT {columns} FROM {table} WHERE {query}"
        try:
            self.cursor.execute(query_query)
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            print("Error while querying db", error)
            return None

    def get_all_download_records(self):
        query = f"SELECT * FROM bp_Downloads"
        try:
            results = self.cursor.execute(query)
            self.conn.commit()
            return results.fetchall()
        except sqlite3.Error as error:
            print("Error while getting all download records", error)
            return False

    def get_formats_for_download(self, download_id):
        query = f"SELECT * FROM bp_available_formats WHERE download_id = '{download_id}'"
        try:
            results = self.cursor.execute(query)
            self.conn.commit()
            return results.fetchall()
        except sqlite3.Error as error:
            print("Error while getting all download records", error)
            return False

    def get_detailed_info(self, download_id):
        query = f"SELECT * FROM bp_detailed_info WHERE download_id = '{download_id}'"
        try:
            results = self.cursor.execute(query)
            self.conn.commit()
            return results.fetchall()
        except sqlite3.Error as error:
            print("Error while getting all download records", error)
            return False


if __name__ == '__main__':
    choice = input("Do you want to create a new database? (y/n)")
    if choice.lower() == 'y':
        db = DBUtilities()
        db.connect('..\\bpData.db')
        db.create_tables()
        db.close()
