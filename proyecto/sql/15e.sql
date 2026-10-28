-- =============================================================================
-- LABORATORIO LI16 | PUNTO 15e: Carga de Datos desde HDFS a Managed Table
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================
USE db_ronald;

LOAD DATA INPATH '/user/hive/warehouse/pseudo_facebook_ronald.csv' 
INTO TABLE db_ronald.fb_ronald;

SELECT COUNT(*) AS total_filas_cargadas 
FROM db_ronald.fb_ronald;
