import requests


class RequesterToAPI:
    """
    The ApiRequests class
    """

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(ApiRequests, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, key: str):
        self.key: str = key

    def get_location_id(self, region: str) -> int:
        """
        This method do request to avito api for getting location code
        :param region: region name
        :type: int
        :return: location_id or 0 if not exist
        :rtype: int
        """

        response: requests.models.Response = requests.get('https://m.avito.ru/api/1/slocations', {
            'key': self.key,
            'q': region,
        })

        for cur_location in response.json()['result']['locations']:
            if cur_location['names']['1'].lower() == region.lower():
                return cur_location['id']
        return 0

    def get_announcement_amount(self, query: str, location_id: int) -> int:
        """
        This method used to gets current amount of announcements by query and location id

        :param query: search text
        :param location_id: location id
        :return: announcement amount
        :rtype: int
        """
        response: requests.models.Response = requests.get('http://m.avito.ru/api/9/items', {
            'key': self.key,
            'locationId': location_id,
            'query': query
        })

        return response.json()['result']['totalCount']

