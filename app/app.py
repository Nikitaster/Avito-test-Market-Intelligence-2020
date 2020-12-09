"""The main application module."""

import asyncio

from typing import List
from datetime import datetime, timedelta

from fastapi import FastAPI, Query, HTTPException, Path
from fastapi.responses import RedirectResponse

from tortoise.contrib.fastapi import register_tortoise
from models import Searches, SearchesModel, SearchesModelReadonly, Stats, StatsModel

from api_requests import get_ads_amount, get_location_id

from conf import UPDATE_INTERVAL

app = FastAPI()

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@database:5432/database",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get('/', include_in_schema=False)
async def root():
    """
    This function redirects to /docs from /
    """

    return RedirectResponse("/docs")


@app.get('/searches/', response_model=List[SearchesModel])
async def searches() -> List[SearchesModel]:
    """This function provides get method to route /searches/

    :return: list of all searches records
    :rtype: List[SearchesModel]
    """

    return await SearchesModel.from_queryset(Searches.all())


@app.post("/add", response_model=SearchesModel)
async def create_search(search: SearchesModelReadonly):
    """This function provides the post method to route /add.

    :param search:
    :type search: :class: `SearchesModelReadonly`
    :return: error message or created Searches record
    """

    search_dict = search.dict(exclude_unset=False)
    search_dict['search_phrase'] = search_dict['search_phrase'].lower()
    search_dict['location_id'] = await get_location_id(search_dict['region'])

    if not search_dict['location_id']:
        raise HTTPException(status_code=404, detail="Region not found")

    search_obj = await Searches.create(**search_dict)

    ads_amount = await get_ads_amount(search_obj.search_phrase, search_obj.location_id)
    await Stats.create(ads_amount=ads_amount, search_id=search_obj.id)
    return await SearchesModel.from_tortoise_orm(search_obj)


@app.get('/stat')
async def stats(search_id: int = Query(..., gt=0),
                from_datetime: datetime = Query(datetime.now() - timedelta(days=7)),
                to_datetime: datetime = Query(datetime.now())
                ):
    """This method provides the get method to route /stats/

    :param search_id: primary key for finding necessary Searches record
    :param from_datetime: first field of datetime interval
    :param to_datetime: second filed of datetime interval
    :return: list of all Stats records for specified Searches record
    """

    stats_queryset = Stats.filter(
        search_id=search_id,
        created_at__gte=from_datetime,
        created_at__lte=to_datetime
    )
    return await StatsModel.from_queryset(stats_queryset)


@app.get('/stats/top/{search_id}', response_model=List[StatsModel])
async def top(search_id: int = Path(..., gt=0)) -> List[StatsModel]:
    """This function provides the get method to route /stats/top/{search_id}

    :param search_id: primary key for finding necessary record
    :return: list of all Stats records for specified Searches record
    :rtype: List[StatsModel]
    """

    stats_all = Stats.filter(search_id=search_id).order_by('-ads_amount').limit(5)
    return await StatsModel.from_queryset(stats_all)


async def stats_update():
    """This is async loop method which updates (appends) Stats for every
    Searches records.

    :return: None
    """

    while True:
        await asyncio.sleep(1)
        searches_all = await Searches.all()
        for search in searches_all:
            stats_filter = await Stats.filter(search_id=search.id).order_by('-created_at').limit(1)
            if stats_filter:
                stat = stats_filter[0]
                if datetime.utcnow().timestamp() - stat.created_at.timestamp() >= UPDATE_INTERVAL:
                    ads_amount = await get_ads_amount(search.search_phrase, search.location_id)
                    await Stats.create(ads_amount=ads_amount, search_id=search.id)


def stats_updater_run():
    """Таким образом я реализовал обход ошибки в тестах 'no running event
    loop'.

    :return: None
    """

    try:
        asyncio.create_task(stats_update())
    except RuntimeError:
        pass


stats_updater_run()
