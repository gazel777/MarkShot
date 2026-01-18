@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "LOGFILE=%~dp0install_log.txt"
set "TARGET=%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
set "SOURCE=%~dp0MarkShot.py"

echo MarkShot Test Installer
echo =======================
echo.

REM Start log file
echo ======================================== > "%LOGFILE%"
echo MarkShot Install Log >> "%LOGFILE%"
echo %date% %time% >> "%LOGFILE%"
echo ======================================== >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM Log system info
echo [System Info] >> "%LOGFILE%"
for /f "tokens=*" %%i in ('ver') do echo Windows: %%i >> "%LOGFILE%"
echo APPDATA: %APPDATA% >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM Log paths
echo [Paths] >> "%LOGFILE%"
echo Source: %SOURCE% >> "%LOGFILE%"
echo Target: %TARGET% >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM Check source file
echo [Process] >> "%LOGFILE%"
if not exist "%SOURCE%" (
    echo [ERROR] MarkShot.py not found! >> "%LOGFILE%"
    echo Source file does not exist >> "%LOGFILE%"
    echo.
    echo [ERROR] MarkShot.py not found!
    echo Please place this file in the same folder as MarkShot.py
    echo.
    echo Log saved: %LOGFILE%
    echo.
    pause
    exit /b 1
)
echo Source file found: OK >> "%LOGFILE%"

REM Create target folder if needed
if not exist "%TARGET%" (
    echo Creating target folder... >> "%LOGFILE%"
    mkdir "%TARGET%" 2>> "%LOGFILE%"
    if !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to create folder >> "%LOGFILE%"
        echo [ERROR] Failed to create folder
        echo Log saved: %LOGFILE%
        pause
        exit /b 1
    )
    echo Target folder created: OK >> "%LOGFILE%"
) else (
    echo Target folder exists: OK >> "%LOGFILE%"
)

REM Copy file
copy /Y "%SOURCE%" "%TARGET%\MarkShot.py" >> "%LOGFILE%" 2>&1

if %ERRORLEVEL% EQU 0 (
    echo. >> "%LOGFILE%"
    echo [RESULT] SUCCESS >> "%LOGFILE%"
    echo Installed to: %TARGET%\MarkShot.py >> "%LOGFILE%"
    echo.
    echo [OK] MarkShot.py installed successfully!
    echo.
    echo Location: %TARGET%\MarkShot.py
    echo.
    echo Next: Restart DaVinci Resolve and test.
) else (
    echo. >> "%LOGFILE%"
    echo [RESULT] FAILED >> "%LOGFILE%"
    echo Copy command failed with error code: %ERRORLEVEL% >> "%LOGFILE%"
    echo.
    echo [ERROR] Installation failed.
)

echo.
echo ======================================== >> "%LOGFILE%"
echo Log saved: %LOGFILE%
echo.
pause
