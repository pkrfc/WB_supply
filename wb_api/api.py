from http import HTTPStatus
from secrets import token_hex

import aiohttp

from wb_api.errors import RPSError, UnauthorizedError, UnexpectedError
from wb_api.schemas import WBSPreorders


class WBSupplyAPI:
    SUPPLIES = ('https://seller.wildberries.ru'
                '/ns/sm-preorder/supply-manager/api/v1/preorder/list')
    SUPPLIES_ADD = ('https://seller.wildberries.ru'
                    '/ns/sm/supply-manager/api/v1/plan/add')
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (HTML, like Gecko) '
                      'Chrome/102.0.0.0 Safari/537.36',
        'Cookie': 'WBToken={}; locale=ru; x-supplier-id={};'
    }

    @classmethod
    async def get_supplies(cls, token, supplier_id):
        url = cls.SUPPLIES
        heads = cls.HEADERS.copy()
        heads['Cookie'] = heads['Cookie'].format(token, supplier_id)
        data = {
            "id": "json-rpc_43",
            "jsonrpc": "2.0"
        }
        async with aiohttp.ClientSession(headers=heads) as _session:
            async with _session.post(url, ssl=False, json=data) as response:
                error_id = token_hex(8)
                if response.ok:
                    preorders = (
                        await response.json()
                    ).get('result').get('preorders')
                    if preorders:
                        return [WBSPreorders(**i) for i in preorders]
                    return []
                elif response.status == HTTPStatus.UNAUTHORIZED:
                    raise UnauthorizedError(error_id, 'Ошибка авторизации.')
                elif response.status == HTTPStatus.TOO_MANY_REQUESTS:
                    raise RPSError(error_id=error_id, secs=60)

                else:
                    raise UnexpectedError(
                        error_id,
                        'Неожиданная ошибка. Свяжитесь с разработчиком.')

    @classmethod
    async def add_supplies(cls, supply, date, token, supplier_id):
        url = cls.SUPPLIES_ADD
        heads = cls.HEADERS.copy()
        heads['Cookie'] = heads['Cookie'].format(token, supplier_id)
        data = {
            "jsonrpc": "2.0",
            "id": "json-rpc_42",
            "params": {"preOrderId": supply, "deliveryDate": date.isoformat()}
        }
        async with aiohttp.ClientSession(headers=heads) as _session:
            async with _session.post(url, ssl=False, json=data) as response:
                if response.ok:
                    resp_json_error = (
                        await response.json()
                    ).get('error').get('message')
                    if resp_json_error:
                        return resp_json_error
