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