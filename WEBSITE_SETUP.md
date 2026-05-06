# Website Setup and Deployment

This folder is the source for the **Portfolio Construction Curriculum** website hosted on GitHub Pages at:

> **https://ryann-teo.github.io/financial_engineering/**

The repository is at:

> **https://github.com/Ryann-teo/financial_engineering**

## How it works

- This folder is a git repository connected to the remote on GitHub.
- `index.html` is the navigation hub. Other `lesson_*.html` files are the lesson dashboards.
- When you push to the `main` branch, GitHub Pages auto-rebuilds within 30 to 60 seconds.

## One-time setup (you only need to do this once)

**Easiest path: run the included setup script.**

Open a terminal in this folder and run:

```bash
# Mac / Linux / Git Bash
./setup-website.sh
```

```cmd
:: Windows command prompt
setup-website.bat
```

The script does git init, stages everything, commits, adds the remote, and pushes. It then prints the next step (enabling Pages on GitHub).

**Manual path** (if you prefer to run each command yourself):

```bash
cd "C:/Users/ryant/Documents/Big Brain/Areas/Global Macro/Teaching Materials/Portfolio Dashboards"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/Ryann-teo/financial_engineering.git
git branch -M main
git push -u origin main
```

If git is already initialised, you only need to push:

```bash
git push -u origin main
```

### Authentication

GitHub no longer accepts plain passwords from the command line. Use one of:

1. **Personal Access Token (easiest).** GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token. Give it `repo` scope. Use the token as your password when git prompts.
2. **SSH keys.** Set up at https://docs.github.com/en/authentication/connecting-to-github-with-ssh and change the remote with `git remote set-url origin git@github.com:Ryann-teo/financial_engineering.git`.

## Enable GitHub Pages

After your first push:

1. Go to https://github.com/Ryann-teo/financial_engineering
2. Settings → Pages (left sidebar)
3. Source: "Deploy from a branch"
4. Branch: **main**, folder: **/ (root)**
5. Save

The first build takes about a minute. Subsequent builds take 30 seconds.

## Workflow: every time you update a lesson

After Claude updates an HTML file (or you do), run:

### Mac / Linux / Git Bash

```bash
./push-updates.sh
```

### Windows command prompt

```cmd
push-updates.bat
```

### Or manually (any platform)

```bash
git add .
git commit -m "Update lesson"
git push origin main
```

The `push-updates` scripts handle staging, commit message, and push in one step. They also print the live URL for you to verify.

## Verifying the site

Live at https://ryann-teo.github.io/financial_engineering/

If it does not appear:

- Wait 60 seconds for the first build.
- Repository → Actions tab: check that the "pages build and deployment" workflow succeeded.
- Settings → Pages: confirm the source branch is `main` and folder is `/ (root)`.

## Folder structure on GitHub

The same folder you are looking at right now becomes the root of the site:

```
/                                        (your live root)
├── index.html                           (navigation hub)
├── lesson_01_returns_stylised_facts.html
├── lesson_02_portfolio_variance.html
├── lesson_03_risk_measures.html
├── lesson_05_markowitz.html
├── lesson_06_kkt_constraints.html
├── lesson_07_risk_budgeting.html
├── lesson_08_sharpe_statistics.html
├── module_a_exercises.ipynb
├── README.md
├── dashboard_building_guide.md
├── lessons_09_to_30_outline.md
└── (lesson_*.py marimo files, kept for reference)
```

URLs:
- Hub: https://ryann-teo.github.io/financial_engineering/
- Lesson 5: https://ryann-teo.github.io/financial_engineering/lesson_05_markowitz.html

## Adding a new lesson

When Claude (or you) creates a new `lesson_NN_*.html` file:

1. **Update `index.html`** to flip the corresponding card from `pending` to `live`. Find the card, change the badge class from `pending` to `live`, change `<div class="card pending">` to `<a href="lesson_NN_*.html" class="card">`, change the badge text from "Coming soon" to "Live".
2. **Run `./push-updates.sh`** (or the Windows equivalent).
3. **Wait 30 to 60 seconds** for GitHub Pages to rebuild.

That is the whole loop.

## Troubleshooting

- **`git push` rejected with "non-fast-forward"**. Someone (or another machine) pushed first. Run `git pull --rebase` then `git push`.
- **GitHub Pages does not update**. Check Settings → Pages and confirm source. Wait a minute. Check the Actions tab.
- **HTML files render as raw code**. The file name must end in `.html` and the content must start with `<!DOCTYPE html>`.
- **KaTeX or Plotly does not load**. The CDN links are absolute https URLs. Check the browser console for blocked content. (GitHub Pages serves over https.)
