@echo off
chcp 65001 >nul
start "" pythonw "%~dp0抖音AI爆款\生僻字发音器.py" 2>nul || start "" python "%~dp0抖音AI爆款\生僻字发音器.py"
exit
