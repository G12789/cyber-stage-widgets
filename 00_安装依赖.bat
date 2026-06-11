@echo off
chcp 65001 >nul
echo 正在安装 Pillow（翻译器梗图需要）...
python -m pip install -r "%~dp0requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    py -3 -m pip install -r "%~dp0requirements.txt" -i https://pypi.tuna.tsinghua.edu.cn/simple
)
echo.
echo 完成。请再运行 00_检测环境.bat 确认。
pause
