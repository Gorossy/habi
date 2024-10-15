# API REST para Habi - Prueba Técnica

## Introducción
Este proyecto tiene como objetivo desarrollar una API REST utilizando Python sin frameworks adicionales, conectándose a una base de datos MySQL. Esta API será presentada como parte de una prueba técnica para la empresa Habi. El enfoque principal es demostrar habilidades en la creación de APIs eficientes y funcionales utilizando las bibliotecas estándar de Python y manejando la conexión a la base de datos de manera directa, sin recurrir a ORMs.

## Tecnologías Utilizadas
- **Lenguaje de Programación**: Python 3.12
- **Base de Datos**: MySQL
- **Bibliotecas de Python**:
  - `mysql-connector-python` para la conexión con MySQL
  - Bibliotecas estándar de Python (`http.server`, `json`, `urllib.parse`, etc.)
  - `swagger-ui-py` para generar documentación Swagger de los endpoints
- **Herramientas de Prueba**:
  - Postman para probar los endpoints de la API
  - Swagger UI para la documentación interactiva de los endpoints

## Proceso de Desarrollo

### 1. Lectura y Comprensión del Problema
Antes de iniciar la implementación, es fundamental entender completamente los requisitos y objetivos de la prueba técnica:

- **Objetivo de la API**: Definir claramente qué funcionalidades debe ofrecer.
- **Requisitos Funcionales**: Identificar las operaciones que la API debe soportar.
- **Requisitos No Funcionales**: Considerar aspectos como el PEP 8, código fácil de mantener y manejar APIs REST.
- **Restricciones**: Utilizar Python sin frameworks y sin ORM, tal como se especifica en la prueba.

### 2. Validación de Credenciales de la Base de Datos MySQL
Asegurarse de que las credenciales proporcionadas para acceder a la base de datos MySQL son correctas y que se puede establecer una conexión exitosa.

**Pasos a Seguir**:
- Verificar detalles de conexión (host, puerto, usuario, contraseña, nombre de la base de datos).
- Utilizar una herramienta de administración de MySQL (como MySQL Workbench) para probar la conexión.

### 3. Exploración de la Base de Datos y Entidades
Comprender la estructura de la base de datos es esencial para diseñar los endpoints de la API.

**Acciones a Realizar**:
- **Identificar Relaciones entre Tablas**: Analizar claves primarias y foráneas para entender las relaciones.
- **Determinar Qué Tablas y Columnas Serán Expuestas**: Decidir qué datos serán accesibles a través de la API.

### 4. Selección de Tecnologías para Conexión con MySQL desde Python
Dado que no se utilizará un ORM ni ningún framework, es crucial elegir una biblioteca adecuada para manejar la conexión y las operaciones con MySQL.

**Decisión**: Se utilizará `mysql-connector-python` por su facilidad de uso y soporte oficial.

**Instalación**:
```bash
pip install mysql-connector-python
```

## Endpoint Implementado

### 1. Endpoint de Consulta de Inmuebles
Este endpoint permite a los usuarios consultar los inmuebles con ciertos filtros específicos. Los usuarios pueden filtrar por ciudad, estado (pre_venta, en_venta, vendido), y año de construcción. Además, se excluyen propiedades con campos nulos como dirección, ciudad, precio y descripción.

**Ruta del Endpoint**:
- `GET /inmuebles`

**Parámetros de Consulta (Query Params)**:
- `city` (opcional): Filtrar por ciudad.
- `status` (opcional): Filtrar por estado (`pre_venta`, `en_venta`, `vendido`).
- `year` (opcional): Filtrar por año de construcción.

**Ejemplo de URL de Consulta**:
```
GET /inmuebles?city=Bogotá&status=en_venta&year=2020
```

**Respuesta Esperada**:
La respuesta incluye los siguientes campos para cada inmueble que cumple con los filtros:
- **Dirección** (`address`)
- **Ciudad** (`city`)
- **Estado** (`status`)
- **Precio de venta** (`price`)
- **Descripción** (`description`)

## Pasos para Iniciar el Proyecto

### 1. Clonar el Repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 2. Crear y Activar un Entorno Virtual
```bash
python -m venv venv
```

**Windows**:
```bash
venv\Scripts\activate
```

