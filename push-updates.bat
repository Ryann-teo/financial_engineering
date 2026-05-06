@echo off
REM Auto-push script for the financial_engineering site (Windows batch).
REM Run this whenever you have updated lesson HTMLs.

echo Checking for changes...
git diff --quiet
if %errorlevel%==0 (
  git diff --cached --quiet
  if %errorlevel%==0 (
    echo No changes to push. Exiting.
    exit /b 0
  )
)

echo Staging changes...
git add .
git status --short

set /p msg=Commit message (Enter for default):
if "%msg%"=="" set msg=Update site - %date% %time%

git commit -m "%msg%"
git push origin main

echo.
echo Pushed to origin/main.
echo GitHub Pages will rebuild within 30 to 60 seconds.
echo Site: https://ryann-teo.github.io/financial_engineering/
