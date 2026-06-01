-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para contabilidad2026
CREATE DATABASE IF NOT EXISTS `contabilidad2026` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `contabilidad2026`;

-- Volcando datos para la tabla contabilidad2026.cuenta: ~1 rows (aproximadamente)
INSERT INTO `cuenta` (`idCuenta`, `nombreCuenta`, `descripcion`, `monto`, `idTipoCuenta`, `idInventario`) VALUES
	(2, 'Caja', 'Dinero el cual inician operaciones', 17500.00, 1, 2);

-- Volcando datos para la tabla contabilidad2026.empresa: ~1 rows (aproximadamente)
INSERT INTO `empresa` (`idEmpresa`, `nombreEmpresa`, `nit`, `direccion`, `descripcion`, `idUsuario`) VALUES
	(1, 'Distribuidora Don Bosco', '123456-7', 'Quetzaltenango, Guatemala', 'Distribución de productos electrónicos', 1);

-- Volcando datos para la tabla contabilidad2026.inventario: ~1 rows (aproximadamente)
INSERT INTO `inventario` (`idInventario`, `idEmpresa`) VALUES
	(2, 1);

-- Volcando datos para la tabla contabilidad2026.librodiario: ~0 rows (aproximadamente)

-- Volcando datos para la tabla contabilidad2026.partidas: ~0 rows (aproximadamente)

-- Volcando datos para la tabla contabilidad2026.roles: ~2 rows (aproximadamente)
INSERT INTO `roles` (`idRol`, `rol`, `estado`) VALUES
	(1, 'admin', 1),
	(2, 'usuario', 1),
	(3, 'admin', 1);

-- Volcando datos para la tabla contabilidad2026.tiposcuentas: ~5 rows (aproximadamente)
INSERT INTO `tiposcuentas` (`idTipoCuenta`, `nombreCuenta`) VALUES
	(1, 'Activo Corriente'),
	(2, 'Activo No Corriente'),
	(3, 'Pasivo Corriente'),
	(4, 'Pasivo No Corriente'),
	(5, 'Capital Contable');

-- Volcando datos para la tabla contabilidad2026.usuario: ~0 rows (aproximadamente)
INSERT INTO `usuario` (`idUsuario`, `nombreUsuario`, `pwd`, `estado`, `idRol`) VALUES
	(1, 'admin', 'admin123', 1, 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
