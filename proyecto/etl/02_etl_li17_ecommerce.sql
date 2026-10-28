-- =============================================================================
-- PIPELINE ETL BIG DATA | FASE 2: LABORATORIO LI17 (E-COMMERCE 541K)
-- Capa: Bronze (Raw) ➔ Silver (Curated / Enriquecida)
-- Estudiante: Ronald Joel Saavedra Vargas | Clúster: Hadoop 3.4.1 + Hive 4.0.1
-- =============================================================================
USE dbec_ronald;

DROP TABLE IF EXISTS dbec_ronald.tec_ronald_silver;

CREATE TABLE dbec_ronald.tec_ronald_silver AS
SELECT 
    InvoiceNo,
    StockCode,
    TRIM(Description) AS descripcion_limpia,
    Quantity,
    UnitPrice,
    ROUND(Quantity * UnitPrice, 2) AS monto_linea,
    CustomerID,
    CASE 
        WHEN CustomerID IS NULL THEN 'Anonimo' 
        ELSE 'Registrado' 
    END AS tipo_cliente,
    Country,
    InvoiceDate,
    YEAR(InvoiceDate) AS anio,
    MONTH(InvoiceDate) AS mes,
    CASE MONTH(InvoiceDate)
        WHEN 1 THEN 'Enero'
        WHEN 2 THEN 'Febrero'
        WHEN 3 THEN 'Marzo'
        WHEN 4 THEN 'Abril'
        WHEN 5 THEN 'Mayo'
        WHEN 6 THEN 'Junio'
        WHEN 7 THEN 'Julio'
        WHEN 8 THEN 'Agosto'
        WHEN 9 THEN 'Septiembre'
        WHEN 10 THEN 'Octubre'
        WHEN 11 THEN 'Noviembre'
        ELSE 'Diciembre'
    END AS mes_nombre,
    DAYOFWEEK(InvoiceDate) AS dia_semana,
    CASE DAYOFWEEK(InvoiceDate)
        WHEN 1 THEN 'Domingo'
        WHEN 2 THEN 'Lunes'
        WHEN 3 THEN 'Martes'
        WHEN 4 THEN 'Miercoles'
        WHEN 5 THEN 'Jueves'
        WHEN 6 THEN 'Viernes'
        ELSE 'Sabado'
    END AS dia_nombre,
    HOUR(InvoiceDate) AS hora,
    CASE 
        WHEN HOUR(InvoiceDate) BETWEEN 6 AND 11 THEN 'Manana (06-11)'
        WHEN HOUR(InvoiceDate) BETWEEN 12 AND 17 THEN 'Tarde (12-17)'
        WHEN HOUR(InvoiceDate) BETWEEN 18 AND 23 THEN 'Noche (18-23)'
        ELSE 'Madrugada (00-05)'
    END AS franja_horaria,
    CASE 
        WHEN InvoiceNo LIKE 'C%' OR Quantity < 0 THEN 'CANCELACION'
        WHEN UnitPrice <= 0 THEN 'AJUSTE_GRATUITO'
        ELSE 'VENTA_VALIDA'
    END AS tipo_transaccion
FROM dbec_ronald.tec_ronald;
