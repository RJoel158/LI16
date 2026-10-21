# Apache Hive & Hadoop HDFS Distributed Environment
**Laboratorio LI16 — Tecnologías Emergentes I**  
**Universidad Privada del Valle (Univalle Bolivia)**  
**Autor:** Ronald Joel Saavedra Vargas  

Este repositorio contiene la configuración, infraestructura y demostración técnica de un clúster analítico distribuido basado en **Apache Hadoop 3.4.1** y **Apache Hive 4.0.1** orquestado mediante **Docker Compose**, procesando un dataset de 99.003 registros de usuarios y ejecutando consultas analíticas complejas mediante HiveQL.

---

## 1. Arquitectura del Clúster y Especificación de Puertos

El despliegue consta de **cuatro microservicios contenerizados** conectados a través de una red puente privada (*bridge network*), con almacenamiento persistente administrado por volúmenes Docker y ejecución de consultas distribuida.

```
       +--------------------------------------------------------------+
       |                      HOST (WINDOWS 11)                       |
       |                                                              |
       |    Navegador Web                 Consola / Cliente SQL       |
       |    http://localhost:9870         Beeline JDBC (:10000)       |
       +--------------+------------------------------+----------------+
                      |                              |
                      | 127.0.0.1:9870               | 127.0.0.1:10000
                      v                              v
       +-----------------------------+ +------------------------------+
       |   li16-ronald-namenode-1    | |  li16-ronald-hive-server-1   |
       |     (Hadoop NameNode)       | |        (HiveServer2)         |
       |                             | |                              |
       |  - Puerto Web: 9870         | |  - Puerto JDBC: 10000        |
       |  - Puerto RPC: 9000 (int.)  | |  - Puerto Web: 10002         |
       |  - Volumen: namenode:/data  | |  - Motor: MapReduce Local    |
       +--------------+--------------+ +--------------+---------------+
                      |                               |
        Red Interna   |                 Thrift RPC    |
          HDFS        |                 Puerto 9083   |
                      v                               v
       +-----------------------------+ +------------------------------+
       |   li16-ronald-datanode-1    | | li16-ronald-hive-metastore-1 |
       |     (Hadoop DataNode)       | |       (Hive Metastore)       |
       |                             | |                              |
       |  - Bloques de datos CSV     | |  - Catálogo esquemas/tablas  |
       |  - Puertos int: 9864/9866   | |  - Base relacional Derby     |
       |  - Volumen: datanode:/data  | |  - Volumen: metastore:/data  |
       +-----------------------------+ +------------------------------+
```

### Matriz Técnica de Contenedores y Puertos

| Servicio | Contenedor | Imagen Base | Puerto Host (Windows) | Puerto Contenedor | Protocolo / Uso | Exposición |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **NameNode** | `li16-ronald-namenode-1` | `apache/hadoop:3.4.1` | **`9870`** | `9870` | HTTP / HDFS Web UI & Health | Pública al Host (`127.0.0.1:9870`) |
| **NameNode** | `li16-ronald-namenode-1` | `apache/hadoop:3.4.1` | - | `9000` | IPC / HDFS Metadata RPC | Red interna del clúster |
| **DataNode** | `li16-ronald-datanode-1` | `apache/hadoop:3.4.1` | - | `9864, 9866` | TCP / Transferencia de bloques HDFS | Red interna del clúster |
| **Hive Metastore** | `li16-ronald-hive-metastore-1` | `apache/hive:4.0.1` | - | **`9083`** | Thrift RPC / Catálogo de esquemas | Red interna (consumido por HiveServer2) |
| **HiveServer2** | `li16-ronald-hive-server-1` | `apache/hive:4.0.1` | **`10000`** | `10000` | TCP / Beeline JDBC SQL Server | Pública al Host (`127.0.0.1:10000`) |
| **HiveServer2** | `li16-ronald-hive-server-1` | `apache/hive:4.0.1` | **`10002`** | `10002` | HTTP / HiveServer2 Web Console | Pública al Host (`127.0.0.1:10002`) |

---

## 2. Definición del Orquestador (`proyecto/compose.yaml`)

El clúster está configurado mediante Docker Compose declarativo, incorporando persistencia en disco, inyección de configuraciones XML (`core-site.xml`, `hdfs-site.xml`) y sincronización condicional basada en *healthchecks*:

