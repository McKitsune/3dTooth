from fastapi import FastAPI
from backend.api.pacientes import router as pacientes_router
from backend.api.archivos import router as archivos_router
from backend.api.historial import router as historial_router

app = FastAPI(title="Smile Designer API", version="1.0")

@app.get("/ping")
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}

app.include_router(pacientes_router, prefix="/pacientes")
app.include_router(archivos_router, prefix="/archivos")
app.include_router(historial_router, prefix="/historial")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
