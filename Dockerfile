# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en /opt/criptomix-analytics
WORKDIR /opt/criptomix-analytics

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Actualizar pip
RUN pip install --upgrade pip

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación en el directorio de trabajo
COPY . .

# Configura el directorio de trabajo 
WORKDIR /opt/criptomix-analytics

RUN echo 1 | python3 analisis_trading.py