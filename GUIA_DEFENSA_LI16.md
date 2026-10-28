# GUÍA MAESTRA DE DEFENSA TÉCNICA — LABORATORIO LI16
**Materia:** Tecnologías Emergentes I  
**Estudiante:** Ronald Joel Saavedra Vargas  
**Entorno:** Apache Hadoop 3.4.1 + Apache Hive 4.0.1 sobre Docker Compose  
**Dataset:** 99.003 usuarios (`pseudo_facebook_ronald.csv`)

---

## 1. Protocolo de Preparación (5 Minutos Antes de la Defensa)

Antes de que inicie tu evaluación, realiza este checklist preventivo:

1. **Abre Docker Desktop** y asegúrate de que el motor esté en verde (*Engine Running*).
2. **Ejecuta el asistente de defensa**:
   - Haz doble clic en `iniciar_asistente.bat` (o corre `.\menu_evidencias.ps1` en PowerShell).
3. **Ejecuta la opción `diag`**:
   - Esto verificará automáticamente que los 4 contenedores estén `Up`, que el puerto Thrift `9083` responda, que Beeline conecte al puerto `10000` y que HDFS no esté en *Safe Mode*.
4. **Ten abiertas en segundo plano las siguientes pestañas del navegador**:
   - Interfaz Web HDFS: `http://localhost:9870/dfshealth.html`
   - Explorador de Archivos HDFS: `http://localhost:9870/explorer.html#/user/hive/warehouse/`
   - Tu repositorio en GitHub: `https://github.com/RJoel158/LI16`
   - El informe formal en PDF: `informe/Informe_LI16_Ronald_Saavedra.pdf`

---

## 2. Speech de Apertura (Los Primeros 60 Segundos)

> *"Buenos días / tardes docente. Para este laboratorio LI16 implementé un clúster analítico propio y desacoplado de Big Data basado en Apache Hadoop 3.4.1 y Apache Hive 4.0.1 mediante Docker Compose. A diferencia del repositorio tradicional de Big Data Europe —que utiliza versiones legadas de Hadoop 2.x e imágenes monolíticas desactualizadas—, esta arquitectura separa las responsabilidades en cuatro microservicios: un NameNode y un DataNode para el sistema de archivos distribuido HDFS, un Hive Metastore con base de datos relacional Derby persistente mediante volúmenes para el catálogo de esquemas, y un HiveServer2 que expone el protocolo JDBC para conexiones remotas con el cliente Beeline.*  
> *Sobre esta infraestructura cargamos un dataset real de 99.003 usuarios de redes sociales, validamos el almacenamiento de bloques en HDFS y ejecutamos consultas analíticas complejas en HiveQL para estudiar el comportamiento de usuarios según género, edad y preferencia de dispositivos móviles frente a escritorio."*

---

## 3. Matriz de Arquitectura del Clúster (Lo que debes saber explicar en la pizarra o pantalla)

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
       |  - Metadata HDFS            | |  - Motor HiveQL / MapReduce  |
       |  - Puerto Web UI: 9870      | |  - Puerto JDBC: 10000        |
       |  - Puerto RPC: 9000 (int.)  | |  - Puerto Web: 10002         |
       |  - Volumen: namenode:/data  | |                              |
       +--------------+--------------+ +--------------+---------------+
                      |                               |
        Red Interna   |                 Thrift RPC    |
          HDFS        |                 Puerto 9083   |
                      v                               v
       +-----------------------------+ +------------------------------+
       |   li16-ronald-datanode-1    | | li16-ronald-hive-metastore-1 |
       |     (Hadoop DataNode)       | |       (Hive Metastore)       |
       |                             | |                              |
       |  - Bloques físicos CSV      | |  - Catálogo de tablas/tipos  |
       |  - Puertos int: 9864/9866   | |  - Base Derby persistente    |
       |  - Volumen: datanode:/data  | |  - Volumen: metastore:/data  |
       +-----------------------------+ +------------------------------+
