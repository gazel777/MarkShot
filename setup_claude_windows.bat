@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo   Claude Code Windows Setup
echo ==========================================
echo.

set "CLAUDE_DIR=%USERPROFILE%\.claude"
set "SOURCE_DIR=%~dp0claude_config"

:: Claude ディレクトリ作成
if not exist "%CLAUDE_DIR%" (
    mkdir "%CLAUDE_DIR%"
    echo [OK] Created %CLAUDE_DIR%
) else (
    echo [OK] %CLAUDE_DIR% already exists
)

:: サブディレクトリ作成
for %%d in (commands skills templates docs) do (
    if not exist "%CLAUDE_DIR%\%%d" (
        mkdir "%CLAUDE_DIR%\%%d"
        echo [OK] Created %%d directory
    )
)

:: 設定ファイルをコピー
echo.
echo Copying configuration files...

:: settings.json
if exist "%SOURCE_DIR%\settings.json" (
    copy /Y "%SOURCE_DIR%\settings.json" "%CLAUDE_DIR%\settings.json" >nul
    echo [OK] settings.json
)

:: .claudeignore
if exist "%SOURCE_DIR%\.claudeignore" (
    copy /Y "%SOURCE_DIR%\.claudeignore" "%CLAUDE_DIR%\.claudeignore" >nul
    echo [OK] .claudeignore
)

:: .mcp.json
if exist "%SOURCE_DIR%\.mcp.json" (
    copy /Y "%SOURCE_DIR%\.mcp.json" "%CLAUDE_DIR%\.mcp.json" >nul
    echo [OK] .mcp.json
)

:: CLAUDE.md
if exist "%SOURCE_DIR%\CLAUDE.md" (
    copy /Y "%SOURCE_DIR%\CLAUDE.md" "%CLAUDE_DIR%\CLAUDE.md" >nul
    echo [OK] CLAUDE.md
)

:: commands フォルダ
if exist "%SOURCE_DIR%\commands" (
    xcopy /Y /E /I "%SOURCE_DIR%\commands" "%CLAUDE_DIR%\commands" >nul
    echo [OK] commands/
)

:: skills フォルダ
if exist "%SOURCE_DIR%\skills" (
    xcopy /Y /E /I "%SOURCE_DIR%\skills" "%CLAUDE_DIR%\skills" >nul
    echo [OK] skills/
)

:: templates フォルダ
if exist "%SOURCE_DIR%\templates" (
    xcopy /Y /E /I "%SOURCE_DIR%\templates" "%CLAUDE_DIR%\templates" >nul
    echo [OK] templates/
)

:: docs フォルダ
if exist "%SOURCE_DIR%\docs" (
    xcopy /Y /E /I "%SOURCE_DIR%\docs" "%CLAUDE_DIR%\docs" >nul
    echo [OK] docs/
)

echo.
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo Configuration installed to: %CLAUDE_DIR%
echo.
echo Available commands:
echo   /add-feature    - Add new feature
echo   /create-pr      - Create pull request
echo   /fix-issue      - Fix GitHub issue
echo   /init-project   - Initialize project
echo   /review-code    - Code review
echo   /security-check - Security audit
echo.
pause
