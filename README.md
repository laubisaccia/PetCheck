# PetCheck - Sistema de Gestión Veterinaria

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

PetCheck es una aplicación web para facilitar la gestión de servicios veterinarios. Permite al personal registrar clientes y mascotas, agendar consultas y mantener historiales médicos completos.

## Características Principales

- **Gestión de Clientes**: Registro y administración de dueños de mascotas
- **Gestión de Mascotas**: Perfiles completos con información de cada mascota
- **Sistema de Citas**: Agendamiento de consultas veterinarias
- **Historial Médico**: Registro de diagnósticos y tratamientos
- **Gestión de Doctores**: Administración del personal veterinario
- **Sistema de Usuarios**: Control de acceso con roles (Admin/Usuario)
- **Autenticación JWT**: Sistema seguro de login con tokens
- **Documentación Automática**: API docs interactiva con Swagger UI

## Tecnologías Utilizadas

### Backend

- **FastAPI**: Framework web moderno y de alto rendimiento
- **SQLAlchemy**: ORM para manejo de base de datos
- **SQLite**: Base de datos ligera y portable
- **Pydantic**: Validación de datos
- **JWT**: Autenticación mediante tokens
- **Bcrypt**: Encriptación de contraseñas
- **Uvicorn**: Servidor de alto rendimiento

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/laubisaccia/PetCheck.git
cd PetCheck
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear usuario administrador

```bash
python create_admin.py
```

Este script crea un usuario admin con las siguientes credenciales:

- **Email**: `admin@petshop.com`
- **Password**: `admin123`

**Nota**: Podes modificar estas credenciales editando el archivo `create_admin.py` antes de ejecutarlo.

### 5. Iniciar el servidor

```bash
uvicorn api.main:app --reload
```

El servidor va a estar disponible en: `http://localhost:8000`

## Documentación de la API

Una vez que el servidor esté corriendo, podes acceder a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs

## Estructura del Proyecto

```
PetCheck/
├── api/
│   ├── auth/              # Autenticación y autorización
│   │   └── endpoint.py    # Login, JWT, verificación de roles
│   ├── customers/         # Gestión de clientes
│   │   └── endpoint.py    # CRUD de clientes
│   ├── pets/              # Gestión de mascotas
│   │   └── endpoint.py    # CRUD de mascotas
│   ├── appointments/      # Gestión de citas
│   │   └── endpoint.py    # CRUD de citas médicas
│   ├── doctors/           # Gestión de doctores
│   │   └── endpoint.py    # CRUD de doctores
│   ├── users/             # Gestión de usuarios del sistema
│   │   └── endpoint.py    # CRUD de usuarios (solo admin)
│   ├── core/              # Configuración central
│   │   ├── database.py    # Conexión a base de datos
│   │   └── models.py      # Modelos de SQLAlchemy
│   └── main.py            # Aplicación principal
├── create_admin.py        # Script para crear usuario admin
├── reset_database.py      # Script para resetear base de datos
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## API Endpoints

### Autenticación

- `POST /api/v1/login` - Iniciar sesión

### Clientes

- `GET /api/v1/customers` - Listar todos los clientes
- `POST /api/v1/customers` - Crear nuevo cliente
- `GET /api/v1/customers/{id}` - Obtener cliente por ID
- `PUT /api/v1/customers/{id}` - Actualizar cliente
- `DELETE /api/v1/customers/{id}` - Eliminar cliente

### Mascotas

- `GET /api/v1/pets` - Listar todas las mascotas
- `POST /api/v1/pets` - Crear nueva mascota
- `GET /api/v1/pets/{id}` - Obtener mascota por ID
- `PUT /api/v1/pets/{id}` - Actualizar mascota
- `DELETE /api/v1/pets/{id}` - Eliminar mascota

### Citas

- `GET /api/v1/appointments` - Listar todas las citas
- `POST /api/v1/appointments` - Crear nueva cita
- `GET /api/v1/appointments/{id}` - Obtener cita por ID
- `PUT /api/v1/appointments/{id}` - Actualizar cita
- `DELETE /api/v1/appointments/{id}` - Eliminar cita

### Doctores

- `GET /api/v1/doctors` - Listar todos los doctores
- `POST /api/v1/doctors` - Crear nuevo doctor
- `GET /api/v1/doctors/{id}` - Obtener doctor por ID
- `PUT /api/v1/doctors/{id}` - Actualizar doctor
- `DELETE /api/v1/doctors/{id}` - Eliminar doctor

### Usuarios (Solo Admin)

- `GET /api/v1/users` - Listar todos los usuarios
- `POST /api/v1/users` - Crear nuevo usuario
- `GET /api/v1/users/{id}` - Obtener usuario por ID
- `PUT /api/v1/users/{id}` - Actualizar usuario
- `DELETE /api/v1/users/{id}` - Eliminar usuario

## Sistema de Roles

### Admin

- Acceso completo al sistema
- Puede crear, editar y eliminar usuarios
- Gestión de todos los módulos

### User (Personal Veterinario)

- Gestión de clientes, mascotas, citas y doctores
- No puede administrar usuarios del sistema

## Scripts Útiles

### Resetear la Base de Datos

Si necesitas borrar todos los datos y empezar de nuevo:

```bash
python reset_database.py
```

Este script:

- Te va a pedir confirmación antes de proceder
- Va a eliminar todas las tablas
- Va a arecrear la estructura de la base de datos
- Deberás ejecutar `create_admin.py` nuevamente después del reset

### Crear Usuario Admin

```bash
python create_admin.py
```

## Configuración de CORS

La aplicación está configurada para aceptar peticiones desde:

- `http://localhost:5173` (Frontend en desarrollo)

Para modificar los orígenes permitidos, edita el archivo `api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Modifica aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Seguridad

- Las contraseñas se almacenan hasheadas usando Bcrypt
- La autenticación utiliza JWT (JSON Web Tokens)
- Los endpoints están protegidos por dependencias de FastAPI
- Validación automática de emails y datos de entrada
- Protección contra inyección SQL mediante SQLAlchemy ORM

## Desarrollo

### Variables de Entorno

Actualmente el proyecto usa valores por defecto. Para producción, considera agregar un archivo `.env` con:

```
DATABASE_URL=sqlite:///./api/core/customers.sqlite
SECRET_KEY=tu-clave-secreta-muy-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Base de Datos

El proyecto usa SQLite por defecto (`customers.sqlite`). Este archivo:

- Se crea automáticamente al iniciar la aplicación
- Está incluido en `.gitignore` (no se sube al repositorio)
- Se puede borrar y recrear usando `reset_database.py`
