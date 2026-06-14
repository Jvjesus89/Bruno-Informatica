from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import uuid

class Estoque(Base):
    __tablename__ = "estoque"

    idproduto: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(100), nullable=True)
    preco_venda: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    quantidade_estoque: Mapped[int] = mapped_column(Integer, nullable=False)

    