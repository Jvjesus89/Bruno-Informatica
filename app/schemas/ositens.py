from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
import uuid

class OSItensCreate(BaseModel):
    idos: uuid.UUID
    idproduto: uuid.UUID
    quantidade: int = Field(1, ge=1, description="Quantidade de itens")
    preco_unitario_aplicado: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Preço unitário aplicado")

    @field_validator('quantidade')
    @classmethod
    def validar_quantidade(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('A quantidade deve ser maior que zero.')
        return v

class OSItensResponse(BaseModel):
    id: uuid.UUID
    idos: uuid.UUID
    idproduto: uuid.UUID
    quantidade: int
    preco_unitario_aplicado: Decimal

    class ConfigDict:
        from_attributes = True