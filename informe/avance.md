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

## Pendientes inmediatos

Integración activada desde Docker Desktop y verificada desde Ubuntu. Docker Engine 29.4.1 y Docker Compose v5.1.3 responden correctamente. `docker ps -a` muestra tres contenedores anteriores detenidos: greenbit-frontend, greenbit-backend y greenbit-db; se conservan sin cambios.

Validar la integración Docker y Ubuntu, preparar el usuario de trabajo y capturar las evidencias con la hora del sistema visible. El borrador Word aún requiere revisión visual: el renderizador detectó que LibreOffice no está instalado en Windows.

Las capturas académicas y los resultados de Hive todavía no se han generado. Los puntos pendientes se completarán después de ejecutarlos.
