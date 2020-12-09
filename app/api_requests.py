"""This module contains the functions operating with m.avito.ru/api."""

import aiohttp

from conf import API_KEY


async def get_location_id(region: str) -> int:
    """This method makes request to avito api for getting location code.

    :param region: region name
    :type: int
    :return: location_id or 0 if not exist
    :rtype: int
    """

    async with aiohttp.ClientSession() as session:
        async with session.get('https://m.avito.ru/api/1/slocations',
                               params={'key': API_KEY, 'q': region}) as response:
            response_json = await response.json()
            locations = list(response_json['result']['locations'])
            for location in locations:
                cur_location_name = location['names']['1']
                if cur_location_name.lower() == region.lower():
                    return location['id']
            return 0


async def get_ads_amount(query: str, location_id: int) -> int:
    """This method is used to get current amount of ads by query and location id.

    :param query: search text
    :type: str
    :param location_id: location id
    :type: int
    :return: ads amount for input search text and region
    :rtype: int
    """

    async with aiohttp.ClientSession() as session:
        async with session.get('http://m.avito.ru/api/9/items',
                               params={
                                   'key': API_KEY,
                                   'locationId': location_id,
                                   'query': query}
                               ) as response:
            result_amount = await response.json()
            return result_amount['result']['mainCount']
