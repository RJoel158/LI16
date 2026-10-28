-- =============================================================================
-- LABORATORIO LI17 | KPI 11: Analisis de Conversion por Dia de la Semana
-- Requerimiento: Identificar el dia con mayor volumen de pedidos e ingresos netos
-- =============================================================================
USE dbec_ronald;

SELECT 
    DAYOFWEEK(InvoiceDate) AS dia_semana, -- 1=Domingo, 7=Sábado
    CASE DAYOFWEEK(InvoiceDate)
        WHEN 1 THEN 'Domingo'
        WHEN 2 THEN 'Lunes'
        WHEN 3 THEN 'Martes'
        WHEN 4 THEN 'Miércoles'
        WHEN 5 THEN 'Jueves'
        WHEN 6 THEN 'Viernes'
        ELSE 'Sábado'
    END AS dia_nombre,
    COUNT(DISTINCT InvoiceNo) AS pedidos,
    ROUND(SUM(Quantity * UnitPrice), 2) AS ingresos
FROM dbec_ronald.tec_ronald
WHERE Quantity > 0 
  AND UnitPrice > 0
GROUP BY DAYOFWEEK(InvoiceDate)
ORDER BY dia_semana ASC;
