from pydantic import BaseModel


class WBSPreorders(BaseModel):
    id: str
    boxTypeName: str
    warehouseName: str
    detailsQuantity: int
    statusId: int
    statusName: str
