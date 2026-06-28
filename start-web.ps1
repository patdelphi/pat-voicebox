# 启动 Voicebox 后端和 Web 前端开发服务。
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File .\start-web.ps1
#
# 脚本会打开两个新的 PowerShell 窗口：
#   1. 后端 API：http://127.0.0.1:17493
#   2. Web 前端：http://localhost:5173

[CmdletBinding()]
param(
  [int]$BackendPort = 17493,
  [int]$FrontendPort = 5173,
  [switch]$OpenBrowser
)

$ErrorActionPreference = 'Stop'

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot 'backend\venv\Scripts\python.exe'

if (-not (Test-Path -LiteralPath $Python)) {
  throw "未找到后端虚拟环境 Python：$Python。请先创建并安装 backend 依赖。"
}

$BunCommand = Get-Command bun -ErrorAction SilentlyContinue
if (-not $BunCommand) {
  throw "未找到 bun。请先安装 Bun，或确认 bun 已加入 PATH。"
}

function Start-DevWindow {
  param(
    [string]$Title,
    [string]$Command
  )

  $WrappedCommand = "`$Host.UI.RawUI.WindowTitle = '$Title'; Set-Location -LiteralPath '$ProjectRoot'; $Command"
  Start-Process powershell.exe -ArgumentList @(
    '-NoExit',
    '-ExecutionPolicy',
    'Bypass',
    '-Command',
    $WrappedCommand
  )
}

Start-DevWindow `
  -Title 'Voicebox Backend' `
  -Command "& '$Python' -m uvicorn backend.main:app --reload --port $BackendPort"

Start-Sleep -Seconds 2

Start-DevWindow `
  -Title 'Voicebox Web' `
  -Command "Set-Location -LiteralPath (Join-Path '$ProjectRoot' 'web'); bun run dev -- --port $FrontendPort"

Write-Host "后端正在启动：http://127.0.0.1:$BackendPort"
Write-Host "Web 前端正在启动：http://localhost:$FrontendPort"

if ($OpenBrowser) {
  Start-Sleep -Seconds 3
  Start-Process "http://localhost:$FrontendPort"
}
