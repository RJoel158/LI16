# Registro de avance LI16

Estudiante: Ronald Joel Saavedra Vargas

Materia: Tecnologías Emergentes I

## Preparación del entorno

- Se verificó Docker Desktop con motor Linux activo.
- La consulta inicial `docker ps` no mostró contenedores en ejecución.
- Se instaló Ubuntu con `wsl --install -d Ubuntu-24.04 --no-launch`.
- Se validó el inicio mediante `wsl -d Ubuntu-24.04 -u root -- cat /etc/os-release`.
- Resultado confirmado: Ubuntu 24.04.5 LTS.
- Se creará un proyecto propio con Docker Compose, diferente de Big Data Europe.
- Se preparó un borrador Word con portada y los 16 puntos resaltados en amarillo.

## Estado actual del laboratorio

- Entorno Docker 100% operativo con 4 contenedores activos (`li16-ronald-namenode-1`, `li16-ronald-datanode-1`, `li16-ronald-hive-metastore-1`, `li16-ronald-hive-server-1`).
- Dataset preparado en `datos/pseudo_facebook_ronald.csv` (99.003 filas cargadas exitosamente en Hive `db_ronald.fb_ronald`).
- Las 7 consultas SQL de HiveQL están probadas y validadas matemáticamente contra el CSV original.
- Interfaz web HDFS activa en `http://localhost:9870`.
- El informe técnico `informe/Informe_LI16_Ronald_Saavedra.docx` y su PDF compilado están listos, cumpliendo con la portada, puntos resaltados en amarillo y análisis reflexivo.
- Creado el lanzador interactivo `iniciar_asistente.bat` (`menu_evidencias.ps1`) para que el estudiante tome las capturas de pantalla completa (con la barra de tareas y reloj de Windows) y las incorpore de forma automática al portapapeles.

