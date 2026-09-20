@echo off
title Analisis Geotecnico - PySection

echo ============================================================
echo       ANALISIS GEOTECNICO DE ESTABILIDAD DE TALUDES
echo ============================================================
echo.
echo Verificando instalacion de Python...
echo.

py --version >nul 2>&1

if errorlevel 1 (
    echo ============================================================
    echo ERROR: Python no esta instalado.
    echo ============================================================
    echo.
    echo Instale Python 3 desde:
    echo https://www.python.org/downloads/
    echo.
    echo Consulte el archivo README.md para obtener instrucciones.
    echo.
    pause
    exit /b 1
)

echo Python encontrado correctamente.
echo.

echo ============================================================
echo INSTALANDO / VERIFICANDO LIBRERIAS
echo ============================================================
echo.

py -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: No fue posible instalar las librerias.
    echo ============================================================
    echo.
    echo Verifique su conexion a Internet.
    echo Consulte la seccion "Solucion de problemas" del README.md.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo LIBRERIAS VERIFICADAS CORRECTAMENTE
echo ============================================================
echo.

echo Iniciando el programa...
echo.

py main.py

echo.
echo ============================================================
echo PROCESO FINALIZADO
echo ============================================================
echo.
echo Revise la carpeta del proyecto para encontrar:
echo - cuna_talud.png
echo - Informe_estabilidad_talud.pdf
echo.
pause
