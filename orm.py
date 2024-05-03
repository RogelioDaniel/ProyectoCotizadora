from models import ToDo, ToDoEmployees
from sqlalchemy.orm import Session
from datetime import datetime

segundos_por_dia = 24 * 60 * 60
dias_por_mes = 30

# Calcular los segundos
segundos_por_mes = dias_por_mes * segundos_por_dia
def add_todo(
        title:str,
        timeMonths:int,
        price:int,
        db:Session,
):
    current_time = datetime.now()
    convert_to_stamp = int(round(current_time.timestamp()))
    new_todo = ToDo(
        title=title,
        created = convert_to_stamp,
        deadline = convert_to_stamp + (timeMonths *segundos_por_mes) ,
        timeMonths=timeMonths,
        price = price,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def add_todo_employees(
        first_name:str,
        last_name:int,
        salary:int,
        db:Session,
):

    new_todo_employee = ToDoEmployees(
        first_name=first_name,
        last_name = last_name,
        salary = salary,
    )
    db.add(new_todo_employee)
    db.commit()
    db.refresh(new_todo_employee)
    return new_todo_employee

def update_todo(todo_id:int,db:Session):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    todo.status = not todo.status
    db.commit()

def delete_todo(
    id:int,
    db:Session
):
    delete = db.query(ToDo).filter(ToDo.id == id).first()
    db.delete(delete)
    db.commit()