```yaml
name: li16-ronald
services:
  namenode:
    image: apache/hadoop:3.4.1
    hostname: namenode
    user: root
    entrypoint: /bin/bash
    command: ["-c", "mkdir -p /data/name; if [ ! -f /data/name/current/VERSION ]; then hdfs namenode -format -nonInteractive; fi; exec hdfs namenode"]
    ports: ["127.0.0.1:9870:9870"]
    volumes:
      - namenode:/data/name
      - ./config/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml:ro
      - ./config/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml:ro

  datanode:
    image: apache/hadoop:3.4.1
    hostname: datanode
    user: root
    entrypoint: /bin/bash
    command: ["-c", "mkdir -p /data/data; exec hdfs datanode"]
    depends_on: [namenode]
    volumes:
      - datanode:/data/data
      - ./config/core-site.xml:/opt/hadoop/etc/hadoop/core-site.xml:ro
      - ./config/hdfs-site.xml:/opt/hadoop/etc/hadoop/hdfs-site.xml:ro

  hive-metastore:
    image: apache/hive:4.0.1
    hostname: hive-metastore
    user: root
    environment:
      SERVICE_NAME: metastore
      HIVE_CUSTOM_CONF_DIR: /hive_custom_conf
      SERVICE_OPTS: "-Djavax.jdo.option.ConnectionURL=jdbc:derby:;databaseName=/data/metastore_db;create=true"
    volumes:
      - metastore:/data
      - ./config/core-site.xml:/hive_custom_conf/core-site.xml:ro
      - ./config/hdfs-site.xml:/hive_custom_conf/hdfs-site.xml:ro
    depends_on: [namenode, datanode]
    healthcheck:
      test: ["CMD", "bash", "-c", "echo > /dev/tcp/localhost/9083"]
      interval: 10s
      timeout: 5s
      retries: 20
      start_period: 30s

  hive-server:
    image: apache/hive:4.0.1
    hostname: hive-server
    environment:
      SERVICE_NAME: hiveserver2
      IS_RESUME: "true"
      HIVE_CUSTOM_CONF_DIR: /hive_custom_conf
    ports: ["127.0.0.1:10000:10000", "127.0.0.1:10002:10002"]
    volumes:
      - ./config:/hive_custom_conf:ro
    depends_on:
      hive-metastore:
        condition: service_healthy

volumes:
  namenode:
  datanode:
  metastore:
```

### Componentes Clave de la Configuración:
* **Formateo Seguro de NameNode:** Evalúa la existencia de `/data/name/current/VERSION` antes de formatear para no destruir datos existentes tras reinicios del motor.
* **Metastore Relacional Persistente:** Emplea Apache Derby con base de datos en `/data/metastore_db` vinculada al volumen persistente `metastore`.
* **Healthcheck Activo de Metastore:** HiveServer2 espera de manera determinista a que el puerto Thrift `9083` acepte conexiones TCP antes de inicializar el servicio de JDBC.

---

## 3. Flujo de Datos y Esquema Tabular

### Pipeline de Ingesta:
1. **Extracción y Limpieza:** El dataset original de Kaggle (`pseudo_facebook.csv`) se descargó en el anfitrión; se eliminó la cabecera de texto para evitar inconsistencias numéricas y se guardó como `datos/pseudo_facebook_ronald.csv` (99.003 filas limpias).
2. **Transferencia a Contenedor:** Copiado hacia `/tmp/` del NameNode mediante `docker cp`.
3. **Ingesta Distribuida HDFS:** Cargado hacia el sistema de archivos distribuido con `hdfs dfs -put /tmp/pseudo_facebook_ronald.csv /user/hive/warehouse/`.
4. **Mapeo Tabular HiveQL:** Creación del catálogo lógico en `db_ronald.fb_ronald` y ejecución de `LOAD DATA INPATH` que mueve los bloques al directorio administrado:
   `hdfs://namenode:9000/user/hive/warehouse/db_ronald.db/fb_ronald`

### Esquema DDL de la Tabla (`db_ronald.fb_ronald`):

