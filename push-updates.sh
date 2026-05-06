#!/bin/bash
# Auto-push script for the financial_engineering site.
# Run this whenever you have updated lesson HTMLs and want them deployed.

set -e

echo "Checking for changes..."
if git diff --quiet && git diff --cached --quiet; then
  if [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "No changes to push. Exiting."
    exit 0
  fi
fi

echo "Changes detected. Staging..."
git add .

# Show a summary of staged changes
echo
echo "Staged changes:"
git diff --cached --stat

echo
read -p "Commit message (or press Enter for default): " msg
if [ -z "$msg" ]; then
  msg="Update site - $(date +'%Y-%m-%d %H:%M:%S')"
fi

git commit -m "$msg"
git push origin main

echo
echo "Pushed to origin/main."
echo "GitHub Pages will rebuild within 30 to 60 seconds."
echo "Site: https://ryann-teo.github.io/financial_engineering/"
