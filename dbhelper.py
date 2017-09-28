import psycopg2
import urllib.parse as urlparse
import os


class DBHelper:
    def __init__(self):
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                    )


    def setup(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (clothes_type text, result text, chat_id text, file_id text, status text)")
        self.conn.commit()

    def add_item(self, item_clothes_type, item_result, item_chat_id, item_file_id):
        cursor = self.conn.cursor()
        stmt = "INSERT INTO items (clothes_type, result, chat_id, file_id, status) VALUES (%s, %s, %s, %s, %s)"
        args = (item_clothes_type, item_result, item_chat_id, item_file_id, "nworn")
        cursor.execute(stmt, args)
        self.conn.commit()

    def reset_items(self, item_chat_id):
        cursor = self.conn.cursor()
        stmt = "UPDATE items SET status = 'nworn' WHERE chat_id = '%s' "
        args = (item_chat_id, )
        cursor.execute(stmt, args)
        self.conn.commit()

    def get_items(self, item_chat_id):
        cursor = self.conn.cursor()
        stmt = "SELECT clothes_type, file_id FROM items WHERE chat_id = ('%s') and status = (%s)"
        args = (item_chat_id, 'nworn')
        cursor.execute(stmt, args)
        results = cursor.fetchall()
        return results

    def accept_items(self, item_chat_id, item_file_id):
        cursor = self.conn.cursor()
        stmt = "UPDATE items SET status = 'worn' WHERE chat_id = ('%s') and file_id = (%s) "
        args = (item_chat_id, item_file_id, )
        cursor.execute(stmt, args)
        self.conn.commit()
