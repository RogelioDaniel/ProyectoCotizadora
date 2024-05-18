from typing import List
from fastapi import HTTPException, Header, APIRouter
from api import db_manager

from models import Project

project = APIRouter()

@project.get('/', response_model=List[Project])
async def index():
    return await db_manager.get_all_projects()

@project.post('/', status_code=201)
async def add_project(payload: Project):
    project_id = await db_manager.add_project(payload)
    response = {
        'id': project_id,
        **payload.dict()
    }

    return response

@project.put('/{id}')
async def update_project(id: int, payload: Project):
    project = await db_manager.get_project(id)
    if not project:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
    project_in_db = Project(**project)

    updated_project = project_in_db.copy(update=update_data)

    return await db_manager.update_movie(id, updated_project)

@project.delete('/{id}')
async def delete_project(id: int):
    project = await db_manager.get_project(id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return await db_manager.delete_project(id)