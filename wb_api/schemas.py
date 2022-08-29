from datetime import datetime

from pydantic import BaseModel
from typing import Optional

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
    monopalletCount: Optional[int]


class DataError(BaseModel):
    trKey: str
    msg: str
    cause: str


class ErrorForSupply(BaseModel):
    code: int
    message: str
    data: DataError


class IdForSupply(BaseModel):
    supplyId: int
    boxTypeId: int
    preorders: list


class SupplyBase(BaseModel):
    id: str
    jsonrpc: str


class SupplyError(SupplyBase):
    error: ErrorForSupply


class SupplyId(SupplyBase):
    result: IdForSupply
