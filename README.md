# Получение незапланированных поставок и добавление поставок в план.

### Docker установка
1. `docker build -t wb_limit:0.5.4 . `
2. `docker run --name wb_limit -dp 8804:8804 wb_limit:0.5.4`


``
Для работы понадобятся WBToken и x-supplier-id
доступно получение в в модуле auth_app.
``

status as [s:___]

[s:200][POST] `/wbs/supply`

[s:200][POST] `/wbs/supply_add`

