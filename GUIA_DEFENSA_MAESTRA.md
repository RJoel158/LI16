# GUÍA MAESTRA DE DEFENSA TÉCNICA UNIFICADA — LABORATORIOS LI16 Y LI17
**Materia:** Tecnologías Emergentes I  
**Estudiante:** Ronald Joel Saavedra Vargas  
**Universidad:** Universidad Privada del Valle (Univalle Bolivia)  
**Clúster:** Apache Hadoop 3.4.1 + Apache Hive 4.0.1 sobre Docker Compose  
**Datasets Coexistentes:**  
- **LI16:** 99.003 usuarios de redes sociales (`pseudo_facebook_ronald.csv`, 12.8 MB, base `db_ronald.fb_ronald`)
- **LI17:** 541.910 transacciones comerciales de retail (`data_ronald.csv`, 45.5 MB, base `dbec_ronald.tec_ronald`)

---

## 1. Protocolo de Preparación (5 Minutos Antes de la Defensa)

Antes de iniciar tu evaluación ante el docente, realiza este checklist preventivo:

1. **Abre Docker Desktop** y asegúrate de que el motor esté en verde (*Engine Running*).
2. **Inicia la Consola Maestra de Defensa**:
   - Haz doble clic en `iniciar_asistente.bat` (o ejecuta `.\menu_evidencias.ps1` en PowerShell).
3. **Ejecuta la opción `diag`**:
   - Esto verificará automáticamente los 4 contenedores (`Up`), HiveServer2 libre de PID fantasma, NameNode fuera de *SafeMode*, y validará que `db_ronald` cuente 99.003 filas y `dbec_ronald` cuente 541.910 filas en vivo.
4. **Ten abiertas en segundo plano las siguientes pestañas del navegador**:
   - Interfaz Web HDFS: `http://localhost:9870/dfshealth.html`
   - Explorador de Archivos HDFS: `http://localhost:9870/explorer.html#/user/hive/warehouse/`
   - Repositorio GitHub: `https://github.com/RJoel158/LI16`
   - Informes formales en PDF: `informe/Informe_LI16_Ronald_Saavedra.pdf` e `informe/Informe_LI17_Ronald_Saavedra.pdf`.

---

## 2. Speech de Apertura Unificado (60 a 90 Segundos)

> *"Buenos días / tardes docente. Para los laboratorios LI16 y LI17 implementé una arquitectura analítica desacoplada de Big Data basada en Apache Hadoop 3.4.1 y Apache Hive 4.0.1 sobre Docker Compose.*  
> *A diferencia de los entornos legados tradicionales de Big Data Europe —que utilizan imágenes monolíticas desactualizadas de Hadoop 2.x—, esta implementación divide las responsabilidades en cuatro microservicios especializados:*  
> *1. Un **Hadoop NameNode** para la gobernanza del árbol de metadatos de HDFS y su Web UI en el puerto 9870.*  
> *2. Un **Hadoop DataNode** para el almacenamiento físico distribuido de los bloques de datos.*  
> *3. Un **Hive Metastore** que expone el catálogo relacional mediante Thrift RPC en el puerto 9083, persistiendo los esquemas en Apache Derby con volúmenes de Docker.*  
> *4. Y un **HiveServer2** que atiende conexiones remotas JDBC en el puerto 10000 mediante el cliente estándar Beeline, compilando consultas HiveQL a trabajos MapReduce.*  
> 
> *Sobre esta infraestructura demostramos la capacidad multi-tenant y de escalabilidad sin reiniciar servicios:*  
> *- En **LI16** gobernamos 99.003 usuarios de redes sociales en la base `db_ronald`, analizando demografía, cohortes generacionales y adopción tecnológica móvil vs web.*  
> *- En **LI17** escalamos a 541.910 transacciones reales de comercio electrónico en la base `dbec_ronald`, calculando 12 KPIs comerciales de facturación (£8.7M válidos), productos líderes, ticket promedio, estacionalidad con Window Functions y tasas de cancelación por país."*

---

