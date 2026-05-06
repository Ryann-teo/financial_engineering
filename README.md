# Portfolio Construction Dashboards: Module A

Three interactive dashboards covering Week 1 of the Portfolio Construction curriculum.

| File | Lesson | Topic |
|------|--------|-------|
| `lesson_01_returns_stylised_facts.html` | 1 | Returns, log returns, stylised facts |
| `lesson_02_portfolio_variance.html`     | 2 | Multivariate distributions and the affine identity |
| `lesson_03_risk_measures.html`          | 3 | Risk measures from variance to drawdown |
| `lesson_05_markowitz.html`              | 5 | The Markowitz problem in four equivalent forms |
| `lesson_06_kkt_constraints.html`        | 6 | KKT, constraints, and the convex programming workflow |
| `lesson_07_risk_budgeting.html`         | 7 | Risk budgeting and the Euler decomposition |
| `lesson_08_sharpe_statistics.html`      | 8 | Sharpe statistics and the Deflated Sharpe Ratio |
| `module_a_exercises.ipynb`              | A | 30 fill-in-the-blank coding exercises (10 per lesson + 3 bonuses) |
| `lessons_09_to_30_outline.md`           | - | Build queue for the remaining 22 lessons |

## Internal docs

- `dashboard_building_guide.md` is a self-instruction document for the agent (Claude or whichever tool picks this up next) on how to build dashboards in the same style. CSS template, math rendering setup, PRNG patterns, Plotly conventions, pedagogical structure.

## Coding companion

The Jupyter notebook `module_a_exercises.ipynb` is the hands-on layer. It ships with synthetic data generators (no internet, no API keys) and 33 exercises in total, each with `___` blanks to fill in and an `assert` to validate your answer. Open it with:

```bash
pip install jupyter numpy pandas scipy statsmodels matplotlib
jupyter notebook module_a_exercises.ipynb
```

Or open the notebook in VS Code (the Python and Jupyter extensions handle it natively).

The matching `.py` files are Marimo equivalents kept around as Python references.

## How to run

**Just open the HTML file in any modern browser.** No install, no Python required. The pages pull KaTeX (math rendering) and Plotly (interactive charts) from CDN.

```
double-click lesson_01_returns_stylised_facts.html
```

For the Python (Marimo) versions:

```bash
pip install -r requirements.txt
marimo edit lesson_01_returns_stylised_facts.py
```

## What is in each dashboard

Every lesson follows the same six block layout:

1. **The big idea.** A short markdown header with the goal.
2. **Inputs panel.** Sliders, dropdowns, toggles for the parameters that matter.
3. **Live plot panel.** Re renders any time you change inputs or your code.
4. **Code editor.** Implement the function for the day. Save with `Ctrl+S` (or `Cmd+S`).
5. **Output panel.** Your function output, validated against expected behaviour.
6. **Self test.** Three questions per lesson: one conceptual, one coding, one numerical.

## Data

Dashboards generate synthetic prices that mimic each asset's stylised behaviour (Student t shocks, GARCH like volatility, leverage effect). No internet or API key required.

If you want real data, replace `synth_prices()` with a `yfinance` call:

```python
import yfinance as yf
prices = yf.download(ticker, period='15y')['Adj Close']
```

## Suggested workflow per lesson

1. Read the "Big idea" markdown at the top.
2. Move the input sliders and watch the plots respond. Build intuition first.
3. Open the code editor block. Read the docstring. Implement the function.
4. Save. Confirm the output panel shows the expected stats.
5. Do the self test. Edit the code if you need to extend it.
6. Write a one paragraph note in `lesson_0X_notes.md` capturing the aha moment.

## Troubleshooting

- **Marimo will not start:** check Python version (3.10+ recommended). `pip install --upgrade marimo`.
- **Plotly plots look empty:** check the data. Print `prices.describe()` to verify.
- **Code editor not saving:** Marimo saves on `Ctrl+S`. The cell underneath will re evaluate within a second.
- **Large arrays slow:** the dashboards cap simulation lengths at 15 years daily by default. Cut `n_years` if your laptop is slow.

## After Module A

Once you can pass the self tests in all three lessons, move to `Portfolio Construction Dashboard Plan.md` and start Week 2 (Markowitz core: Lessons 5, 6, 8).
