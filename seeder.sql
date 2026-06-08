USE Contabilidad2026;
GO

-- Insertar roles
INSERT INTO ROLES (rol, estado) VALUES ('admin', 1), ('usuario', 1);

-- Insertar empresa inicial
INSERT INTO EMPRESA (nombreEmpresa, nit, descripcion, direccion) 
VALUES ('Distribuidora Don Bosco', '123456-7', 'Distribución electrónica', 'Quetzaltenango');

-- Insertar tipos de cuenta
INSERT INTO TIPOSCUENTAS (nombreCuenta) 
VALUES ('Activo Corriente'), ('Activo No Corriente'), ('Pasivo'), ('Capital');

-- Insertar usuario admin (puedes cambiar 'admin123' por un hash si prefieres)
INSERT INTO USUARIO (nombreUsuario, pwd, estado, idEmpresa, idRol) 
VALUES ('admin', 'admin123', 1, 1, 1);
GO