from datetime import datetime

from pydantic import BaseModel


class WBSPreordersPost(BaseModel):
    token: str
    supplier_id: str


class WBSPreorders(BaseModel):
    id: str
    boxTypeName: str
    warehouseName: str
    detailsQuantity: int
    statusId: int
    statusName: str


class WBSupplyAdd(BaseModel):
    token: str
    supplier_id: str
    preOrderId: int
    deliveryDate: datetime
