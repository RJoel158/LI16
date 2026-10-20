SELECT gender, COUNT(*) AS usuarios, ROUND(AVG(friend_count),2) AS promedio_amigos FROM db_ronald.fb_ronald WHERE gender IN ('male','female') GROUP BY gender ORDER BY promedio_amigos DESC;