```

### Roles Clave de Cada Contenedor:
1. **NameNode (`li16-ronald-namenode-1`)**: Administra el árbol del sistema de archivos distribuido (inodos, permisos) y mapea qué bloques pertenecen a qué archivo. No guarda el contenido de los datos, solo la metadata.
2. **DataNode (`li16-ronald-datanode-1`)**: Almacena físicamente los bloques de datos (divididos por defecto en bloques HDFS) y atiende las lecturas/escrituras.
3. **Hive Metastore (`li16-ronald-hive-metastore-1`)**: Servicio desacoplado que expone mediante Thrift RPC (puerto 9083) la definición de esquemas, bases de datos y columnas, guardando esta metadata en una base relacional Derby persistida en volumen.
4. **HiveServer2 (`li16-ronald-hive-server-1`)**: Es el servidor de procesamiento que compila las consultas HiveQL, las traduce al motor de ejecución (MapReduce local en este caso) y permite a clientes externos conectarse mediante JDBC en el puerto 10000 usando Beeline.

---

## 4. Paso a Paso Detallado: Guía Punto por Punto (Puntos 01 al 16g)

A continuación tienes qué comando mostrar, qué decir y qué te puede preguntar el docente en cada punto de la guía oficial:

---

### FASE 1: INFRAESTRUCTURA Y CONTENEDORES (Puntos 01 al 05)

#### Punto 01: Contenedores existentes en el host
- **Comando:** `docker ps -a`
- **Speech sugerido:** *"Al iniciar el laboratorio revisamos qué contenedores estaban presentes en el host para asegurar que los puertos estándar de Hadoop y Hive (como el 9870 y el 10000) estuvieran libres y evitar conflictos de red."*
- **Pregunta trampa del docente:** *¿Qué pasaría si ya tuvieras un contenedor escuchando en el puerto 9870?*
- **Respuesta experta:** *"Docker rechazaría levantar el contenedor NameNode con un error de 'bind: address already in use'. Tendríamos que remapear el puerto en el host (ej. `9871:9870`) o detener el contenedor preexistente."*

#### Punto 02: Repositorio propio frente a Big Data Europe
- **Comando:** `git log -3 --oneline` y mostrar estructura del proyecto.
- **Speech sugerido:** *"La guía solicita crear un repositorio propio diferente al de Big Data Europe. Construimos una configuración limpia con las versiones estables oficiales Apache Hadoop 3.4.1 y Apache Hive 4.0.1, garantizando portabilidad con volúmenes persistentes y compatibilidad con arquitecturas modernas."*
- **Pregunta trampa del docente:** *¿Por qué no usar simplemente la imagen clásica de bde2020?*
- **Respuesta experta:** *"Las imágenes de BDE2020 quedaron congeladas en Hadoop 2.7 y Hive 2.x hace más de 4 años, tienen fallas de seguridad conocidas y no soportan características de Hive 4.0 como el nuevo Metastore desacoplado ni Beeline sobre JDBC moderno."*

#### Punto 03: Despliegue con Docker Compose
- **Comando:** `docker compose -f proyecto/compose.yaml ps`
- **Speech sugerido:** *"Definimos el clúster de forma declarativa en `compose.yaml`. Incluye healthchecks condicionales: HiveServer2 solo arranca cuando el Metastore responde exitosamente en el puerto Thrift 9083, evitando caídas por condición de carrera."*

#### Punto 04: Verificación de contenedores activos
- **Comando:** `docker ps`
- **Speech sugerido:** *"Aquí evidenciamos que los 4 microservicios requeridos están en estado 'Up' y 'healthy', exponiendo hacia Windows los puertos 9870 (NameNode Web UI), 10000 (Hive Beeline JDBC) y 10002 (HiveServer2 Status UI)."*

#### Punto 05: Análisis reflexivo de consumo de recursos
- **Comando:** `docker stats --no-stream`
- **Speech sugerido:** *"Monitoreamos el consumo con `docker stats`. HiveServer2 y el NameNode son los que más memoria RAM reservan (~1.2 GB y ~800 MB respectivamente), ya que instancian Máquinas Virtuales Java (JVM) completas para gestionar el catálogo en memoria y el procesamiento MapReduce."*

---

### FASE 2: ARQUITECTURA HDFS Y NAMENODE (Puntos 06 al 09)

#### Punto 06: Shell interactivo del NameNode
- **Comando:** `docker exec -it li16-ronald-namenode-1 bash -c "whoami; hostname; pwd; ls -la /opt/hadoop"`
- **Speech sugerido:** *"Accedemos al shell del NameNode para verificar el entorno base de Hadoop en `/opt/hadoop`, donde residen los binarios y los archivos de configuración `core-site.xml` y `hdfs-site.xml` montados desde nuestro repositorio."*

#### Punto 07: Inspección del Warehouse inicial en HDFS
- **Comando:** `docker exec li16-ronald-namenode-1 hdfs dfs -ls /user/hive/warehouse/`
- **Speech sugerido:** *"Listamos el directorio raíz analítico en HDFS. Inicialmente este directorio está vacío o solo contiene permisos predeterminados (`drwxrwxrwx`), ya que aún no se ha creado ninguna base de datos ni tabla."*
- **Pregunta trampa del docente:** *¿Por qué los comandos de HDFS empiezan con `hdfs dfs`?*
- **Respuesta experta:** *"`hdfs dfs` es el comando cliente genérico que interactúa con el sistema de archivos distribuido a través del protocolo RPC `hdfs://namenode:9000`."*

