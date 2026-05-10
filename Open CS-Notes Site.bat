@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "URL=http://localhost:3000/#/"
set "HEALTH_URL=http://localhost:3000/"

where npm >nul 2>nul
if errorlevel 1 (
  echo npm was not found.
  echo Install Node.js from https://nodejs.org/ and try again.
  echo.
  pause
  exit /b 1
)

if not exist "node_modules\.bin\docsify.cmd" (
  echo Installing CS-Notes dependencies. This is only needed the first time.
  echo.
  call npm install
  if errorlevel 1 (
    echo.
    echo npm install failed.
    pause
    exit /b 1
  )
)

call :check_site
if "!SITE_READY!"=="1" (
  echo CS-Notes already appears to be running.
  start "" "%URL%"
  exit /b 0
)

echo Starting CS-Notes...
echo URL: %URL%
echo.

start "CS-Notes Docsify Server" cmd /k "cd /d ""%~dp0"" && npm run docs:serve"

for /L %%I in (1,1,60) do (
  timeout /t 1 /nobreak >nul
  call :check_site
  if "!SITE_READY!"=="1" (
    echo CS-Notes is running at %URL%
    start "" "%URL%"
    exit /b 0
  )
)

echo Timed out waiting for Docsify to start.
echo Check the "CS-Notes Docsify Server" window for details.
echo.
pause
exit /b 1

:check_site
set "SITE_READY=0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $response = Invoke-WebRequest -UseBasicParsing -Uri '%HEALTH_URL%' -TimeoutSec 2; if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { exit 0 }; exit 1 } catch { exit 1 }" >nul 2>nul
if not errorlevel 1 set "SITE_READY=1"
exit /b 0
