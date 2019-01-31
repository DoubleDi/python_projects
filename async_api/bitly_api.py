import asyncio
import aiohttp
from base64 import b64encode
from collections import namedtuple
import json
import logging

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

    def __init__(self, session, access_token=None):
        self.session = session
        self.access_token = access_token
        self.base_url = "https://api-ssl.bitly.com"
        self.uri = []

    def __build_url(self):
        path = "/".join(self.uri)
        self.uri = []
        return f"{self.base_url}/v3/{path}"

    def __getattr__(self, attr):
        self.uri.append(attr)
        return self

    async def __call__(self, *args, **kwargs):
        logger.info(f"Request method {self.uri} with args {kwargs}")
        url = self.__build_url()
        kwargs['access_token'] = self.access_token

        logger.debug(f"Request url {url}")
        async with self.session.get(url, params=kwargs) as response:
            if response.status != 200:
                raise APIException(response.status, 'BITLY API ERROR')
            json_response = await response.json()
            if json_response.get('data', None) is None:
                raise APIException(json_response['status_code'], json_response['status_txt'])

            response_tuple = namedtuple('response', json_response['data'].keys())
            return response_tuple(**json_response['data'])


class BitlyAPI(object):
    def __init__(self, username=None, password=None, token=None):
        assert(username and password or token)

        self.username = username
        self.password = password
        self.token = token

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()

        if self.token is None:
            url = 'https://api-ssl.bitly.com/oauth/access_token'
            base64_token = b64encode(f'{self.username}:{self.password}'.encode()).decode()
            headers = {'Authorization': 'Basic ' + base64_token}
            async with self.session.post(url, headers=headers) as response:
                text = await response.text()
                try:
                    bad_response = json.loads(text)
                    raise APIException(bad_response['status_code'], bad_response['status_txt'])
                except json.JSONDecodeError:
                    self.token = text

        return self

    def __getattr__(self, attr):
        api = BitlyLinkAPI(self.session, self.token)
        return getattr(api, attr)


    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


async def call_bitly_api(**credentials):
    async with BitlyAPI(**credentials) as api:
        links = ['http://bit.ly/2RSlC59', 'http://bit.ly/2RSlC59']
        try:
            responses = await asyncio.gather(
                *[api.link.clicks(link=link) for link in links],
            )

            for link, response in zip(links, responses):
                logger.info(f"{link} has {response.link_clicks} clicks")  # output: <number of clicks>
        except APIException as err:
            logger.warn(err)
        try:
            responses = await asyncio.gather(
                api.link.countries(link='http://bit.ly/2RSlC59'),
                api.user.clicks(),
            )

            logger.info(f"http://bit.ly/2RSlC59 has {responses[0]}")
            logger.info(f"user has {responses[1]}")
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
