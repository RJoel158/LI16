-- =============================================================================
-- LABORATORIO LI16 | PUNTO 16d: Comparativa de Popularidad (Likes Recibidos)
-- Requerimiento: Jovenes (13 a 25 anos) vs Adultos mayores a 35 anos
-- =============================================================================
USE db_ronald;

SELECT 
    CASE 
        WHEN age BETWEEN 13 AND 25 THEN '13 a 25'
        ELSE 'mayores de 35'
    END AS grupo_etario,
    COUNT(*) AS usuarios,
    SUM(likes_received) AS total_likes_recibidos,
    ROUND(AVG(likes_received), 2) AS promedio_likes_recibidos
FROM db_ronald.fb_ronald 
WHERE age BETWEEN 13 AND 25 
   OR age > 35 
GROUP BY 
    CASE 
        WHEN age BETWEEN 13 AND 25 THEN '13 a 25'
        ELSE 'mayores de 35'
    END 
ORDER BY grupo_etario;
