import asyncio
import logging
from typing import Union

from fastapi import FastAPI, status
from starlette.responses import Response

import config
from wb_api.api import WBSupplyAPI
from wb_api.errors import RPSError, UnauthorizedError, UnexpectedError
from wb_api.schemas import (SupplyError, SupplyId, WBSPreorders,
                            WBSPreordersPost, WBSupplyAdd)

server = FastAPI(
    debug=config.DEBUG,
    title='WBS_Supply',
    description='''Сервис поставок''',
    version=config.VERSION
)

wbs = WBSupplyAPI()

log = logging.getLogger('SupplysAPP')

MAX_VALUE_COUNTER = 1000

SLEEP_STEP = 5


@server.post(
    '/wbs/supply', response_model=list[WBSPreorders],
    name='Получить поставки', tags=['WBSupply'], responses={
        status.HTTP_200_OK: {
            'model': list[WBSPreorders]
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'Превышено количество запросов,'
                           ' попробуйте повторить запрос'
                           ' через 1 минуту.'
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Ошибка авторизации. '
                           'Возможно неверный `token` или `supplier_id`.'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Во время запроса что-то пошло не так, '
                           'попробуйте повторить запрос позже, '
                           'если проблема сохранится, '
                           'свяжитесь с разработчиком.'
        }
    },
)
async def get_preorders(request: WBSPreordersPost):
    try:
        log.debug(f'Called with args: ({request})')
        return await wbs.get_supplies(request)
    except UnauthorizedError:
        log.error(
            'Cant authorize seller by provided WBToken and supplier_id!'
        )
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except UnexpectedError:
        log.error(
            "Can't view supplies"
        )
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except RPSError:
        return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@server.post(
    '/wbs/supply_add',
    name='Запланировать поставку',
    tags=['WBSupply_add'],
    responses={
        status.HTTP_200_OK: {
            'model': Union[SupplyId, SupplyError]
        },
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Ошибка авторизации. '
                           'Возможно неверный `token` или `supplier_id`.'
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Во время запроса что-то пошло не так, '
                           'попробуйте повторить запрос позже, '
                           'если проблема сохранится, '
                           'свяжитесь с разработчиком.'
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'Превышено количество запросов,'
                           ' попробуйте повторить запрос'
                           ' через 1 минуту.'
        }
    },
)
async def add_preorders(request: WBSupplyAdd):
    try:
        log.debug(f'Called with args: ({request})')
        return await wbs.add_supplies(request)
    except UnauthorizedError:
        log.error(
            "Can't authorize seller by provided WBToken and supplier_id!"
        )
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except UnexpectedError:
        log.error(
            "Can't add supply"
        )
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except RPSError:
        return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@server.post(
    '/wbs/supply_add_unlimited',
    name='Запланировать поставку',
    tags=['WBSupply_add'],
    responses={
        status.HTTP_200_OK: {
            'model': Union[SupplyId, SupplyError]
        }})
async def add_preorders_no_limit(request: WBSupplyAdd):
    counter = 0
    answer = None
    while counter < MAX_VALUE_COUNTER:
        try:
            answer = await wbs.add_supplies(request)
            if answer.get('result'):
                break
            counter += 1
            await asyncio.sleep(SLEEP_STEP)
        except UnauthorizedError:
            log.error(
                "Can't authorize seller by provided WBToken and supplier_id!"
            )
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        except UnexpectedError:
            log.error(
                "Can't add supply"
            )
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except RPSError:
            return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    return answer

