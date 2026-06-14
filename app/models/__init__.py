# app/models/__init__.py
from app.core.database import Base
from app.models.clientes import Clientes
from app.models.equipamento import Equipamento
from app.models.produtos import Produtos
from app.models.usuario import Usuario

from app.models.os import OS
from app.models.ositens import OSItens

# from app.models.solicitacao import SolicitacaoCompra

__all__ = ["Base", "Clientes", "Equipamento", "Produtos", "Usuario", "OS", "OSItens"]