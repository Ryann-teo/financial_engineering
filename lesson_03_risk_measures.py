"""
Lesson 3: Risk Measures from Variance to Drawdown.

Module A, Week 1, Lesson 3 of the Portfolio Construction curriculum.

Run with:
    marimo edit lesson_03_risk_measures.py
"""

import marimo

__generated_with = "0.9.0"
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
    return go, make_subplots, np, pd, stats


@app.cell
def _(mo):
    mo.md(
        r"""
        # Lesson 3: Risk Measures from Variance to Drawdown

        Variance is the textbook risk measure. Real portfolios face tail loss
        and path dependent drawdown. This lesson builds the four measures you
        will reach for again and again.

        - **Variance** (and volatility): symmetric, easy to optimise.
        - **VaR** $_\alpha$: a quantile of the loss distribution. Not coherent.
        - **CVaR** $_\alpha$: expected loss given you are past the VaR. Coherent.
        - **Drawdown**: peak to trough loss along the equity curve.

        Slide the controls. Then implement the two functions in the code cell.
        """
    )
    return


@app.cell
def _(mo):
    asset = mo.ui.dropdown(
        options=[
            "SPY (equity)",
            "AGG (bonds)",
            "GLD (gold)",
            "BTC (crypto)",
            "60/40 mix",
        ],
        value="SPY (equity)",
        label="Asset",
    )
    n_years = mo.ui.slider(start=5, stop=25, step=1, value=20, label="Years of history")
    alpha = mo.ui.slider(start=0.90, stop=0.999, step=0.001, value=0.95, label="alpha (VaR / CVaR confidence)")
    method = mo.ui.radio(
        options=["historical", "Gaussian fit", "Student t fit"],
        value="historical",
        label="Distribution method",
    )
    return alpha, asset, method, n_years


@app.cell
def _(alpha, asset, method, mo, n_years):
    mo.hstack([asset, n_years, alpha, method], justify="start", gap=2)
    return


@app.cell
def _(np, pd):
    def synth_returns(asset_name: str, n_years: int = 20) -> pd.Series:
        """Generate daily returns with realistic stylised features.

        Includes a 'crisis injection' so all assets except bonds show a
        fat left tail you can see in the histogram.
        """
        np.random.seed(abs(hash(asset_name)) % (2**32))
        n = int(n_years * 252)

        params = {
            "SPY (equity)": dict(mu=0.08, vol=0.15, df=5, crisis_prob=0.005, crisis_drop=-0.04),
            "AGG (bonds)": dict(mu=0.04, vol=0.05, df=8, crisis_prob=0.001, crisis_drop=-0.015),
            "GLD (gold)":  dict(mu=0.06, vol=0.18, df=6, crisis_prob=0.003, crisis_drop=-0.05),
            "BTC (crypto)":dict(mu=0.30, vol=0.80, df=3, crisis_prob=0.010, crisis_drop=-0.15),
            "60/40 mix":   dict(mu=0.06, vol=0.10, df=6, crisis_prob=0.003, crisis_drop=-0.025),
        }
        p = params[asset_name]

        # Base t shocks
        eps = np.random.standard_t(p["df"], n) * (p["vol"] / np.sqrt(252))
        eps += p["mu"] / 252

        # Inject occasional crisis days
        crisis_mask = np.random.rand(n) < p["crisis_prob"]
        eps[crisis_mask] += p["crisis_drop"]

        # GARCH like clustering: smooth the variance
        vol_t = np.zeros(n)
        vol_t[0] = p["vol"] / np.sqrt(252)
        for t in range(1, n):
            vol_t[t] = np.sqrt(0.05 * eps[t - 1] ** 2 + 0.94 * vol_t[t - 1] ** 2 + 1e-7)
        # rescale to keep mean vol roughly correct
        eps = eps * (p["vol"] / np.sqrt(252)) / np.std(eps)

        idx = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n)
        return pd.Series(eps, index=idx, name=asset_name)
    return (synth_returns,)


