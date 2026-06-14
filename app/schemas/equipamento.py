from pydantic import BaseModel, Field
import uuid

class EquipamentoCreate(BaseModel):
    tipo: str = Field(..., max_length=50, description="Tipo do equipamento")
    marca: str = Field(..., max_length=50, description="Marca do equipamento")
    modelo: str = Field(..., max_length=50, description="Modelo do equipamento")
    numero_serie: str | None = Field(None, max_length=100, description="Número de série opcional")
    idcliente: uuid.UUID = Field(..., description="ID do cliente proprietário")

class EquipamentoResponse(BaseModel):
    idequipamento: uuid.UUID
    tipo: str
    marca: str
    modelo: str
    numero_serie: str | None
    idcliente: uuid.UUID

    class ConfigDict:
        from_attributes = True
