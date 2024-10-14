# API REST para Habi - Prueba Técnica

## Introducción

Este proyecto tiene como objetivo desarrollar una API REST utilizando Python sin frameworks adicionales, conectándose a una base de datos MySQL. Esta API será presentada como parte de una prueba técnica para la empresa **Habi**. El enfoque principal es demostrar habilidades en la creación de APIs eficientes y funcionales utilizando las bibliotecas estándar de Python y manejando la conexión a la base de datos de manera directa, sin recurrir a ORMs.

## Tecnologías Utilizadas

- **Lenguaje de Programación:** Python 3.x
- **Base de Datos:** MySQL
- **Bibliotecas de Python:**
  - `mysql-connector-python` para la conexión con MySQL
  - Bibliotecas estándar de Python (`http.server`, `json`, `urllib.parse`, etc.)
  - `swagger-ui-py` para generar documentación Swagger de los endpoints
- **Herramientas de Prueba:**
  - **Postman** para probar los endpoints de la API
  - **Swagger UI** para la documentación interactiva de los endpoints


## Proceso de Desarrollo

### 1. Lectura y Comprensión del Problema

Antes de iniciar la implementación, es fundamental entender completamente los requisitos y objetivos de la prueba técnica:

- **Objetivo de la API:** Definir claramente qué funcionalidades debe ofrecer.
- **Requisitos Funcionales:** Identificar las operaciones que la API debe soportar.
- **Requisitos No Funcionales:** Considerar aspectos como el pep8, codigo facil de mantener y manejar apis rest.
- **Restricciones:** Utilizar Python sin frameworks y sin ORM, tal como se especifica en la prueba.

### 2. Validación de Credenciales de la Base de Datos MySQL

Asegurarse de que las credenciales proporcionadas para acceder a la base de datos MySQL son correctas y que se puede establecer una conexión exitosa.

**Pasos a Seguir:**

- **Verificar Detalles de Conexión:**
  - Host
  - Puerto
  - Usuario
  - Contraseña
  - Nombre de la base de datos

- **Probar la Conexión:**
  - Utilizar una herramienta de administración de MySQL (como MySQL Workbench) para verificar la conexión.

### 3. Exploración de la Base de Datos y Entidades

Comprender la estructura de la base de datos es esencial para diseñar los endpoints de la API.

**Acciones a Realizar:**

- **Identificar Relaciones entre Tablas:** Analizar claves primarias y foráneas para entender las relaciones.
- **Determinar Qué Tablas y Columnas Serán Expuestas:** Decidir qué datos serán accesibles a través de la API.

### 4. Selección de Tecnologías para Conexión con MySQL desde Python

Dado que no se utilizará un ORM ni ningún framework, es crucial elegir una biblioteca adecuada para manejar la conexión y las operaciones con MySQL.

**Opciones de Bibliotecas:**

- **`mysql-connector-python`:** Biblioteca oficial mantenida por Oracle, fácil de usar y con buen soporte.

**Decisión:** Se utilizará `mysql-connector-python` por su facilidad de uso y soporte oficial.

**Instalación:**

```bash
pip install mysql-connector-python
```