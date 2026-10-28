-- =============================================================================
-- LABORATORIO LI16 | PUNTO 16b: Demografia - Usuarios Mayores a 25 Anios
-- Requerimiento: Cantidad de usuarios con edad estrictamente mayor a 25 años
-- =============================================================================
USE db_ronald;

SELECT 
    COUNT(*) AS usuarios_mayores_25
FROM db_ronald.fb_ronald 
WHERE age > 25;
