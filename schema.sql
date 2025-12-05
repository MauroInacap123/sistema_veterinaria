-- ============================================
-- Script de creación de Base de Datos
-- Sistema de Gestión Veterinaria
-- Oracle SQL Developer
-- Mauricio Bustamante - INACAP
-- ============================================

-- Eliminar tablas si existen (para pruebas)
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE cita CASCADE CONSTRAINTS';
   EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE mascota CASCADE CONSTRAINTS';
   EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE veterinario CASCADE CONSTRAINTS';
   EXCEPTION WHEN OTHERS THEN NULL;
END;
/

BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE cliente CASCADE CONSTRAINTS';
   EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- ============================================
-- Tabla: CLIENTE (Dueño de mascotas)
-- ============================================
CREATE TABLE cliente (
    id_cliente NUMBER PRIMARY KEY,
    rut VARCHAR2(12) NOT NULL,
    nombres VARCHAR2(100) NOT NULL,
    apellidos VARCHAR2(100) NOT NULL,
    telefono VARCHAR2(20),
    email VARCHAR2(100),
    direccion VARCHAR2(200),
    CONSTRAINT uk_cliente_rut UNIQUE (rut),
    CONSTRAINT uk_cliente_email UNIQUE (email)
);

-- ============================================
-- Tabla: MASCOTA (Paciente)
-- ============================================
CREATE TABLE mascota (
    id_mascota NUMBER PRIMARY KEY,
    nombre VARCHAR2(50) NOT NULL,
    especie VARCHAR2(20) NOT NULL,
    raza VARCHAR2(50),
    edad NUMBER NOT NULL,
    color VARCHAR2(30),
    peso NUMBER(5, 2),
    id_cliente NUMBER NOT NULL,
    CONSTRAINT fk_mascota_cliente 
        FOREIGN KEY (id_cliente) 
        REFERENCES cliente(id_cliente)
        ON DELETE CASCADE,
    CONSTRAINT ck_mascota_especie 
        CHECK (especie IN ('PERRO', 'GATO', 'AVE', 'CONEJO', 'HAMSTER')),
    CONSTRAINT ck_mascota_edad 
        CHECK (edad >= 0 AND edad <= 50),
    CONSTRAINT ck_mascota_peso 
        CHECK (peso > 0 AND peso <= 500)
);

-- ============================================
-- Tabla: VETERINARIO (Doctor)
-- ============================================
CREATE TABLE veterinario (
    id_veterinario NUMBER PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    apellido VARCHAR2(100) NOT NULL,
    especialidad VARCHAR2(100),
    telefono VARCHAR2(20),
    email VARCHAR2(100),
    CONSTRAINT uk_veterinario_email UNIQUE (email)
);

-- ============================================
-- Tabla: CITA (Consulta médica)
-- ============================================
CREATE TABLE cita (
    id_cita NUMBER PRIMARY KEY,
    id_mascota NUMBER NOT NULL,
    id_veterinario NUMBER NOT NULL,
    fecha DATE NOT NULL,
    hora VARCHAR2(10) NOT NULL,
    motivo VARCHAR2(500),
    estado VARCHAR2(20) DEFAULT 'PENDIENTE',
    diagnostico VARCHAR2(1000),
    CONSTRAINT fk_cita_mascota 
        FOREIGN KEY (id_mascota) 
        REFERENCES mascota(id_mascota)
        ON DELETE CASCADE,
    CONSTRAINT fk_cita_veterinario 
        FOREIGN KEY (id_veterinario) 
        REFERENCES veterinario(id_veterinario)
        ON DELETE CASCADE,
    CONSTRAINT ck_cita_estado 
        CHECK (estado IN ('PENDIENTE', 'CONFIRMADA', 'COMPLETADA', 'CANCELADA'))
);

-- ============================================
-- Secuencias para generar IDs automáticos
-- ============================================
CREATE SEQUENCE seq_cliente START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_mascota START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_veterinario START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE seq_cita START WITH 1 INCREMENT BY 1;

-- ============================================
-- Datos de prueba
-- ============================================

