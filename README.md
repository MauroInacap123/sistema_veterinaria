# Sistema de Gestión Veterinaria

**Autor:** Mauricio Bustamante  
**Institución:** INACAP Renca  
**Asignatura:** Programación Orientada a Objetos Segura (TI3021)  
**Evaluación:** ES2 - Unidad 2

## 📋 Descripción

Sistema de gestión para clínicas veterinarias desarrollado en Python que permite administrar:
- **Clientes** (dueños de mascotas)
- **Mascotas** (pacientes)
- **Veterinarios** (doctores)
- **Citas** (consultas médicas)

Implementa el paradigma de **Programación Orientada a Objetos** con conexión segura a **Oracle Database**.

## 🏗️ Arquitectura

```
sistema_veterinaria/
├── models/              # Clases del dominio (POO)
│   ├── cliente.py       # Cliente con @property
│   ├── mascota.py       # Mascota con validaciones
│   ├── veterinario.py   # Veterinario
│   └── cita.py          # Cita médica
├── dao/                 # Data Access Objects (CRUD)
│   ├── cliente_dao.py
│   ├── mascota_dao.py
│   ├── veterinario_dao.py
│   └── cita_dao.py
├── database.py          # Configuración de conexión
├── main.py              # Aplicación principal con menús
├── schema.sql           # Script de creación de BD
├── .env                 # Credenciales (no incluido)
├── .env.example         # Plantilla de configuración
└── requirements.txt     # Dependencias Python
```

## 🚀 Instalación Rápida

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar credenciales
```bash
cp .env.example .env
# Editar .env con tus datos de Oracle
```

### 3. Crear tablas en Oracle
- Abrir SQL Developer
- Ejecutar `schema.sql` completo (F5)

### 4. Ejecutar aplicación
```bash
python main.py
```

## 📊 Modelo de Datos

### Relaciones:
- **Cliente** (1:N) → **Mascota**
- **Mascota** (N:M) → **Veterinario** (a través de Cita)
- **Cita**: tabla intermedia con datos propios

## 🔒 Características de Seguridad

✅ Encapsulamiento con `@property`  
✅ Validaciones en setters  
✅ Credenciales en `.env`  
✅ Prepared statements (SQL injection)  
✅ Manejo de excepciones  
✅ Integridad referencial (FK)

## 📚 Funcionalidades CRUD

Cada entidad tiene:
- **CREATE:** Insertar nuevos registros
- **READ:** Consultar por ID o listar todos
- **UPDATE:** Modificar registros existentes
- **DELETE:** Eliminar registros

Funciones adicionales:
- Mascotas por cliente
- Citas por mascota
- Citas por veterinario
- Validación de especies
- Cálculo de edad (cachorro/senior)

## ✅ Cumplimiento de Requisitos

✅ Programación Orientada a Objetos  
✅ Encapsulamiento (`@property`)  
✅ Conexión segura a Oracle  
✅ CRUD completo (4 entidades)  
✅ Manejo de excepciones  
✅ Interfaz por terminal  
✅ Relaciones entre clases  
✅ Validaciones de negocio

## 👨‍💻 Autor

**Mauricio Bustamante**  
Estudiante de Ingeniería en Informática  
INACAP Renca - 2025

