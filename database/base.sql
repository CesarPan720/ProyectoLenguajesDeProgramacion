SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS elecciones_2026_peru;
USE elecciones_2026_peru;

-- Tabla para el padrón electoral
CREATE TABLE IF NOT EXISTS padron_electoral (
    dni VARCHAR(8) PRIMARY KEY,
    fecha_nacimiento DATE NOT NULL,
    votado BOOLEAN DEFAULT FALSE,
    biometria_registrada BOOLEAN DEFAULT FALSE
);

-- Tabla para los candidatos
CREATE TABLE IF NOT EXISTS candidatos (
    id_candidato INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    partido VARCHAR(100) NOT NULL,
    simbolo VARCHAR(255),
    foto VARCHAR(255),
    votos INT DEFAULT 0
);

-- Insertar los datos por defecto (IGNORE evita errores si el DNI ya existe)
INSERT IGNORE INTO padron_electoral (dni, fecha_nacimiento, votado, biometria_registrada) VALUES
('70123456', '1998-04-12', FALSE, TRUE),
('40123456', '1985-11-30', FALSE, TRUE),
('10123456', '2001-07-05', FALSE, FALSE);

INSERT IGNORE INTO candidatos (id_candidato, nombre, partido, simbolo, foto, votos) VALUES
(1, 'Ana Martínez', 'Partido Tecnológico', 'candidatos/candidato_1_simbolo.png', 'candidatos/candidato_1_foto.jpg', 0),
(2, 'Carlos Mendoza', 'Unión Digital', 'candidatos/candidato_2_simbolo.png', 'candidatos/candidato_2_foto.jpg', 0),
(3, 'Voto en Blanco', 'N/A', NULL, NULL, 0);