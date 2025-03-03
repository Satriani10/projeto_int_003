@echo off

:: Verifica se o Python está no PATH do sistema
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python não encontrado. Instalando via Microsoft Store...
    winget install -e --id Python.Python.3.12
) ELSE (
    echo Python já está instalado.
)

:: Verifica se o Python está no PATH após a instalação
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Não foi possível encontrar o Python. Verifique a instalação manualmente.
    pause
    exit /b
)

:: Verifica se o pip está instalado
where pip >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Pip não encontrado. Instalando...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
) ELSE (
    echo Pip já está instalado.
)

echo Instalando bibliotecas...
pip install django django-messages

echo Instalação concluída!
pause
