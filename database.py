import mysql.connector
import pandas as pd


def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="notas2026"
    )
    return conexion


def obtenerusuarios(username):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username=%s", (username,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario


def obtenerestudiantes():
    conn = conectar()
    query = "SELECT id, Nombre, Edad, Carrera, nota1, nota2, nota3, Promedio, Desempeño FROM estudiantes"
    df = pd.read_sql(query, conn)
    conn.close()

    df['Edad']     = pd.to_numeric(df['Edad'],     errors='coerce')
    df['Promedio'] = pd.to_numeric(df['Promedio'], errors='coerce')
    df['nota1']    = pd.to_numeric(df['nota1'],    errors='coerce')
    df['nota2']    = pd.to_numeric(df['nota2'],    errors='coerce')
    df['nota3']    = pd.to_numeric(df['nota3'],    errors='coerce')

    df['Nombre']    = df['Nombre'].str.strip()
    df['Carrera']   = df['Carrera'].str.strip()
    df['Desempeño'] = df['Desempeño'].str.strip()

    print("=== DB: datos cargados ===")
    print(f"Filas: {len(df)}")
    print(df[['Nombre', 'Edad', 'Carrera', 'Promedio', 'Desempeño']].head(3).to_string(index=False))
    print(f"Tipos:\n{df.dtypes}")
    print("==========================")

    return df


def estudianteexiste(nombre, carrera):
    """Devuelve True si ya existe un estudiante con ese nombre Y carrera."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM estudiantes WHERE Nombre=%s AND Carrera=%s",
        (nombre.strip(), carrera.strip())
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def insertarestudiante(nombre, edad, carrera, nota1, nota2, nota3):
    """Inserta estudiante nuevo. Calcula promedio y desempeño automáticamente."""
    promedio = round((float(nota1) + float(nota2) + float(nota3)) / 3, 2)

    if promedio >= 4.5:
        desempeno = "Excelente"
    elif promedio >= 3.5:
        desempeno = "Bueno"
    elif promedio >= 2.5:
        desempeno = "Regular"
    else:
        desempeno = "Deficiente"

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO estudiantes
           (Nombre, Edad, Carrera, nota1, nota2, nota3, Promedio, Desempeño)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (nombre.strip(), int(edad), carrera.strip(),
         float(nota1), float(nota2), float(nota3),
         promedio, desempeno)
    )
    conn.commit()
    conn.close()


def carguemasivo(df_excel):
    """
    Recibe un DataFrame leído del Excel y carga los estudiantes válidos.
    Retorna un dict con: insertados, duplicados, errores, detalle y rechazados (DataFrame).
    Columnas esperadas: Nombre, Edad, Carrera, nota1, nota2, nota3
    """
    import pandas as pd

    insertados      = 0
    duplicados      = 0
    errores         = 0
    detalle_errores = []
    rechazados      = []   # lista de filas rechazadas con motivo

    columnas_requeridas = {'Nombre', 'Edad', 'Carrera', 'nota1', 'nota2', 'nota3'}
    if not columnas_requeridas.issubset(set(df_excel.columns)):
        faltantes = columnas_requeridas - set(df_excel.columns)
        return {
            'insertados': 0, 'duplicados': 0, 'errores': len(df_excel),
            'detalle_errores': [f"El archivo no tiene las columnas: {', '.join(faltantes)}"],
            'rechazados': pd.DataFrame()
        }

    for i, fila in df_excel.iterrows():
        num_fila = i + 2
        motivo   = None

        try:
            nombre  = str(fila['Nombre']).strip()  if pd.notna(fila['Nombre'])  else ''
            carrera = str(fila['Carrera']).strip()  if pd.notna(fila['Carrera']) else ''
            edad_raw = fila['Edad']
            nota1_raw = fila['nota1']
            nota2_raw = fila['nota2']
            nota3_raw = fila['nota3']

            # Datos faltantes
            if not nombre or not carrera:
                motivo = "Datos faltantes: Nombre o Carrera vacíos"
            elif pd.isna(edad_raw) or pd.isna(nota1_raw) or pd.isna(nota2_raw) or pd.isna(nota3_raw):
                motivo = "Datos faltantes: Edad o notas vacías"
            else:
                edad  = int(edad_raw)
                nota1 = float(nota1_raw)
                nota2 = float(nota2_raw)
                nota3 = float(nota3_raw)

                # Edad negativa
                if edad < 0:
                    motivo = f"Edad inválida: {edad} (debe ser positiva)"
                # Notas fuera de rango
                elif not (0 <= nota1 <= 5):
                    motivo = f"nota1 fuera de rango (0-5): {nota1}"
                elif not (0 <= nota2 <= 5):
                    motivo = f"nota2 fuera de rango (0-5): {nota2}"
                elif not (0 <= nota3 <= 5):
                    motivo = f"nota3 fuera de rango (0-5): {nota3}"
                # Duplicado
                elif estudianteexiste(nombre, carrera):
                    motivo = f"Duplicado: '{nombre}' ya está registrado en {carrera}"

            if motivo:
                # Agregar a rechazados
                rechazados.append({
                    'Fila_Excel': num_fila,
                    'Nombre':     fila.get('Nombre',  ''),
                    'Edad':       fila.get('Edad',    ''),
                    'Carrera':    fila.get('Carrera', ''),
                    'nota1':      fila.get('nota1',   ''),
                    'nota2':      fila.get('nota2',   ''),
                    'nota3':      fila.get('nota3',   ''),
                    'Motivo_Rechazo': motivo
                })
                if 'Duplicado' in motivo:
                    duplicados += 1
                else:
                    errores += 1
                detalle_errores.append(f"Fila {num_fila}: {motivo}")
            else:
                insertarestudiante(nombre, edad, carrera, nota1, nota2, nota3)
                insertados += 1

        except Exception as e:
            errores += 1
            msg = f"Fila {num_fila}: Error inesperado — {str(e)}"
            detalle_errores.append(msg)
            rechazados.append({
                'Fila_Excel': num_fila,
                'Nombre':     fila.get('Nombre',  ''),
                'Edad':       fila.get('Edad',    ''),
                'Carrera':    fila.get('Carrera', ''),
                'nota1':      fila.get('nota1',   ''),
                'nota2':      fila.get('nota2',   ''),
                'nota3':      fila.get('nota3',   ''),
                'Motivo_Rechazo': str(e)
            })

    df_rechazados = pd.DataFrame(rechazados) if rechazados else pd.DataFrame(
        columns=['Fila_Excel','Nombre','Edad','Carrera','nota1','nota2','nota3','Motivo_Rechazo']
    )

    return {
        'insertados':      insertados,
        'duplicados':      duplicados,
        'errores':         errores,
        'detalle_errores': detalle_errores,
        'rechazados':      df_rechazados
    }


if __name__ == "__main__":
    conn = conectar()
    print("Conexión exitosa")
    conn.close()
    df = obtenerestudiantes()