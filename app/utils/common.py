import aiohttp
from aiohttp import TCPConnector

from app.utils.log import logger


async def async_request(
        method: str, url: str, auth=None, headers: dict = None, params: dict = None, json_body: dict = None):
    async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        kwargs = {
            'method': method,
            'url': url
        }
        if auth:
            kwargs['auth'] = auth
        if headers:
            kwargs['headers'] = headers
        if params:
            kwargs['params'] = params
        if json_body:
            kwargs['json'] = json_body
        async with session.request(**kwargs) as resp:
            resp_text = None
            resp_json = None
            try:
                resp_json = await resp.json()
            except aiohttp.ContentTypeError:
                try:
                    resp_text = await resp.text()
                except aiohttp.ContentTypeError:
                    pass
            resp.json_ = resp_json
            if resp.status in range(200, 300):
                logger.info(
                    'async_request METHOD - {}, URL - {}, STATUS - {}, OUTCOME_JSON - {}, JSON - {}, TEXT - {}'.format(
                        method, url, resp.status, json_body, resp.json_, resp_text))
            else:
                logger.error(
                    'async_request METHOD - {}, URL - {}, STATUS - {}, OUTCOME_JSON - {} JSON - {}, TEXT - {}'.format(
                        method, url, resp.status, json_body, resp.json_, resp_text))
            return resp


async def async_upload_file(method: str, url: str, file, token):
    async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        kwargs = {
            'method': method,
            'url': url,
            'data': file,
            'headers': {'Authorization': "Bearer {}".format(token)}}

        async with session.request(**kwargs) as resp:
            print(resp.status)
            if resp.status in range(200, 300):
                response = await resp.text()
                logger.info(response)
                return response
            else:
                logger.error(f'RESPONSE - {resp.status}, METHOD - {resp.method}, URL - {resp.url}')


async def parse_profile(row):
    json_body = dict()
    fio = row['ФИО'].split(' ')
    json_body["last_name"] = fio[0]
    json_body["first_name"] = fio[1]
    try:
        if fio[2] != '':
            json_body["middle_name"] = fio[2]
    except IndexError:
        pass
    json_body['position'] = row['Должность']

    money = row['Ожидания по ЗП'].replace(' ', '').replace('.0', '')
    money = "".join(c for c in money if c.isdecimal())
    json_body["money"] = money + ' руб'
    return json_body
