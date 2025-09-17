

CREATE TABLE tipo_suelo (
  id_tipo_suelo SERIAL PRIMARY KEY,
  nombre_tipo_suelo VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE sistema_riego (
  id_sistema_riego SERIAL PRIMARY KEY,
  nombre_sistema_riego VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE tipo_sensor (
  id_tipo_sensor SERIAL PRIMARY KEY,
  nombre_tipo_sensor VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE finca (
  id_finca SERIAL PRIMARY KEY,
  nombre_finca   VARCHAR(120) NOT NULL,
  region         VARCHAR(80)  NOT NULL,
  es_organico    BOOLEAN NOT NULL DEFAULT false,
  id_tipo_suelo  INT NOT NULL REFERENCES tipo_suelo(id_tipo_suelo)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  id_sistema_riego INT NOT NULL REFERENCES sistema_riego(id_sistema_riego)
    ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE tecnico (
  id_tecnico SERIAL PRIMARY KEY,
  nombre_tecnico VARCHAR(120) NOT NULL
);

CREATE TABLE cultivo (
  id_cultivo SERIAL PRIMARY KEY,
  tipo_cultivo VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE variedad_cultivo (
  id_variedad SERIAL PRIMARY KEY,
  nombre_variedad VARCHAR(120) NOT NULL,
  id_cultivo INT NOT NULL REFERENCES cultivo(id_cultivo)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  CONSTRAINT uq_variedad_por_cultivo UNIQUE (id_cultivo, nombre_variedad)
);

CREATE TABLE sensor (
  id_sensor VARCHAR(50) PRIMARY KEY,
  estado_sensor VARCHAR(40) NOT NULL,
  fecha_mantenimiento DATE,
  id_finca INT NOT NULL REFERENCES finca(id_finca)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  id_tipo_sensor INT NOT NULL REFERENCES tipo_sensor(id_tipo_sensor)
    ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE medicion (
  id_medicion BIGSERIAL PRIMARY KEY,
  id_sensor VARCHAR(50) NOT NULL REFERENCES sensor(id_sensor)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  valor NUMERIC(12,3) NOT NULL CHECK (valor >= 0),
  fecha_hora TIMESTAMP NOT NULL,
  CONSTRAINT ix_medicion_sensor_fecha UNIQUE (id_sensor, fecha_hora)
);

CREATE TABLE finca_cultivo (
  id_finca_cultivo BIGSERIAL PRIMARY KEY,
  id_finca INT NOT NULL REFERENCES finca(id_finca)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  id_variedad INT NOT NULL REFERENCES variedad_cultivo(id_variedad)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  produccion_toneladas NUMERIC(12,3) NOT NULL DEFAULT 0 CHECK (produccion_toneladas >= 0),
  CONSTRAINT uq_fc_finca_variedad UNIQUE (id_finca, id_variedad)
);

CREATE TABLE asignacion_tecnico (
  id_asignacion BIGSERIAL PRIMARY KEY,
  id_finca   INT NOT NULL REFERENCES finca(id_finca)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  id_tecnico INT NOT NULL REFERENCES tecnico(id_tecnico)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE,
  CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

CREATE TABLE fertilizacion (
  id_fertilizacion BIGSERIAL PRIMARY KEY,
  id_finca INT NOT NULL REFERENCES finca(id_finca)
    ON UPDATE RESTRICT ON DELETE RESTRICT,
  fertilizante_usado VARCHAR(120) NOT NULL,
  fecha_aplicacion DATE
);