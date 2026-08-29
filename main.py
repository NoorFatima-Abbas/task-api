from database import delete_task_from_db, add_task, get_all_tasks,get_task_by_id, init_db, update_task_in_db
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError

# for the POST updates in CRUD
class TaskCreate(BaseModel):
   title:str

# for the PUT(update) in CRUD
class TaskUpdate(BaseModel):
   title:str|None=None
   done:bool|None=None
   
app=FastAPI()
# call init_db in main.py
init_db()


@app.get("/", summary="API Info")
def read_root():
   return {"name":"Task API", "version":"1.0", "endpoints":["/tasks"]}

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}", summary="List the task by ID")
def get_task(task_id: int):
    task=get_task_by_id(task_id)
    if task is None:
        return JSONResponse(
            status_code=404, content={"error":f"Task {task_id} not found"}
        )
    return task

@app.get("/health", summary="Check Server Health")
def read_health():
 return {"status":"ok"}

#stage 3: Endpoint- Create Post a new task
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task:TaskCreate):
   if not task.title or not task.title.strip():
      return JSONResponse(status_code=400, 
                          content={"error":"Title cannot be empty or contain only whitespace."})
   new_task=add_task(task.title.strip())
   return new_task

@app.exception_handler(RequestValidationError)
def validation_error_handler(request:Request, exc:RequestValidationError):
   return JSONResponse(status_code=400,content={"error":"Title is required and cannot be empty."})

@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int,task_update:TaskUpdate ):
    # Validate title if it was provided
    if task_update.title is not None and not task_update.title.strip():
        return JSONResponse(
            status_code=400, content={"error": "Title cannot be empty"}
        )

    # Clean title string if provided
    clean_title = (
        task_update.title.strip() if task_update.title is not None else None
    )

    updated_task = update_task_in_db(
        task_id=task_id, title=clean_title, done=task_update.done
    )

    if updated_task is None:
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )

    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
def delete_task(task_id:int):
    deleted = delete_task_from_db(task_id)

    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )

    return None  # Returns 204 No Content
