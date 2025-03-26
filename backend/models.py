from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy import text
from database.db import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)

    archivos = relationship("Archivo", back_populates="paciente", cascade="all, delete", lazy="joined")
    historial = relationship("Historial", back_populates="paciente", cascade="all, delete", lazy="joined")

class Archivo(Base):
    __tablename__ = "archivos"
    __table_args__ = (Index("idx_paciente_id", "paciente_id"),)
    
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    nombre = Column(String(255))
    tipo = Column(String(50))  
    ruta = Column(String(255))
    fecha_subida = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    paciente = relationship("Paciente", back_populates="archivos", lazy="select")

class Historial(Base):
    __tablename__ = "historiales"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    descripcion = Column(String(500))
    fecha = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    paciente = relationship("Paciente", back_populates="historial", lazy="select")
