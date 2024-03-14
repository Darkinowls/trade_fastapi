from datetime import datetime

from pydantic import BaseModel, Field


class OperationCreateRequest(BaseModel):
    quantity: int = Field(title="Quantity of operations")
    figi: str = Field(title="FIGI of operations")
    instrument_type: str = Field(title="Type of instrument")
    type: str = Field(title="Type of operation")
