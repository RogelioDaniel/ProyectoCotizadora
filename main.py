from typing import List
from fastapi import FastAPI, HTTPException, Request, Depends, Form, status, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import get_db
from database import engine
from sqlalchemy.orm import Session
from models import ToDo, ToDoEmployees
from orm import add_todo,add_todo_employees,update_todo,delete_todo
from starlette.responses import RedirectResponse
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import schema   
import models



app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
models.Base.metadata.create_all(bind=engine)
router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)
templates = Jinja2Templates("templates")
async def homepage(request):
    return templates.TemplateResponse(request, 'index.html')

class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    status: bool
    salary: int
    role: str
    skill: List[str]
    experience_time: int

    class Config:
        orm_mode = True
        
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
    return todos_employee
@app.post("/recommendations", response_model=List[schema.Employee])
def get_recommendations(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ToDo).filter(ToDo.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    employees = db.query(ToDoEmployees).all()
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")

    # Convertir las habilidades a un formato binario
    all_skills = set(skill for emp in employees if emp.skill for skill in emp.skill)
    skill_index = {skill: idx for idx, skill in enumerate(all_skills)}
    needed_skills_vector = np.zeros(len(skill_index))
    for skill in project.needed_skills:
        if skill in skill_index:
            needed_skills_vector[skill_index[skill]] = 1

    employee_vectors = []
    for emp in employees:
        if emp.skill:
            emp_vector = np.zeros(len(skill_index))
            for skill in emp.skill:
                if skill in skill_index:
                    emp_vector[skill_index[skill]] = 1
            employee_vectors.append(emp_vector)

    if not employee_vectors:
        raise HTTPException(status_code=404, detail="No employee skills available for comparison")

    employee_vectors = np.array(employee_vectors)
    similarities = cosine_similarity([needed_skills_vector], employee_vectors)[0]

    # Ordenar los empleados por similitud
    sorted_indices = np.argsort(similarities)[::-1]
    sorted_employees = [employees[idx] for idx in sorted_indices]

    return sorted_employees

@app.post("/add",status_code=status.HTTP_201_CREATED)

def add(post_post:schema.Project, db:Session = Depends(get_db)):

    new_post = models.ToDo(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    url = app.url_path_for("todo_projects")
    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)


@app.post("/add_employee",status_code=status.HTTP_201_CREATED)
def add_employee(post_post:schema.Employee, db:Session = Depends(get_db)

):
    new_post = models.ToDoEmployees(**post_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
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