#### Punto 08: Interfaz Web del NameNode (Salud del clúster)
- **Comando / Acción:** Mostrar en el navegador `http://localhost:9870/dfshealth.html`
- **Speech sugerido:** *"En la consola web de Hadoop 3.4.1 podemos comprobar el estado del sistema: espacio total, bloques vivos, 0 bloques corruptos y la presencia del DataNode en estado 'Live'. Esto valida que el NameNode tiene conectividad completa con los nodos de almacenamiento."*

#### Punto 09: Navegación del HDFS (Browse the file system)
- **Comando / Acción:** Mostrar en navegador `http://localhost:9870/explorer.html#/user/hive/warehouse/`
- **Speech sugerido:** *"A través del explorador gráfico web podemos navegar por la jerarquía de directorios de HDFS y verificar los permisos POSIX de los bloques."*

---

### FASE 3: PIPELINE DE INGESTA Y DATASET (Puntos 10 al 13)

#### Punto 10: Descarga y renombrado a `pseudo_facebook_ronald.csv`
- **Comando:** `Get-Item datos\pseudo_facebook_ronald.csv | Format-List Name, Length, LastWriteTime`
- **Speech sugerido:** *"Descargamos el dataset oficial de Facebook de Kaggle y lo renombramos a `pseudo_facebook_ronald.csv`. Tiene un tamaño de 12.8 MB y contiene 99.003 registros de usuarios."*

#### Punto 11: Eliminación del encabezado del CSV
- **Comando:** `Get-Content datos\pseudo_facebook_ronald.csv -Head 5`
- **Speech sugerido:** *"Se removió la fila inicial de nombres de columnas. Esto es una buena práctica cuando se cargan archivos delimitados en Hive para evitar que los títulos de texto intenten parsearse como datos numéricos, garantizando que el 100% de las 99.003 líneas sean registros puros."*

#### Punto 12: Copia del CSV al contenedor NameNode en `/tmp/`
- **Comando:** `docker exec li16-ronald-namenode-1 ls -lh /tmp/pseudo_facebook_ronald.csv`
- **Speech sugerido:** *"Como los contenedores operan en un espacio de nombres aislado del sistema Windows, copiamos el CSV mediante `docker cp` al almacenamiento temporal del NameNode como paso previo a su inserción en HDFS."*

