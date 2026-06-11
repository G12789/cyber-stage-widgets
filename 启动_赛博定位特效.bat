@echo off

chcp 65001 >nul

start "" pythonw "%~dp0抖音AI爆款\赛博定位特效.py" 2>nul || start "" python "%~dp0抖音AI爆款\赛博定位特效.py"

exit

