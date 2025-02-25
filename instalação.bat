@echo off
SET PYTHON_URL=https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
SET PYTHON_INSTALLER=python_installer.exe
SET PYTHON_DIR=C:\Python312


where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python não encontrado. Baixando e instalando...
    curl -o %PYTHON_INSTALLER% %PYTHON_URL%
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 TargetDir=%PYTHON_DIR%
    del %PYTHON_INSTALLER%
) ELSE (
    echo Python já está instalado.
)


SET PATH=%PYTHON_DIR%;%PYTHON_DIR%\Scripts;%PATH%


echo Instalando bibliotecas...
pip install django django-messages

echo Instalacao concluída!
pause
