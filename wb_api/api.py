import logging
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

    log = logging.getLogger('WBS_Supply_API')

    @classmethod
    async def get_supplies(cls, request):
        cls.log.debug(f'Called with args: ({request})')
        url = cls.SUPPLIES
        heads = cls.HEADERS.copy()
        heads['Cookie'] = heads['Cookie'].format(
            request.token, request.supplier_id
        )
        data = {
            "id": "json-rpc_43",
            "jsonrpc": "2.0"
        }
        async with aiohttp.ClientSession(headers=heads) as _session:
            async with _session.post(url, ssl=False, json=data) as response:
                error_id = token_hex(8)
                if response.ok:
                    cls.log.debug(f'API returns [{response.status}]')
                    preorders = (
                        await response.json()
                    ).get('result').get('preorders')
                    if preorders:
                        return [WBSPreorders(**i) for i in preorders]
                    return []
                elif response.status == HTTPStatus.UNAUTHORIZED:
                    cls.log.error(
                        f'User use invalid/expired WBToken or '
                        f'unknown supplier_id. ({error_id})'
                    )
                    raise UnauthorizedError(error_id, 'Ошибка авторизации.')
                elif response.status == HTTPStatus.TOO_MANY_REQUESTS:
                    cls.log.error(
                        f'Triggered SUPPLY_API rate limit! ({error_id})'
                    )
                    raise RPSError(error_id=error_id)

                else:
                    api_resp = await response.json()
                    cls.log.error(
                        f'Unexpected API error ({error_id}) '
                        f'[{response.status}]: {api_resp}.'
                    )
                    raise UnexpectedError(
                        error_id,
                        'Неожиданная ошибка. Свяжитесь с разработчиком.')

    @classmethod
    async def add_supplies(cls, request):
        cls.log.debug(f'Called with args: ({request})')
        url = cls.SUPPLIES_ADD
        heads = cls.HEADERS.copy()
        heads['Cookie'] = heads['Cookie'].format(
            request.token, request.supplier_id
        )
        if request.monopalletCount is not None:
            params = {
                "preOrderId": request.preOrderId,
                "deliveryDate": request.deliveryDate.isoformat(),
                "monopalletCount": request.monopalletCount
            }
        else:
            params = {
                "preOrderId": request.preOrderId,
                "deliveryDate": request.deliveryDate.isoformat()
            }
        data = {
            "jsonrpc": "2.0",
            "id": "json-rpc_42",
            "params": params
        }
        async with aiohttp.ClientSession(headers=heads) as _session:
            async with _session.post(url, ssl=False, json=data) as response:
                error_id = token_hex(8)
                if response.ok:
                    return await response.json()
                elif response.status == HTTPStatus.UNAUTHORIZED:
                    cls.log.error(
                        f'User use invalid/expired WBToken or '
                        f'unknown supplier_id. ({error_id})'
                    )
                    raise UnauthorizedError(error_id, 'Ошибка авторизации.')
                elif response.status == HTTPStatus.TOO_MANY_REQUESTS:
                    cls.log.error(
                        f'Triggered SUPPLY_API rate limit! ({error_id})'
                    )
                    raise RPSError(error_id=error_id)
                else:
                    api_resp = await response.json()
                    cls.log.error(
                        f'Unexpected API error ({error_id}) '
                        f'[{response.status}]: {api_resp}.'
                    )
                    raise UnexpectedError(
                        error_id,
                        'Неожиданная ошибка. Свяжитесь с разработчиком.')
