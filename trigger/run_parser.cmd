@echo off
setlocal

rem Determine project root (parent of trigger directory)
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_ROOT=%%~fI"
set "PYTHON_DIR=%PROJECT_ROOT%\vendor\python"
set "PYTHON_EXEC=%PYTHON_DIR%\python.exe"

if not exist "%PYTHON_EXEC%" (
    echo [ERROR] Bundled Python runtime not found at "%PYTHON_EXEC%".
    echo         Download the Windows embeddable package from python.org and extract it to:
    echo         %PYTHON_DIR%
    echo         See README for detailed steps.
    pause
    exit /b 1
)

pushd "%PROJECT_ROOT%" >nul
"%PYTHON_EXEC%" "%PROJECT_ROOT%\trigger\run_parser.py" %*
popd >nul

endlocal
