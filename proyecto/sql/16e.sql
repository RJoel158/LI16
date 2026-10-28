-- =============================================================================
-- LABORATORIO LI16 | PUNTO 16e: Estacionalidad y Cumpleanos por Mes
-- Requerimiento: Total de usuarios nacidos en cada mes del año (1 a 12)
-- =============================================================================
USE db_ronald;

SELECT 
    dob_month AS mes_cumpleanios,
    COUNT(*) AS total_usuarios
FROM db_ronald.fb_ronald 
GROUP BY dob_month 
ORDER BY dob_month ASC;
