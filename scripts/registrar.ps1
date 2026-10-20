param([Parameter(Mandatory=$true)][string]$Id,[Parameter(Mandatory=$true)][string]$Titulo,[Parameter(Mandatory=$true)][string]$Comando)
$ErrorActionPreference = 'Continue'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskStart = Get-Date
$taskOutput = (& ([scriptblock]::Create($Comando)) 2>&1 | Out-String -Width 210)
$taskExit = $LASTEXITCODE
$taskRecord = [ordered]@{id=$Id;titulo=$Titulo;fecha=$taskStart.ToString('o');comando=$Comando;salida=$taskOutput;exit_code=$taskExit}
$taskRecord | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot "registros/$Id.json") -Encoding utf8
$taskOutput
