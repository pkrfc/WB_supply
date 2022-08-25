import aiohttp
import asyncio
import json

from wb_api.schemas import WBSPreorders


class WBSupplyAPI:
    SUPPLIES = 'https://seller.wildberries.ru/ns/sm-preorder/supply-manager/api/v1/preorder/list'
    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/102.0.0.0 Safari/537.36')
    COOKIE = ('*')
    HEADERS = {
        'User-Agent': USER_AGENT,
        'Cookie': COOKIE
    }

    @classmethod
    async def get_supplies(cls):
        url = cls.SUPPLIES
        heads = cls.HEADERS
        data = {
            "id": "json-rpc_43",
            "jsonrpc": "2.0"
        }
        async with aiohttp.ClientSession(headers=heads) as _session:
            async with _session.post(url, ssl=False, json=data) as response:
                if response.ok:
                    preorders = (await response.json()).get('result').get('preorders')
                    if preorders:
                        return [WBSPreorders(**i) for i in preorders]
                    return []


