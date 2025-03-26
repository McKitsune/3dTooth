import requests

API_URL = "http://localhost:8000"

# --- Pacientes ---

def obtener_pacientes():
    """Llama al backend para obtener la lista de pacientes."""
    try:
        response = requests.get(f"{API_URL}/pacientes")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Error al obtener pacientes:", e)
        return {"pacientes": []}

def crear_paciente(nombre, edad):
    """Llama al backend para crear un nuevo paciente."""
    try:
        response = requests.post(f"{API_URL}/pacientes", json={"nombre": nombre, "edad": edad})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Error al agregar paciente:", e)
        return {}

# --- Archivos ---

def obtener_archivos(paciente_id):
    try:
        response = requests.get(f"{API_URL}/archivos/{paciente_id}")
        response.raise_for_status()
        return response.json().get("archivos", [])
    except requests.exceptions.RequestException as e:
        print("Error al obtener archivos:", e)
        return []

def subir_archivo(paciente_id, tipo, filepath):
    """Sube un archivo al backend para un paciente específico."""
    try:
        with open(filepath, "rb") as file:
            files = {"archivo": file}
            data = {"paciente_id": paciente_id, "tipo": tipo}
            response = requests.post(f"{API_URL}/archivos/upload", files=files, data=data)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print("❌ Error al subir archivo:", e)
        raise

# --- Historial ---

def obtener_historial(paciente_id):
    """Obtiene el historial del paciente."""
    try:
        response = requests.get(f"{API_URL}/historial/{paciente_id}")
        response.raise_for_status()
        return response.json().get("historial", [])
    except requests.exceptions.RequestException as e:
        print("❌ Error al obtener historial:", e)
        return []

def agregar_historial(paciente_id, descripcion):
    """Agrega una entrada al historial del paciente."""
    try:
        response = requests.post(
            f"{API_URL}/historial/{paciente_id}",
            json={"descripcion": descripcion}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Error al agregar historial:", e)
        raise

# --- Modelos 3D ---

def combinar_modelos(ids):
    """Solicita al backend combinar modelos 3D por sus IDs."""
    try:
        response = requests.post(f"{API_URL}/archivos/combine_stl", json={"ids": ids})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Error al combinar modelos:", e)
        raise
