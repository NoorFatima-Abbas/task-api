from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import Request
from fastapi.exceptions import RequestValidationError

# for the POST updates in CRUD
class TaskCreate(BaseModel):
   title:str

# for the PUT(update) in CRUD
class TaskUpdate(BaseModel):
   title:str|None=None
   done:bool|None=None
   
app=FastAPI()

#in-memory list of task dictionaries
tasks = [
    {"id": 0, "title": "Assignment 1", "done": False},
    {"id": 1, "title": "Assignment 2", "done": False},
    {"id": 2, "title": "Writing FastAPI code", "done": True},
]
next_id = 3

@app.get("/", summary="API Info")
def read_root():
   return {"name":"Task API", "version":"1.0", "endpoints":["/tasks"]}

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="List the task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task 
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.get("/health", summary="Check Server Health")
def read_health():
 return {"status":"ok"}

#stage 3: Endpoint- Create Post a new task
@app.post("/tasks", status_code=201, summary="Create a new task")
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

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int,task_update:TaskUpdate ):
    # 1. Find the task
    found_task = None
    for task in tasks:
        if task["id"] == task_id:
            found_task = task
            break

    # 2. Handle 404 outside the loop
    if not found_task:
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )
    # Validate title if it was provided
    if task_update.title is not None:
       if not task_update .title.strip():
          return JSONResponse(status_code=400, content={"error":"Title cannot be empty"})
       found_task["title"]=task_update.title

       #Update done status it it was provided
    if task_update.done is not None:
          found_task["done"]=task_update.done
    return found_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id:int):
    #Loop to find the task
    for task in tasks:
        if task["id"]==task_id:
            tasks.remove(task)
            return None       #204 response with an empty body

    #if loop finishes without returning , task wasn't found
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error":f"Task {task_id} not found"}
    )
