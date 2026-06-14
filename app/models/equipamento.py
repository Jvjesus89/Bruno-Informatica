from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import uuid

class Equipamento(Base):
    __tablename__ = "equipamentos"

    idequipamento: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False) 
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    numero_serie: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    idcliente: Mapped[uuid.UUID] = mapped_column(ForeignKey("clientes.idcliente", ondelete="RESTRICT"), nullable=False)
    cliente: Mapped["Clientes"] = relationship(back_populates="equipamentos")