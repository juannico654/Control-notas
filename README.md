# Control de Notas 2026

Sistema de gestión académica con Flask + Dash + MySQL.

---

## Estructura del proyecto

```
controlnotas/
├── app.py               ← Punto de entrada Flask
├── config.py            ← Configuración (BD, secret key, puerto)
├── database.py          ← Conexión MySQL y consultas
├── dashprincipal.py     ← Dashboard Dash con gráficas
├── requirements.txt     ← Dependencias Python
├── notas2026.sql        ← Script para crear e importar la BD
└── templates/
    ├── login.html       ← Página de inicio de sesión
    └── dashprinci.html  ← Redirección (compatibilidad)
```

---

## Instalación paso a paso

### 1. Requisitos previos
- Python 3.9 o superior
- MySQL / MariaDB corriendo en localhost
- pip actualizado: `python -m pip install --upgrade pip`

### 2. Clonar / copiar el proyecto
Coloca todos los archivos en una carpeta, por ejemplo `controlnotas/`.

### 3. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

Si necesitas instalar manualmente:
```bash
pip install flask dash plotly pandas mysql-connector-python statsmodels
```

### 5. Importar la base de datos
Abre tu cliente MySQL (phpMyAdmin, MySQL Workbench o terminal) y ejecuta:
```sql
SOURCE ruta/a/notas2026.sql;
```
O desde la terminal:
```bash
mysql -u root -p < notas2026.sql
```

### 6. Verificar la conexión
```bash
python database.py
```
Debes ver: `Conexión exitosa` y los primeros registros de la tabla.

### 7. Ejecutar la aplicación
```bash
python app.py
```
Abre en el navegador: http://localhost:5000

---

## Credenciales de prueba

| Usuario   | Contraseña | Rol           |
|-----------|------------|---------------|
| admin     | aaa        | administrador |
| docente1  | abcd       | docente       |
| docente2  | abcd       | docente       |

---

## Solución de problemas comunes

**Error: ModuleNotFoundError**
→ Asegúrate de tener el entorno virtual activado y haber corrido `pip install -r requirements.txt`

**Error de conexión a MySQL**
→ Verifica que MySQL esté corriendo y que en `config.py` el usuario/contraseña sean correctos

**Gráficas vacías**
→ Corre `python database.py` y verifica que imprima filas con datos. Si el Promedio aparece como `object` en los tipos, significa que MySQL devuelve el decimal como string — el código ya lo corrige automáticamente.

**trendline='ols' falla**
→ Instala statsmodels: `pip install statsmodels`
