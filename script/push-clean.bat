@echo off
setlocal enabledelayedexpansion

:: 执行你的Git命令
git rev-list --objects --all

:: 创建名为"new"的孤儿分支
git checkout --orphan new
git add .
git commit -m "v0.2.0"

:: 删除旧的main分支（如果需要）
git branch -d main

:: 重命名当前分支为"main"
git branch -m main

:: 强制推送到origin远程仓库
git push -f origin main

:: 设置上游分支并拉取更新
git branch --set-upstream-to=origin/main main
git pull

:: 再次列出所有对象
git rev-list --objects --all

echo 所有操作已完成。
endlocal
