import asyncio
import aiohttp
from collections import namedtuple
import logging
import sys
from base64 import b64encode

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ACCESS_TOKEN = '_'
USERNAME = '_'
PASSWORD = '_'

class APIException(Exception):

    def __init__(self, status, message):
        super(APIException, self).__init__(f"[{status}] {message}")


class BitlyLinkAPI(object):

    def __init__(self, access_token=None):
        asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()
        self.access_token = access_token
        self.base_url = "https://api-ssl.bitly.com"

    def __build_url(self, link):
        if not link.startswith("http"):
            link = f"http://bit.ly/{link}"
        return f"{self.base_url}/v3/link/clicks?access_token={self.access_token}&link={link}"

    async def clicks(self, link=None):
        logger.info(f"GET clicks for url {link}")
        url = self.__build_url(link)

        logger.debug(f"Request url {url}")
        async with self.session.get(url) as response:
            if response.status != 200:
                raise APIException(response.status, 'BITLY API ERROR')
            json_response = await response.json()
            if json_response.get('data', None) is None:
                raise APIException(404, 'NOT FOUND')
            return namedtuple('response', json_response['data'].keys())(**json_response['data'])

    async def close(self):
        await self.session.close()


class BitlyAPI(object):
    def __init__(self, username=None, password=None, token=None):
        assert(username and password or token)

        self.username = username
        self.password = password
        self.token = token

    async def __aenter__(self):
        if self.token is None:
            url = 'https://api-ssl.bitly.com/oauth/access_token'
            headers = {'Authorization': 'Basic ' + b64encode(f'{self.username}:{self.password}'.encode()).decode()}
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url) as response:
                    self.token = await response.text()


        self.link = BitlyLinkAPI(self.token)

        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.link.close()


async def call_bitly_api(**credentials):
    async with BitlyAPI(**credentials) as api:
        links = ['http://bit.ly/2RSlC59', '2RSlC59']
        try:
            responses = await asyncio.gather(
                *[api.link.clicks(link=link) for link in links],
            )

            for link, response in zip(links, responses):
                logger.info(f"{link} has {response.link_clicks} clicks")  # output: <number of clicks>
        except APIException as err:
            logger.warn(err)

        try:
            response = await api.link.clicks(link='very_bad_link')
        except APIException as err:
            logger.warn(err)  # output: [404] NOT FOUND

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(call_bitly_api(token=ACCESS_TOKEN))
    loop.run_until_complete(call_bitly_api(username=USERNAME, password=PASSWORD))
    loop.close()
