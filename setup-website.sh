#!/bin/bash
# One-shot setup script. Run from inside this folder.
#
# Prerequisites: you have already created the empty repo on GitHub at
#   https://github.com/Ryann-teo/financial_engineering
# Do NOT initialise it with a README; it must be empty.

set -e

REPO_URL="https://github.com/Ryann-teo/financial_engineering.git"
SITE_URL="https://ryann-teo.github.io/financial_engineering/"

echo "============================================================"
echo "Portfolio Construction Curriculum: one-shot website setup"
echo "============================================================"
echo

# 1. Initialise git if needed
if [ ! -d .git ]; then
  echo "[1/5] Initialising git..."
  git init
else
  echo "[1/5] Git already initialised, skipping."
fi

# 2. Stage everything
echo "[2/5] Staging files..."
git add .

# 3. Initial commit if there is no commit yet
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "[3/5] Creating initial commit..."
  git commit -m "Initial commit: Portfolio Construction curriculum"
else
  echo "[3/5] Repo has commits already. Adding update commit..."
  if git diff --cached --quiet; then
    echo "      No new staged changes."
  else
    git commit -m "Add website index and deployment files"
  fi
fi

# 4. Set up remote
if git remote get-url origin >/dev/null 2>&1; then
  echo "[4/5] Remote 'origin' already exists. Updating URL..."
  git remote set-url origin "$REPO_URL"
else
  echo "[4/5] Adding remote 'origin'..."
  git remote add origin "$REPO_URL"
fi

# Make sure we are on main branch
git branch -M main

# 5. Push
echo "[5/5] Pushing to $REPO_URL ..."
echo "      You may be asked for your GitHub credentials. Use a personal access"
echo "      token as the password (Settings -> Developer settings on GitHub)."
echo
git push -u origin main

echo
echo "============================================================"
echo "Done. Now finish setup on GitHub:"
echo
echo "  1. Go to https://github.com/Ryann-teo/financial_engineering/settings/pages"
echo "  2. Source: Deploy from a branch"
echo "  3. Branch: main, Folder: / (root)"
echo "  4. Save."
echo
echo "After 30 to 60 seconds your site will be live at:"
echo "  $SITE_URL"
echo "============================================================"
