# app/routers/cliente.py
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.clientes import Clientes  # Modelo SQLAlchemy
from app.schemas.cliente import ClienteCreate, ClientesResponse  # Schemas Pydantic

# A variável PRECISA se chamar "router" exatamente assim para o main.py encontrá-la
router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClientesResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    query_cpf = select(Clientes).where(Clientes.cpf_cnpj == cliente.cpf_cnpj)
    if db.scalars(query_cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF/CNPJ já cadastrado."
        )
    query_email = select(Clientes).where(Clientes.email == cliente.email)
    if db.scalars(query_email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )

    novo_cliente = Clientes(
        nome=cliente.nome,
        cpf_cnpj=cliente.cpf_cnpj,
        email=cliente.email,
        telefone=cliente.telefone
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

@router.get("/", response_model=List[ClientesResponse])
def listar_clientes(
    nome: str | None = Query(None, description="Filtrar clientes por parte do nome"),
    skip: int = Query(0, ge=0, description="Número de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de registros a retornar (limit)"),
    
    db: Session = Depends(get_db)
):
    query = select(Clientes)
    
    if nome:
        query = query.where(Clientes.nome.ilike(f"%{nome}%"))
    
    query = query.offset(skip).limit(limit)
    resultado = db.scalars(query).all()
    
    return resultado