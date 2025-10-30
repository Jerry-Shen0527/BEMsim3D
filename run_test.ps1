# BEMsim3D 测试脚本 - 单表面模拟
# 用法: .\run_test.ps1

Set-Location c:\Users\Pengfei\WorkSpace\repos\BEMsim3D\build

Write-Host "运行: bem3d -c 0 -d 0 -e 1.0 -l 12.5 -o 1024 -w 2.5 -z test" -ForegroundColor Cyan
Write-Host ""

.\bem3d.exe -c 0 -d 0 -e 1.0 -l 12.5 -o 1024 -w 2.5 -z test

Write-Host ""
Write-Host "输出文件: ../data/test/BRDF_wvl0_wi0.binary" -ForegroundColor Green
