"""
Lesson 2: Multivariate Distributions and the Affine Identity.

Module A, Week 1, Lesson 2 of the Portfolio Construction curriculum.

Run with:
    marimo edit lesson_02_portfolio_variance.py
"""

import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from scipy import stats

    return go, make_subplots, np


@app.cell
def _(mo):
    mo.md(r"""
    # Lesson 2: Multivariate Distributions and the Affine Identity

    A portfolio return is a **linear function** of asset returns:

    $$r_p = w^\top r$$

    Its mean and variance are linear and quadratic functions of $w$:

    $$\mathbb{E}[r_p] = w^\top \mu \qquad \text{Var}(r_p) = w^\top \Sigma w$$

    Slide $w$ in the simplex below. Watch the joint return cloud,
    the **covariance ellipsoid**, and the projection onto the $w$
    direction respond. The 1D variance of the projection equals
    $w^\top \Sigma w$ exactly.
    """)
    return


@app.cell
def _(mo):
    n_assets = mo.ui.radio(options=["2", "3"], value="2", label="Number of assets")
    n_sims = mo.ui.slider(start=300, stop=5000, step=100, value=1500, label="Simulated draws")
    dist = mo.ui.radio(options=["Gaussian", "Student t (df=4)"], value="Gaussian", label="Joint distribution")
    return dist, n_assets, n_sims


@app.cell
def _(dist, mo, n_assets, n_sims):
    mo.hstack([n_assets, n_sims, dist], justify="start", gap=2)
    return


@app.cell
def _(mo):
    # Two-asset sliders
    mu1 = mo.ui.slider(start=-0.05, stop=0.20, step=0.005, value=0.08, label="mu_1 (asset 1 mean)")
    mu2 = mo.ui.slider(start=-0.05, stop=0.20, step=0.005, value=0.05, label="mu_2 (asset 2 mean)")
    sigma1 = mo.ui.slider(start=0.05, stop=0.50, step=0.01, value=0.20, label="sigma_1 (asset 1 vol)")
    sigma2 = mo.ui.slider(start=0.05, stop=0.50, step=0.01, value=0.10, label="sigma_2 (asset 2 vol)")
    rho12 = mo.ui.slider(start=-0.95, stop=0.95, step=0.05, value=-0.20, label="rho_12")

    # Asset 3 sliders (used only if n_assets == 3)
    mu3 = mo.ui.slider(start=-0.05, stop=0.20, step=0.005, value=0.06, label="mu_3 (asset 3 mean)")
    sigma3 = mo.ui.slider(start=0.05, stop=0.50, step=0.01, value=0.15, label="sigma_3 (asset 3 vol)")
    rho13 = mo.ui.slider(start=-0.95, stop=0.95, step=0.05, value=0.10, label="rho_13")
    rho23 = mo.ui.slider(start=-0.95, stop=0.95, step=0.05, value=-0.10, label="rho_23")

    # Weights
    w1 = mo.ui.slider(start=-0.5, stop=1.5, step=0.05, value=0.6, label="w_1 (weight on asset 1)")
    w2 = mo.ui.slider(start=-0.5, stop=1.5, step=0.05, value=0.4, label="w_2 (weight on asset 2 if N=3)")
    return mu1, mu2, mu3, rho12, rho13, rho23, sigma1, sigma2, sigma3, w1, w2


@app.cell
def _(
    mo,
    mu1,
    mu2,
    mu3,
    n_assets,
    rho12,
    rho13,
    rho23,
    sigma1,
    sigma2,
    sigma3,
    w1,
    w2,
):
    if n_assets.value == "2":
        rows = mo.vstack([
            mo.hstack([mu1, sigma1], gap=2),
            mo.hstack([mu2, sigma2], gap=2),
            mo.hstack([rho12, w1], gap=2),
        ])
    else:
        rows = mo.vstack([
            mo.hstack([mu1, sigma1], gap=2),
            mo.hstack([mu2, sigma2], gap=2),
            mo.hstack([mu3, sigma3], gap=2),
            mo.hstack([rho12, rho13, rho23], gap=2),
            mo.hstack([w1, w2], gap=2),
        ])
    rows
    return


