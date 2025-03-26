import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from backend.models import Paciente, Archivo, Historial

router = APIRouter()

UPLOAD_FOLDER = "storage/uploads"

@router.post("/upload")
def subir_archivo(
    paciente_id: int = Form(...),
    tipo: str = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    file_ext = os.path.splitext(archivo.filename)[1].lower()

    # Clasificación por tipo
    if tipo == "imagen":
        subfolder = "images"
    elif tipo == "modelo":
        subfolder = "models_3d"
    elif tipo == "dicom":
        subfolder = "db"
    elif tipo == "documento":
        subfolder = "documents"
    else:
        raise HTTPException(status_code=400, detail="Tipo de archivo no soportado")

    # Crear nombre y ruta
    filename = f"{uuid4().hex}{file_ext}"
    storage_path = os.path.join("storage", subfolder, filename)
    os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    with open(storage_path, "wb") as buffer:
        buffer.write(archivo.file.read())

    nuevo_archivo = Archivo(
        paciente_id=paciente_id,
        nombre=archivo.filename,
        tipo=tipo,
        ruta=storage_path
    )
    db.add(nuevo_archivo)
    db.commit()
    return {"message": "Archivo subido", "archivo_id": nuevo_archivo.id}


@router.get("/{paciente_id}")
def listar_archivos(paciente_id: int, db: Session = Depends(get_db)):
    archivos = db.query(Archivo).filter(Archivo.paciente_id == paciente_id).all()
    return {
        "archivos": [
            {
                "id": a.id,
                "nombre": a.nombre,
                "tipo": a.tipo,
                "ruta": a.ruta,
                "fecha_subida": a.fecha_subida.isoformat() if a.fecha_subida else None
            } for a in archivos
        ]
    }
