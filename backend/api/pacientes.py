from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.db import get_db
from backend.models import Paciente, Archivo, Historial

router = APIRouter()

class PacienteCreate(BaseModel):
    nombre: str
    edad: int

@router.get("/")
def obtener_pacientes(db: Session = Depends(get_db)):
    return {"pacientes": db.query(Paciente).all()}

@router.post("/")
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    nuevo_paciente = Paciente(nombre=paciente.nombre, edad=paciente.edad)
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)
    return {"message": "Paciente creado", "id": nuevo_paciente.id}

@router.delete("/{paciente_id}")
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    db.delete(paciente)
    db.commit()
    return {"message": "Paciente eliminado"}
