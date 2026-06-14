from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.equipamento import Equipamento
from app.schemas.equipamento import EquipamentoCreate, EquipamentoResponse

router = APIRouter(prefix="/equipamentos", tags=["Equipamentos"])

@router.post("/", response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_equipamento(equipamento: EquipamentoCreate, db: Session = Depends(get_db)):
    if equipamento.numero_serie:
        query_serie = select(Equipamento).where(Equipamento.numero_serie == equipamento.numero_serie)
        if db.scalars(query_serie).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Equipamento com este número de série já cadastrado."
            )

    novo_equipamento = Equipamento(
        tipo=equipamento.tipo,
        marca=equipamento.marca,
        modelo=equipamento.modelo,
        numero_serie=equipamento.numero_serie,
        idcliente=equipamento.idcliente
    )
    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)
    return novo_equipamento

@router.get("/", response_model=List[EquipamentoResponse])
def listar_equipamentos(
    skip: int = Query(0, ge=0, description="Número de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de registros a retornar (limit)"),
    db: Session = Depends(get_db)
):
    query = select(Equipamento).offset(skip).limit(limit)
    resultado = db.scalars(query).all()
    return resultado
