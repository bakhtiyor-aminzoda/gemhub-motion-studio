# GemHub Motion Studio — установка для Windows
# powershell -ExecutionPolicy Bypass -File scripts/setup.ps1 [-Check] [-Extra]
param([switch]$Check, [switch]$Extra)
$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$Root = Split-Path -Parent $PSScriptRoot
function Has($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function Step($t) { Write-Host "`n== $t" -ForegroundColor Cyan }
$Core = @('heygen-com/hyperframes','remotion-dev/skills','AbubakrChan/product-launch-motion','greensock/gsap-skills','emilkowalski/skills')
$More = @('pbakaus/impeccable','nextlevelbuilder/ui-ux-pro-max-skill')

Step 'Проверка'
foreach ($c in 'python','node','npx','git','ffmpeg') { if (Has $c) { Write-Host "  есть: $c" } else { Write-Host "  нет:  $c" -ForegroundColor Yellow } }
python -c "import playwright, faster_whisper, numpy, scipy, PIL; print('  Python-пакеты: есть')" 2>$null
if ($LASTEXITCODE -ne 0) { Write-Host '  Python-пакеты: не все' -ForegroundColor Yellow }
if (Test-Path "$HOME\Developer\video-use") { Write-Host '  video-use: есть' } else { Write-Host '  video-use: нет' -ForegroundColor Yellow }
if ($Check) { exit 0 }

Step 'Программы (winget)'
$pkgs = [ordered]@{ 'python'='Python.Python.3.12'; 'node'='OpenJS.NodeJS.LTS'; 'git'='Git.Git'; 'ffmpeg'='Gyan.FFmpeg' }
foreach ($k in $pkgs.Keys) {
  if (-not (Has $k)) {
    if (Has 'winget') { winget install --id $pkgs[$k] -e --accept-source-agreements --accept-package-agreements }
    else { Write-Host "  Поставьте $k вручную" -ForegroundColor Yellow }
  }
}
$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')

Step 'Python-пакеты и браузер'
python -m pip install --upgrade pip
python -m pip install playwright faster-whisper numpy scipy pillow
python -m playwright install chromium

Step 'video-use'
$vu = "$HOME\Developer\video-use"
if (-not (Test-Path $vu)) { New-Item -ItemType Directory -Force "$HOME\Developer" | Out-Null; git clone https://github.com/browser-use/video-use $vu }
Push-Location $vu; python -m pip install -e .; Pop-Location
if (-not (Test-Path "$vu\.env")) { Set-Content "$vu\.env" 'ELEVENLABS_API_KEY=' }

Step 'Скиллы'
$list = $Core; if ($Extra) { $list += $More }
foreach ($r in $list) { npx --yes skills add $r -g -a '*' --skill '*' -y }
npx --yes skills add "$vu" -g -a '*' --skill '*' -y

Set-Content "$Root\.installed" (Get-Date -Format s)
Write-Host "`nГотово. Ключ ElevenLabs впишите в $vu\.env и в .env проекта. В чат ключи не отправляйте." -ForegroundColor Green