## 3. Matriz Arquitectural del Clúster Desacoplado

```
       +--------------------------------------------------------------------+
       |                         HOST (WINDOWS 11)                          |
       |                                                                    |
       |     Navegador Web                 Consola Maestra / Cliente SQL    |
       |     http://localhost:9870         Beeline JDBC (:10000)            |
       +-----------------+------------------------------+-------------------+
                         |                              |
                         | 127.0.0.1:9870               | 127.0.0.1:10000
                         v                              v
       +--------------------------------+ +---------------------------------+
       |     li16-ronald-namenode-1     | |    li16-ronald-hive-server-1    |
       |        (Hadoop NameNode)       | |          (HiveServer2)          |
       |                                | |                                 |
       |  - Árbol de inodos de HDFS     | |  - Motor HiveQL / MapReduce     |
       |  - Puerto Web UI: 9870         | |  - Puerto JDBC: 10000           |
       |  - Puerto RPC: 9000 (interno)  | |  - Web UI Status: 10002         |
       |  - Volumen: namenode:/data     | |                                 |
       +-----------------+--------------+ +-----------------+---------------+
                         |                                  |
           Red Interna   |                    Thrift RPC    |
             Bridge      |                    Puerto 9083   |
                         v                                  v
       +--------------------------------+ +---------------------------------+
       |     li16-ronald-datanode-1     | |   li16-ronald-hive-metastore-1  |
       |        (Hadoop DataNode)       | |         (Hive Metastore)        |
       |                                | |                                 |
       |  - Bloques físicos distribuidos| |  - Catálogo de tablas y tipos   |
       |  - Puertos int.: 9864 / 9866   | |  - Apache Derby en volumen      |
       |  - Volumen: datanode:/data     | |  - Volumen: metastore:/data     |
       +--------------------------------+ +---------------------------------+
```

### Principio de Coexistencia Multi-Tenant:
En el mismo sistema de archivos HDFS conviven las dos bases de datos:
- `/user/hive/warehouse/db_ronald.db/fb_ronald/` (Datos de redes sociales de LI16)
- `/user/hive/warehouse/dbec_ronald.db/tec_ronald/` (Datos transaccionales de LI17)
Ambas son gestionadas por el mismo metastore y procesadas por el mismo HiveServer2 sin colisión de nombres ni interferencia de recursos.

---

## 4. Guía Paso a Paso: Walkthrough de Inicio a Fin (47 Requerimientos)

La Consola Maestra (`menu_evidencias.ps1`) incluye el comando **`walkthrough`**, que recorre los dos laboratorios de manera secuencial. A continuación se resume la ficha técnica de cada paso:

### FASE 1: INFRAESTRUCTURA Y DOCKER (LI16)
- **Paso 01 (`01`): Contenedores existentes.** `docker ps -a`.  
  *Por qué:* Validar higiene de puertos (9870, 10000) y evitar colisiones de bind.  
  *Pregunta:* ¿Qué error da Docker si el puerto 9870 está ocupado? *Respuesta:* `bind: address already in use`.
- **Paso 02 (`02`): Repositorio propio.** `git log -3 --oneline`.  
  *Por qué:* Arquitectura desacoplada propia con Hadoop 3.4.1 y Hive 4.0.1 oficiales vs imágenes de 2017 de BDE.  
  *Pregunta:* ¿Por qué no BDE? *Respuesta:* BDE quedó congelado en Hadoop 2.7 y carece de soporte para Hive 4 y Java moderno.
- **Paso 03 (`03`): Docker Compose ps.** `docker compose -f proyecto/compose.yaml ps`.  
  *Por qué:* Orquestación declarativa, red bridge y volúmenes persistentes.
- **Paso 04 (`04`): Contenedores activos.** `docker ps`.  
  *Por qué:* Comprobar que los 4 nodos están `Up` con sus puertos mapeados.
- **Paso 05 (`05`): Consumo de recursos.** `docker stats --no-stream`.  
  *Por qué:* Análisis de consumo de memoria JVM: HiveServer2 (~1.2 GB) y Metastore son los mayores consumidores.

