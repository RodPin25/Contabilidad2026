CREATE DATABASE IF NOT EXISTS contabilidad2026
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

USE contabilidad2026;

CREATE TABLE IF NOT EXISTS Roles (
    idRol INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    estado TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Usuario (
    idUsuario INT AUTO_INCREMENT PRIMARY KEY,
    nombreUsuario VARCHAR(100) NOT NULL UNIQUE,
    pwd VARCHAR(255) NOT NULL,
    estado TINYINT(1) NOT NULL DEFAULT 1,
    idRol INT NOT NULL,
    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (idRol) REFERENCES Roles(idRol)
);

CREATE TABLE IF NOT EXISTS Empresa (
    idEmpresa INT AUTO_INCREMENT PRIMARY KEY,
    nombreEmpresa VARCHAR(150) NOT NULL,
    nit VARCHAR(30),
    direccion VARCHAR(255),
    descripcion VARCHAR(255),
    idUsuario INT NOT NULL,
    CONSTRAINT fk_empresa_usuario
        FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario)
);

CREATE TABLE IF NOT EXISTS Inventario (
    idInventario INT AUTO_INCREMENT PRIMARY KEY,
    idEmpresa INT NOT NULL,
    CONSTRAINT fk_inventario_empresa
        FOREIGN KEY (idEmpresa) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE IF NOT EXISTS TiposCuentas (
    idTipoCuenta INT PRIMARY KEY,
    nombreCuenta VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Cuenta (
    idCuenta INT AUTO_INCREMENT PRIMARY KEY,
    nombreCuenta VARCHAR(150) NOT NULL,
    descripcion VARCHAR(255),
    monto DECIMAL(15, 2) NOT NULL DEFAULT 0,
    idTipoCuenta INT NOT NULL,
    idInventario INT NOT NULL,
    CONSTRAINT fk_cuenta_tipo
        FOREIGN KEY (idTipoCuenta) REFERENCES TiposCuentas(idTipoCuenta),
    CONSTRAINT fk_cuenta_inventario
        FOREIGN KEY (idInventario) REFERENCES Inventario(idInventario)
);

CREATE TABLE IF NOT EXISTS LibroDiario (
    idLibroDiario INT AUTO_INCREMENT PRIMARY KEY,
    mes TINYINT UNSIGNED NOT NULL,
    year SMALLINT UNSIGNED NOT NULL,
    idEmpresa INT NOT NULL,
    CONSTRAINT uq_libro_diario_periodo UNIQUE (mes, year, idEmpresa),
    CONSTRAINT fk_libro_diario_empresa
        FOREIGN KEY (idEmpresa) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE IF NOT EXISTS Partidas (
    idPartida INT AUTO_INCREMENT PRIMARY KEY,
    noPartida INT NOT NULL,
    descripcionPartida VARCHAR(255) NOT NULL,
    fechaPartida DATE NOT NULL,
    idLibroDiario INT NOT NULL,
    CONSTRAINT uq_partida_libro UNIQUE (noPartida, idLibroDiario),
    CONSTRAINT fk_partida_libro_diario
        FOREIGN KEY (idLibroDiario) REFERENCES LibroDiario(idLibroDiario)
);

CREATE TABLE IF NOT EXISTS AsientoDiario (
    idAsiento INT AUTO_INCREMENT PRIMARY KEY,
    idPartida INT NOT NULL,
    idCuenta INT NOT NULL,
    debe DECIMAL(15, 2) NOT NULL DEFAULT 0,
    haber DECIMAL(15, 2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_asiento_partida
        FOREIGN KEY (idPartida) REFERENCES Partidas(idPartida),
    CONSTRAINT fk_asiento_cuenta
        FOREIGN KEY (idCuenta) REFERENCES Cuenta(idCuenta),
    CONSTRAINT chk_asiento_montos CHECK (debe >= 0 AND haber >= 0)
);

INSERT IGNORE INTO Roles (idRol, rol, estado)
VALUES (1, 'admin', 1);

INSERT IGNORE INTO Usuario (idUsuario, nombreUsuario, pwd, estado, idRol)
VALUES (1, 'admin', 'admin123', 1, 1);

INSERT IGNORE INTO Empresa (
    idEmpresa, nombreEmpresa, nit, direccion, descripcion, idUsuario
) VALUES (
    1,
    'Distribuidora Don Bosco',
    '123456-7',
    'Quetzaltenango, Guatemala',
    'Distribucion de productos electronicos',
    1
);

INSERT IGNORE INTO Inventario (idInventario, idEmpresa)
VALUES (2, 1);

INSERT IGNORE INTO TiposCuentas (idTipoCuenta, nombreCuenta) VALUES
    (1, 'Activo Corriente'),
    (2, 'Activo No Corriente'),
    (3, 'Pasivo Corriente'),
    (4, 'Pasivo No Corriente'),
    (5, 'Capital Contable');

INSERT IGNORE INTO Cuenta (
    idCuenta, nombreCuenta, descripcion, monto, idTipoCuenta, idInventario
) VALUES
    (2, 'Caja', 'Efectivo disponible', 17500.00, 1, 2),
    (5, 'Capital Contable', 'Aportes de propietarios', 0.00, 5, 2),
    (6, 'Ventas', 'Ingresos por ventas', 0.00, 5, 2),
    (7, 'IVA Debito Fiscal', 'IVA generado en ventas', 0.00, 3, 2),
    (8, 'IVA Credito Fiscal', 'IVA pagado en compras', 0.00, 1, 2),
    (10, 'Gastos Generales', 'Gastos operativos', 0.00, 1, 2);

INSERT IGNORE INTO LibroDiario (idLibroDiario, mes, year, idEmpresa)
VALUES (1, 6, 2026, 1);

INSERT IGNORE INTO Partidas (
    idPartida, noPartida, descripcionPartida, fechaPartida, idLibroDiario
) VALUES
    (1, 1, 'Partida de apertura', '2026-06-01', 1),
    (2, 2, 'Compra de suministros al contado', '2026-06-02', 1);

INSERT IGNORE INTO AsientoDiario (
    idAsiento, idPartida, idCuenta, debe, haber
) VALUES
    (1, 1, 2, 17500.00, 0.00),
    (2, 1, 5, 0.00, 17500.00),
    (3, 2, 10, 1000.00, 0.00),
    (4, 2, 8, 120.00, 0.00),
    (5, 2, 2, 0.00, 1120.00);
