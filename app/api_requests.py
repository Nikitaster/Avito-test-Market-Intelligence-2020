import aiohttp

from conf import API_KEY


async def get_location_id(region: str) -> int:
    """
    This method do request to avito api for getting location code
    :param region: region name
    :type: int
    :return: location_id or 0 if not exist
    :rtype: int
    """

    async with aiohttp.ClientSession() as session:
        async with session.get('https://m.avito.ru/api/1/slocations',
                               params={'key': API_KEY, 'q': region}) as response:
            locations = await response.json()
            for cur_location in locations['result']['locations']:
                if cur_location['names']['1'].lower() == region.lower():
                    return cur_location['id']
                return 0


async def get_announcement_amount(query: str, location_id: int) -> int:
    """
    This method used to gets current amount of announcements by query and location id

    :param query: search text
    :param location_id: location id
    :return: announcement amount
    :rtype: int
    """

    async with aiohttp.ClientSession() as session:
        async with session.get('http://m.avito.ru/api/9/items',
                               params={'key': API_KEY, 'locationId': location_id, 'query': query}) as response:
            result_amount = await response.json()
            return result_amount['result']['mainCount']
