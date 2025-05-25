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
    header("Location: index.php?success=1");
    exit;
  } else {
    echo "❌ Error al registrar: " . $conn->error;
  }
  $insert_stmt->close();
}
?>