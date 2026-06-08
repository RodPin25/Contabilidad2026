-- Crear base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Contabilidad2026')
    CREATE DATABASE Contabilidad2026;
GO

USE Contabilidad2026;
GO

CREATE TABLE ROLES (
    idRol INT IDENTITY(1,1) PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    estado INT NOT NULL
);

CREATE TABLE EMPRESA (
    idEmpresa INT IDENTITY(1,1) PRIMARY KEY,
    nombreEmpresa VARCHAR(100) NOT NULL,
    nit VARCHAR(20) NOT NULL,
    descripcion VARCHAR(255),
    direccion VARCHAR(255)
);

CREATE TABLE USUARIO (
    idusuario INT IDENTITY(1,1) PRIMARY KEY,
    nombreUsuario VARCHAR(100) NOT NULL,
    pwd VARCHAR(255) NOT NULL,
    estado INT NOT NULL,
    idEmpresa INT NOT NULL,
    idRol INT NOT NULL,
    FOREIGN KEY (idEmpresa) REFERENCES EMPRESA(idEmpresa),
    FOREIGN KEY (idRol) REFERENCES ROLES(idRol)
);

CREATE TABLE TIPOSCUENTAS (
    idTipoCuenta INT IDENTITY(1,1) PRIMARY KEY,
    nombreCuenta VARCHAR(100) NOT NULL
);

CREATE TABLE INVENTARIO (
    idInventario INT IDENTITY(1,1) PRIMARY KEY,
    idEmpresa INT NOT NULL,
    FOREIGN KEY (idEmpresa) REFERENCES EMPRESA(idEmpresa)
);

CREATE TABLE CUENTA (
    idcuenta INT IDENTITY(1,1) PRIMARY KEY,
    nombreCuenta VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    monto DECIMAL(18,2) NOT NULL,
    idTipoCuenta INT NOT NULL,
    FOREIGN KEY (idTipoCuenta) REFERENCES TIPOSCUENTAS(idTipoCuenta)
);

-- Tabla intermedia (He renombrado las tablas para evitar el conflicto de nombre "CONTIENE")
CREATE TABLE INVENTARIO_CONTIENE_CUENTA (
    idInventario INT NOT NULL,
    idcuenta INT NOT NULL,
    PRIMARY KEY (idInventario, idcuenta),
    FOREIGN KEY (idInventario) REFERENCES INVENTARIO(idInventario),
    FOREIGN KEY (idcuenta) REFERENCES CUENTA(idcuenta)
);

CREATE TABLE LIBRODIARIO (
    idLibroDiario INT IDENTITY(1,1) PRIMARY KEY,
    mes INT NOT NULL,
    year INT NOT NULL,
    idEmpresa INT NOT NULL,
    FOREIGN KEY (idEmpresa) REFERENCES EMPRESA(idEmpresa)
);

CREATE TABLE PARTIDAS (
    idPartida INT IDENTITY(1,1) PRIMARY KEY,
    fechaPartida DATETIME NOT NULL,
    noPartida INT NOT NULL,
    descripcionPartida VARCHAR(255),
    idLibroDiario INT NOT NULL,
    FOREIGN KEY (idLibroDiario) REFERENCES LIBRODIARIO(idLibroDiario)
);

CREATE TABLE PARTIDA_CONTIENE_CUENTA (
    idPartida INT NOT NULL,
    idcuenta INT NOT NULL,
    PRIMARY KEY (idPartida, idcuenta),
    FOREIGN KEY (idPartida) REFERENCES PARTIDAS(idPartida),
    FOREIGN KEY (idcuenta) REFERENCES CUENTA(idcuenta)
);