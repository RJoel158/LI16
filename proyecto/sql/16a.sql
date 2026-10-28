-- =============================================================================
-- LABORATORIO LI16 | PUNTO 16a: Total de Usuarios y Verificacion de Unicidad
-- Requerimiento: Total de usuarios en la red social y confirmar clave primaria única
-- =============================================================================
USE db_ronald;

SELECT 
    COUNT(*) AS total_usuarios,
    COUNT(DISTINCT userid) AS usuarios_distintos
FROM db_ronald.fb_ronald;
