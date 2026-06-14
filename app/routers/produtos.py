from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.produtos import Produtos
from app.schemas.produtos import ProdutoCreate, ProdutoResponse

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    # Valida duplicidade de nome
    query_nome = select(Produtos).where(Produtos.nome == produto.nome)
    if db.scalars(query_nome).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto com este nome já cadastrado."
        )

    novo_produto = Produtos(
        nome=produto.nome,
        descricao=produto.descricao,
        preco_venda=produto.preco_venda,
        quantidade_estoque=produto.quantidade_estoque
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    # Filtros opcionais via Query Params
    nome: str | None = Query(None, description="Filtrar produtos por parte do nome"),
    preco_maximo: float | None = Query(None, description="Filtrar produtos com preço até este valor"),
    
    skip: int = Query(0, ge=0, description="Número de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de registros a retornar (limit)"),
    db: Session = Depends(get_db)
):
    query = select(Produtos)
    if nome:
        query = query.where(Produtos.nome.ilike(f"%{nome}%"))
    if preco_maximo:
        query = query.where(Produtos.preco_venda <= preco_maximo)
    query = query.offset(skip).limit(limit)
    resultado = db.scalars(query).all()
    return resultado