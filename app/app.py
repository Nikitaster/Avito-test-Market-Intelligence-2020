from typing import List
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse

from tortoise.contrib.fastapi import register_tortoise
from models import Searches, SearchesModel, SearchesModelReadonly, Stats, \
    StatsModel, StatsModelReadonly

from datetime import datetime
from api_requests import RequesterToAPI

app = FastAPI()

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@database:5432/database",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get('/')
async def root():
    return RedirectResponse('/docs')


@app.get('/searches/', response_model=List[SearchesModel])
async def searches():
    return await SearchesModel.from_queryset(Searches.all())


@app.get('/searches/get/{pk}', response_model=SearchesModel)
async def get(pk: int):
    return await Searches.get(id=pk)


@app.post("/add", response_model=SearchesModel)
async def create_search(search: SearchesModelReadonly):
    api_requests: RequesterToAPI = RequesterToAPI('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')

    search_dict = search.dict(exclude_unset=False)
    search_dict['search_phrase'] = search_dict['search_phrase'].lower()
    search_dict['location_id'] = api_requests.get_location_id(search_dict['region'])

    if not search_dict['location_id']:
        raise HTTPException(status_code=404, detail="Region not found")

    search_obj = await Searches.create(**search_dict)
    return await SearchesModel.from_tortoise_orm(search_obj)


@app.get('/stats/')
async def stats(pk: int = Query(..., gt=0),
                from_datetime: datetime = Query(...),
                to_datetime: datetime = Query(datetime.now())
                ):
    stats_queryset = Stats.filter(search_id=pk, created_at__gte=from_datetime, created_at__lte=to_datetime)
    return await StatsModel.from_queryset(stats_queryset)



