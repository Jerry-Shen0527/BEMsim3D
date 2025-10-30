# BEM3D 运行脚本
# 使用方法: .\run_bem3d.ps1 -c 0 -d 0 -e 1.0 -l 12.5 -o 1024 -w 2.5 -z test

param(
    [string]$c,
    [string]$d,
    [string]$e,
    [string]$l,
    [string]$o,
    [string]$w,
    [string]$z
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 构建命令
$cmd = @(".\build\bem3d.exe")
if ($c) { $cmd += "-c"; $cmd += $c }
if ($d) { $cmd += "-d"; $cmd += $d }
if ($e) { $cmd += "-e"; $cmd += $e }
if ($l) { $cmd += "-l"; $cmd += $l }
if ($o) { $cmd += "-o"; $cmd += $o }
if ($w) { $cmd += "-w"; $cmd += $w }
if ($z) { $cmd += "-z"; $cmd += $z }

Write-Host "运行: $($cmd -join ' ')" -ForegroundColor Green
& $cmd[0] $cmd[1..($cmd.Length-1)]
Write-Host "完成。退出代码: $LASTEXITCODE" -ForegroundColor Green
