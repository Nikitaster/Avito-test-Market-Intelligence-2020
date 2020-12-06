from typing import List
from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise
from models import Searches, SearchesModel, SearchesModelReadonly, Stats, StatsModel, StatsModelReadonly


app = FastAPI()

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@database:5432/database",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get('/searches/', response_model=List[SearchesModel])
async def root():
    return await SearchesModel.from_queryset(Searches.all())


@app.get('/searches/get/{pk}', response_model=SearchesModel)
async def get(pk: int):
    return await Searches.get(id=pk)


@app.post("/add", response_model=SearchesModel)
async def create_search(search: SearchesModelReadonly):
    search_dict = search.dict(exclude_unset=False)
    search_dict['search_phrase'] = search_dict['search_phrase'].lower()
    search_dict['region'] = search_dict['region'].lower()
    search_obj = await Searches.create(**search_dict)
    return await SearchesModel.from_tortoise_orm(search_obj)


@app.get('/stats/', response_model=List[StatsModel])
async def stats():
    return await StatsModel.from_queryset(Stats.all())