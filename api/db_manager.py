from models import projects, database,ToDo


async def add_projects(payload: ToDo):
    query = projects.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_movies():
    query = projects.select()
    return await database.fetch_all(query=query)

async def get_movie(id):
    query = projects.select(projects.c.id==id)
    return await database.fetch_one(query=query)

async def delete_movie(id: int):
    query = projects.delete().where(projects.c.id==id)
    return await database.execute(query=query)

async def update_movie(id: int, payload: ToDo): 
    query = (
        projects
        .update()
        .where(projects.c.id == id)
        .values(**payload.dict())
    )
    return await database.execute(query=query)