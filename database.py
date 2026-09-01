import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.environ["DATABASE_URL"]

def get_connection():
   conn=psycopg.connect(DATABASE_URL, row_factory=dict_row)
   return conn

def init_db():
    conn=get_connection()
    cursor=conn.cursor()
# create the table if it does not exist
    cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id SERIAL PRIMARY KEY,
title TEXT,
done BOOLEAN
)
   """ )
# seed initial data if table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count=cursor.fetchone()["count"]

    if count==0:
      cursor.execute(
        "INSERT INTO tasks(title, done) VALUES (%s, %s)",
        ("Do Exercise", False),
    )
      cursor.execute(
        "INSERT INTO tasks(title, done) VALUES (%s, %s)",
        ("Finish Backend Engineering Assignment", False),
    )
      cursor.execute(
        "INSERT INTO tasks(title, done) VALUES(%s, %s)",
        ("Read SQLite Documentation", False),
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

   #to covert each row object to a dictionary
   return[
      {"id":r["id"], "title":r["title"], "done":bool(r["done"])}
      for r in rows
   ]

# to get the task_by_id
def get_task_by_id(task_id:int):
   conn=get_connection()
   cursor=conn.cursor()

   cursor.execute(
      "SELECT id, title, done FROM tasks WHERE ID=%s",(task_id,)
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
   #new tasks default  done=0
   cursor.execute(
      "INSERT INTO tasks(title, done) VALUES (%s, %s) RETURNING id", (title, False),
   )
   new_id=cursor.fetchone()["id"]
   conn.commit()
   conn.close()
   return {"id":new_id, "title": title, "done":False}

# to update a task
def update_task_in_db(
    task_id: int, title: str | None = None, done: bool | None = None
):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Check if task exists
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    new_title = title if title is not None else row["title"]
    new_done = done if done is not None else row["done"]

    # 3. Update the database record
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s",
        (new_title, new_done, task_id),
    )
    conn.commit()
    conn.close()

    return {"id": task_id, "title": new_title, "done": bool(new_done)}

# to delete a task
def delete_task_from_db(task_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()

    return deleted_count > 0

if __name__=="__main__":
    init_db()
