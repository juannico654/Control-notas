import os

# Configuración de base de datos (MySQL)
DB_CONFIG = {
    "host":     os.environ.get("DB_HOST", "localhost"),
    "user":     os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "notas2026")
}

# Clave secreta (mejor no hardcodeada en producción)
SECRET_KEY = os.environ.get("SECRET_KEY", "40414732")

# Configuración para producción
PORT  = int(os.environ.get("PORT", 5000))   # Render usa su propio $PORT
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
