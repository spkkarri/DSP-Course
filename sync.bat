@echo off
title DSP Course Auto-Sync
echo =========================================
echo       DSP Course Content Auto-Sync       
echo =========================================
echo.

:: Stage all changes
echo [1/3] Staging updated course files...
git add .

:: Prompt for commit message
set "commit_msg="
set /p commit_msg="Enter what you changed (or press Enter for default 'Update course content'): "
if "%commit_msg%"=="" set commit_msg=Update course content

:: Commit
echo.
echo [2/3] Committing changes...
git commit -m "%commit_msg%"

:: Push to remote
echo.
echo [3/3] Syncing with the cloud...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Sync failed. Make sure you have added your GitHub remote repository.
    echo to add it run: git remote add origin [YOUR_GITHUB_REPO_URL]
) else (
    echo.
    echo 🎉 SUCCESS! All notes, PDFs, and interactive dashboard are updated in the cloud.
)
echo.
pause