### FASE 2: ARQUITECTURA HDFS Y NAMENODE (LI16)
- **Paso 06 (`06`): Shell del NameNode.** `docker exec li16-ronald-namenode-1 bash ...`  
  *Por qué:* Comprobar entorno Linux Debian y binarios de Hadoop en `/opt/hadoop`.
- **Paso 07 (`07`): Warehouse inicial.** `docker exec li16-ronald-namenode-1 hdfs dfs -ls /user/hive/warehouse/`.  
  *Por qué:* Raíz analítica gobernada por Hive en HDFS.
- **Paso 08 (`08`): NameNode Web UI (:9870).** Abre navegador en `http://localhost:9870`.  
  *Por qué:* Comprobar métricas del clúster: SafeMode OFF, DataNodes vivos, capacidad configurada.  
  *Pregunta:* ¿Por qué puerto 9870 y no 50070? *Respuesta:* Hadoop 3.x reasignó los puertos por defecto para evitar colisiones.
- **Paso 09 (`09`): HDFS Explorer.** Abre `http://localhost:9870/explorer.html#/user/hive/warehouse/`.  
  *Por qué:* Exploración visual de inodos, réplicas y permisos.

### FASE 3: INGESTA Y DATASET DEMOGRÁFICO (LI16)
- **Paso 10 (`10`): Dataset local.** Inspección de `pseudo_facebook_ronald.csv` (12.8 MB, 99.003 filas) con SHA-256.  
  *Por qué:* Integridad de datos antes del procesamiento.
- **Paso 11 (`11`): Depuración de cabecera.** Verificación de datos puros en línea 1 (sin cabecera de texto).  
  *Por qué:* Evitar que la cabecera contamine los tipos `BIGINT` e `INT` en Hive.
- **Paso 12 (`12`): Staging en NameNode.** `docker exec li16-ronald-namenode-1 ls -lh /tmp/pseudo_facebook_ronald.csv`.  
  *Por qué:* Patrón de dos etapas (Host -> Contenedor /tmp/ -> HDFS).
- **Paso 13 (`13`): Ingesta distribuida a HDFS.** `hdfs dfs -ls -R /user/hive/warehouse/db_ronald.db/`.  
  *Por qué:* División física del archivo en bloques gobernados por el DataNode.

### FASE 4: CATÁLOGO Y TABLAS EN HIVE (LI16)
- **Paso 14 (`14`): Shell de HiveServer2.** `docker exec li16-ronald-hive-server-1 ...`  
  *Por qué:* Validar la versión oficial Apache Hive 4.0.1.
- **Paso 15a (`15a`): Creación de base de datos.** `CREATE DATABASE IF NOT EXISTS db_ronald; SHOW DATABASES;`.  
  *Por qué:* Namespace aislado y creación de carpeta `db_ronald.db` en HDFS.
- **Paso 15b (`15b`): Mapeo de columnas y tipos.** `DESCRIBE db_ronald.fb_ronald;`.  
  *Por qué:* Schema-on-Read: `userid(BIGINT)`, `age(INT)`, `gender(STRING)`, `friend_count(INT)`, `likes(BIGINT)`.
- **Paso 15c (`15c`): Creación de tabla `fb_ronald`.** `SHOW TABLES IN db_ronald;`.  
  *Por qué:* DDL con `ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE`.
- **Paso 15d (`15d`): Location HDFS.** `DESCRIBE FORMATTED db_ronald.fb_ronald;` (Location & Table Type).  
  *Por qué:* Confirmar que es `MANAGED_TABLE` ubicada en `/user/hive/warehouse/db_ronald.db/fb_ronald`.  
  *Pregunta:* ¿Qué pasa si hago `DROP TABLE`? *Respuesta:* Se borra la metadata en Derby Y el archivo físico en HDFS.
- **Paso 15e (`15e`): Validación masiva.** `SELECT COUNT(*) FROM db_ronald.fb_ronald;` -> **99.003 filas**.  
  *Por qué:* Coincidencia exacta 1:1 con las líneas del CSV original.
