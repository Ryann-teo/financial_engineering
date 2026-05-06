"""
Lesson 1: Returns, Log Returns, and Stylised Facts.

Module A, Week 1, Lesson 1 of the Portfolio Construction curriculum.

Run with:
    marimo edit lesson_01_returns_stylised_facts.py
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
    from statsmodels.tsa.stattools import acf

    return acf, go, make_subplots, np, pd, stats


@app.cell
def _(mo):
    mo.md("""
    # Lesson 1: Returns, Log Returns, and Stylised Facts

    Every later module sits on top of a return series. Get the definitions
    right and learn what "normal" returns actually look like.

    **The five stylised facts to internalise.**

    1. Returns have approximately zero autocorrelation.
    2. Absolute returns autocorrelate strongly (volatility clustering).
    3. Returns have heavy tails (kurtosis well above 3).
    4. Equities show a leverage effect: negative returns predict higher future vol.
    5. Aggregational Gaussianity: returns at low frequency look more normal.

    Slide the controls below. Then implement `compute_stats` in the code cell.
    """)
    return


@app.cell
def _(mo):
    asset = mo.ui.dropdown(
        options=[
            "SPY (equity)",
            "AGG (bonds)",
            "GLD (gold)",
            "BTC (crypto)",
            "VIX (vol index)",
        ],
        value="SPY (equity)",
        label="Asset",
    )
    freq = mo.ui.dropdown(
        options=["Daily", "Weekly", "Monthly", "Yearly"],
        value="Daily",
        label="Frequency",
    )
    return_type = mo.ui.radio(
        options=["simple", "log"],
        value="log",
        label="Return type",
    )
    n_years = mo.ui.slider(start=2, stop=20, value=15, step=1, label="Years of history")
    return asset, freq, n_years, return_type


@app.cell
def _(asset, freq, mo, n_years, return_type):
    mo.hstack([asset, freq, return_type, n_years], justify="start", gap=2)
    return


@app.cell
def _(np, pd):
    def synth_prices(asset_name: str, n_years: int = 15) -> pd.Series:
        """Generate prices that match each asset's stylised behaviour.

        Uses Student t shocks (heavy tails) and a simple GARCH(1,1) variance
        process (volatility clustering), with a leverage parameter that lets
        equities show the asymmetric vol response to negative returns.
        """
        np.random.seed(abs(hash(asset_name)) % (2**32))
        n = int(n_years * 252)
        params = {
            "SPY (equity)":   dict(mu=0.08 / 252, base_vol=0.15 / np.sqrt(252), df=5, leverage=-0.4),
            "AGG (bonds)":    dict(mu=0.04 / 252, base_vol=0.05 / np.sqrt(252), df=8, leverage=-0.1),
            "GLD (gold)":     dict(mu=0.06 / 252, base_vol=0.18 / np.sqrt(252), df=6, leverage=0.0),
            "BTC (crypto)":   dict(mu=0.30 / 252, base_vol=0.80 / np.sqrt(252), df=3, leverage=-0.2),
            "VIX (vol index)":dict(mu=-0.05 / 252, base_vol=0.90 / np.sqrt(252), df=3, leverage=0.6),
        }
        p = params[asset_name]

        eps = np.random.standard_t(p["df"], n)
        eps = eps / np.std(eps)  # standardise

        vol = np.zeros(n)
        ret = np.zeros(n)
        vol[0] = p["base_vol"]
        for t in range(1, n):
            shock = vol[t - 1] * eps[t - 1]
            # leverage effect: negative shocks raise next period vol more
            asym = 1.0 + p["leverage"] * (1 if shock < 0 else 0)
            vol[t] = np.sqrt(
                1e-7
                + 0.05 * (shock * asym) ** 2
                + 0.93 * vol[t - 1] ** 2
            )
            ret[t] = p["mu"] + vol[t] * eps[t]

        prices = 100 * np.exp(np.cumsum(ret))
        idx = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n)
        return pd.Series(prices, index=idx, name=asset_name)

    return (synth_prices,)


@app.cell
def _(asset, freq, n_years, np, return_type, synth_prices):
    raw_prices = synth_prices(asset.value, n_years.value)

    freq_map = {"Daily": "B", "Weekly": "W-FRI", "Monthly": "ME", "Yearly": "YE"}
    if freq.value == "Daily":
        prices = raw_prices
    else:
        prices = raw_prices.resample(freq_map[freq.value]).last().dropna()

    if return_type.value == "simple":
        rets = prices.pct_change().dropna()
    else:
        rets = np.log(prices / prices.shift(1)).dropna()
    return prices, rets


@app.cell
def _(mo):
    mo.md("""
    ## Code it yourself

    Implement the seven statistics below. The output panel underneath will
    re render the moment you save (Ctrl or Cmd plus S).

    **Hints.**

    - `r.mean() * periods_per_year` for annualised mean.
    - `r.std(ddof=1) * np.sqrt(periods_per_year)` for annualised vol.
    - `scipy.stats.skew(r)` and `scipy.stats.kurtosis(r, fisher=True)` for higher moments.
    - For tail probabilities: fit `stats.norm` and `stats.t` then use the survival function `sf`.
    - Empirical exceedances: `np.sum(np.abs(r - r.mean()) > 3 * r.std())`.
    """)
    return


@app.cell
def _(mo):
    code_editor = mo.ui.code_editor(
        value='''def compute_stats(returns, periods_per_year):
    """Implement the stylised-facts statistics for a return series.

    Args:
        returns: pd.Series of returns
        periods_per_year: 252 daily, 52 weekly, 12 monthly, 1 yearly

    Returns:
        dict with keys:
            mean_ann, vol_ann, skew, excess_kurt,
            p_norm_3sigma, p_t_3sigma, empirical_3sigma_count
    """
    import numpy as np
    from scipy import stats

    r = returns.values

    mean_ann = r.mean() * periods_per_year
    vol_ann = r.std(ddof=1) * (periods_per_year ** 0.5)

    # higher moments
    skew = float(stats.skew(r))
    excess_kurt = float(stats.kurtosis(r, fisher=True))

    # tail probabilities under fitted normal vs Student t
    mu_n, sd_n = r.mean(), r.std(ddof=1)
    p_norm_3sigma = 2.0 * stats.norm.sf(3 * sd_n, loc=0, scale=sd_n)

    df_t, mu_t, s_t = stats.t.fit(r)
    # P(|X| > 3 * sd_n) under the fitted t
    z = 3 * sd_n
    p_t_3sigma = stats.t.sf((z - mu_t) / s_t, df_t) + stats.t.cdf((-z - mu_t) / s_t, df_t)

    # empirical exceedances
    empirical_3sigma_count = int(np.sum(np.abs(r - mu_n) > 3 * sd_n))

    return dict(
        mean_ann=mean_ann,
        vol_ann=vol_ann,
        skew=skew,
        excess_kurt=excess_kurt,
        p_norm_3sigma=p_norm_3sigma,
        p_t_3sigma=p_t_3sigma,
        empirical_3sigma_count=empirical_3sigma_count,
    )
    ''',
        language="python",
        label="Edit compute_stats below, then save",
    )
    return (code_editor,)


@app.cell
def _(code_editor):
    code_editor
    return


@app.cell
def _(code_editor, freq, mo, rets):
    periods_map = {"Daily": 252, "Weekly": 52, "Monthly": 12, "Yearly": 1}
    ppy = periods_map[freq.value]

    user_globals: dict = {}
    error = None
    result = None
    try:
        exec(code_editor.value, user_globals)
        compute_stats = user_globals.get("compute_stats")
        if compute_stats is None:
            error = "Function compute_stats is not defined."
        else:
            result = compute_stats(rets, ppy)
    except Exception as e:
        error = f"{type(e).__name__}: {e}"

    if error is not None:
        out = mo.md(f"**Implementation incomplete.** `{error}`")
    else:
        normal_expected = 0.0027 * len(rets)  # ~0.27% under normal
        out = mo.md(
            f"""
            ### Stats for {rets.name} ({freq.value}, {len(rets)} obs)

            | Metric | Value |
            |--------|-------|
            | Annualised mean | {result['mean_ann']:.2%} |
            | Annualised vol  | {result['vol_ann']:.2%} |
            | Skewness        | {result['skew']:+.3f} |
            | Excess kurtosis | {result['excess_kurt']:+.3f} |
            | P(\\|r\\| > 3 sigma) under fitted normal | {result['p_norm_3sigma']:.3%} |
            | P(\\|r\\| > 3 sigma) under fitted t      | {result['p_t_3sigma']:.3%} |
            | Empirical 3 sigma exceedances           | **{result['empirical_3sigma_count']}** |
            | Normal expected (~0.27% of n)           | {normal_expected:.1f} |

            If `empirical_3sigma_count` is much larger than the normal expected,
            the tail is heavier than Gaussian.
            """
        )
    out
    return


@app.cell
def _(acf, go, make_subplots, np, prices, rets, stats):
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "Price",
            "Return time series",
            "ACF of returns",
            "ACF of |returns|",
            "Histogram with fitted normal vs t",
            "QQ plot vs normal",
        ),
        vertical_spacing=0.10,
        horizontal_spacing=0.10,
    )

    # Row 1
    fig.add_trace(
        go.Scatter(x=prices.index, y=prices.values, mode="lines", showlegend=False),
        row=1, col=1,
    )
    fig.add_trace(
        go.Scatter(x=rets.index, y=rets.values, mode="lines", showlegend=False, line=dict(width=0.7)),
        row=1, col=2,
    )

    # Row 2: ACFs
    n_lags = min(40, len(rets) // 4)
    a_r = acf(rets.values, nlags=n_lags, fft=True)
    a_abs = acf(np.abs(rets.values), nlags=n_lags, fft=True)
    fig.add_trace(go.Bar(x=list(range(len(a_r))), y=a_r, showlegend=False), row=2, col=1)
    fig.add_trace(go.Bar(x=list(range(len(a_abs))), y=a_abs, showlegend=False), row=2, col=2)
    ci = 1.96 / np.sqrt(len(rets))
    for col in (1, 2):
        for y in (ci, -ci):
            fig.add_hline(y=y, line=dict(dash="dash", color="gray", width=1), row=2, col=col)

    # Row 3: histogram with fits, QQ
    x_grid = np.linspace(rets.min(), rets.max(), 300)
    mu, sigma = float(rets.mean()), float(rets.std(ddof=1))
    norm_pdf = stats.norm.pdf(x_grid, loc=mu, scale=sigma)
    df_t, mu_t, s_t = stats.t.fit(rets.values)
    t_pdf = stats.t.pdf(x_grid, df_t, loc=mu_t, scale=s_t)

    fig.add_trace(
        go.Histogram(x=rets.values, histnorm="probability density", opacity=0.55, showlegend=False, nbinsx=60),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=x_grid, y=norm_pdf, mode="lines", name="Normal", line=dict(color="firebrick")),
        row=3, col=1,
    )
    fig.add_trace(
        go.Scatter(x=x_grid, y=t_pdf, mode="lines", name=f"t (df={df_t:.1f})", line=dict(color="forestgreen")),
        row=3, col=1,
    )

    osm, osr = stats.probplot(rets.values, dist="norm", fit=False)
    fig.add_trace(
        go.Scatter(x=osm, y=osr, mode="markers", showlegend=False, marker=dict(size=3)),
        row=3, col=2,
    )
    line_x = np.linspace(osm.min(), osm.max(), 50)
    fig.add_trace(
        go.Scatter(x=line_x, y=line_x * sigma + mu, mode="lines", line=dict(color="firebrick", width=1.2), showlegend=False),
        row=3, col=2,
    )

    fig.update_layout(
        height=900,
        title_text=f"{prices.name} stylised facts",
        showlegend=True,
        legend=dict(orientation="h", y=-0.05),
    )
    fig
    return


@app.cell
def _(mo):
    mo.md("""
    ## Aha moment

    1. Switch the asset to **SPY (equity)** at **Daily** frequency. Look at the bottom right
       QQ plot. The curve bends away from the red line at both tails. That bending is
       kurtosis you can see.

    2. Now switch the frequency to **Yearly**. The QQ curve straightens. The histogram fits
       the normal almost perfectly. This is **aggregational Gaussianity** in motion.

    3. Compare the two ACF plots. Returns themselves are essentially uncorrelated (zero
       autocorrelation, bars within the gray band). Absolute returns are highly persistent
       (bars sit far above the band for many lags). That gap is **volatility clustering**.

    4. Try **BTC (crypto)** at daily frequency. The empirical 3 sigma count is many times
       the normal expected count. Heavy tails are not optional.

    ## Self test

    1. **Conceptual.** Why does the leverage effect matter for risk management?
       If your model assumes constant volatility, what kind of bias do you get during
       market drawdowns?

    2. **Coding.** Extend `compute_stats` to also return `var_99` (the historical 1 day
       99% VaR). The output panel will show it once you save.

    3. **Numerical.** For SPY daily, what is the ratio of empirical 3 sigma exceedances
       to the normal expected count? Should be roughly 2 to 5 times in real data.

    ## Notes

    Save the aha moments and answers in `lesson_01_notes.md` next to this file.
    """)
    return


if __name__ == "__main__":
    app.run()
