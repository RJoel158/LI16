-- =============================================================================
-- LABORATORIO LI16: Auditoria y Validacion de Integridad de Datos
-- Requerimiento: Confirmar la ingesta íntegra de 99.003 filas y rango de edades
-- =============================================================================
USE db_ronald;

SELECT 
    COUNT(*) AS filas_totales,
    COUNT(DISTINCT userid) AS usuarios_unicos,
    MIN(age) AS edad_minima,
    MAX(age) AS edad_maxima
FROM db_ronald.fb_ronald;
