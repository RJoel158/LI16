from pathlib import Path
r=Path(__file__).resolve().parents[1]
out=r/'proyecto/sql';out.mkdir(exist_ok=True)
sql={
'15a':'CREATE DATABASE IF NOT EXISTS db_ronald; SHOW DATABASES;',
'15c':'''CREATE TABLE IF NOT EXISTS db_ronald.fb_ronald (
userid BIGINT, age INT, dob_day INT, dob_year INT, dob_month INT,
gender STRING, tenure INT, friend_count INT, friendships_initiated INT,
likes BIGINT, likes_received BIGINT, mobile_likes BIGINT,
mobile_likes_received BIGINT, www_likes BIGINT, www_likes_received BIGINT
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE TBLPROPERTIES ('serialization.null.format'='NA');
DESCRIBE db_ronald.fb_ronald;''',
'15d':'DESCRIBE FORMATTED db_ronald.fb_ronald;',
'15e':"LOAD DATA INPATH '/user/hive/warehouse/pseudo_facebook_ronald.csv' INTO TABLE db_ronald.fb_ronald;",
'15f':'SELECT * FROM db_ronald.fb_ronald LIMIT 10;',
'16a':'SELECT COUNT(*) AS total_usuarios, COUNT(DISTINCT userid) AS usuarios_distintos FROM db_ronald.fb_ronald;',
'16b':'SELECT COUNT(*) AS usuarios_mayores_25 FROM db_ronald.fb_ronald WHERE age > 25;',
'16c':"SELECT gender, COUNT(*) AS usuarios, ROUND(AVG(friend_count),2) AS promedio_amigos FROM db_ronald.fb_ronald WHERE gender IN ('male','female') GROUP BY gender ORDER BY promedio_amigos DESC;",
'16d':"SELECT CASE WHEN age BETWEEN 13 AND 25 THEN '13 a 25' ELSE 'mayores de 35' END AS grupo, COUNT(*) AS usuarios, SUM(likes_received) AS likes_recibidos, ROUND(AVG(likes_received),2) AS promedio_recibidos FROM db_ronald.fb_ronald WHERE age BETWEEN 13 AND 25 OR age > 35 GROUP BY CASE WHEN age BETWEEN 13 AND 25 THEN '13 a 25' ELSE 'mayores de 35' END ORDER BY grupo;",
'16e':'SELECT dob_month AS mes_cumpleanios, COUNT(*) AS usuarios FROM db_ronald.fb_ronald GROUP BY dob_month ORDER BY dob_month;',
'16f':'SELECT COUNT(*) AS usuarios_13_25, SUM(mobile_likes) AS likes_celular, SUM(www_likes) AS likes_web, ROUND(AVG(mobile_likes),2) AS promedio_celular, ROUND(AVG(www_likes),2) AS promedio_web FROM db_ronald.fb_ronald WHERE age BETWEEN 13 AND 25;',
'16g':'SELECT COUNT(*) AS usuarios_mayores_25, SUM(mobile_likes) AS likes_celular, SUM(www_likes) AS likes_web, ROUND(AVG(mobile_likes),2) AS promedio_celular, ROUND(AVG(www_likes),2) AS promedio_web FROM db_ronald.fb_ronald WHERE age > 25;',
'validacion':"SELECT COUNT(*) AS filas, SUM(CASE WHEN userid IS NULL THEN 1 ELSE 0 END) AS ids_nulos, SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) AS genero_nulo, SUM(CASE WHEN tenure IS NULL THEN 1 ELSE 0 END) AS tenure_nulo, MIN(age) AS edad_minima, MAX(age) AS edad_maxima FROM db_ronald.fb_ronald;"
}
for name,query in sql.items(): (out/f'{name}.sql').write_text(query+'\n',encoding='utf-8')
