from fastapi import FastAPI, status

from schemas import WBSPreorders
from wb_api.api import WBSupplyAPI



server = FastAPI(
    debug=True,
    title='WBSPreorders',
    description='''Сервис поставок''',
    version='0.5.4'
)

wbs = WBSupplyAPI()

@server.get(
    '/wbs/supply', response_model=list[WBSPreorders],
    name='Получить отзывы', tags=['WBSupply'], responses={
        status.HTTP_200_OK: {
            'model': list[WBSPreorders]}})
async def get_preorders():
    x = await wbs.get_supplies()
    return await wbs.get_supplies()
