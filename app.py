from fastapi import FastAPI, status
from typing import Union

from starlette.responses import Response

from wb_api.api import WBSupplyAPI
from wb_api.errors import UnauthorizedError, UnexpectedError, RPSError
from wb_api.schemas import WBSPreorders, WBSPreordersPost, WBSupplyAdd, SupplyError, SupplyId

server = FastAPI(
    debug=True,
    title='WBSPreorders',
    description='''Сервис поставок''',
    version='0.5.4'
)

wbs = WBSupplyAPI()


@server.post(
    '/wbs/supply', response_model=list[WBSPreorders],
    name='Получить поставки', tags=['WBSupply'], responses={
        status.HTTP_200_OK: {
            'model': list[WBSPreorders]
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            'description': 'Превышено колличество запросов,'
                           ' попробуйте повторить запрос'
                           ' через 1 минуту.\n\n`retry_after` '
                           '- Колличество секунд которое необходимо'
                           ' подождать перед следующим запросом.'
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
    token = request.token
    supplier_id = request.supplier_id
    try:
        return await wbs.get_supplies(token, supplier_id)
    except UnauthorizedError:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except UnexpectedError:
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
            'description': 'Превышено колличество запросов,'
                           ' попробуйте повторить запрос'
                           ' через 1 минуту.\n\n`retry_after` '
                           '- Колличество секунд которое необходимо'
                           ' подождать перед следующим запросом.'
        }
    },
)
async def add_preorders(request: WBSupplyAdd):
    try:
        return await wbs.add_supplies(request)
    except UnauthorizedError:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    except UnexpectedError:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except RPSError:
        return Response(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


