param(
    [string]$Python = "python",
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

if (-not $SkipInstall) {
    & $Python -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('PyInstaller') else 1)" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[info] Installing PyInstaller..."
        & $Python -m pip install --upgrade pip
        & $Python -m pip install --upgrade pyinstaller
    }
}

$bundleName = "HPRAParser"
$pyInstallerArgs = @("--onefile", "--name", $bundleName, "--clean", "trigger/run_parser.py")
& $Python -m PyInstaller @pyInstallerArgs

$exePath = Join-Path $projectRoot "dist\$bundleName.exe"
if (-not (Test-Path $exePath)) {
    throw "Expected executable not found at $exePath"
}

$bundleDir = Join-Path $projectRoot "dist\$bundleName-bundle"
if (Test-Path $bundleDir) {
    Remove-Item -Recurse -Force $bundleDir
}
New-Item -ItemType Directory -Path $bundleDir | Out-Null

Copy-Item $exePath -Destination (Join-Path $bundleDir "$bundleName.exe") -Force

foreach ($sub in @("input", "output")) {
    $targetDir = Join-Path $bundleDir "data\$sub"
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Copy-Item (Join-Path $projectRoot "README.md") -Destination $bundleDir -Force

Write-Host "[done] Bundle folder created at $bundleDir"
Write-Host "Drop HPRA XML files into data\\input and run $bundleName.exe"
