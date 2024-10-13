@echo off
set "currentFolder=%~dp0"
set "folderName=%currentFolder:~0,-1%"
for %%i in ("%folderName%") do set "folderName=%%~nxi"
set "urlPrefix=https://git.hcat.work/Yokaze/"
set "fullUrl=%urlPrefix%%folderName%"
echo %fullUrl%
git remote add gitcat %fullUrl%

git init
git add .
git commit -m "-"
git push gitcat