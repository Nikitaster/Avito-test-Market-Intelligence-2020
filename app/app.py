import asyncio

from typing import List
from fastapi import FastAPI, Query, HTTPException, Path

from tortoise.contrib.fastapi import register_tortoise
from models import Searches, SearchesModel, SearchesModelReadonly, Stats, StatsModel

from datetime import datetime, timedelta
from api_requests import get_announcement_amount, get_location_id

app = FastAPI()

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@database:5432/database",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


async def stats_update():
    while True:
        await asyncio.sleep(1)
        searches_all = await Searches.all()
        for search in searches_all:
            stats_filter = await Stats.filter(search_id=search.id).order_by('-created_at').limit(1)
            if stats_filter:
                stat = stats_filter[0]
                if datetime.now().timestamp() - stat.created_at.timestamp() >= 3600:
                    announcement_amount = await get_announcement_amount(search.search_phrase, search.location_id)
                    await Stats.create(announcement_amount=announcement_amount, search_id=search.id)

asyncio.create_task(stats_update())


@app.get('/searches/', response_model=List[SearchesModel])
async def searches():
    return await SearchesModel.from_queryset(Searches.all())


@app.post("/add", response_model=SearchesModel)
async def create_search(search: SearchesModelReadonly):
    search_dict = search.dict(exclude_unset=False)
    search_dict['search_phrase'] = search_dict['search_phrase'].lower()
    search_dict['location_id'] = await get_location_id(search_dict['region'])

    if not search_dict['location_id']:
        raise HTTPException(status_code=404, detail="Region not found")

    search_obj = await Searches.create(**search_dict)

    announcement_amount = await get_announcement_amount(search_obj.search_phrase, search_obj.location_id)
    await Stats.create(announcement_amount=announcement_amount, search_id=search_obj.id)
    return await SearchesModel.from_tortoise_orm(search_obj)


@app.get('/stats/')
async def stats(pk: int = Query(..., gt=0),
                from_datetime: datetime = Query(datetime.now() - timedelta(days=7)),
                to_datetime: datetime = Query(datetime.now())
                ):
    stats_queryset = Stats.filter(search_id=pk, created_at__gte=from_datetime, created_at__lte=to_datetime)
    return await StatsModel.from_queryset(stats_queryset)


@app.get('/stats/top/{search_id}', response_model=List[StatsModel])
async def top(search_id: int = Path(..., gt=0)):
    stats_all = Stats.filter(search_id=search_id).order_by('-announcement_amount').limit(5)
    return await StatsModel.from_queryset(stats_all)

