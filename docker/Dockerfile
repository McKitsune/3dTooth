FROM python:3.11-slim

# Instar dependencias de sistema para OpenCV, open3D y PyQt
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    qtbase5-dev \
    libglib2.0-0 \
    build-essential \
    git && \
    rm -rf /var/lib/apt/lists/*

# Copiar codigo dependencias y código
COPY requeriments.txt /app/requeriments.txt
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requeriments.txt

# Comandos por defecto
CMD ["python", "backend/main.py"]