#### Punto 13: Subida a HDFS y verificación con `ls`
- **Comando:** `docker exec li16-ronald-namenode-1 hdfs dfs -ls /user/hive/warehouse/`
- **Speech sugerido:** *"Ejecutamos `hdfs dfs -put` para transferir el CSV desde el sistema local del contenedor hacia HDFS. A partir de este momento, el archivo queda distribuido en bloques administrados por el DataNode."*

---

### FASE 4: CATÁLOGO Y TABLAS EN APACHE HIVE (Puntos 14 al 15f)

#### Punto 14: Acceso al shell de HiveServer2
- **Comando:** `docker exec li16-ronald-hive-server-1 bash -c "hive --version 2>&1 | head -n 4"`
- **Speech sugerido:** *"Comprobamos el acceso al contenedor HiveServer2 y validamos la versión oficial de Apache Hive 4.0.1."*

#### Punto 15a: Creación de la base de datos `db_ronald`
- **Comando:** `docker exec -i li16-ronald-hive-server-1 beeline -u "jdbc:hive2://localhost:10000" -n hive -e "SHOW DATABASES;"`
- **Speech sugerido:** *"Creamos la base de datos aislada `db_ronald` con `CREATE DATABASE IF NOT EXISTS db_ronald;`. La salida de `SHOW DATABASES;` confirma su persistencia en el Metastore."*
- **Pregunta trampa del docente:** *¿Dónde se guarda físicamente la metadata de la base de datos?*
- **Respuesta experta:** *"En el contenedor `hive-metastore`, dentro de la base de datos relacional Apache Derby ubicada en el volumen persistente `metastore:/data/metastore_db`."*

#### Punto 15b: Identificación de columnas y tipos de datos
- **Comando:** `docker exec -i li16-ronald-hive-server-1 beeline -u "jdbc:hive2://localhost:10000" -n hive -e "DESCRIBE db_ronald.fb_ronald;"`
- **Speech sugerido:** *"Analizamos los tipos de datos: `userid` se definió como BIGINT para soportar identificadores grandes; `age`, `dob_day`, `dob_year`, `dob_month` como INT; `gender` como STRING para admitir valores textuales y nulos; y las métricas de amigos y likes (`likes`, `likes_received`, `mobile_likes`, `www_likes`) como BIGINT / INT para evitar desbordamientos aritméticos en sumas acumulativas."*

#### Punto 15c: Creación de la tabla `fb_ronald`
- **Comando:** `docker exec -i li16-ronald-hive-server-1 beeline -u "jdbc:hive2://localhost:10000" -n hive -e "SHOW TABLES IN db_ronald;"`
- **Speech sugerido:** *"Creamos la tabla indicando `ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE;`. Al ser un archivo de texto plano separado por comas, Hive aplica el deserializador LazySimpleSerDe de forma nativa."*

#### Punto 15d: Verificación del parámetro `Location` en HDFS
- **Comando:** `docker exec -i li16-ronald-hive-server-1 beeline -u "jdbc:hive2://localhost:10000" -n hive -e "DESCRIBE FORMATTED db_ronald.fb_ronald;" | Select-String "Location:|Table Type:"`
- **Speech sugerido:** *"Al consultar `DESCRIBE FORMATTED`, observamos que `Table Type` es `MANAGED_TABLE` y `Location` apunta exactamente a `hdfs://namenode:9000/user/hive/warehouse/db_ronald.db/fb_ronald`. Esto demuestra que Hive es el propietario del ciclo de vida del directorio."*
- **Pregunta trampa del docente:** *¿Qué diferencia hay entre MANAGED_TABLE y EXTERNAL_TABLE?*
- **Respuesta experta:** *"Si borramos una MANAGED_TABLE con `DROP TABLE`, Hive elimina tanto los metadatos como los archivos físicos de HDFS. En una EXTERNAL_TABLE, si hacemos `DROP TABLE`, solo se borran los metadatos en el Metastore, pero los datos físicos en HDFS permanecen intactos."*

