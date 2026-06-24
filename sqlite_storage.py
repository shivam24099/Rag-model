import sqlite3

conn = sqlite3.connect(
    "chat_storage.db",
    check_same_thread=False
)

c = conn.cursor()

# c.execute("""CREATE TABLE student(
#           Name text,
#           Id integer,
#           Age integer
#           )""")

# Name = input("Name")
# id = int(input("id:"))
# age = int(input("age:"))

# first way of insertion 
# c.execute("INSERT INTO student VALUES (?, ?, ?)", (Name, id, age))

# second way of insertion (i think better for project ) (uses dictionary)
# c.execute("INSERT INTO student VALUES (:Name, :Id, :Age)",
#         ({'Name':Name, 'Id':id, 'Age':age}))

# c.execute("SELECT * FROM student WHERE Age=22")

# print(c.fetchall())

def create_message_table():
    c.execute("""
              CREATE TABLE messages(
              message_id integer PRIMARY KEY AUTOINCREMENT,  
              chat_id integer,
              role text,
              content text)""")


def save_message(chat_id, role, content):
    
    conn = sqlite3.connect("chat_storage.db")
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO messages(chat_id, role, content)
        VALUES (?, ?, ?)
        """,
        (chat_id, role, content)
    )

    conn.commit()
    conn.close()

def load_chat(chat_id):  
    conn = sqlite3.connect("chat_storage.db")
    c = conn.cursor()

    c.execute("SELECT role, content FROM messages WHERE chat_id=? ORDER BY message_id", (chat_id,))

    rows = c.fetchall()

    history = []

    for role, content in rows:

        history.append({
            "role": role,
            "content": content
        })

    conn.close()
    return history

def chat_table():
    c.execute("""
            CREATE TABLE chats (
              chat_id integer PRIMARY KEY AUTOINCREMENT)""")

def create_chat():
    conn = sqlite3.connect("chat_storage.db")
    c = conn.cursor()

    c.execute("INSERT INTO chats DEFAULT VALUES")

    conn.commit()

    chat_id = c.lastrowid
    conn.close()

    return chat_id


def get_all_chats():

    conn = sqlite3.connect("chat_storage.db")
    c = conn.cursor()

    c.execute("SELECT chat_id FROM chats")

    chats = [row[0] for row in c.fetchall()]

    conn.close()

    return chats

def delete_chat(chat_id):
    conn = sqlite3.connect("chat_storage.db")
    c = conn.cursor()

    c.execute("""
            DELETE FROM chats
            WHERE chat_id =?""", (chat_id,))
    
    c.execute("""
            DELETE FROM messages
            WHERE chat_id =?""", (chat_id,))
    
    conn.commit()
    
    c.close