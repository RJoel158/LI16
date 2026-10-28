-- =============================================================================
-- LABORATORIO LI16 | PUNTO 16g: Adultos (> 25 anos) - Celular vs Web
-- Requerimiento: Comparar interacción móvil vs web en usuarios adultos
-- =============================================================================
USE db_ronald;

SELECT 
    COUNT(*) AS total_adultos,
    SUM(mobile_likes) AS total_likes_celular,
    SUM(www_likes) AS total_likes_web,
    ROUND(AVG(mobile_likes), 2) AS promedio_celular,
    ROUND(AVG(www_likes), 2) AS promedio_web
FROM db_ronald.fb_ronald 
WHERE age > 25;
