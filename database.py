import sqlite3


DB_NAME="tasks.db"

def get_connection():
   conn=sqlite3.connect(DB_NAME)
   conn.row_factory=sqlite3.Row
   return conn

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
# to get all the tasks
def get_all_tasks():
   conn=get_connection()
   cursor=conn.cursor()
   cursor.execute("SELECT id, title, done FROM tasks")
   rows=cursor.fetchall()
   conn.close()

   #to covert each r ow object to a dictionary
   return[
      {"id":row["id"], "title":row["title"], "done":bool(row["done"])}
      for row in rows
   ]

# to get the task_by_id
def get_task_by_id(task_id:int):
   conn=get_connection()
   cursor=conn.cursor()

   cursor.execute(
      "SELECT id, title, done FROM tasks WHERE ID=?",(task_id,)
   )
   row=cursor.fetchone()
   conn.close()
   if row is None:
      return None

   return {"id":row["id"], "title":row["title"], "done":bool(row["done"])}


#to post  a task
def add_task(title:str):
   conn=get_connection()
   cursor=conn.cursor()
   #new tasks default o done=0
   cursor.execute(
      "INSERT INTO tasks(title, done) VALUES (?, ?)", (title, 0)
   )
   conn.commit()
   #retrieve the auto-incremented primary key
   new_id=cursor.lastrowid
   conn.close()
   return {"id":new_id, "title": title, "done":False}

# to update a task
def update_task_in_db(
    task_id: int, title: str | None = None, done: bool | None = None
):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Check if task exists
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    # 2. Keep existing values if optional fields weren't passed
    current_title = row["title"]
    current_done = row["done"]

    new_title = title if title is not None else current_title
    new_done = int(done) if done is not None else current_done

    # 3. Update the database record
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, task_id),
    )
    conn.commit()
    conn.close()

    return {"id": task_id, "title": new_title, "done": bool(new_done)}

# to delete a task
def delete_task_from_db(task_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    deleted_count = cursor.rowcount
    conn.close()

    return deleted_count > 0

if __name__=="__main__":
    init_db()