@app.cell
def _(asset, n_years, np, synth_returns):
    rets = synth_returns(asset.value, n_years.value)
    equity = (1 + rets).cumprod()
    return equity, rets


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Code it yourself

        Implement two functions.

        **1. `historical_var_cvar(losses, alpha)`**

        Given a 1D array of **losses** (i.e. negative returns), return the
        historical VaR and CVaR at confidence $\alpha$.

        $$\text{VaR}_\alpha(L) = \inf\{x : P(L > x) \leq 1 - \alpha\}$$
        $$\text{CVaR}_\alpha(L) = \mathbb{E}[L \mid L \geq \text{VaR}_\alpha(L)]$$

        Hint: `np.quantile(losses, alpha)` is the VaR. CVaR is the mean of
        losses that meet or exceed it.

        **2. `max_drawdown(equity)`**

        Given a pandas Series of equity values, return a dict with
        `max_dd` (positive number, e.g. 0.34 for a 34% drawdown), `peak_date`,
        and `trough_date`.

        Hint: use `np.maximum.accumulate(equity.values)` to get the running peak.
        """
    )
    return


@app.cell
def _(mo):
    code_editor = mo.ui.code_editor(
        value='''import numpy as np
import pandas as pd


def historical_var_cvar(losses, alpha):
    """Historical VaR and CVaR at confidence alpha.

    Args:
        losses: 1D array of losses (positive = loss).
        alpha: confidence level, e.g. 0.95 or 0.99.

    Returns:
        dict with keys 'var' and 'cvar'.
    """
    losses = np.asarray(losses)
    var = float(np.quantile(losses, alpha))
    tail = losses[losses >= var]
    cvar = float(tail.mean()) if len(tail) > 0 else var
    return {"var": var, "cvar": cvar}


def max_drawdown(equity):
    """Peak to trough max drawdown of an equity curve.

    Args:
        equity: pd.Series of cumulative wealth.

    Returns:
        dict with 'max_dd' (positive fraction), 'peak_date', 'trough_date'.
    """
    eq = equity.values
    peak = np.maximum.accumulate(eq)
    dd = 1 - eq / peak
    trough_i = int(np.argmax(dd))
    peak_i = int(np.argmax(eq[: trough_i + 1]))
    return {
        "max_dd": float(dd[trough_i]),
        "peak_date": equity.index[peak_i],
        "trough_date": equity.index[trough_i],
    }
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
def _(alpha, code_editor, equity, method, mo, np, rets, stats):
    user_globals: dict = {}
    err = None
    var_emp = cvar_emp = None
    dd_info = None
    var_param = cvar_param = None

    try:
        exec(code_editor.value, user_globals)
        historical_var_cvar = user_globals["historical_var_cvar"]
        max_drawdown_fn = user_globals["max_drawdown"]

        losses = -rets.values
        out_hist = historical_var_cvar(losses, alpha.value)
        var_emp = out_hist["var"]
        cvar_emp = out_hist["cvar"]

        # Parametric variants for comparison
        if method.value == "Gaussian fit":
            mu_, sd_ = float(rets.mean()), float(rets.std(ddof=1))
            var_param = -mu_ + sd_ * stats.norm.ppf(alpha.value)
            # CVaR closed form for Gaussian:
            phi = stats.norm.pdf(stats.norm.ppf(alpha.value))
            cvar_param = -mu_ + sd_ * phi / (1 - alpha.value)
        elif method.value == "Student t fit":
            df_t, mu_t, s_t = stats.t.fit(rets.values)
            q = stats.t.ppf(alpha.value, df_t, loc=0, scale=1)
            var_param = -mu_t + s_t * q
            # CVaR for t (Acerbi-Tasche style)
            tau = stats.t.pdf(q, df_t)
            cvar_param = -mu_t + s_t * (tau / (1 - alpha.value)) * ((df_t + q ** 2) / (df_t - 1))

        dd_info = max_drawdown_fn(equity)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"

    if err is not None:
        out = mo.md(f"**Implementation incomplete.** `{err}`")
    else:
        # 1 day VaR/CVaR translated to percentage
        var_emp_pct = var_emp * 100
        cvar_emp_pct = cvar_emp * 100

        sortino_denom = float(np.sqrt(np.mean(np.minimum(rets.values, 0) ** 2)) * np.sqrt(252))
        sortino = (rets.mean() * 252) / sortino_denom if sortino_denom > 0 else float("nan")

        rows = (
            f"| Historical VaR_{int(alpha.value*1000)/10:.1f}%   | {var_emp_pct:.2f}% per day |\n"
            f"| Historical CVaR_{int(alpha.value*1000)/10:.1f}% | {cvar_emp_pct:.2f}% per day |\n"
        )
        if var_param is not None:
            rows += (
                f"| Parametric VaR ({method.value})  | {var_param * 100:.2f}% per day |\n"
                f"| Parametric CVaR ({method.value}) | {cvar_param * 100:.2f}% per day |\n"
            )
        rows += (
            f"| Max drawdown                       | {dd_info['max_dd'] * 100:.1f}% |\n"
            f"| Peak date                          | {dd_info['peak_date'].date()} |\n"
            f"| Trough date                        | {dd_info['trough_date'].date()} |\n"
            f"| Sortino ratio (annualised)         | {sortino:.2f} |\n"
        )

        out = mo.md(
            f"""
            ### Risk metrics for {rets.name}

            | Metric | Value |
            |--------|-------|
            {rows}
            """
        )
    out
    return (
        cvar_emp,
        cvar_param,
        dd_info,
        out,
        var_emp,
        var_param,
    )


@app.cell
def _(
    alpha,
    cvar_emp,
    dd_info,
    equity,
    go,
    make_subplots,
    np,
    rets,
    var_emp,
):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Loss histogram with VaR / CVaR",
            "Equity curve and drawdown",
            "Drawdown path (% from peak)",
            "Loss tail (right tail of losses) zoomed",
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.10,
    )

    losses = -rets.values

    # 1. Histogram with VaR/CVaR markers
    fig.add_trace(
        go.Histogram(x=losses * 100, nbinsx=80, marker_color="#1f77b4", opacity=0.7, showlegend=False),
        row=1, col=1,
    )
    if var_emp is not None:
        fig.add_vline(x=var_emp * 100, line=dict(color="orange", width=2, dash="dash"),
                      row=1, col=1, annotation_text=f"VaR={var_emp * 100:.2f}%", annotation_position="top")
    if cvar_emp is not None:
        fig.add_vline(x=cvar_emp * 100, line=dict(color="red", width=2),
                      row=1, col=1, annotation_text=f"CVaR={cvar_emp * 100:.2f}%", annotation_position="top right")

    # 2. Equity curve with peak / trough markers
    fig.add_trace(
        go.Scatter(x=equity.index, y=equity.values, mode="lines", line=dict(color="navy"), showlegend=False),
        row=1, col=2,
    )
    if dd_info is not None:
        fig.add_trace(
            go.Scatter(
                x=[dd_info["peak_date"], dd_info["trough_date"]],
                y=[float(equity.loc[dd_info["peak_date"]]), float(equity.loc[dd_info["trough_date"]])],
                mode="markers",
                marker=dict(size=10, color=["green", "red"]),
                showlegend=False,
            ),
            row=1, col=2,
        )

    # 3. Drawdown path
    eq = equity.values
    peak = np.maximum.accumulate(eq)
    dd = (1 - eq / peak) * 100
    fig.add_trace(
        go.Scatter(
            x=equity.index, y=-dd, mode="lines",
            line=dict(color="firebrick"), fill="tozeroy", showlegend=False,
        ),
        row=2, col=1,
    )

    # 4. Right tail of losses (above 90th percentile of losses)
    tail_thresh = np.quantile(losses, 0.90)
    tail = losses[losses >= tail_thresh] * 100
    fig.add_trace(
        go.Histogram(x=tail, nbinsx=40, marker_color="#d62728", opacity=0.8, showlegend=False),
        row=2, col=2,
    )
    if var_emp is not None:
        fig.add_vline(x=var_emp * 100, line=dict(color="orange", width=2, dash="dash"), row=2, col=2)
    if cvar_emp is not None:
        fig.add_vline(x=cvar_emp * 100, line=dict(color="red", width=2), row=2, col=2)

    fig.update_xaxes(title_text="loss (% per day)", row=1, col=1)
    fig.update_yaxes(title_text="frequency", row=1, col=1)
    fig.update_yaxes(title_text="growth of $1", row=1, col=2)
    fig.update_yaxes(title_text="% from peak", row=2, col=1)
    fig.update_xaxes(title_text="loss (% per day, right tail)", row=2, col=2)

    fig.update_layout(height=800, title_text=f"{rets.name}: alpha = {alpha.value:.3f}")
    fig
    return (fig,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Aha moments

        1. **VaR is a quantile, CVaR is an expectation past it.** Slide $\alpha$ from
           $0.95$ to $0.99$ to $0.999$. VaR moves slowly. CVaR jumps. The 99th percentile
           loss is mild. The expected loss conditional on being in that tail is a different
           animal.

        2. **Parametric Gaussian underestimates tail risk.** Switch the method to
           **Gaussian fit** with $\alpha = 0.99$. Compare to **historical**. The Gaussian
           VaR is consistently smaller. The historical and Student t numbers are closer.
           This is why Basel III backtests Gaussian VaR models so harshly.

        3. **Drawdown is path dependent.** Two return distributions can produce the same
           variance but very different max drawdown. Switch from **SPY** to **BTC**:
           the drawdown path is dramatically deeper even though variance scales linearly.

        4. **Sub additivity.** With 60/40 chosen, write the variance, VaR, CVaR. Compare
           to a 100% SPY portfolio. CVaR satisfies CVaR(60/40) <= 0.6 CVaR(SPY) + 0.4 CVaR(AGG).
           VaR can violate this. CVaR is **coherent** and VaR is not. This single property
           is why CVaR is preferred for portfolio optimisation.

        ## Self test

        1. **Conceptual.** Give one situation where VaR is fine and one where it is dangerous.
           Tip: think about portfolios with long convexity vs short convexity.

        2. **Coding.** Add a `conditional_drawdown_at_risk(equity, alpha)` function that
           returns the average drawdown across the worst $1 - \alpha$ fraction of the path.
           This is CDaR. The dashboard should pick it up after you save.

        3. **Numerical.** For SPY at $\alpha = 0.99$, compute the ratio of CVaR / VaR.
           For a normal distribution this ratio is `phi(z_alpha) / ((1 - alpha) * z_alpha)`,
           which is about 1.15 at $\alpha = 0.99$. The empirical ratio for SPY should be
           higher because of fat tails.

        ## Notes

        Save the answers in `lesson_03_notes.md`.
        """
    )
    return


if __name__ == "__main__":
    app.run()