- **Paso 15f (`15f`): Muestreo de datos.** `SELECT * FROM db_ronald.fb_ronald LIMIT 10;`.  
  *Por qué:* Fetch Task directo sin MapReduce para verificar que las columnas no estén desfasadas.

### FASE 5: CONSULTAS ANALÍTICAS HIVEQL (LI16)
- **Paso 16a (`16a`): Total y unicidad.** `COUNT(*)` = 99.003 y `COUNT(DISTINCT userid)` = 99.003.  
  *Interpretación:* Cero duplicados; cada fila es un usuario único.
- **Paso 16b (`16b`): Segmento > 25 años.** 73.047 usuarios (**73.78%** del total).  
  *Interpretación:* Tres de cada cuatro usuarios son adultos; plataforma madura.
- **Paso 16c (`16c`): Amigos por género.** Mujeres: **241.97** amigos vs Hombres: **165.43** amigos.  
  *Interpretación:* Las mujeres tienen en promedio **+76.54 amigos más** (+46% de sociabilidad en red).
- **Paso 16d (`16d`): Likes por cohorte.** Jóvenes (13-25) promedian **~267.4** likes vs Adultos (>35) **~67.1** likes.  
  *Interpretación:* Los jóvenes reciben **4 veces más likes**, demostrando mayor necesidad de validación social.
- **Paso 16e (`16e`): Cumpleaños por mes.** Enero se dispara a **11.833** usuarios vs ~7.900 en los demás meses.  
  *Interpretación:* Sesgo de fecha por defecto (`01/01`) cuando el usuario no desea ingresar su fecha de nacimiento real.
- **Paso 16f (`16f`): Jóvenes: ¿Celular o Computadora?** >**83.2%** de los likes otorgados son móviles.  
  *Interpretación:* Generación Mobile-First absoluta; el uso web es residual.
- **Paso 16g (`16g`): Adultos: ¿Celular o Computadora?** Celular lidera (**68.5%**), pero web sube a **31.5%**.  
  *Interpretación:* En adultos el uso de computadora de escritorio se duplica por el entorno laboral de oficina.

---

### TRANSICIÓN ARQUITECTURAL: ESCALAMIENTO A E-COMMERCE (LI17)
- **Paso Transición (`transicion`): Coexistencia Multi-Tenant.**  
  Ejecuta: `SELECT 'LI16: db_ronald.fb_ronald', COUNT(*) ... UNION ALL SELECT 'LI17: dbec_ronald.tec_ronald', COUNT(*) ...`  
  *Speech:* *"Demostramos que sin reiniciar el clúster ni alterar configuraciones, la infraestructura escala de 99k filas de redes sociales a 541k transacciones comerciales gracias a la separación de esquemas en Hive."*

---

### FASE 6: INGESTA COMERCIAL & TABLA tec_ronald (LI17)
- **Paso 17_01 (`17_01`): Dataset comercial.** `data_ronald.csv` (45.5 MB, 541.910 transacciones).  
  *Por qué:* Normalización previa de fecha `InvoiceDate` a ISO `YYYY-MM-DD HH:MM:SS`.
- **Paso 17_02a (`17_02a`): Base de datos comercial.** `CREATE DATABASE IF NOT EXISTS dbec_ronald;`.
- **Paso 17_02b (`17_02b`): Mapeo de columnas y tipos.** `InvoiceNo(STRING)`, `StockCode(STRING)`, `Quantity(INT)`, `UnitPrice(DOUBLE)`, `CustomerID(STRING)`, `Country(STRING)`, `InvoiceDate(TIMESTAMP)`.
- **Paso 17_02c (`17_02c`): Creación de tabla con skip.header.** `TBLPROPERTIES ("skip.header.line.count"="1")`.  
  *Por qué:* Ignora automáticamente la primera línea sin tener que modificar físicamente el CSV fuente.
