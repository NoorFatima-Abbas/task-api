from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app=FastAPI()

#in-memory list of task dictionaries
tasks = [
    {"id": 0, "title": "Assignment 1", "done": False},
    {"id": 1, "title": "Assignment 2", "done": False},
    {"id": 2, "title": "Writing FastAPI code", "done": True},
]
next_id = 3

@app.get("/")
def read_root():
   return {"name":"Task API", "version":"1.0", "endpoints":["/tasks"]}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task 
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.get("/health")
def read_health():
 return {"status":"ok"}