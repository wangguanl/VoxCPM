# ============================================================
#  VoxCPM2 一键启动脚本 (Windows PowerShell)
#  功能：合并最新注册表 User PATH -> 校验模型 -> 启动 Web Demo
#  用法：右键 "使用 PowerShell 运行" 或在本目录执行 .\start_voxcpm.ps1
# ============================================================

# 允许脚本执行（若当前会话策略限制，取消注释下一行）
# Set-ExecutionPolicy -Scope Process Bypass -Force

# 0. 合并最新注册表 User PATH，覆盖 toolhost 继承的旧快照
$env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User") + ";" + $env:PATH

# 1. 路径配置 -------------------------------------------------
$ProjectRoot   = "E:\Pro2\VoxCPM"
$PythonExe     = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$AppScript     = Join-Path $ProjectRoot "app.py"
$ModelRoot     = "E:\huggingface_cache\modelscope"
$ModelId       = Join-Path $ModelRoot "models\OpenBMB\VoxCPM2"
$Port          = 8808

# 2. 环境变量 -------------------------------------------------
$env:MODELSCOPE_CACHE             = $ModelRoot
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"
# 若未显式指定且本地已存在降噪模型，则指向本地路径避免重复下载
if (-not $env:VOXCPM_ZIPENHANCER_PATH) {
    $localZip = Join-Path $ModelRoot "models\iic\speech_zipenhancer_ans_multiloss_16k_base"
    if (Test-Path $localZip) {
        $env:VOXCPM_ZIPENHANCER_PATH = $localZip
    }
}

# 3. 前置检查 -------------------------------------------------
$fail = $false
if (-not (Test-Path $PythonExe))  { Write-Host "[X] 未找到虚拟环境解释器: $PythonExe"  -ForegroundColor Red;   $fail = $true }
if (-not (Test-Path $AppScript))  { Write-Host "[X] 未找到启动脚本: $AppScript"      -ForegroundColor Red;   $fail = $true }
if (-not (Test-Path $ModelId))    { Write-Host "[X] 未找到模型: $ModelId"            -ForegroundColor Red;   $fail = $true }
if ($fail) { Write-Host "请先检查下载与依赖同步，脚本中止。" -ForegroundColor Yellow; exit 1 }

# 4. 端口占用检查并提示 -----------------------------------------
$inUse = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($inUse) {
    Write-Host "[!] 端口 $Port 已被占用，可能已有实例在运行。" -ForegroundColor Yellow
    Write-Host "    如需重启，请先关闭旧进程，或修改下方 \$Port 变量。" -ForegroundColor Yellow
}

# 5. 启动服务 -------------------------------------------------
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  VoxCPM2 Web Demo 启动中..."                 -ForegroundColor Cyan
Write-Host "  模型目录 : $ModelId"                        -ForegroundColor Cyan
Write-Host "  访问地址 : http://localhost:$Port"          -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "首次加载模型需数分钟，请耐心等待日志出现 'Running on' 后即可访问。" -ForegroundColor DarkGray

& $PythonExe -u $AppScript --model-id $ModelId --port $Port --device auto
exit $LASTEXITCODE