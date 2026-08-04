@echo off
REM connect_my_code launcher (Windows cmd.exe / PowerShell).
REM
REM   cmc extract .
REM
REM Picks the first usable interpreter: %CMC_PYTHON%, then the py launcher,
REM then python on PATH. Nothing is installed.
setlocal

if defined CMC_PYTHON (
    "%CMC_PYTHON%" "%~dp0cmc.py" %*
    exit /b %ERRORLEVEL%
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    py -3 "%~dp0cmc.py" %*
    exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
    python "%~dp0cmc.py" %*
    exit /b %ERRORLEVEL%
)

echo connect_my_code: no Python interpreter found on PATH. >&2
echo Install Python 3.10+ or set CMC_PYTHON=C:\path\to\python.exe >&2
exit /b 127
