from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.db import get_db
from backend.models import Paciente, Archivo, Historial
from datetime import datetime

router = APIRouter()

class HistorialCreate(BaseModel):
    descripcion: str

@router.get("/{paciente_id}")
def obtener_historial(paciente_id: int, db: Session = Depends(get_db)):
    historial = db.query(Historial).filter(Historial.paciente_id == paciente_id).all()
    return {"historial": historial}

@router.post("/{paciente_id}")
def agregar_historial(paciente_id: int, entrada: HistorialCreate, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    nuevo = Historial(
        paciente_id=paciente_id,
        descripcion=entrada.descripcion,
        fecha=datetime.utcnow()
    )
    db.add(nuevo)
    db.commit()
    return {"message": "Historial agregado", "id": nuevo.id}
