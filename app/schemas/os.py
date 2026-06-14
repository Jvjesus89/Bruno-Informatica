from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from decimal import Decimal
import uuid

class OSCreate(BaseModel):
    idcliente: uuid.UUID
    idequipamento: uuid.UUID
    idtecnico: uuid.UUID
    status: str = Field("ABERTA", max_length=50, description="Status da OS")
    descricao_defeito: str = Field(..., max_length=100, description="Descrição do defeito")
    valor_total: Decimal = Field(Decimal("0.00"), max_digits=10, decimal_places=2, description="Valor total da OS")

    @field_validator('status')
    @classmethod
    def validar_status(cls, v: str) -> str:
        v_upper = v.upper()
        permitidos = ["ABERTA", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"]
        if v_upper not in permitidos:
            raise ValueError(f"Status inválido. Escolha entre: {', '.join(permitidos)}")
        return v_upper

class OSResponse(BaseModel):
    idos: uuid.UUID
    idcliente: uuid.UUID
    idequipamento: uuid.UUID
    idtecnico: uuid.UUID
    status: str
    descricao_defeito: str | None
    valor_total: Decimal
    data_abertura: datetime
    data_conclusao: datetime | None

    class ConfigDict:
        from_attributes = True