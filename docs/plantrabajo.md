# Proyecto Smile Designer – Plan de Trabajo (Modo Híbrido)

##  Tecnologías y Librerías

| Área        | Lenguaje / Framework / Librerías                              |
|-------------|---------------------------------------------------------------|
| Frontend    | Python, PyQt5 o PySide6, Open3D, PyVista, OpenCV, Pillow       |
| Backend     | Python, FastAPI, Uvicorn, Pydantic, OpenCV, Open3D            |
| Base de datos | SQLite (modo offline), archivos JSON (historial por paciente) |
| Docker      | Python 3.10 base, librerías de sistema para Qt y Open3D       |
| Empaquetado | PyInstaller                                                   |

---

##  Plan de Trabajo – Desarrollo Híbrido y Simultáneo

###  FASE 1: Infraestructura Base y Setup

| Frontend (PyQt)                                 | Backend (FastAPI / offline)                                |
|-------------------------------------------------|-------------------------------------------------------------|
| - Crear estructura base en `frontend/`          | - Crear estructura en `backend/`                            |
| - Ventana principal (PyQt)                      | - Servidor básico con `/ping` y `/pacientes`               |
| - Modo híbrido: `modo_offline = True/False`     | - Lógica base para importar como módulo (sin FastAPI)       |
| - Leer configuración desde `config.py`          | - Crear `Dockerfile` con OpenCV/Open3D listo                |

Estimado: **2-3 días**

---

###  FASE 2:  Carga y Visualización de Datos

| Frontend (PyQt)                                             | Backend (FastAPI / offline)                        |
|-------------------------------------------------------------|---------------------------------------------------|
| - UI para cargar imagen y archivo STL/OBJ                  | - Recibir archivos y guardarlos (si se usa API)   |
| - Mostrar imagen en QLabel / 3D con Open3D o PyVista        | - Validar tipos y formatos (PNG, JPG, STL, OBJ)   |
| - Mostrar nombre del paciente actual                        | - Crear estructura de almacenamiento por paciente |

 Estimado: **4 días**

---

###  FASE 3:  Edición Manual de Sonrisas

| Frontend (PyQt)                                             | Backend (procesamiento puro o API opcional)       |
|-------------------------------------------------------------|---------------------------------------------------|
| - Herramienta para selección de dientes (marcado manual)   | - Función para aislar zonas de imagen             |
| - Interfaz de pincel/máscara (OpenCV + PyQt)                | - Procesamiento con OpenCV: cropping, resaltado   |
| - Botón “Aplicar edición” → guardar nuevo modelo            | - Guardar/crear versión modificada del modelo     |

 Estimado: **5 días**

---

###  FASE 4:  Gestión de Pacientes y Archivos

| Frontend (PyQt)                                     | Backend (API u offline)                           |
|-----------------------------------------------------|---------------------------------------------------|
| - Lista desplegable de pacientes                    | - Crear estructura tipo: `/storage/pacientes/{id}` |
| - Botón para crear nuevo paciente                   | - Guardar nombre, ID, historial en JSON/SQLite    |
| - Asociar imágenes y modelos a cada uno             | - API: GET/POST `/pacientes`, `/historial`        |

 Estimado: **4 días**

---

###  FASE 5:  Modo Híbrido / Conexión API

| Frontend (PyQt)                                             | Backend (FastAPI + lógica compartida)             |
|-------------------------------------------------------------|---------------------------------------------------|
| - Todas las acciones deben funcionar en modo offline o API  | - Exponer funciones como endpoint REST            |
| - Función `get_data()` que detecta el modo y actúa          | - Documentar endpoints con Swagger (opcional)     |

 Estimado: **3 días**

---

###  FASE 6:  Empaquetado como App .EXE

| Frontend (PyQt + recursos)                      | Backend (opcional empaquetado o ejecución aparte) |
|-------------------------------------------------|---------------------------------------------------|
| - Generar `.spec` para PyInstaller              | - Incluir lógica embebida o lanzar proceso aparte |
| - Incluir imágenes, modelos y configuraciones   | - Documentar ejecución en modo producción         |

 Estimado: **2 días**

---

###  FASE 7 (opcional):  Modo Servidor (multiusuario / red local / nube)

| Frontend                                          | Backend                                           |
|--------------------------------------------------|--------------------------------------------------|
| - Conectarse a un backend en red/local           | - Montar servidor accesible desde LAN o nube     |
| - Soporte para login, múltiples clínicas          | - Usuarios, sesiones, autenticación básica       |

 Estimado: **1 semana**

---

##  Notas Finales

- Docker se usará para ejecutar componentes con dependencias complicadas (OpenCV, Open3D).

