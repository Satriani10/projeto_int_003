@echo off
cd /d "%~dp0Library\biblioteca"

:: Inicia o servidor Django
echo Iniciando servidor Django...
start /B python manage.py runserver

timeout /t 5 /nobreak > nul

start http://127.0.0.1:8000/

ENDLOCAL
pause
