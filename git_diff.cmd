@echo off
if exist d:\temp\git.out del d:\temp\git.out
git diff %1 %2 --color=never > d:\temp\git.out
D:\bin\Akelpad\AkelPad.exe d:\temp\git.out
rem --cached
rem --staged
