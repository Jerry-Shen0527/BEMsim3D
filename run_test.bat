@echo off
REM BEMsim3D 测试脚本 - 单表面模拟
cd /d C:\Users\Pengfei\WorkSpace\repos\BEMsim3D\build
.\bem3d.exe -c 0 -d 0 -e 1.0 -l 12.5 -o 1024 -w 2.5 -z test
pause
