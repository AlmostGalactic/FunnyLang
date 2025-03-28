@echo off
REM Run your Funny language interpreter with a given file

if "%1"=="" (
    echo Usage: funny.bat filename.funny
    exit /b 1
)

python funny.py %1
pause
