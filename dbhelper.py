import sqlite3

class DBHelper:
    def __init__(self, dbname="fashioner.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (clothes_type text, result text, chat_id text, file_id text, status text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, item_clothes_type, item_result, item_chat_id, item_file_id):
        stmt = "INSERT INTO items (clothes_type, result, chat_id, file_id, status) VALUES (?, ?, ?, ?, ?)"
        args = (item_clothes_type, item_result, item_chat_id, item_file_id, "nworn")
        self.conn.execute(stmt, args)
        self.conn.commit()

    def reset_items(self, item_chat_id):
        stmt = "UPDATE items SET status = 'nworn' WHERE chat_id = (?) "
        args = (item_chat_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, item_chat_id):
        stmt = "SELECT clothes_type, file_id FROM items WHERE chat_id = (?) and status = (?)"
        args = (item_chat_id, 'nworn')
        cursor = self.conn.execute(stmt,args)
        results = cursor.fetchall()
        return results

    def accept_items(self, item_chat_id, item_file_id):
        stmt = "UPDATE items SET status = 'worn' WHERE chat_id = (?) and file_id = (?) "
        args = (item_chat_id, item_file_id, )
        self.conn.execute(stmt, args)
        self.conn.commit()
