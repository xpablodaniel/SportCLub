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
