from pydantic import BaseModel, Field, field_validator
import uuid

class ClienteCreate(BaseModel):
    nome: str = Field(..., max_length=100, description="Nome do cliente")
    cpf_cnpj: str = Field(..., max_length=14, description="CPF ou CNPJ do cliente")
    email: str = Field(..., max_length=100, description="E-mail do cliente")
    telefone: str = Field(..., max_length=15, description="Telefone do cliente")

    @field_validator('email')
    @classmethod
    def validar_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('E-mail inválido.')
        return v

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: str) -> str:
        raw_digits = ''.join(filter(str.isdigit, v))
        if len(raw_digits) not in (10, 11):
            raise ValueError('Telefone deve ter 10 ou 11 dígitos.')
        return v

    @field_validator('cpf_cnpj')
    @classmethod
    def validar_cpf_cnpj(cls, v: str) -> str:
        raw_digits = ''.join(filter(str.isdigit, v))
        if len(raw_digits) not in (11, 14):
            raise ValueError('CPF ou CNPJ deve conter 11 ou 14 dígitos.')
        return v

class ClientesResponse(BaseModel):
    idcliente: uuid.UUID
    nome: str
    cpf_cnpj: str
    email: str
    telefone: str

    class ConfigDict:
        from_attributes = True