param([string[]]$Ids)
$taskRoot=Split-Path $PSScriptRoot -Parent
foreach($taskId in $Ids){
 $taskFile=Join-Path $taskRoot "proyecto/sql/$taskId.sql"
 docker cp $taskFile "li16-ronald-hive-server-1:/tmp/$taskId.sql" | Out-Null
 & "$PSScriptRoot/registrar.ps1" -Id $taskId -Titulo "Punto $taskId Consulta ejecutada en Apache Hive" -Comando "docker exec li16-ronald-hive-server-1 beeline -u jdbc:hive2://localhost:10000 -n hive --silent=true --showHeader=true --outputformat=tsv2 -f /tmp/$taskId.sql"
}
