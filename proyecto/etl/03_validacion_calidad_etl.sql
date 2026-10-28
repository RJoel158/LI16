-- =============================================================================
-- PIPELINE ETL BIG DATA | FASE 3: AUDITORIA Y CONTROL DE CALIDAD (DATA QUALITY)
-- Reconciliación Bronze ➔ Silver para LI16 y LI17
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================

-- 1. RECONCILIACION LI16: Comparacion de Filas Bronze vs Silver
SELECT 
    'LI16_Facebook' AS dataset,
    (SELECT COUNT(*) FROM db_ronald.fb_ronald) AS filas_bronze_raw,
    (SELECT COUNT(*) FROM db_ronald.fb_ronald_silver) AS filas_silver_curated,
    CASE 
        WHEN (SELECT COUNT(*) FROM db_ronald.fb_ronald) = (SELECT COUNT(*) FROM db_ronald.fb_ronald_silver)
        THEN 'INTEGRIDAD 100% (0 PERDIDAS)' 
        ELSE 'DESCUADRE DETECTADO' 
    END AS estado_auditoria;

-- 2. LI16: Segmentacion de Usuarios por Canal de Preferencia
SELECT 
    canal_preferido,
    COUNT(*) AS total_usuarios,
    ROUND(COUNT(*) * 100.0 / 99003, 2) AS porcentaje
FROM db_ronald.fb_ronald_silver
GROUP BY canal_preferido
ORDER BY total_usuarios DESC;

-- 3. RECONCILIACION LI17: Comparacion de Filas Bronze vs Silver
SELECT 
    'LI17_ECommerce' AS dataset,
    (SELECT COUNT(*) FROM dbec_ronald.tec_ronald) AS filas_bronze_raw,
    (SELECT COUNT(*) FROM dbec_ronald.tec_ronald_silver) AS filas_silver_curated,
    CASE 
        WHEN (SELECT COUNT(*) FROM dbec_ronald.tec_ronald) = (SELECT COUNT(*) FROM dbec_ronald.tec_ronald_silver)
        THEN 'INTEGRIDAD 100% (0 PERDIDAS)' 
        ELSE 'DESCUADRE DETECTADO' 
    END AS estado_auditoria;

-- 4. LI17: Clasificacion de Transacciones (Ventas vs Cancelaciones)
SELECT 
    tipo_transaccion,
    COUNT(*) AS total_lineas,
    ROUND(COUNT(*) * 100.0 / 541910, 2) AS porcentaje_transacciones,
    ROUND(SUM(monto_linea), 2) AS impacto_financiero_total
FROM dbec_ronald.tec_ronald_silver
GROUP BY tipo_transaccion
ORDER BY total_lineas DESC;
