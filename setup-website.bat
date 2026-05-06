@echo off
REM One-shot Windows setup script. Run from this folder by double-clicking,
REM or via: cmd /c setup-website.bat

setlocal

set REPO_URL=https://github.com/Ryann-teo/financial_engineering.git
set SITE_URL=https://ryann-teo.github.io/financial_engineering/

echo ============================================================
echo Portfolio Construction Curriculum: one-shot website setup
echo ============================================================
echo.

REM 1. Initialise git if needed
if not exist ".git" (
  echo [1/5] Initialising git...
  git init
) else (
  echo [1/5] Git already initialised, skipping.
)

REM 2. Stage everything
echo [2/5] Staging files...
git add .

REM 3. Commit
git rev-parse HEAD >nul 2>&1
if errorlevel 1 (
  echo [3/5] Creating initial commit...
  git commit -m "Initial commit: Portfolio Construction curriculum"
) else (
  echo [3/5] Repo has commits already.
  git diff --cached --quiet >nul 2>&1
  if errorlevel 1 (
    git commit -m "Add website index and deployment files"
  ) else (
    echo       No new staged changes.
  )
)

REM 4. Remote
git remote get-url origin >nul 2>&1
if errorlevel 1 (
  echo [4/5] Adding remote origin...
  git remote add origin %REPO_URL%
) else (
  echo [4/5] Remote origin exists, updating URL...
  git remote set-url origin %REPO_URL%
)

git branch -M main

REM 5. Push
echo [5/5] Pushing to %REPO_URL% ...
echo       You may be asked for your GitHub credentials. Use a personal access
echo       token as the password (Settings -^> Developer settings on GitHub).
echo.
git push -u origin main

echo.
echo ============================================================
echo Done. Now finish setup on GitHub:
echo.
echo   1. Go to https://github.com/Ryann-teo/financial_engineering/settings/pages
echo   2. Source: Deploy from a branch
echo   3. Branch: main, Folder: / (root)
echo   4. Save.
echo.
echo After 30 to 60 seconds your site will be live at:
echo   %SITE_URL%
echo ============================================================

endlocal
pause
