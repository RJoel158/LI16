-- =============================================================================
-- LABORATORIO LI16 | PUNTO 16f: Jovenes (13 a 25 anos) - Celular vs Web
-- Requerimiento: Comparar likes dados desde la app móvil vs interfaz de escritorio
-- =============================================================================
USE db_ronald;

SELECT 
    COUNT(*) AS total_jovenes,
    SUM(mobile_likes) AS total_likes_celular,
    SUM(www_likes) AS total_likes_web,
    ROUND(AVG(mobile_likes), 2) AS promedio_celular,
    ROUND(AVG(www_likes), 2) AS promedio_web
FROM db_ronald.fb_ronald 
WHERE age BETWEEN 13 AND 25;
