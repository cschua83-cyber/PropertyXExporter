@echo off

echo Closing Edge...
taskkill /F /IM msedge.exe >nul 2>&1

timeout /t 2 >nul

echo Starting Edge Debug Mode...

start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\EdgeDebug"

timeout /t 3 >nul

echo.
echo Edge Started.
echo.

pause