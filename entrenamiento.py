import mysql.connector
from datetime import datetime

# --- Parte 1: Configuración y Datos Maestros ---

# Datos de conexión a MySQL
config = {
    'user': 'pablo',         # <- reemplazá con tu usuario de MySQL
    'password': 'usuario',   # <- reemplazá con tu contraseña
    'host': 'localhost',
    'database': 'Sportclub',
    'raise_on_warnings': True
}

# Diccionario de Ejercicios Maestros
# Basado en tu output de 'select id_ejercicio, grupo_muscular, nombre_ejercicio from ejercicios;'
# ASEGÚRATE de que este diccionario esté completo y sea preciso con tus 52 ejercicios.
# He corregido 'Sentadillas frontales con Manc' a 'Squats frontales' según tu tabla 'ejercicios'.
all_exercises = {
    1: ('Espalda', 'Jalones estrechos al pecho'),
    2: ('Espalda', 'Remo uni con mancuerna'),
    3: ('Espalda', 'Jalones al pecho'),
    4: ('Espalda', 'Remo en polea baja'),
    5: ('Espalda', 'Remo soga Pullover'),
    6: ('Biceps', 'Curl de concentración en banco'),
    7: ('Biceps', 'Curl en polea'),
    8: ('Biceps', 'Curl concentrado bayesian'),
    9: ('Biceps', 'Curl con mancuernas'),
    10: ('Biceps', 'Curl concentrado banco inclinado'),
    11: ('Cuádriceps', 'Squats frontales'),
    12: ('Cuádriceps', 'Estocadas'),
    13: ('Cuádriceps', 'Prensa'),
    14: ('Cuádriceps', 'Extension de Cuadriceps en sillon'),
    15: ('Cuádriceps', 'Bulgaras'),
    16: ('Cuádriceps', 'Sentadilla Goblet'),
    17: ('Pecho', 'Press de banca plano'),
    18: ('Pecho', 'Press de banca inclinado Mancuerna'),
    19: ('Pecho', 'Aperturas con mancuernas'),
    20: ('Pecho', 'Cruces en polea'),
    21: ('Pecho', 'Extension de pecho en maquina'),
    22: ('Pecho', 'Prensa de pecho en maquina'),
    23: ('Triceps', 'Press francés'),
    24: ('Triceps', 'Extensiones de tríceps en polea media altura'),
    25: ('Triceps', 'Patadas de tríceps'),
    26: ('Triceps', 'Extension Tricep Unilateral'),
    27: ('Triceps', 'Extension de Tricep sobre la cabeza'),
    28: ('Triceps', 'Extension Tricep con barra'),
    29: ('Triceps', 'Flexiones de Tricep'),
    30: ('Triceps', 'Extensiones de tríceps con cuerda'),
    31: ('Hombros', 'Press de banca inclinado Barra'),
    32: ('Hombros', 'Elevación Lateral con Mancuernas'),
    33: ('Hombros', 'Elevación Lateral con Cable'),
    34: ('Hombros', 'Elevación Frontal con Cuerda en Polea'),
    35: ('Hombros', 'Press Militar con Mancuernas'),
    36: ('Hombros', 'Jalón a la Cara con Cuerda'),
    37: ('Hombros', 'Press de Hombros en Máquina'),
    38: ('Hombros', 'Apertura Posterior en Máquina'),
    39: ('Hombros', 'Apertura Posterior con Mancuernas'),
    40: ('Pierna', 'Peso muerto rumano'),
    41: ('Pierna', 'Elevación de talones'),
    42: ('Pierna', 'Curl de femorales'),
    43: ('Pierna', 'Abductores en máquina'),
    44: ('Pierna', 'Aductores en máquina'),
    45: ('Biceps', 'Curl de Bíceps Martillo'),
    46: ('Cuádriceps', 'Zancadas inversas'),
    47: ('Biceps', 'Curl predicador con barra Z'),
    48: ('Biceps', 'Curl araña con mancuernas'),
    49: ('Espalda', 'Remo Sentado en Máquina'),
    50: ('Espalda', 'Extensiones lumbares'),
    51: ('Espalda', 'Remo con barra'),
    52: ('Hombros', 'Press Arnold')
}

