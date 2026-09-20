$ErrorActionPreference = 'Stop'

$installDir = Join-Path $env:LOCALAPPDATA 'Programs\Better Calculator'
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$pathEntries = @($userPath -split ';' | Where-Object { $_ -and $_.Trim() -ne '' -and $_ -ne $installDir })
[Environment]::SetEnvironmentVariable('Path', ($pathEntries -join ';'), 'User')

$shortcutPaths = @(
	(Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\Better Calculator.lnk'),
	(Join-Path ([Environment]::GetFolderPath('Desktop')) 'Better Calculator.lnk')
)
foreach ($shortcutPath in $shortcutPaths) {
	if (Test-Path $shortcutPath) { Remove-Item $shortcutPath -Force }
}
if (Test-Path $installDir) { Remove-Item $installDir -Recurse -Force }

Write-Host 'Better Calculator zostal odinstalowany.' -ForegroundColor Green
Write-Host 'Zamknij i otworz ponownie terminal, aby odswiezyc PATH.'