#### Punto 15e: Carga de datos con `LOAD DATA` y validación de 99.003 filas
- **Comando:** `docker exec -i li16-ronald-hive-server-1 beeline -u "jdbc:hive2://localhost:10000" -n hive -e "SELECT COUNT(*) AS total_cargado FROM db_ronald.fb_ronald;"`
- **Speech sugerido:** *"Ejecutamos `LOAD DATA INPATH` y confirmamos mediante `SELECT COUNT(*)` que se cargaron con exactitud las **99.003 filas**. Cabe resaltar que Hive no copia el archivo, sino que lo 'mueve' desde su ubicación temporal en HDFS hacia el subdirectorio formal de la tabla."*

#### Punto 15f: Muestreo de validación (`LIMIT 10`)
- **Comando:** `docker exec -i li16-ronald-hive-server-1 beeline -u "jdbc:hive2://localhost:10000" -n hive -e "SELECT * FROM db_ronald.fb_ronald LIMIT 10;"`
- **Speech sugerido:** *"Verificamos que todos los campos coincidan perfectamente con sus cabeceras (edad, género, amigos, likes) sin columnas corridas ni datos corruptos."*

---

### FASE 5: CONSULTAS ANALÍTICAS HIVEQL (Puntos 16a al 16g)

Aprende estos resultados clave para responder con seguridad:

| Punto | Pregunta de Negocio | Código SQL Clave | Resultado Exacto | Interpretación Técnica |
| :---: | :--- | :--- | :---: | :--- |
| **16a** | Total de usuarios y unicidad | `SELECT COUNT(*), COUNT(DISTINCT userid)` | **99.003 usuarios** | 99.003 filas totales y 99.003 IDs distintos; no existen duplicados en el dataset. |
| **16b** | Usuarios mayores de 25 años | `WHERE age > 25` | **73.047 usuarios** | Representan el **73.78%** del total; la red social tiene una base predominantemente adulta. |
| **16c** | Amigos promedio por género | `GROUP BY gender; AVG(friend_count)` | **Femenino: 241.97**<br>Masculino: 165.43 | Las mujeres tienen en promedio **76 amigos más** que los hombres en esta muestra. |
| **16d** | Likes recibidos: Jóvenes (13-25) vs Mayores de 35 | `CASE WHEN age BETWEEN 13 AND 25...` | **Jóvenes: ~267.4**<br>Mayores 35: ~67.1 | Los usuarios jóvenes reciben **4 veces más likes** que los mayores de 35 años. |
| **16e** | Distribución por mes de cumpleaños | `GROUP BY dob_month ORDER BY mes` | Enero lidera con **11.833**; otros meses promedian ~7.500 a 8.500 | Distribución uniforme a lo largo del año con pico en enero (típico sesgo por fecha por defecto 01/01). |
| **16f** | Jóvenes (13-25): ¿Celular o Computadora? | `SUM(mobile_likes), SUM(www_likes)` | **Móvil: 83.2%**<br>Web: 16.8% | Los jóvenes interactúan masivamente desde smartphones. |
| **16g** | Adultos (> 25): ¿Celular o Computadora? | `SUM(mobile_likes), SUM(www_likes)` | **Móvil: 68.5%**<br>Web: 31.5% | El móvil sigue liderando en adultos, pero el uso web se duplica respecto a los jóvenes. |

---

## 5. Banco de Preguntas Difíciles del Docente (Q&A de Alta Dificultad)

### P1: ¿Por qué usas Beeline en vez del comando `hive` tradicional?
> **Respuesta:** *"En Apache Hive 4.0, la consola local CLI clásica (`hive`) fue oficialmente deprecada debido a que acoplaba el compilador directamente con el almacenamiento sin seguridad ni soporte concurrente. Beeline es el estándar oficial recomendado por Apache; opera como un cliente JDBC ligero y seguro que se conecta a través del protocolo Thrift a HiveServer2, permitiendo autenticación y concurrencia multi-hilo."*

