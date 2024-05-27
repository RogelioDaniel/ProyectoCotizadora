from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

segundos_por_dia = 24 * 60 * 60
dias_por_mes = 30

# Calcular los segundos
segundos_por_mes = dias_por_mes * segundos_por_dia
current_time = datetime.now()
convert_to_stamp = int(round(current_time.timestamp()))
class Project(BaseModel):
    
    id: Optional[int] = None
    title: str
    status: bool = None
    timeMonths : int
    created = convert_to_stamp,
    deadline = convert_to_stamp + (segundos_por_mes) ,
    left_time : Optional[int] = None
    price : int
    employee_in : List[str] = None
    needed_skills: List[str] = None

    class Config:
        orm_mode = True

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