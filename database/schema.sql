-- =======================================================
-- BASE DE DATOS POSTGRESQL - INTEGRA
-- Compatible con PostgreSQL y Supabase
-- =======================================================

-- Tabla para registrar solicitudes de citas
CREATE TABLE IF NOT EXISTS citas (
    id_cita SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    tipo_servicio VARCHAR(80) NOT NULL,
    modalidad VARCHAR(50) NOT NULL,
    fecha_preferida DATE NOT NULL,
    hora_preferida TIME NOT NULL,
    mensaje TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para registrar mensajes del formulario de contacto
CREATE TABLE IF NOT EXISTS mensajes_contacto (
    id_mensaje SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(150) NOT NULL,
    asunto VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla opcional para servicios ofrecidos por Integra
CREATE TABLE IF NOT EXISTS servicios (
    id_servicio SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo'
);

-- Datos iniciales para servicios
INSERT INTO servicios (nombre, descripcion, estado)
VALUES
(
    'Psicoterapia',
    'Servicio de acompañamiento psicológico individual orientado a brindar apoyo emocional, fortalecer recursos personales y trabajar dificultades relacionadas con ansiedad, estrés, autoestima, duelo, relaciones interpersonales u otros procesos personales.',
    'Activo'
),
(
    'Talleres Psicoeducativos',
    'Espacios grupales de aprendizaje y reflexión sobre temas de salud mental, autocuidado, manejo emocional, comunicación, estrés, autoestima y bienestar integral.',
    'Activo'
);