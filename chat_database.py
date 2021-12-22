import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('chat.db')
        print ("Opened database successfully")

        check_table = conn.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='chat'; """).fetchall()

        if check_table:
            return conn
        else:
            conn.execute('''CREATE TABLE chat
                    (
                        chat_msg   TEXT    NOT NULL,
                        timestamp  DATETIME     NOT NULL
                    );''')
            return conn
    except Exception as ex:
        print("connection error")
        return False