- **Paso 17_02d (`17_02d`): Location HDFS de tec_ronald.** `/user/hive/warehouse/dbec_ronald.db/tec_ronald`.
- **Paso 17_02e (`17_02e`): Carga masiva.** `SELECT COUNT(*) FROM dbec_ronald.tec_ronald;` -> **541.910 filas**.
- **Paso 17_02f (`17_02f`): Muestreo comercial.** `SELECT * FROM dbec_ronald.tec_ronald LIMIT 10;`.

---

### FASE 7: INTELIGENCIA DE NEGOCIOS & 12 KPIs HIVEQL (LI17)
- **KPI 01 (`kpi1` / `03_01`): Ingreso total válido.** **£8.703.833,70**.  
  *Por qué:* Filtrar `Quantity > 0 AND UnitPrice > 0` para excluir cancelaciones y notas de crédito.
- **KPI 02 (`kpi2` / `03_02`): Top 10 productos más vendidos.**  
  1. `RABBIT NIGHT LIGHT`: 30.788 unidades en 994 órdenes.  
  2. `MINI PAINT SET VINTAGE`: 26.633 unidades en 380 órdenes.  
  *Insight:* Artículos de bajo precio unitario y altísima rotación para regalos infantiles.
- **KPI 03 (`kpi3` / `03_03`): Clientes por país.**  
  Reino Unido concentra el **90.35%** (3.950 clientes), seguido por Alemania (95) y Francia (87).  
  *Uso técnico:* Window Function `SUM(COUNT(DISTINCT CustomerID)) OVER ()`.
- **KPI 04 (`kpi4` / `03_04`): Ticket promedio vs Mediana.**  
  Promedio = **£523.76** | Mediana estimada (p0.5) = **£302.61**.  
  *Explicación estadística:* Asimetría positiva fuerte debida a pedidos mayoristas atípicos de hasta £168.000 que elevan la media. La mediana representa mejor al comprador típico.
- **KPI 05 (`kpi5` / `03_05`): Ventas mes a mes.**  
  Pico absoluto en **Noviembre 2011**: 2.767 órdenes y **£1.505.319,46**.  
  *Causa comercial:* Campaña navideña y Black Friday en el Reino Unido. Diciembre cae a £468k porque el dataset concluye el 9 de diciembre.
- **KPI 06 (`kpi6` / `03_06`): Tasa de devolución por producto.**  
  Productos con hasta **20.00%** de devolución (ej. `Beach Hut Design Blackboard`).  
  *Uso técnico:* `HAVING COUNT(*) >= 10` para evitar sesgo en productos con pocas ventas. Permite auditoría de embalajes y logística inversa.
- **KPI 07 (`kpi7` / `03_07`): Ventas por hora del día.**  
  Pico transaccional entre las **12:00 y las 15:00 horas**.  
  *Insight:* Horario de almuerzo y compras corporativas. Se recomienda enviar correos promocionales a las 11:00 am.
- **KPI 08 (`kpi8` / `03_08`): Productos estacionales.**  
  Productos navideños concentran hasta el **80%** de su venta en 1-2 meses.  
  *Uso técnico:* Window Function `PARTITION BY Description` para normalizar la demanda mensual por producto.
- **KPI 09 (`kpi9` / `03_09`): Margen implícito proxy.**  
  Score = `AVG(UnitPrice) * Pedidos_con_producto`.  
  *Insight:* Identifica productos de alto valor unitario con frecuencia respetable para priorizar en promociones.
- **KPI 10 (`kpi10` / `03_10`): Clientes Anónimos vs Registrados.**  
  Registrados generaron **£8.703.833,70** (18.524 órdenes) vs Anónimos **£1.745.631,66** (1.427 órdenes).  
  *Insight:* Los clientes registrados aportan el 83% de los ingresos totales y tienen canastas más grandes; justifica planes de fidelización.
- **KPI 11 (`kpi11` / `03_11`): Conversión por día de la semana.**  
  **Jueves** es el día récord comercial: 4.244 pedidos y **£2.193.268,30**. Sábado tiene 0 pedidos por cierre de almacén mayorista.