@app.cell
def _(
    mu1,
    mu2,
    mu3,
    n_assets,
    np,
    rho12,
    rho13,
    rho23,
    sigma1,
    sigma2,
    sigma3,
    w1,
    w2,
):
    if n_assets.value == "2":
        mu = np.array([mu1.value, mu2.value])
        Sigma = np.array([
            [sigma1.value ** 2, rho12.value * sigma1.value * sigma2.value],
            [rho12.value * sigma1.value * sigma2.value, sigma2.value ** 2],
        ])
        # 2 assets: w_2 = 1 - w_1
        w = np.array([w1.value, 1 - w1.value])
    else:
        mu = np.array([mu1.value, mu2.value, mu3.value])
        Sigma = np.array([
            [
                sigma1.value ** 2,
                rho12.value * sigma1.value * sigma2.value,
                rho13.value * sigma1.value * sigma3.value,
            ],
            [
                rho12.value * sigma1.value * sigma2.value,
                sigma2.value ** 2,
                rho23.value * sigma2.value * sigma3.value,
            ],
            [
                rho13.value * sigma1.value * sigma3.value,
                rho23.value * sigma2.value * sigma3.value,
                sigma3.value ** 2,
            ],
        ])
        # 3 assets: w_3 = 1 - w_1 - w_2
        w = np.array([w1.value, w2.value, 1 - w1.value - w2.value])
    return Sigma, mu, w


@app.cell
def _(Sigma, np):
    # Sanity check: Sigma should be positive semi definite. Project the smallest
    # eigenvalue up to zero if a slider combo creates an invalid matrix.
    eigvals = np.linalg.eigvalsh(Sigma)
    psd_ok = bool(eigvals.min() > -1e-10)
    return eigvals, psd_ok


