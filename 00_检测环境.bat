@echo off
chcp 65001 >nul
echo ===== 环境检测 =====
echo.

set OK=1

where py >nul 2>&1 && (echo [OK] py 启动器) || (echo [X]  未找到 py)
where python >nul 2>&1 && (echo [OK] python) || (echo [X]  未找到 python)

python -c "import sys; print('[OK] Python', sys.version.split()[0])" 2>nul || (
    echo [X]  Python 不可用 — 请先安装并勾选 Add to PATH
    set OK=0
)

python -c "import tkinter; print('[OK] tkinter')" 2>nul || (
    echo [X]  tkinter 缺失
    set OK=0
)

python -c "import PIL; print('[OK] Pillow', PIL.__version__)" 2>nul || (
    echo [!]  Pillow 未装 — 翻译器梗图需要，请运行 00_安装依赖.bat
)

if exist "%~dp0抖音AI爆款\翻译器.py" (echo [OK] 源码目录) else (
    echo [X]  找不到 抖音AI爆款 文件夹
    set OK=0
)

echo.
if "%OK%"=="1" (echo 环境正常，可以双击启动脚本) else (echo 请先安装 Python)
echo.
pause
