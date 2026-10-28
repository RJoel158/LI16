-- =============================================================================
-- LABORATORIO LI17 | REQUERIMIENTO 02e: Ingesta Masiva desde HDFS (541.910 Filas)
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================
USE dbec_ronald;

LOAD DATA INPATH '/datos/data_ronald.csv' 
INTO TABLE dbec_ronald.tec_ronald;

SELECT COUNT(*) AS total_filas_cargadas 
FROM dbec_ronald.tec_ronald;
