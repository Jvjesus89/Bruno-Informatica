from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Valida duplicidade de email
    query_email = select(Usuario).where(Usuario.email == usuario.email)
    if db.scalars(query_email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado."
        )

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha,
        tipo=usuario.tipo
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    # Filtros opcionais via Query Params
    nome: str | None = Query(None, description="Filtrar usuarios por parte do nome"),
    tipo: str | None = Query(None, description="Filtrar usuarios por tipo"),
    
    skip: int = Query(0, ge=0, description="Número de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de registros a retornar (limit)"),
    db: Session = Depends(get_db)
):
    query = select(Usuario)
    if nome:
        query = query.where(Usuario.nome.ilike(f"%{nome}%"))
    if tipo:
        query = query.where(Usuario.tipo == tipo)
    query = query.offset(skip).limit(limit)
    resultado = db.scalars(query).all()
    return resultado