rem @echo off
if exist d:\temp\git.out del d:\temp\git.out
git log --pretty=oneline --abbrev-commit --graph --date=short --decorate=full -5 > d:\temp\git.out
rem --pretty=format:"<%h> %s %d " 
rem > d:\temp\git.out
D:\bin\Akelpad\AkelPad.exe d:\temp\git.out