```sql
CREATE DATABASE IF NOT EXISTS db_ronald;

CREATE TABLE IF NOT EXISTS db_ronald.fb_ronald(
    userid                 BIGINT,
    age                    INT,
    dob_day                INT,
    dob_year               INT,
    dob_month              INT,
    gender                 STRING,
    tenure                 INT,
    friend_count           INT,
    friendships_initiated  INT,
    likes                  BIGINT,
    likes_received         BIGINT,
    mobile_likes           BIGINT,
    mobile_likes_received  BIGINT,
    www_likes              BIGINT,
    www_likes_received     BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

---

## 4. Consultas Analíticas Demostrativas (HiveQL)

Las 7 consultas analíticas requeridas por la guía oficial fueron ejecutadas en Beeline sobre MapReduce y contrastadas matemáticamente contra el CSV original:

### 16.a. Número total de usuarios:
```sql
SELECT COUNT(*) AS total_usuarios, COUNT(DISTINCT userid) AS usuarios_distintos FROM db_ronald.fb_ronald;
```
* **Resultado:** **99.003** usuarios (conteo total y conteo único idénticos, sin duplicados).

### 16.b. Usuarios mayores de 25 años:
```sql
SELECT COUNT(*) AS mayores_de_25 FROM db_ronald.fb_ronald WHERE age > 25;
```
* **Resultado:** **56.676** usuarios (**57,25%** del universo total).

### 16.c. Comparación de promedio de amigos por género:
```sql
SELECT gender, COUNT(*) AS usuarios, AVG(friend_count) AS promedio_amigos 
FROM db_ronald.fb_ronald WHERE gender IS NOT NULL GROUP BY gender;
```
* **Resultado:** **Femenino:** 241,97 amigos/promedio | **Masculino:** 165,04 amigos/promedio *(las mujeres superan a los varones por 76,93 amistades en promedio)*.

### 16.d. Likes recibidos: Jóvenes (13-25 años) vs. Mayores (> 35 años):
```sql
SELECT grupo_edad, COUNT(*) AS usuarios, SUM(likes_received) AS total_likes, AVG(likes_received) AS promedio_likes 
FROM (
    SELECT CASE WHEN age BETWEEN 13 AND 25 THEN '13-25' WHEN age > 35 THEN '35+' END AS grupo_edad, likes_received 
    FROM db_ronald.fb_ronald WHERE (age BETWEEN 13 AND 25) OR (age > 35)
) t GROUP BY grupo_edad;
```
* **Resultado:** **Jóvenes (13-25):** 8.477.550 likes (promedio **200,29**) vs. **Mayores (>35):** 3.982.359 likes (promedio **104,70**).

### 16.e. Distribución de usuarios por mes de cumpleaños:
```sql
SELECT dob_month AS mes_cumpleanos, COUNT(*) AS usuarios 
FROM db_ronald.fb_ronald GROUP BY dob_month ORDER BY mes_cumpleanos;
```
* **Resultado:** Máximo en **Enero** (11.772 usuarios) y mínimo en **Noviembre** (7.205 usuarios).

### 16.f. Plataforma preferida en jóvenes (13-25 años):
```sql
SELECT SUM(mobile_likes) AS movil, SUM(www_likes) AS web, AVG(mobile_likes) AS prom_movil, AVG(www_likes) AS prom_web 
FROM db_ronald.fb_ronald WHERE age BETWEEN 13 AND 25;
```
* **Resultado:** Móvil: **5.248.117** likes (promedio 123,99) vs. Web: **2.349.153** likes (promedio 55,50). Predomina el móvil.

### 16.g. Plataforma preferida en adultos (> 25 años):
```sql
SELECT SUM(mobile_likes) AS movil, SUM(www_likes) AS web, AVG(mobile_likes) AS prom_movil, AVG(www_likes) AS prom_web 
FROM db_ronald.fb_ronald WHERE age > 25;
```
* **Resultado:** Móvil: **5.257.715** likes (promedio 92,77) vs. Web: **2.597.277** likes (promedio 45,83). Predomina el móvil.

---

## 5. Instrucciones de Operación y Reproducción

### 1. Iniciar el clúster:
```bash
docker compose -f proyecto/compose.yaml up -d
```

### 2. Verificar estado de los servicios:
```bash
docker compose -f proyecto/compose.yaml ps
```

### 3. Conexión interactiva SQL mediante Beeline:
```bash
docker exec -it li16-ronald-hive-server-1 beeline -u jdbc:hive2://localhost:10000 -n hive
```

### 4. Acceso a interfaces web:
* **Hadoop NameNode UI:** [http://localhost:9870](http://localhost:9870)
* **Explorador HDFS:** [http://localhost:9870/explorer.html#/user/hive/warehouse](http://localhost:9870/explorer.html#/user/hive/warehouse)

---

## 6. Documentación y Entregables Oficiales

* 📕 **Informe Oficial en PDF:** [`informe/Informe_LI16_Ronald_Saavedra.pdf`](informe/Informe_LI16_Ronald_Saavedra.pdf)  
  *(Incluye portada reglamentaria con logo institucional de Univalle, los 16 requerimientos resaltados en amarillo, evidencias de pantalla completa con hora del sistema y análisis reflexivo).*
* 📄 **Informe Editable en Word:** [`informe/Informe_LI16_Ronald_Saavedra.docx`](informe/Informe_LI16_Ronald_Saavedra.docx)
* 🖼️ **Banco de Evidencias Reales:** [`evidencias/`](evidencias/) *(Capturas de pantalla completa de todas las ejecuciones).*
