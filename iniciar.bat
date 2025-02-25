cd /d "%~dp0Library\biblioteca"

:: Inicia o servidor Django
echo Iniciando servidor Django...
python manage.py runserver

ENDLOCAL
pause