from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class PurchaseModel(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    date: date
    text: str
    price: float
