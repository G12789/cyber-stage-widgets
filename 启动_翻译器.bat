@echo off
chcp 65001 >nul
start "" pythonw "%~dp0抖音AI爆款\翻译器.py" 2>nul || start "" python "%~dp0抖音AI爆款\翻译器.py"
exit
