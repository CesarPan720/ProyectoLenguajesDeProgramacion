SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS elecciones_2026_peru;
USE elecciones_2026_peru;

-- Tabla para el padrón electoral
CREATE TABLE IF NOT EXISTS padron_electoral (
    dni VARCHAR(8) PRIMARY KEY,
    votado BOOLEAN DEFAULT FALSE,
    biometria_registrada BOOLEAN DEFAULT FALSE
);

-- Tabla para los candidatos
CREATE TABLE IF NOT EXISTS candidatos (
    id_candidato INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    partido VARCHAR(100) NOT NULL,
    votos INT DEFAULT 0
);

-- Insertar los datos por defecto (IGNORE evita errores si el DNI ya existe)
INSERT IGNORE INTO padron_electoral (dni, votado, biometria_registrada) VALUES 
('70123456', FALSE, TRUE),
('40123456', FALSE, TRUE),
('10123456', FALSE, FALSE);

INSERT IGNORE INTO candidatos (id_candidato, nombre, partido, votos) VALUES 
(1, 'Ana Martínez', 'Partido Tecnológico', 0),
(2, 'Carlos Mendoza', 'Unión Digital', 0),
(3, 'Voto en Blanco', 'N/A', 0);