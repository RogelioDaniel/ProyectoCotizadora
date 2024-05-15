from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import get_db
import models
from database import engine
from sqlalchemy.orm import Session
from models import ToDo, ToDoEmployees
from orm import add_todo,add_todo_employees,update_todo,delete_todo
from starlette.responses import RedirectResponse
from datetime import datetime

app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates("templates")
async def homepage(request):
    return templates.TemplateResponse(request, 'index.html')
@app.get("/", response_class=HTMLResponse)
async def home(
        request:Request, 
        db: Session = Depends(get_db),
):
    todos = db.query(ToDo).all()
    return templates.TemplateResponse("index.html",{"request":request,"todo_list":todos})
@app.get("/all_projects", response_class=HTMLResponse)
async def todo_projects(
        request:Request, 
        db: Session = Depends(get_db),
):
    todos = db.query(ToDo).all()
    return templates.TemplateResponse("buttons.html",{"request":request,"todo_list":todos})

@app.get("/employee")
def page_employee(
        request:Request, 
        db: Session = Depends(get_db),
):
    todos_employee = db.query(ToDoEmployees).all()
    return templates.TemplateResponse("employees.html",{"request":request,"todo_list_emp":todos_employee})

@app.post("/add")
def add(
    request:Request,
    db: Session=  Depends(get_db),
    title:str = Form(...),
    timeMonths:int = Form(...),
    price:int = Form(...),
):
    add_todo(title,timeMonths,price,db)
    url = app.url_path_for("todo_projects")
    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.post("/add_employee")
def add_employee(
    request:Request,
    db: Session=  Depends(get_db),
    first_name:str = Form(...),
    last_name:str = Form(...),
    salary:int = Form(...),
):
    add_todo_employees(first_name,last_name,salary,db)
    url = app.url_path_for("page_employee")
    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.get("/update/{todo_id}")
def update(
    request:Request,
    todo_id:int,
    db:Session = Depends(get_db)
):
    update_todo(todo_id,db)
    url = app.url_path_for("todo_projects")
    return RedirectResponse(url,status_code=status.HTTP_302_FOUND)

@app.get("/delete/{id}")
def delete(
    request:Request,
    id:int,
    db:Session = Depends(get_db)
):
    delete_todo(id,db)
    url = app.url_path_for("todo_projects")
    return RedirectResponse(url,status_code=status.HTTP_302_FOUND)



@app.get("/time/{todo_id}")
def time_left(
    request:Request,
    todo_id:int,
    db:Session = Depends(get_db)
):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    current_time = datetime.now()
    convert_to_stamp = int(round(current_time.timestamp()))
    todo_left =  todo.deadline - convert_to_stamp
    todo.left_time = todo_left
    db.commit()
    url = app.url_path_for("todo_projects")
    return RedirectResponse(url,status_code=status.HTTP_302_FOUND)