**Linux/macOS**:
```bash
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar el Archivo .env
Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias para conectarse a la base de datos MySQL:
```
DB_HOST=localhost
DB_PORT=puerto_de_ejemplo
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_la_base_de_datos
```

### 5. Iniciar el Servidor
```bash
python main.py
```
El servidor se ejecutará en el puerto 8000.

### 6. Probar el Endpoint
Puedes probar el endpoint utilizando herramientas como Postman o Swagger UI:
- **URL del Endpoint**: `http://localhost:8000/inmuebles`
- **Método**: `GET`

## Segunda Integración: Servicio de "Me gusta"

El servicio de "Me gusta" para los inmuebles se puede plantear de la siguiente manera, en términos conceptuales y técnicos:

### 1. Entidades involucradas
Para implementar esta funcionalidad, necesitaríamos crear una nueva tabla que registre los "me gusta" de los usuarios sobre los inmuebles, además de utilizar las tablas de User y Property. A continuación describo cómo se puede estructurar:

- **Tabla User**: Tabla que ya existe o debe existir, donde se almacenan los usuarios registrados en la plataforma. Cada usuario tiene un ID único.
- **Tabla Property**: Tabla que almacena los inmuebles.
- **Tabla Likes (nueva)**: Una nueva tabla que registre los "me gusta". Esta tabla debe registrar qué usuario dio "me gusta" a qué inmueble, junto con una marca de tiempo para llevar un histórico.

### 2. Estructura de la tabla Likes
Tendríamos que crear una tabla Likes con las siguientes columnas:

- **id (PK)**: Identificador único para cada registro de "me gusta".
- **user_id (FK hacia la tabla User)**: El usuario que dio el "me gusta".
- **property_id (FK hacia la tabla Property)**: El inmueble al que el usuario le dio "me gusta".
- **created_at**: Fecha y hora en que se dio el "me gusta" (para llevar un historial de cuándo ocurrió).

**SQL para la tabla Likes**:
```sql
CREATE TABLE Likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    property_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (property_id) REFERENCES Property(id),
    UNIQUE (user_id, property_id)  -- Un usuario solo puede dar un me gusta por propiedad
);
```

### 3. Lógica del servicio de "Me gusta"
Conceptualmente, los usuarios solo pueden darle "me gusta" a un inmueble una vez. Si el usuario ya dio "me gusta" a ese inmueble, no debería poder volver a darle "me gusta" hasta que retire su "me gusta". Esto puede manejarse fácilmente con la lógica de inserción en la base de datos.

### 4. Endpoints requeridos
Necesitaríamos al menos dos endpoints para este servicio:

- **POST /likes**: Para que un usuario registrado le dé "me gusta" a un inmueble.
- **DELETE /likes**: Para que un usuario pueda quitar su "me gusta" a un inmueble.





### 5. Consulta para obtener el historial de "Me gusta" de un usuario
Si deseas permitir que un usuario vea su historial de "me gusta" (a qué propiedades ha dado "me gusta"), puedes usar una consulta simple para obtener esta información.

**SQL**:
```sql
SELECT p.address, p.city, p.price, p.description, p.year
FROM Likes l
JOIN Property p ON l.property_id = p.id
WHERE l.user_id = {user_id};
```

### 6. Consideraciones adicionales:
- **Validaciones adicionales**: Puedes agregar validaciones adicionales para asegurarte de que el `user_id` y el `property_id` existan antes de insertar o eliminar un "me gusta".
- **Contador de "Me gusta"**: Si se desea llevar un contador de "me gusta" para cada propiedad, se podría añadir una columna en la tabla Property para almacenar este valor y actualizarlo cada vez que un usuario dé o quite un "me gusta".

**Actualización del contador de "Me gusta" al añadir**:
```sql
UPDATE Property SET likes_count = likes_count + 1 WHERE id = {property_id};
```

**Actualización del contador de "Me gusta" al eliminar**:
```sql
UPDATE Property SET likes_count = likes_count - 1 WHERE id = {property_id};
```

### 7. Diagrama Entidad-Relación (ER) del Servicio de 'Me gusta'
El servicio de 'Me gusta' se representa con tres tablas principales:
- **User** → Relación de uno a muchos con **Likes**.
- **Property** → Relación de uno a muchos con **Likes**.
- **Likes** → Relación de muchos a uno con ambas tablas.

