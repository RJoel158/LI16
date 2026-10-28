-- =============================================================================
-- PIPELINE ETL BIG DATA | FASE 1: LABORATORIO LI16 (FACEBOOK 99K)
-- Capa: Bronze (Raw) ➔ Silver (Curated / Enriquecida)
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================
USE db_ronald;

DROP TABLE IF EXISTS db_ronald.fb_ronald_silver;

CREATE TABLE db_ronald.fb_ronald_silver AS
SELECT 
    userid,
    age,
    CASE 
        WHEN age < 18 THEN 'Adolescentes (<18)'
        WHEN age BETWEEN 18 AND 25 THEN 'Jovenes (18-25)'
        WHEN age BETWEEN 26 AND 35 THEN 'Adultos Jovenes (26-35)'
        WHEN age BETWEEN 36 AND 50 THEN 'Adultos (36-50)'
        ELSE 'Senior (>50)'
    END AS segmento_etario,
    CASE 
        WHEN gender = 'male' THEN 'Masculino'
        WHEN gender = 'female' THEN 'Femenino'
        ELSE 'No Reportado'
    END AS genero_estandar,
    tenure,
    ROUND(tenure / 365.25, 2) AS antiguedad_anios,
    friend_count,
    friendships_initiated,
    likes,
    likes_received,
    mobile_likes,
    www_likes,
    CASE 
        WHEN mobile_likes > 0 AND www_likes = 0 THEN 'Exclusivo Celular'
        WHEN www_likes > 0 AND mobile_likes = 0 THEN 'Exclusivo Web'
        WHEN mobile_likes > 0 AND www_likes > 0 THEN 'Omnicanal (Ambos)'
        ELSE 'Sin Actividad Likes'
    END AS canal_preferido,
    ROUND(mobile_likes * 100.0 / NULLIF(likes, 0), 2) AS ratio_movil_pct,
    (friend_count + likes + likes_received) AS score_engagement,
    dob_day,
    dob_month,
    dob_year
FROM db_ronald.fb_ronald;
