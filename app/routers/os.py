from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
import uuid

from app.core.database import get_db
from app.models.os import OS
from app.models import Clientes, Equipamento, Usuario
from app.schemas.os import OSCreate, OSResponse

router = APIRouter(prefix="/os", tags=["OS"])

STATUS_PERMITIDOS = ["ABERTA", "EM_ANDAMENTO", "CONCLUIDA", "CANCELADA"]

MAPA_TRANSIÇÕES = {
    "ABERTA": ["EM_ANDAMENTO", "CANCELADA"],
    "EM_ANDAMENTO": ["CONCLUIDA", "CANCELADA"],
    "CONCLUIDA": [], 
    "CANCELADA": []   
}

@router.post("/", response_model=OSResponse, status_code=status.HTTP_201_CREATED)
def criar_os(os_input: OSCreate, db: Session = Depends(get_db)):
    # 1. Valida se o cliente existe
    query_cliente = select(Clientes).where(Clientes.idcliente == os_input.idcliente)
    if not db.scalars(query_cliente).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente não encontrado."
        )

    # 2. Valida se o equipamento existe
    query_equip = select(Equipamento).where(Equipamento.idequipamento == os_input.idequipamento)
    if not db.scalars(query_equip).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Equipamento não encontrado."
        )

    # 3. Valida se o técnico existe
    query_tec = select(Usuario).where(Usuario.id == os_input.idtecnico)
    if not db.scalars(query_tec).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Técnico não encontrado."
        )

    nova_os = OS(
        idcliente=os_input.idcliente,
        idequipamento=os_input.idequipamento,
        idtecnico=os_input.idtecnico,
        status=os_input.status,
        descricao_defeito=os_input.descricao_defeito,
        valor_total=os_input.valor_total
    )
    db.add(nova_os)
    db.commit()
    db.refresh(nova_os)
    return nova_os

@router.get("/{id_os}", response_model=OSResponse)
def buscar_os(id_os: uuid.UUID, db: Session = Depends(get_db)):
    query = select(OS).where(OS.idos == id_os)
    os_registro = db.scalars(query).first()
    if not os_registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de Serviço não encontrada."
        )
    return os_registro

@router.put("/{id_os}/status", status_code=status.HTTP_200_OK)
def atualizar_status_os(
    id_os: uuid.UUID,
    novo_status: str,
    db: Session = Depends(get_db)
):
    # 1. Valida se o status enviado existe no sistema
    novo_status = novo_status.upper()
    if novo_status not in STATUS_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Escolha entre: {', '.join(STATUS_PERMITIDOS)}"
        )

    # 2. Busca a Ordem de Serviço no banco
    query = select(OS).where(OS.idos == id_os)
    os_registro = db.scalars(query).first()

    if not os_registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de Serviço não encontrada."
        )

    status_atual = os_registro.status.upper()

    # 3. Se o status já for o mesmo, não faz nada
    if status_atual == novo_status:
        return {"message": "A OS já está com este status.", "status": status_atual}

    # 4. Valida a Regra de Transição (Máquina de Estados)
    transicoes_possiveis = MAPA_TRANSIÇÕES.get(status_atual, [])
    if novo_status not in transicoes_possiveis:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Transição de estado inválida. Uma OS '{status_atual}' não pode ser alterada para '{novo_status}'."
        )

    # 5. Se passou pelas regras, atualiza o banco de dados
    os_registro.status = novo_status
    db.commit()
    db.refresh(os_registro)

    return {
        "message": "Status atualizado com sucesso!",
        "id_os": os_registro.idos,
        "status_anterior": status_atual,
        "status_atual": os_registro.status
    }
    
@router.get("/", response_model=List[OSResponse])
def listar_OS(
    # Filtros opcionais via Query Params
    skip: int = Query(0, ge=0, description="Número de registros a pular (offset)"),
    limit: int = Query(10, ge=1, le=100, description="Quantidade máxima de registros a retornar (limit)"),
    db: Session = Depends(get_db)
):
    query = select(OS)
    if skip > 0:
        query = query.offset(skip)
    if limit > 0:
        query = query.limit(limit)
    resultado = db.scalars(query).all()
    return resultado