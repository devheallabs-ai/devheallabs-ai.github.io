@echo off
REM DevHeal Labs Website — Local Preview (Windows)
REM Usage: start.bat

echo.
echo   DevHeal Labs Website — Local Preview
echo   =====================================
echo.

where python >nul 2>&1
if %errorlevel%==0 (
    echo   [+] Starting server at http://localhost:9000
    echo   [*] Press Ctrl+C to stop
    echo.
    python -m http.server 9000 --bind 127.0.0.1
    goto :eof
)

where python3 >nul 2>&1
if %errorlevel%==0 (
    echo   [+] Starting server at http://localhost:9000
    echo   [*] Press Ctrl+C to stop
    echo.
    python3 -m http.server 9000 --bind 127.0.0.1
    goto :eof
)

echo   [x] Python not found. Install Python to preview locally.
echo   [*] Or just open index.html in your browser.
