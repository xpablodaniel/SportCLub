# Crear el contenido completo del README.md con toda la documentación del proyecto

readme_content = """# 🏋️‍♂️ SportclubWeb: Registro de Entrenamientos en PHP + MySQL

> Proyecto colaborativo y abierto para registrar rutinas de entrenamiento a través de un formulario web conectado a una base de datos MySQL. Incluye tanto una interfaz web como un script en Python para inserciones manuales.

---

## ✅ Características

- 🌐 Formulario web interactivo para registrar:
  - Fecha
  - Grupo muscular
  - Ejercicio (autocompletado)
  - Series
  - Repeticiones
  - Peso utilizado
- 📑 Inserción segura con sentencias preparadas (`Prepared Statements`)
- 🧠 Validación contra duplicados por ejercicio y fecha
- 🧾 Script Python adicional para carga rápida por línea de comandos
- 🎨 Estilo visual responsivo y simple

---

## 📁 Estructura del Proyecto

```bash
/SportclubWeb/
├── index.php       # Formulario web
├── procesar.php    # Lógica de inserción + AJAX
├── config.php      # Conexión MySQL
├── style.css       # Estilos visuales
├── script.js       # Autocompletado dinámico por grupo muscular
├── entrenar_validado.py  # Script en Python para inserciones manuales

🗃️ Base de Datos

Tablas

CREATE TABLE ejercicios (
  id_ejercicio INT AUTO_INCREMENT PRIMARY KEY,
  grupo_muscular VARCHAR(100),
  nombre_ejercicio VARCHAR(150),
  descripcion_ejercicio TEXT,
  nombre_ingles VARCHAR(150)
);

CREATE TABLE rutinas (
  id_ejercicio INT,
  grupo_muscular VARCHAR(100),
  nombre_ejercicio VARCHAR(150),
  fecha DATE NOT NULL,
  series INT NOT NULL,
  repeticiones INT NOT NULL,
  peso DECIMAL(5,2),
  FOREIGN KEY (id_ejercicio) REFERENCES ejercicios(id_ejercicio)
);

🖥️ Código de Archivos

config.php
<?php
$host     = 'localhost';
$user     = 'pablo';
$password = 'usuario';
$database = 'Sportclub';

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    die("❌ Conexión fallida: " . $conn->connect_error);
}
?>

index.php
<?php include 'config.php'; ?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Registro de Rutina</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h2>📝 Registrar Rutina de Entrenamiento</h2>
  <form action="procesar.php" method="POST">
    <label>Fecha:</label>
    <input type="date" name="fecha" value="<?= date('Y-m-d') ?>" required><br>

    <label>Grupo Muscular:</label>
    <select name="grupo_muscular" id="grupo_muscular" required>
      <option value="">Seleccionar</option>
      <?php
        $grupos = $conn->query("SELECT DISTINCT grupo_muscular FROM ejercicios ORDER BY grupo_muscular");
        while ($row = $grupos->fetch_assoc()) {
          echo "<option value='{$row['grupo_muscular']}'>{$row['grupo_muscular']}</option>";
        }
      ?>
    </select><br>

    <label>Ejercicio:</label>
    <select name="id_ejercicio" id="id_ejercicio" required>
      <option value="">Seleccionar grupo primero</option>
    </select><br>

    <label>Series:</label>
    <input type="number" name="series" min="1" required><br>

    <label>Repeticiones:</label>
    <input type="number" name="repeticiones" min="1" required><br>

    <label>Peso (kg):</label>
    <input type="number" step="0.5" name="peso"><br>

    <button type="submit">💾 Registrar</button>
  </form>

  <script src="script.js"></script>
</body>
</html>

script.js

document.getElementById('grupo_muscular').addEventListener('change', function () {
  const grupo = this.value;
  const ejercicioSelect = document.getElementById('id_ejercicio');
  ejercicioSelect.innerHTML = '<option value="">Cargando...</option>';

  fetch('procesar.php?grupo=' + encodeURIComponent(grupo))
    .then(response => response.json())
    .then(data => {
      ejercicioSelect.innerHTML = '<option value="">Seleccionar</option>';
      data.forEach(item => {
        ejercicioSelect.innerHTML += `<option value="\${item.id}">\${item.nombre}</option>`;
      });
    });
});

procesar.php
<?php
include 'config.php';

if (isset($_GET['grupo'])) {
  $grupo = $conn->real_escape_string($_GET['grupo']);
  $sql = "SELECT id_ejercicio, nombre_ejercicio FROM ejercicios WHERE grupo_muscular = '$grupo' ORDER BY nombre_ejercicio";
  $result = $conn->query($sql);
  $salida = [];
  while ($row = $result->fetch_assoc()) {
    $salida[] = ['id' => $row['id_ejercicio'], 'nombre' => $row['nombre_ejercicio']];
  }
  header('Content-Type: application/json');
  echo json_encode($salida);
  exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $id_ejercicio   = (int)$_POST['id_ejercicio'];
  $grupo_muscular = $_POST['grupo_muscular'];
  $fecha          = $_POST['fecha'];
  $series         = (int)$_POST['series'];
  $repeticiones   = (int)$_POST['repeticiones'];
  $peso           = isset($_POST['peso']) ? (float)$_POST['peso'] : null;

  $sql = "SELECT nombre_ejercicio FROM ejercicios WHERE id_ejercicio = ?";
  $stmt = $conn->prepare($sql);
  $stmt->bind_param("i", $id_ejercicio);
  $stmt->execute();
  $stmt->bind_result($nombre_ejercicio);
  $stmt->fetch();
  $stmt->close();

  $check_sql = "SELECT COUNT(*) FROM rutinas WHERE id_ejercicio = ? AND fecha = ?";
  $check_stmt = $conn->prepare($check_sql);
  $check_stmt->bind_param("is", $id_ejercicio, $fecha);
  $check_stmt->execute();
  $check_stmt->bind_result($count);
  $check_stmt->fetch();
  $check_stmt->close();

  if ($count > 0) {
    echo "🟡 Ya existe este ejercicio para esa fecha. <a href='index.php'>Volver</a>";
    exit;
  }

  $insert_sql = "INSERT INTO rutinas (id_ejercicio, grupo_muscular, nombre_ejercicio, fecha, series, repeticiones, peso)
                 VALUES (?, ?, ?, ?, ?, ?, ?)";
  $insert_stmt = $conn->prepare($insert_sql);
  $insert_stmt->bind_param("isssiii", $id_ejercicio, $grupo_muscular, $nombre_ejercicio, $fecha, $series, $repeticiones, $peso);
  if ($insert_stmt->execute()) {
    echo "✅ ¡Ejercicio registrado correctamente! <a href='index.php'>Volver</a>";
  } else {
    echo "❌ Error al registrar: " . $conn->error;
  }
  $insert_stmt->close();
}
?>
entrenar_validado.py (script manual)
import mysql.connector
from datetime import datetime

config = {
    'user': 'pablo',
    'password': 'usuario',
    'host': 'localhost',
    'database': 'Sportclub',
    'raise_on_warnings': True
}

fecha_rutina = '2025-05-21'
rutina_semanal_ids = [
    (46, 3, 12, 7.5),
    (14, 4, 10, 72),
    (43, 4, 10, 65)
]

all_exercises = {
    46: ('Cuádriceps', 'Zancadas inversas'),
    14: ('Cuádriceps', 'Extension de Cuadriceps en sillon'),
    43: ('Pierna', 'Abductores en máquina')
}

conn = None
cursor = None
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    sql_insert = '''
        INSERT INTO rutinas (
            id_ejercicio, grupo_muscular, nombre_ejercicio,
            fecha, series, repeticiones, peso
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    sql_check = "SELECT COUNT(*) FROM rutinas WHERE id_ejercicio = %s AND fecha = %s"

    insertados = 0
    for ejercicio_id, series, repeticiones, peso in rutina_semanal_ids:
        if ejercicio_id in all_exercises:
            grupo_muscular, nombre_ejercicio = all_exercises[ejercicio_id]
            cursor.execute(sql_check, (ejercicio_id, fecha_rutina))
            if cursor.fetchone()[0] == 0:
                cursor.execute(sql_insert, (
                    ejercicio_id, grupo_muscular, nombre_ejercicio,
                    fecha_rutina, series, repeticiones, peso
                ))
                insertados += 1
            else:
                print(f"🟡 Ya existe {nombre_ejercicio} para {fecha_rutina}")
    conn.commit()
    print(f"✅ Insertados: {insertados}")
except Exception as e:
    print("❌ Error:", e)
    if conn: conn.rollback()
finally:
    if cursor: cursor.close()
    if conn and conn.is_connected(): conn.close()

📌 Autor y Colaboración
Este proyecto fue creado por Pablo (Mar del Plata, Argentina) como una forma de registrar sus entrenamientos a diario.
¡Estás invitado a colaborar, mejorar o adaptar este sistema a tus necesidades!

📄 Licencia
Este repositorio es de uso libre bajo la Licencia MIT.
"""