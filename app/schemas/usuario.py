from pydantic import BaseModel, Field, field_validator
import uuid

class UsuarioCreate(BaseModel):
    nome: str = Field(..., max_length=100, description="Nome do usuario")
    email: str = Field(..., max_length=100, description="E-mail do usuario")
    senha: str = Field(..., max_length=100, description="Senha do usuario")
    tipo: str = Field(..., max_length=100, description="Tipo do usuario")

    @field_validator('email')
    @classmethod
    def validar_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('E-mail inválido.')
        return v

class UsuarioResponse(BaseModel):
    id: uuid.UUID
    nome: str
    email: str
    tipo: str

    class ConfigDict:
        from_attributes = True