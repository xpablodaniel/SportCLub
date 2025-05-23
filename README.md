# 🏋️‍♂️ SportclubWeb: Registro de Entrenamientos en PHP + MySQL

> Proyecto colaborativo y abierto para registrar rutinas de entrenamiento a través de un formulario web conectado a una base de datos MySQL. Incluye tanto una interfaz web como un script en Python para inserciones manuales.

---

## ✅ Características

- 🌐 Formulario web interactivo para registrar:
  - Fecha, Grupo muscular, Ejercicio (autocompletado)
  - Series, Repeticiones, Peso utilizado
- 📑 Inserción segura con sentencias preparadas
- 🧠 Validación contra duplicados por ejercicio y fecha
- 🧾 Script Python adicional para carga rápida por consola
- 🎨 Estilo visual responsivo y minimalista

---

## 🗃️ Estructura de la Base de Datos

```sql
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
```

---

## 📁 Estructura del Proyecto

```bash
/SportclubWeb/
├── index.php            # Formulario web principal
├── procesar.php         # Lógica de inserción y respuestas AJAX
├── config.php           # Configuración de conexión MySQL
├── style.css            # Estilos visuales
├── script.js            # Autocompletado dinámico
├── entrenamiento.py     # Script en Python para carga manual
```

---

## 🚀 Cómo usar

1. Clona el repositorio.
2. Crea una base de datos MySQL con las tablas especificadas arriba.
3. Configura el archivo `config.php` con tus credenciales.
4. Abre `index.php` en un navegador para comenzar a registrar tus rutinas.

---

## 🧪 Script Python Opcional

Puedes registrar ejercicios rápidamente desde consola ejecutando:

```bash
python entrenamiento.py
```

Este script conecta a la misma base de datos y permite registrar rutinas predeterminadas.

---

## 📌 Autor y Colaboración

Este proyecto fue creado por Pablo (Mar del Plata, Argentina) como una forma de registrar sus entrenamientos diarios.

¡Estás invitado a colaborar, mejorar o adaptar este sistema a tus necesidades!

---

## 📄 Licencia

Este repositorio está disponible bajo la [Licencia MIT](LICENSE).
