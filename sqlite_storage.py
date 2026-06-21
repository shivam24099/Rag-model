import sqlite3

conn = sqlite3.connect('chat_storage.db')

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

    c.execute(
        """
        INSERT INTO messages(chat_id, role, content)
        VALUES (?, ?, ?)
        """,
        (chat_id, role, content)
    )

    conn.commit()

def load_chat(chat_id):    
    c.execute("SELECT * FROM messages WHERE chat_id=? ORDER BY message_id", (chat_id,))
    print(c.fetchall())


