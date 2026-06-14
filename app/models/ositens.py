from sqlalchemy import ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import uuid

class OSItens(Base):
    __tablename__ = "os_itens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    
    idos: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("OS.idos", ondelete="CASCADE"), 
        nullable=False
    )
    idproduto: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("produtos.idproduto", ondelete="RESTRICT"), 
        nullable=False
    )
    
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    preco_unitario_aplicado: Mapped[float] = mapped_column(
        Numeric(10, 2), 
        nullable=False
    )
    ordem_servico: Mapped["OS"] = relationship(
        back_populates="itens"
    )
    produto: Mapped["Produtos"] = relationship()