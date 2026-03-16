-- Active: 1742855324021@@127.0.0.1@3306@boardai
-- ============================================================
--  Base de datos: notas2026
--  Servidor: MariaDB / MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS `notas2026`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE `notas2026`;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- ------------------------------------------------------------
--  Tabla: estudiantes
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `estudiantes`;

CREATE TABLE `estudiantes` (
  `id`        INT(11)      NOT NULL AUTO_INCREMENT,
  `Nombre`    VARCHAR(100) DEFAULT NULL,
  `Edad`      INT(11)      DEFAULT NULL,
  `Carrera`   VARCHAR(100) DEFAULT NULL,
  `nota1`     DECIMAL(3,2) DEFAULT NULL,
  `nota2`     DECIMAL(3,2) DEFAULT NULL,
  `nota3`     DECIMAL(3,2) DEFAULT NULL,
  `Promedio`  DECIMAL(3,2) DEFAULT NULL,
  `Desempeño` VARCHAR(20)  DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `estudiantes`
  (`id`,`Nombre`,`Edad`,`Carrera`,`nota1`,`nota2`,`nota3`,`Promedio`,`Desempeño`) VALUES
(1,  'Paula',        21,'Fisica',      4.00,4.00,3.00,3.00,'Bueno'),
(2,  'Ana',          18,'Ingenieria',  2.00,5.00,3.00,3.00,'Regular'),
(3,  'Maria',        23,'Ingenieria',  5.00,4.00,3.00,4.00,'Bueno'),
(4,  'Luis',         22,'Matematicas', 2.00,3.00,4.00,3.00,'Regular'),
(5,  'Ana',          21,'Ingenieria',  5.00,5.00,5.00,5.00,'Excelente'),
(6,  'Maria',        23,'Ingenieria',  4.00,3.00,3.00,3.00,'Regular'),
(7,  'Ana',          20,'Fisica',      2.00,3.00,3.00,2.00,'Regular'),
(8,  'Luis',         20,'Ingenieria',  4.00,2.00,4.00,3.00,'Bueno'),
(9,  'Luis',         23,'Fisica',      4.00,3.00,2.00,3.00,'Regular'),
(10, 'Luis',         22,'Ingenieria',  3.00,3.00,2.00,2.00,'Regular'),
(11, 'Ana',          20,'Fisica',      5.00,3.00,2.00,3.00,'Regular'),
(12, 'Carlos',       19,'Fisica',      4.00,2.00,2.00,2.00,'Regular'),
(13, 'Luis',         21,'Fisica',      2.00,5.00,5.00,4.00,'Bueno'),
(14, 'Maria',        22,'Fisica',      5.00,2.00,2.00,3.00,'Regular'),
(15, 'Jose',         18,'Fisica',      4.00,3.00,2.00,3.00,'Regular'),
(16, 'Paula',        21,'Fisica',      5.00,4.00,2.00,3.00,'Bueno'),
(17, 'Luis',         22,'Ingenieria',  2.00,3.00,2.00,2.00,'Deficiente'),
(18, 'Maria',        22,'Matematicas', 5.00,5.00,2.00,4.00,'Bueno'),
(19, 'Luis',         20,'Matematicas', 5.00,4.00,5.00,4.00,'Excelente'),
(20, 'Ana',          22,'Ingenieria',  2.00,3.00,4.00,3.00,'Regular'),
(21, 'Ana',          20,'Fisica',      3.00,5.00,2.00,3.00,'Bueno'),
(22, 'Carlos',       20,'Ingenieria',  2.00,4.00,5.00,3.00,'Bueno'),
(23, 'Luis',         23,'Fisica',      3.00,2.00,5.00,3.00,'Bueno'),
(24, 'Ana',          21,'Ingenieria',  3.00,5.00,4.00,4.00,'Bueno'),
(25, 'Carlos',       19,'Matematicas', 4.00,3.00,3.00,3.00,'Regular'),
(26, 'Maria',        18,'Fisica',      3.00,3.00,5.00,3.00,'Bueno'),
(27, 'Carlos',       22,'Matematicas', 3.00,4.00,2.00,3.00,'Regular'),
(28, 'Luis',         21,'Ingenieria',  2.00,3.00,5.00,3.00,'Regular'),
(29, 'Jose',         20,'Matematicas', 4.00,3.00,3.00,3.00,'Regular'),
(30, 'Ana',          19,'Ingenieria',  3.00,2.00,3.00,3.00,'Regular'),
(31, 'Maria',        18,'Ingenieria',  5.00,4.00,4.00,4.00,'Excelente'),
(32, 'Maria',        23,'Fisica',      2.00,3.00,4.00,3.00,'Regular'),
(33, 'Jose',         18,'Matematicas', 5.00,3.00,4.00,4.00,'Bueno'),
(34, 'Ana',          18,'Matematicas', 5.00,2.00,5.00,4.00,'Bueno'),
(35, 'Jose',         20,'Fisica',      2.00,2.00,2.00,2.00,'Deficiente'),
(36, 'Paula',        23,'Fisica',      5.00,5.00,3.00,4.00,'Bueno'),
(37, 'Jose',         18,'Fisica',      4.00,3.00,3.00,3.00,'Bueno'),
(38, 'Ana',          21,'Fisica',      5.00,3.00,5.00,4.00,'Excelente'),
(39, 'Ana',          22,'Ingenieria',  3.00,5.00,2.00,3.00,'Bueno'),
(40, 'Ana',          23,'Fisica',      3.00,2.00,2.00,2.00,'Regular'),
(41, 'Luis',         18,'Fisica',      3.00,3.00,4.00,3.00,'Bueno'),
(42, 'Luis',         23,'Fisica',      3.00,4.00,3.00,3.00,'Bueno'),
(43, 'Ana',          22,'Fisica',      2.00,5.00,3.00,3.00,'Regular'),
(44, 'Maria',        21,'Fisica',      5.00,5.00,4.00,4.00,'Excelente'),
(45, 'Paula',        20,'Matematicas', 2.00,3.00,2.00,2.00,'Deficiente'),
(46, 'Ana',          18,'Fisica',      5.00,2.00,2.00,3.00,'Regular'),
(47, 'Felipe Tellez',23,'Ingenieria',  4.00,4.00,4.00,4.00,'Bueno');

-- ------------------------------------------------------------
--  Tabla: usuarios
-- ------------------------------------------------------------
DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `id`       INT(11)      NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50)  DEFAULT NULL,
  `password` VARCHAR(100) DEFAULT NULL,
  `rol`      VARCHAR(20)  DEFAULT NULL,
  `carrera`  VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `usuarios` (`id`,`username`,`password`,`rol`,`carrera`) VALUES
(1, 'admin',    'aaa',  'administrador', NULL),
(2, 'docente1', 'abcd', 'docente',       'Ingeniería'),
(3, 'docente2', 'abcd', 'docente',       'Administración');

ALTER TABLE `estudiantes` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;
ALTER TABLE `usuarios`    MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
