from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
import uuid

class ProdutoCreate(BaseModel):
    nome: str = Field(..., max_length=100, description="Nome do produto")
    descricao: str | None = Field(None, max_length=100, description="Descrição opcional do produto")
    preco_venda: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Preço de venda deve ser maior que zero")
    quantidade_estoque: int = Field(..., description="Quantidade inicial em estoque")

    @field_validator('quantidade_estoque')
    @classmethod
    def validar_estoque_nao_negativo(cls, v: int) -> int:
        if v < 0:
            raise ValueError('A quantidade inicial de estoque não pode ser negativa.')
        return v

class ProdutoResponse(BaseModel):
    idproduto: uuid.UUID
    nome: str
    descricao: str | None
    preco_venda: Decimal
    quantidade_estoque: int

    class ConfigDict:
        from_attributes = True