-- Clientes
INSERT INTO cliente VALUES (seq_cliente.NEXTVAL, '12345678-9', 'Juan', 'Pérez García', '+56912345678', 'juan.perez@email.cl', 'Av. Libertador 123, Santiago');
INSERT INTO cliente VALUES (seq_cliente.NEXTVAL, '98765432-1', 'María', 'González López', '+56923456789', 'maria.gonzalez@email.cl', 'Calle Los Robles 456, Providencia');
INSERT INTO cliente VALUES (seq_cliente.NEXTVAL, '11223344-5', 'Pedro', 'Sánchez Muñoz', '+56934567890', 'pedro.sanchez@email.cl', 'Pasaje Las Flores 789, Las Condes');
INSERT INTO cliente VALUES (seq_cliente.NEXTVAL, '55667788-9', 'Ana', 'Martínez Silva', '+56945678901', 'ana.martinez@email.cl', 'Av. Apoquindo 321, Vitacura');

-- Mascotas
INSERT INTO mascota VALUES (seq_mascota.NEXTVAL, 'Max', 'PERRO', 'Golden Retriever', 3, 'Dorado', 32.5, 1);
INSERT INTO mascota VALUES (seq_mascota.NEXTVAL, 'Luna', 'GATO', 'Siamés', 2, 'Blanco', 4.2, 2);
INSERT INTO mascota VALUES (seq_mascota.NEXTVAL, 'Rocky', 'PERRO', 'Pastor Alemán', 5, 'Negro y café', 35.0, 1);
INSERT INTO mascota VALUES (seq_mascota.NEXTVAL, 'Michi', 'GATO', 'Persa', 1, 'Gris', 3.8, 3);
INSERT INTO mascota VALUES (seq_mascota.NEXTVAL, 'Pepito', 'AVE', 'Loro', 10, 'Verde', 0.5, 4);
INSERT INTO mascota VALUES (seq_mascota.NEXTVAL, 'Bobby', 'PERRO', 'Poodle', 4, 'Blanco', 8.0, 2);

-- Veterinarios
INSERT INTO veterinario VALUES (seq_veterinario.NEXTVAL, 'Dra. Carmen', 'Rodríguez', 'Medicina General', '+56956789012', 'carmen.rodriguez@vetclinic.cl');
INSERT INTO veterinario VALUES (seq_veterinario.NEXTVAL, 'Dr. Luis', 'Fernández', 'Cirugía', '+56967890123', 'luis.fernandez@vetclinic.cl');
INSERT INTO veterinario VALUES (seq_veterinario.NEXTVAL, 'Dra. Patricia', 'Torres', 'Dermatología', '+56978901234', 'patricia.torres@vetclinic.cl');
INSERT INTO veterinario VALUES (seq_veterinario.NEXTVAL, 'Dr. Roberto', 'Morales', 'Cardiología', '+56989012345', 'roberto.morales@vetclinic.cl');

-- Citas
INSERT INTO cita VALUES (seq_cita.NEXTVAL, 1, 1, TO_DATE('2024-12-10', 'YYYY-MM-DD'), '10:00', 'Control de vacunas', 'CONFIRMADA', NULL);
INSERT INTO cita VALUES (seq_cita.NEXTVAL, 2, 3, TO_DATE('2024-12-11', 'YYYY-MM-DD'), '11:30', 'Revisión de piel', 'PENDIENTE', NULL);
INSERT INTO cita VALUES (seq_cita.NEXTVAL, 3, 2, TO_DATE('2024-12-12', 'YYYY-MM-DD'), '15:00', 'Castración', 'CONFIRMADA', NULL);
INSERT INTO cita VALUES (seq_cita.NEXTVAL, 4, 1, TO_DATE('2024-12-13', 'YYYY-MM-DD'), '09:00', 'Consulta general', 'PENDIENTE', NULL);
INSERT INTO cita VALUES (seq_cita.NEXTVAL, 5, 4, TO_DATE('2024-12-14', 'YYYY-MM-DD'), '14:00', 'Chequeo cardíaco', 'CONFIRMADA', NULL);
INSERT INTO cita VALUES (seq_cita.NEXTVAL, 1, 1, TO_DATE('2024-11-20', 'YYYY-MM-DD'), '10:00', 'Vacuna antirrábica', 'COMPLETADA', 'Vacuna aplicada correctamente. Próxima dosis en 1 año.');

COMMIT;

-- Verificar creación
SELECT 'Clientes: ' || COUNT(*) AS total FROM cliente;
SELECT 'Mascotas: ' || COUNT(*) AS total FROM mascota;
SELECT 'Veterinarios: ' || COUNT(*) AS total FROM veterinario;
SELECT 'Citas: ' || COUNT(*) AS total FROM cita;
