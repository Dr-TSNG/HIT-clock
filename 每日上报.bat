@echo off
FOR /F "delims=" %%I IN ("pip3.exe") DO (if not exist %%~$PATH:I (
echo 未安装python
timeout 2 >nul
))
python3 每日上报.py
timeout 2 >nul