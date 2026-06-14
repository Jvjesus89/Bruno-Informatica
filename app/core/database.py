# app/core/database.py
from typing import Generator
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
import os

# Pega a URL do banco do ambiente (.env)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tio_bruno_db")

# Cria a Engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Nova forma de criar a classe Base no SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# Função de Injeção de Dependência (será usada nos Routers do FastAPI)
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()