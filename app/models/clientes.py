from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import uuid
from typing import List

class Clientes(Base):
    __tablename__ = "clientes"

    idcliente: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf_cnpj: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(15), nullable=False)
    data_cadastro: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    equipamentos: Mapped[List["Equipamento"]] = relationship(back_populates="cliente", cascade="all, delete-orphan")

    ordens_servico: Mapped[List["OS"]] = relationship(back_populates="cliente", cascade="all, delete-orphan")