# --- Parte 2: Datos de la Rutina Semanal ---

# Fecha de la rutina (puedes mantenerla manual o generarla dinámicamente)
fecha_rutina = '2025-05-22' # Hoy es 21 de Mayo de 2025

# Definición de la rutina por ID de ejercicio, series, repeticiones y peso.
# Los campos grupo_muscular y nombre_ejercicio se buscarán automáticamente.
# Formato: (id_ejercicio, series, repeticiones, peso)

rutina_semanal_ids = [
     
    (32, 4, 8, 10),
    (33, 4, 10, 17),
    (34, 3, 10, 23),
    (35, 4, 10, 22.5),
    (36, 3, 10, 47),
    (37, 4, 8, 59),
    (39, 3, 10, 10),
    (40, 4, 10, 20),
    (41, 3, 10, 53),
    (42, 4, 10, 41)
    
]
# --- Parte 3: Lógica de Conexión y Inserción con Validación ---

conn = None
cursor = None
inserted_count = 0
skipped_count = 0

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    sql_check = "SELECT COUNT(*) FROM rutinas WHERE id_ejercicio = %s AND fecha = %s"
    sql_insert = """
        INSERT INTO rutinas (
            id_ejercicio, grupo_muscular, nombre_ejercicio,
            fecha, series, repeticiones, peso
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    print(f"Iniciando inserción de rutina para la fecha: {fecha_rutina}")
    print("-" * 50)

    for ejercicio_id, series, repeticiones, peso in rutina_semanal_ids:
        if ejercicio_id not in all_exercises:
            print(f"⚠️ Advertencia: ID de ejercicio {ejercicio_id} no encontrado en la lista maestra. Se omite.")
            skipped_count += 1
            continue # Pasa al siguiente ejercicio en la lista

        grupo_muscular, nombre_ejercicio = all_exercises[ejercicio_id]
        
        # Prepara los datos completos del ejercicio para la validación/inserción
        ejercicio_data_full = (ejercicio_id, grupo_muscular, nombre_ejercicio, fecha_rutina, series, repeticiones, peso)

        # 1. Validar duplicado
        cursor.execute(sql_check, (ejercicio_data_full[0], ejercicio_data_full[3]))
        if cursor.fetchone()[0] > 0:
            print(f"🟡 Ya existe el ejercicio '{ejercicio_data_full[2]}' (ID: {ejercicio_data_full[0]}) para la fecha {ejercicio_data_full[3]}. Se omite.")
            skipped_count += 1
        else:
            # 2. Insertar si no es duplicado
            try:
                cursor.execute(sql_insert, ejercicio_data_full)
                print(f"✅ Insertado: '{ejercicio_data_full[2]}' (ID: {ejercicio_data_full[0]}) para la fecha {ejercicio_data_full[3]}.")
                inserted_count += 1
            except mysql.connector.Error as insert_err:
                # Manejar errores específicos de inserción si es necesario, aunque el duplicado ya se validó
                print(f"❌ Error al insertar '{ejercicio_data_full[2]}': {insert_err}")
                skipped_count += 1
                conn.rollback() # Opcional: rollback del último execute si falla individualmente

    # Confirmar todos los cambios si no hubo errores críticos
    conn.commit()
    print("-" * 50)
    print(f"Resumen de la operación para la fecha {fecha_rutina}:")
    print(f"  Total de ejercicios a procesar: {len(rutina_semanal_ids)}")
    print(f"  ✅ Ejercicios insertados: {inserted_count}")
    print(f"  🟡 Ejercicios omitidos (duplicados o no encontrados): {skipped_count}")

except mysql.connector.Error as err:
    print(f"❌ Error crítico en la base de datos: {err}")
    if conn:
        conn.rollback() # Deshace cualquier cambio si ocurre un error antes del commit final

except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None and conn.is_connected():
        conn.close()
        print("🔌 Conexión a la base de datos cerrada.")