### **📝 Documentación: Actualización de la Tabla `rutinas` y Uso de `JOIN`s**

#### **1\. Estructura Actual de las Tablas**

CREATE TABLE ejercicios (  
  id\_ejercicio INT AUTO\_INCREMENT PRIMARY KEY,  
  grupo\_muscular VARCHAR(100),  
  nombre\_ejercicio VARCHAR(150),  
  descripcion\_ejercicio TEXT,  
  nombre\_ingles VARCHAR(150)  
);

CREATE TABLE rutinas (  
  id\_ejercicio INT,  
  grupo\_muscular VARCHAR(100), \-- ¡Redundante\!  
  nombre\_ejercicio VARCHAR(150), \-- ¡Redundante\!  
  fecha DATE NOT NULL,  
  series INT NOT NULL,  
  repeticiones INT NOT NULL,  
  peso DECIMAL(5,2),  
  FOREIGN KEY (id\_ejercicio) REFERENCES ejercicios(id\_ejercicio)  
);

#### **2\. Problema: Redundancia de Datos en `rutinas`**

Las columnas `grupo_muscular` y `nombre_ejercicio` en la tabla `rutinas` son redundantes. Esta información ya está almacenada en la tabla `ejercicios` y está vinculada por la clave foránea `id_ejercicio`. Esto causa:

* **Inconsistencia:** Si cambia el nombre o grupo de un ejercicio en `ejercicios`, los registros en `rutinas` no se actualizan automáticamente.  
* **Espacio:** Almacenar la misma información repetidamente ocupa espacio innecesario.  
* **Mantenimiento:** Requiere actualizar los mismos datos en múltiples lugares.

#### 

#### **3\. Solución: Normalización de la Tabla `rutinas`**

Eliminar las columnas redundantes de la tabla `rutinas`.

\-- Estructura OPTIMIZADA para 'rutinas'  
CREATE TABLE rutinas (  
  id\_rutina INT UNSIGNED PRIMARY KEY AUTO\_INCREMENT,  
  id\_ejercicio INT UNSIGNED NOT NULL,  
  fecha DATE NOT NULL,  
  series INT NOT NULL,  
  repeticiones INT NOT NULL,  
  peso DECIMAL(5,2),  
  FOREIGN KEY (id\_ejercicio) REFERENCES ejercicios(id\_ejercicio)  
);

* **`id_rutina` (Nuevo):** Clave primaria para identificar cada registro de rutina.  
* **`id_ejercicio`:** Clave foránea que vincula cada rutina a un ejercicio específico en la tabla `ejercicios`.  
* **Eliminamos `grupo_muscular` y `nombre_ejercicio`:** Ya no son necesarios en `rutinas`.

#### 

#### **4\. Migración de Datos (Opcional, si ya tienes datos en `rutinas`)**

#### **5\. Ventajas de Usar `JOIN`s para Consultas**

Después de normalizar la tabla `rutinas`, usaremos `JOIN`s para combinar datos de ambas tablas cuando sea necesario.

* **Evita la Redundancia:** No almacenamos la misma información en múltiples lugares.  
* **Consistencia de Datos:** Los cambios en la tabla `ejercicios` se reflejan automáticamente en las consultas que usan `JOIN`s.  
* **Integridad Referencial:** La clave foránea `id_ejercicio` asegura que solo podamos registrar rutinas para ejercicios que realmente existen en la tabla `ejercicios`.  
* **Flexibilidad:** Podemos obtener diferentes combinaciones de datos de ambas tablas según nuestras necesidades.

#### **6\. Ejemplo de Consulta con `JOIN`**

Para obtener el nombre y grupo muscular de un ejercicio junto con los detalles de la rutina:

SELECT

    r.id\_rutina,

    e.nombre\_ejercicio,

    e.grupo\_muscular,

    r.fecha,

    r.series,

    r.repeticiones,

    r.peso

FROM

    rutinas AS r

JOIN

    ejercicios AS e ON r.id\_ejercicio \= e.id\_ejercicio

ORDER BY

    r.fecha DESC, e.nombre\_ejercicio ASC;

#### **7\. Vistas (Opcional)**

Puedes crear una vista para encapsular esta consulta y simplificar su uso:

CREATE VIEW vista\_rutinas\_completas AS

SELECT

    r.id\_rutina,

    e.nombre\_ejercicio,

    e.grupo\_muscular,

    r.fecha,

    r.series,

    r.repeticiones,

    r.peso

FROM

    rutinas AS r

JOIN

    ejercicios AS e ON r.id\_ejercicio \= e.id\_ejercicio;

\-- Luego, puedes consultar la vista:

SELECT \* FROM vista\_rutinas\_completas WHERE fecha \= '2025-05-25';

