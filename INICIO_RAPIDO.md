# 🚀 Inicio Rápido - Sistema Veterinaria

## Pasos (5 minutos)

### 1. Instalar librerías
```bash
pip install -r requirements.txt
```

### 2. Configurar BD
Edita `.env`:
```
ORACLE_USER="system"
ORACLE_PASSWORD="tu_password"
ORACLE_DSN="localhost:1521/xe"
```

### 3. Crear tablas
En SQL Developer: Ejecutar `schema.sql` (F5)

### 4. Ejecutar
```bash
python main.py
```

## Demo Rápida

1. **Crear cliente:** Menú 1 → Opción 1
2. **Crear mascota:** Menú 2 → Opción 1 → Asignar al cliente
3. **Crear veterinario:** Menú 3 → Opción 1
4. **Agendar cita:** Menú 4 → Opción 1
5. **Ver citas por mascota:** Menú 4 → Opción 4

## Solución de Problemas

❌ **"No module named 'oracledb'"**
```bash
pip install oracledb python-dotenv
```

❌ **"Connection refused"**
- Verifica que Oracle esté corriendo
- Revisa credenciales en `.env`

❌ **"Table does not exist"**
- Ejecuta `schema.sql` en SQL Developer
