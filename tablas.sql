-- Tabla Paises
CREATE TABLE paises (
    pais_id INT AUTO_INCREMENT PRIMARY KEY,
    pais_nombre VARCHAR(50) NOT NULL
);

-- Tabla Ciudades
CREATE TABLE ciudades (
    ciud_id INT AUTO_INCREMENT PRIMARY KEY,
    ciud_pais_id INT,
    ciud_nombre VARCHAR(50) NOT NULL,
    CONSTRAINT fk_ciudad_pais FOREIGN KEY (ciud_pais_id) REFERENCES paises(pais_id)
);

-- Tabla Localizaciones
CREATE TABLE localizaciones (
    localiz_id INT AUTO_INCREMENT PRIMARY KEY,
    localiz_ciudad_id INT NOT NULL,
    localiz_direccion VARCHAR(255),
    CONSTRAINT fk_localiz_ciudad FOREIGN KEY (localiz_ciudad_id) REFERENCES ciudades(ciud_id)
);

-- Tabla Departamentos
CREATE TABLE departamentos (
    dpto_id INT AUTO_INCREMENT PRIMARY KEY,
    depto_nombre VARCHAR(255) NOT NULL
);

-- Tabla Cargos
CREATE TABLE cargos (
    cargo_id INT AUTO_INCREMENT PRIMARY KEY,
    cargo_nombre VARCHAR(250) NOT NULL,
    cargo_sueldo_minimo DECIMAL(10, 2) NOT NULL,
    cargo_sueldo_maximo DECIMAL(10, 2) NOT NULL
);

-- Tabla Empleados
CREATE TABLE empleados (
    empl_id INT AUTO_INCREMENT PRIMARY KEY,
    empl_primer_nombre VARCHAR(50) NOT NULL,
    empl_segundo_nombre VARCHAR(50),
    empl_email VARCHAR(100) NOT NULL,
    empl_fecha_nac DATE NOT NULL,
    empl_sueldo DECIMAL(10, 2) NOT NULL,
    empl_comision DECIMAL(10, 2),
    empl_direccion VARCHAR(255),
    empl_ciudad VARCHAR(255),
    empl_cargo_id INT,
    empl_gerente_id INT,
    empl_dpto_id INT,
    CONSTRAINT fk_empleado_cargo FOREIGN KEY (empl_cargo_id) REFERENCES cargos(cargo_id),
    CONSTRAINT fk_empleado_gerente FOREIGN KEY (empl_gerente_id) REFERENCES empleados(empl_id),
    CONSTRAINT fk_empleado_dpto FOREIGN KEY (empl_dpto_id) REFERENCES departamentos(dpto_id)
);

-- Tabla Histórico
CREATE TABLE historico (
    emphist_id INT AUTO_INCREMENT PRIMARY KEY,
    emphist_fecha_retiro DATE,
    emphist_cargo_id INT,
    emphist_dpto_id INT,
    CONSTRAINT fk_historico_cargo FOREIGN KEY (emphist_cargo_id) REFERENCES cargos(cargo_id),
    CONSTRAINT fk_historico_dpto FOREIGN KEY (emphist_dpto_id) REFERENCES departamentos(dpto_id)
);