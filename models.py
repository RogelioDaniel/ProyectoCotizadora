from database import Base, SQLALCHEMY_DATABASE_URL
from sqlalchemy.types import Boolean,Integer,String, DateTime
from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
from databases import Database
from database import SQLALCHEMY_DATABASE_URL
from pydantic import BaseModel
metadata = MetaData()

projects = Table(
    'projects',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(50)),
    Column('status', Boolean, default=False),
    Column('created', Integer, nullable=True),
    Column('deadline', Integer, nullable=True),
    Column('left_time', Integer, nullable=True),
    Column('timeMonths',Integer, nullable=True),
    Column('price', Integer, nullable=True),
    Column('employee_in', ARRAY(String), nullable=True),
)

class ToDo(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    status = Column(Boolean,default=False)
    created = Column(Integer,  nullable=True)
    deadline = Column(Integer, nullable=True)
    left_time = Column(Integer,  nullable=True)
    timeMonths = Column(Integer,  nullable=True)
    price = Column(Integer, nullable=True)
    employee_in = Column(ARRAY(String),nullable=True)
    needed_skills= Column(ARRAY(String),nullable=True)

class ToDoEmployees(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    status = Column(Boolean,default=False)
    salary = Column(Integer)
    role = Column(String)
    skill = Column(ARRAY(String),nullable=True)
    experience_time = Column(Integer)
database = Database(SQLALCHEMY_DATABASE_URL)