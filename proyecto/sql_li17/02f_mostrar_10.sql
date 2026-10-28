-- =============================================================================
-- LABORATORIO LI17 | REQUERIMIENTO 02f: Muestreo de las Primeras 10 Transacciones
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================
USE dbec_ronald;

SELECT * 
FROM dbec_ronald.tec_ronald 
LIMIT 10;
