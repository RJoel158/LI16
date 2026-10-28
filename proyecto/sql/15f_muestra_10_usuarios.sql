-- =============================================================================
-- LABORATORIO LI16 | PUNTO 15f: Muestreo de las Primeras 10 Filas de Datos
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================
USE db_ronald;

SELECT * 
FROM db_ronald.fb_ronald 
LIMIT 10;
