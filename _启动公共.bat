@echo off
setlocal EnableExtensions
chcp 65001 >nul

set "SCRIPT=%~1"
if not exist "%SCRIPT%" (
    echo.
    echo [错误] 找不到程序文件：
    echo   %SCRIPT%
    echo.
    echo 请确认：启动脚本与「抖音AI爆款」文件夹在同一目录下。
    echo 不要改文件夹名字，也不要把 .py 单独拎出来。
    pause
    exit /b 1
)

set "PYW="
set "PY="

where py >nul 2>&1 && (
    py -3 -c "import sys" >nul 2>&1 && set "PYW=py -3" && set "PY=py -3"
)
if not defined PY where python >nul 2>&1 && set "PYW=pythonw" && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PYW=python3" && set "PY=python3"

for %%V in (313 312 311 310 39 38) do (
    if not defined PY if exist "%LocalAppData%\Programs\Python\Python%%V\python.exe" (
        set "PYW=%LocalAppData%\Programs\Python\Python%%V\pythonw.exe"
        set "PY=%LocalAppData%\Programs\Python\Python%%V\python.exe"
    )
)
for %%V in (313 312 311 310) do (
    if not defined PY if exist "C:\Program Files\Python%%V\python.exe" (
        set "PYW=C:\Program Files\Python%%V\pythonw.exe"
        set "PY=C:\Program Files\Python%%V\python.exe"
    )
)

if not defined PY (
    echo.
    echo ========================================
    echo   这台电脑还没装 Python，所以打不开
    echo ========================================
    echo.
    echo 请按下面做（只需一次）：
    echo   1. 浏览器打开 https://www.python.org/downloads/
    echo   2. 下载 Python 3.12 并安装
    echo   3. 安装时务必勾选 「Add python.exe to PATH」
    echo   4. 装完后双击「00_安装依赖.bat」
    echo   5. 再双击启动脚本
    echo.
    pause
    exit /b 1
)

if exist "%PYW%" (
    start "" "%PYW%" "%SCRIPT%" 2>nul
    if not errorlevel 1 exit /b 0
)

start "" %PY% "%SCRIPT%"
exit /b %errorlevel%