### P2: ¿Qué motor de ejecución utiliza Hive en tu laboratorio y qué alternativas existen?
> **Respuesta:** *"En nuestro clúster utilizamos MapReduce local como motor de ejecución base para compatibilidad sin dependencias adicionales de YARN. En entornos de producción empresarial, Hive utiliza motores modernos en memoria como **Apache Tez** o **Apache Spark**, que reducen la latencia de las consultas de minutos a segundos al evitar escrituras intermedias a disco."*

### P3: ¿Qué pasaría si se cae el contenedor `li16-ronald-namenode-1`?
> **Respuesta:** *"El clúster quedaría inoperativo de inmediato para cualquier lectura o escritura, ya que el NameNode es el punto único de fallo (SPOF) que almacena la tabla de inodos y el mapeo de bloques en memoria RAM. Aunque los datos físicos seguirían a salvo en el disco del DataNode, ningún cliente sabría cómo reconstruirlos. Para producción, Hadoop resuelve esto con una arquitectura de Alta Disponibilidad (HA) con dos NameNodes (Active y Standby) coordinados mediante Apache ZooKeeper y JournalNodes."*

### P4: ¿Por qué elegiste Apache Derby para el Metastore y qué limitación tiene?
> **Respuesta:** *"Elegimos Derby en modo embebido por su simplicidad de despliegue para laboratorio educativo, persistiendo sus archivos en el volumen `metastore:/data/metastore_db`. Su gran limitación es que solo admite una conexión activa concurrente a la vez (bloquea la base de datos). En un entorno real de equipo o producción se utiliza un motor relacional multi-usuario como **PostgreSQL** o **MySQL/MariaDB**."*

### P5: ¿Qué significa que una consulta HiveQL ejecute una etapa MapReduce?
> **Respuesta:** *"Significa que el optimizador de consultas de Hive tradujo la sentencia declarativa SQL en un grafo acíclico dirigido (DAG) de tareas Map (que leen y filtran los bloques del CSV en paralelo) y tareas Reduce (que realizan las agregaciones como `SUM`, `AVG` y `GROUP BY`)."*

---

## 6. Plan de Contingencia en Vivo (Troubleshooting Playbook)

Si durante la defensa algo no responde, no entres en pánico. Usa estas soluciones inmediatas:

| Síntoma en Vivo | Causa Probable | Solución Inmediata en 5 Segundos |
| :--- | :--- | :--- |
| **Error:** `failed to connect to docker API...` | Docker Desktop se cerró o se está actualizando. | Abre Docker Desktop desde el menú de inicio y espera 10 segundos a que el ícono esté en verde. |
| **Error:** `container is not running` | Los contenedores se detuvieron al apagar la PC. | En PowerShell corre: `docker start li16-ronald-namenode-1 li16-ronald-datanode-1 li16-ronald-hive-metastore-1 li16-ronald-hive-server-1` o escribe `diag` en el asistente. |
| **Error en HiveServer2:** `HiveServer2 running as process 7. Stop it first.` | El contenedor se apagó abruptamente y dejó un PID fantasma. | Ejecuta: `docker rm -f li16-ronald-hive-server-1` seguido de `docker compose -f proyecto/compose.yaml up -d hive-server`. El metastore no se pierde. |
| **Error en Beeline:** `Could not open client transport with JDBC Uri` | HiveServer2 aún está iniciando o el Metastore no está listo. | Espera 10 segundos a que el healthcheck pase (`docker ps`) y reintenta la conexión. |
| **Error HDFS:** `Name node is in safe mode` | HDFS entró en modo seguro de lectura tras un reinicio. | Corre: `docker exec li16-ronald-namenode-1 hdfs dfsadmin -safemode leave`. |
