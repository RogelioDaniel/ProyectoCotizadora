from database import Base
from sqlalchemy.types import Boolean,Integer,String, DateTime
from sqlalchemy import Column

class ToDo(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(Boolean,default=False)
    created = Column(Integer)
    deadline = Column(Integer)
    left_time = Column(Integer)
    timeMonths = Column(Integer)
    price = Column(Integer)
class ToDoEmployees(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    status = Column(Boolean,default=False)
    salary = Column(Integer)
    role = Column(String)
