import sqlite3

DB_NAME="tasks.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
# create the table if it does not exist
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY,
title TEXT,
done INTEGER
)
   """ )
# seed initial data if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count=cursor.fetchone()[0]

    if count==0:
      cursor.execute(
        "INSERT INTO tasks(title, done) VALUES (?, ?)",
        ("Do Exercise", 0),
    )
      cursor.execute(
        "INSERT INTO tasks(title, done) VALUES (?, ?)",
        ("Finish Backend Engineering Assignment", 0),
    )
      cursor.execute(
        "INSERT INTO tasks(title, done) VALUES(?,?)",
        ("Read SQLite Documentation", 0),
    )
# save changes and close
    conn.commit()
    conn.close()

if __name__=="__main__":
    init_db()
