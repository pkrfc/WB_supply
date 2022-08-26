from fastapi import FastAPI, status

from wb_api.api import WBSupplyAPI
from wb_api.schemas import WBSPreorders, WBSPreordersPost, WBSupplyAdd

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
    return await wbs.get_supplies(token, supplier_id)


@server.post(
    '/wbs/supply_add',
    name='Запланировать поставку',
    tags=['WBSupply_add'])
async def add_preorders(request: WBSupplyAdd):
    supply = request.preOrderId
    date = request.deliveryDate
    token = request.token
    supplier_id = request.supplier_id
    return await wbs.add_supplies(supply, date, token, supplier_id)