@app.cell
def _(Sigma, dist, mu, n_assets, n_sims, np):
    rng = np.random.default_rng(0)
    if dist.value == "Gaussian":
        try:
            sample = rng.multivariate_normal(mu, Sigma, size=n_sims.value)
        except np.linalg.LinAlgError:
            # If user picks a non PSD config, fall back to nearest PSD via clipping
            w_, V = np.linalg.eigh(Sigma)
            w_ = np.clip(w_, 1e-8, None)
            S2 = V @ np.diag(w_) @ V.T
            sample = rng.multivariate_normal(mu, S2, size=n_sims.value)
    else:
        df = 4
        # Multivariate t = MV normal scaled by sqrt(df / chi2_df)
        z = rng.multivariate_normal(np.zeros(int(n_assets.value)), Sigma, size=n_sims.value)
        u = rng.chisquare(df, size=n_sims.value)
        sample = mu + z / np.sqrt(u / df)[:, None]
    return (sample,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Code it yourself

    Three functions, each one line of math.

    1. `portfolio_var(w, Sigma)` returns $w^\top \Sigma w$.
    2. `portfolio_mean(w, mu)` returns $w^\top \mu$.
    3. `min_var_two_asset(sigma1, sigma2, rho)` returns the closed form
       $w_1^\star$ that minimises portfolio variance for the 2 asset case:

       $$w_1^\star = \frac{\sigma_2^2 - \rho \sigma_1 \sigma_2}{\sigma_1^2 + \sigma_2^2 - 2 \rho \sigma_1 \sigma_2}$$
    """)
    return


@app.cell
def _(mo):
    code_editor = mo.ui.code_editor(
        value='''def portfolio_var(w, Sigma):
    """Return w' Sigma w."""
    import numpy as np
    return float(w @ Sigma @ w)


    def portfolio_mean(w, mu):
    """Return w' mu."""
    import numpy as np
    return float(w @ mu)


    def min_var_two_asset(sigma1, sigma2, rho):
    """Closed form minimum variance weight on asset 1 for the 2 asset case."""
    num = sigma2 ** 2 - rho * sigma1 * sigma2
    den = sigma1 ** 2 + sigma2 ** 2 - 2 * rho * sigma1 * sigma2
    return num / den
    ''',
        language="python",
        label="Edit and save (Ctrl/Cmd + S)",
    )
    return (code_editor,)


@app.cell
def _(code_editor):
    code_editor
    return


@app.cell
def _(Sigma, code_editor, mo, mu, n_assets, rho12, sigma1, sigma2, w):
    user_globals: dict = {}
    err = None
    pv = pm = w1_star = None
    try:
        exec(code_editor.value, user_globals)
        portfolio_var = user_globals["portfolio_var"]
        portfolio_mean = user_globals["portfolio_mean"]
        min_var_two_asset = user_globals["min_var_two_asset"]

        pv = portfolio_var(w, Sigma)
        pm = portfolio_mean(w, mu)
        if n_assets.value == "2":
            w1_star = min_var_two_asset(sigma1.value, sigma2.value, rho12.value)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"

    if err is not None:
        out = mo.md(f"**Implementation incomplete.** `{err}`")
    else:
        rows_md = (
            f"| Portfolio mean (annualised) | {pm:+.2%} |\n"
            f"| Portfolio variance | {pv:.6f} |\n"
            f"| Portfolio volatility (annualised) | {pv ** 0.5:.2%} |\n"
        )
        if n_assets.value == "2":
            rows_md += f"| Closed form min-var weight on asset 1 | {w1_star:+.4f} |\n"
        out = mo.md(
            f"""
            ### Live portfolio statistics

            | Metric | Value |
            |--------|-------|
            {rows_md}

            Move the `w_1` slider until you find the minimum on the
            "Portfolio variance vs w_1" plot below. It should match the
            closed form value.
            """
        )
    out
    return


@app.cell
def _(Sigma, code_editor, go, make_subplots, mu, n_assets, np, sample, w):
    # Recover user functions for live computation
    user_globals: dict = {}
    exec(code_editor.value, user_globals)
    portfolio_var = user_globals.get("portfolio_var", lambda w, S: float(w @ S @ w))
    portfolio_mean = user_globals.get("portfolio_mean", lambda w, m: float(w @ m))

    # Sweep w_1 from -0.5 to 1.5 (with the budget constraint: w_2 = 1 - w_1 in 2 asset case)
    if n_assets.value == "2":
        w1_grid = np.linspace(-0.5, 1.5, 200)
        var_grid = np.array([portfolio_var(np.array([x, 1 - x]), Sigma) for x in w1_grid])
        mean_grid = np.array([portfolio_mean(np.array([x, 1 - x]), mu) for x in w1_grid])
    else:
        # Sweep w_1, hold w_2 at current value, w_3 = 1 - w_1 - w_2
        w1_grid = np.linspace(-0.5, 1.5, 200)
        w2_now = w[1]
        var_grid = np.array([
            portfolio_var(np.array([x, w2_now, 1 - x - w2_now]), Sigma) for x in w1_grid
        ])
        mean_grid = np.array([
            portfolio_mean(np.array([x, w2_now, 1 - x - w2_now]), mu) for x in w1_grid
        ])

    sigma_grid = np.sqrt(var_grid)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Joint return cloud (assets 1 vs 2)",
            "Projection onto the w direction",
            "Portfolio variance vs w_1",
            "Mini efficient frontier (sweep w_1)",
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.12,
    )

    # 1. Joint return cloud (assets 1 and 2)
    fig.add_trace(
        go.Scatter(
            x=sample[:, 0], y=sample[:, 1], mode="markers",
            marker=dict(size=3, opacity=0.4),
            showlegend=False,
        ),
        row=1, col=1,
    )

    # Covariance ellipsoid (1 sigma) for the first two assets
    Sigma2 = Sigma[:2, :2]
    eigvals, eigvecs = np.linalg.eigh(Sigma2)
    theta = np.linspace(0, 2 * np.pi, 100)
    ellipse = (
        np.array([np.sqrt(eigvals[0]) * np.cos(theta), np.sqrt(eigvals[1]) * np.sin(theta)])
    )
    ellipse = eigvecs @ ellipse + mu[:2, None]
    fig.add_trace(
        go.Scatter(
            x=ellipse[0], y=ellipse[1], mode="lines",
            line=dict(color="red", width=2),
            name="1 sigma ellipsoid",
        ),
        row=1, col=1,
    )

    # The w direction (vector from origin)
    fig.add_trace(
        go.Scatter(
            x=[mu[0], mu[0] + 0.3 * w[0]],
            y=[mu[1], mu[1] + 0.3 * w[1]],
            mode="lines+markers",
            line=dict(color="green", width=3),
            marker=dict(size=8),
            name="w direction",
        ),
        row=1, col=1,
    )

    # 2. Projection onto w direction (1D histogram of w' r)
    proj = sample @ w
    fig.add_trace(
        go.Histogram(x=proj, nbinsx=60, marker_color="green", opacity=0.6, showlegend=False),
        row=1, col=2,
    )

    # 3. Portfolio variance vs w_1
    fig.add_trace(
        go.Scatter(x=w1_grid, y=var_grid, mode="lines", line=dict(color="navy"), name="variance"),
        row=2, col=1,
    )
    # Highlight current w_1
    fig.add_trace(
        go.Scatter(
            x=[w[0]], y=[float(w @ Sigma @ w)],
            mode="markers", marker=dict(size=10, color="red"),
            name="current",
        ),
        row=2, col=1,
    )

    # 4. Mini efficient frontier
    fig.add_trace(
        go.Scatter(x=sigma_grid, y=mean_grid, mode="lines", line=dict(color="navy"), name="frontier"),
        row=2, col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=[float(np.sqrt(w @ Sigma @ w))], y=[float(w @ mu)],
            mode="markers", marker=dict(size=10, color="red"),
            name="current",
        ),
        row=2, col=2,
    )

    fig.update_xaxes(title_text="r_1", row=1, col=1)
    fig.update_yaxes(title_text="r_2", row=1, col=1)
    fig.update_xaxes(title_text="w' r", row=1, col=2)
    fig.update_xaxes(title_text="w_1", row=2, col=1)
    fig.update_yaxes(title_text="variance", row=2, col=1)
    fig.update_xaxes(title_text="portfolio sigma", row=2, col=2)
    fig.update_yaxes(title_text="portfolio mean", row=2, col=2)
    fig.update_layout(height=800, showlegend=False)
    fig
    return (eigvals,)


@app.cell
def _(eigvals, mo, psd_ok):
    if not psd_ok:
        warn = mo.md(
            f"**Warning:** the current correlation choice produces a non PSD covariance "
            f"(min eigenvalue = {eigvals.min():.4f}). The simulation is using the nearest PSD "
            f"projection. Lower the magnitudes of `rho` to clear this."
        )
    else:
        warn = mo.md("")
    warn
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Aha moments

    1. **Diversification is real.** Set $\rho_{12}$ to $-0.95$. Watch the ellipsoid pancake
       into a thin diagonal. Move $w_1$ around. There is a value of $w_1$ where
       $w^\top \Sigma w$ is essentially zero. With perfect negative correlation, the right
       weights cancel almost all variance.

    2. **Geometry of the closed form.** In two assets, the minimum variance $w_1^\star$
       depends only on $\sigma_1, \sigma_2, \rho$, not on $\mu$. Slide $\mu_1$ and $\mu_2$ to
       random values: the location of the minimum on the "variance vs $w_1$" plot does not
       move. Means choose your point on the frontier, covariance chooses the frontier shape.

    3. **The affine identity is everything.** Compare the orange histogram of `w' r` with
       the spread of the joint cloud. The 1D variance of `w' r` equals $w^\top \Sigma w$.
       This single identity is why every portfolio optimisation problem in the rest of the
       course is a quadratic in $w$.

    ## Self test

    1. **Conceptual.** Why does the minimum variance weight depend only on $\Sigma$ and
       not on $\mu$? Hint: write the first order condition.

    2. **Coding.** Add a `tangency_two_asset(mu1, mu2, sigma1, sigma2, rho, rf=0)` function
       to the code editor. Closed form:

       $$w_1^\star = \frac{(\mu_1 - r_f) \sigma_2^2 - (\mu_2 - r_f) \rho \sigma_1 \sigma_2}{(\mu_1 - r_f) \sigma_2^2 + (\mu_2 - r_f) \sigma_1^2 - (\mu_1 + \mu_2 - 2 r_f) \rho \sigma_1 \sigma_2}$$

       After saving, the dashboard will pick it up. Print the value in the output panel.

    3. **Numerical.** Set $\sigma_1 = 0.20$, $\sigma_2 = 0.10$, $\rho = -0.5$. Compute
       $w_1^\star$ by hand. Compare to the dashboard.

    ## Notes

    Save the answers in `lesson_02_notes.md`.
    """)
    return


if __name__ == "__main__":
    app.run()