- **KPI 12 (`kpi12` / `03_12`): Tasa de cancelación por país.**  
  Mide fricciones aduaneras o demoras de paquetería internacional.
- **Cierre (`cierre`): Síntesis final de la demostración.**

---

## 5. Banco de Preguntas Trampa del Docente y Respuestas Maestras

1. **¿Por qué usamos Beeline en lugar de la CLI `hive`?**  
   *R:* En Hive 4.0 la CLI monolítica `hive` fue formalmente deprecada. Beeline es un cliente ligero basado en SQLLine que se comunica con HiveServer2 por JDBC, garantizando arquitectura multi-hilo, concurrencia y seguridad.

2. **¿Qué diferencia hay entre Managed Table y External Table?**  
   *R:* En una Managed Table (como `fb_ronald` y `tec_ronald`), Hive gobierna tanto los metadatos en Derby como los datos físicos en HDFS; un `DROP TABLE` elimina ambos. En una External Table (`CREATE EXTERNAL TABLE ... LOCATION`), Hive solo administra el esquema; un `DROP TABLE` borra el registro del catálogo pero preserva intactos los archivos en HDFS.

3. **¿Por qué un `SELECT COUNT(*)` ejecuta MapReduce mientras un `SELECT ... LIMIT 10` es instantáneo?**  
   *R:* `LIMIT 10` es un *Fetch Task*: HiveServer2 lee directamente los primeros bytes de los bloques en HDFS. `COUNT(*)` requiere escanear todo el dataset distribuido agregando contadores parciales en la fase *Map* y consolidándolos en la fase *Reduce*.

4. **¿Dónde residen físicamente los datos del CSV y qué hizo `LOAD DATA INPATH`?**  
   *R:* `LOAD DATA INPATH` es una operación de traslado (*MOVE*) en el sistema de archivos distribuido HDFS. Movió el archivo a `/user/hive/warehouse/<db>.db/<table>/`. Los bloques residen en el DataNode, mientras el NameNode mantiene el mapeo de bloques.

5. **¿Qué ocurriría si se apaga el contenedor `li16-ronald-namenode-1`?**  
   *R:* HDFS queda inoperativo inmediatamente. Aunque el DataNode conserve los bloques físicos en disco, el NameNode es el único que posee el mapa en memoria de qué bloques componen cada archivo.

6. **¿Por qué la media aritmética difiere de la mediana en el ticket de compra?**  
   *R:* La media aritmética es vulnerable a valores extremos (*outliers* positivos, como pedidos mayoristas de £168.000). La mediana (percentil 50) divide la muestra en dos mitades exactas y refleja con mayor realismo el gasto del comprador minorista habitual (£302.61).

---

## 6. Playbook de Troubleshooting de Emergencia durante la Defensa

| Síntoma en Terminal | Causa Raíz | Solución Rápida |
| :--- | :--- | :--- |
| `HiveServer2 running as process 7. Stop it first.` | PID residual tras reinicio abrupto de Docker. | Ejecuta `diag` en la consola o corre: `docker rm -f li16-ronald-hive-server-1` y `docker compose -f proyecto/compose.yaml up -d hive-server`. |
| `Name node is in safe mode.` | El NameNode arrancó y aún espera reportes de bloques del DataNode. | Ejecuta en terminal: `docker exec li16-ronald-namenode-1 hdfs dfsadmin -safemode leave`. |
| `No files matching path /datos/data_ronald.csv` | `LOAD DATA` movió el archivo previamente. | La opción `diag` de la consola resube automáticamente el archivo a `/datos/data_ronald.csv` en HDFS. |
| `ParseException ... character '\ufeff' not supported` | BOM UTF-8 en scripts SQL. | Todos los SQLs en `proyecto/sql/` y `proyecto/sql_li17/` ya están saneados en UTF-8 puro sin BOM. |
| Contenedores detenidos (`0/4 activos`). | Docker Desktop estuvo cerrado o suspendido. | Ejecuta `diag` en la consola; detectará Docker y levantará los 4 contenedores automáticamente. |
