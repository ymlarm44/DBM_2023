-- Database: produccion_hc

-- DROP DATABASE IF EXISTS produccion_hc;

CREATE DATABASE produccion_hc
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Table: public.empresas

-- DROP TABLE IF EXISTS public.empresas;

CREATE TABLE IF NOT EXISTS public.empresas
(
    id SERIAL PRIMARY KEY,
    nombre character varying(50) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.empresas
    OWNER to postgres;

-- Table: public.extraccion

-- DROP TABLE IF EXISTS public.extraccion;

CREATE TABLE IF NOT EXISTS public.extraccion
(
    id SERIAL PRIMARY KEY,
    tipo_extraccion character varying(20) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.extraccion
    OWNER to postgres;

-- Table: public.pozos

-- DROP TABLE IF EXISTS public.pozos;

CREATE TABLE IF NOT EXISTS public.pozos
(
    id SERIAL PRIMARY KEY,
    coordenada_x double precision,
    coordenada_y double precision
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.pozos
    OWNER to postgres;

-- Table: public.provincias

-- DROP TABLE IF EXISTS public.provincias;

CREATE TABLE IF NOT EXISTS public.provincias
(
    id SERIAL PRIMARY KEY,
    nombre character varying(20) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.provincias
    OWNER to postgres;

-- Table: public.tiempo

-- DROP TABLE IF EXISTS public.tiempo;

CREATE TABLE IF NOT EXISTS public.tiempo
(
    id SERIAL PRIMARY KEY,
    anio smallint,
    mes smallint,
    nombre_mes character varying(10) COLLATE pg_catalog."default",
    trimestre integer,
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tiempo
    OWNER to postgres;

-- Table: public.produccion

-- DROP TABLE IF EXISTS public.produccion;

CREATE TABLE IF NOT EXISTS public.produccion
(
    id SERIAL PRIMARY KEY,
    fecha integer,
    empresa integer,
    pozo integer,
    provincia integer,
    extraccion integer,
    produccion_petroleo_mes double precision,
    produccion_gas_mes double precision,
    CONSTRAINT produccion_empresa_fkey FOREIGN KEY (empresa)
        REFERENCES public.empresas (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT produccion_extraccion_fkey FOREIGN KEY (extraccion)
        REFERENCES public.extraccion (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT produccion_fecha_fkey FOREIGN KEY (fecha)
        REFERENCES public.tiempo (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT produccion_pozo_fkey FOREIGN KEY (pozo)
        REFERENCES public.pozos (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT produccion_provincia_fkey FOREIGN KEY (provincia)
        REFERENCES public.provincias (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.produccion
    OWNER to postgres;