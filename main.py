from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import Request
from fastapi.exceptions import RequestValidationError

class TaskCreate(BaseModel):
   title:str
   
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

#stage 3: Endpoint- Create Post a new task
@app.post("/tasks", status_code=201)
def create_task(task:TaskCreate):
   if not task.title or not task.title.strip():
      return JSONResponse(status_code=400, 
                          content={"error":"Title cannot be empty or contain only whitespace."})
   global next_id
   new_task={"id":next_id, "title":task.title, "done":False}
   tasks.append(new_task)
   next_id+=1
   return new_task

@app.exception_handler(RequestValidationError)
def validation_error_handler(request:Request, exc:RequestValidationError):
   return JSONResponse(status_code=400,content={"error":"Title is required and cannot be empty."})

