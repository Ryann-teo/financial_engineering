# Lessons 9 to 30: Build Outline

Module B is complete (Lessons 5, 6, 7, 8). The remaining 22 lessons each take roughly 5 to 7 hours to build at the same production quality as Module A and B. Building all 22 in a single run is impractical.

This document is the build queue. Each entry has the title, the planned demos, the macrosynergy article anchors, and the priority. Tackle them in the order suggested.

## Priority order (the 8-week curriculum sequence)

| Order | Lesson | File name | Module | Status |
|-------|--------|-----------|--------|--------|
| 1 | 9. Why MV breaks | `lesson_09_why_mv_breaks.html` | C | pending |
| 2 | 10. Shrinkage | `lesson_10_shrinkage.html` | C | pending |
| 3 | 13. Covariance estimation | `lesson_13_covariance.html` | C | pending |
| 4 | 11. Black-Litterman | `lesson_11_black_litterman.html` | C | pending |
| 5 | 12. Robust optimisation | `lesson_12_robust.html` | C | pending |
| 6 | 14. ERC and risk parity | `lesson_14_erc.html` | D | pending |
| 7 | 15. Hierarchical Risk Parity | `lesson_15_hrp.html` | D | pending |
| 8 | 16. CVaR and drawdown | `lesson_16_cvar_drawdown.html` | D | pending |
| 9 | 20. Transaction costs | `lesson_20_costs.html` | E | pending |
| 10 | 21. Vol targeting | `lesson_21_vol_targeting.html` | E | pending |
| 11 | 22. Kelly criterion | `lesson_22_kelly.html` | E | pending |
| 12 | 24. Factor models | `lesson_24_factor_models.html` | F | pending |
| 13 | 25. Mandate constraints, TE | `lesson_25_constraints_te.html` | F | pending |
| 14 | 26. Signal blending | `lesson_26_signal_blending.html` | F | pending |
| 15 | 23. Backtesting and CPCV | `lesson_23_backtesting.html` | G | pending |
| 16 | 27. Regime allocation | `lesson_27_regime.html` | G | pending |
| 17 | 29. Capstone | `lesson_29_capstone.html` | G | pending |

Lessons 17, 18, 19, 28, 30 are deferred (covered by other lessons or considered optional in the 8-week plan).

---

## Detailed build spec per lesson

### Lesson 9: Why mean-variance fails out of sample
- **Demos:** error maximisation simulator (slider for $\mu$ perturbation, watch weights swing); condition number vs $T/N$; DeMiguel ratio (1/N vs MV out of sample).
- **Math companion:** $w^\star \propto \Sigma^{-1} \mu$ derivative analysis; condition number of Wishart estimators; the $T/N$ cliff.
- **MS box:** conceptual parity as the answer (art 3, 28).
- **Notebook exercises:** error simulator; bootstrap weight distribution; DeMiguel-style horse race.

### Lesson 10: Shrinkage and Bayesian estimation
- **Demos:** shrinkage intensity slider; sample vs Ledoit-Wolf vs single-factor covariance heatmaps; out-of-sample variance vs $\delta$.
- **Math companion:** James-Stein, Ledoit-Wolf optimal shrinkage formula, NIW posterior.
- **MS box:** art 4, 25, 45 (regression-based ML / ridge as production shrinkage).
- **Notebook:** Ledoit-Wolf from scratch; cross-validate shrinkage intensity; shrinkage vs sample size sweep.

### Lesson 11: Black-Litterman
- **Demos:** view encoder (slider for view return, confidence); equilibrium-implied returns vs posterior; tau slider effect.
- **Math companion:** master formula derivation, role of $\Omega$, common $\tau$ choices.
- **MS box:** MS does not use BL; conceptual parity is the priors layer.
- **Notebook:** implement BL master formula; absolute vs relative views; confidence sensitivity.

### Lesson 12: Robust optimisation
- **Demos:** uncertainty radius slider $\kappa$ for ellipsoidal box; nominal vs robust frontier; Wasserstein-DRO toggle.
- **Math companion:** SOCP form, Bertsimas-Sim uncertainty sets, regularisation interpretation.
- **MS box:** art 4, 45 (signal reliability adjustment as robust shrinkage).
- **Notebook:** robust MV with cvxpy; resampled efficiency by Michaud; comparison of methods.

### Lesson 13: Covariance estimation in depth
- **Demos:** six estimators side-by-side heatmaps; eigenvalue spectrum + Marcenko-Pastur cutoff; min-var weights from each estimator.
- **Math companion:** RMT eigenvalue cleaning, factor model decomposition, hierarchical block structure.
- **MS box:** art 37 (PCA), art 89 (correlation regimes), art 99 (vol estimators).
- **Notebook:** RMT cleaning from scratch; single-factor decomposition; out-of-sample comparison.

### Lesson 14: Equal Risk Contribution
- **Demos:** ERC vs equal-weight vs min-var bar charts; CCD convergence animation; risk contributions over time.
- **Math companion:** Spinu convex form, existence/uniqueness theorem, asymmetric risk budgets.
- **MS box:** art 23 (macro-aware risk parity), art 88 (factors for risk parity).
- **Notebook:** ERC by CCD; macro tilt overlay; backtest vs 60/40.

### Lesson 15: Hierarchical Risk Parity
- **Demos:** algorithm in 4 stages (correlation, dendrogram, quasi-diagonal, weights tree); HRP vs ERC vs min-var on noisy covariance.
- **Math companion:** distance metric construction, linkage methods, recursive bisection.
- **MS box:** art 121 (ML for portfolio diversification).
- **Notebook:** HRP from scratch; bootstrap stability test.

### Lesson 16: CVaR and drawdown optimisation
- **Demos:** mean-variance vs mean-CVaR frontier; drawdown path replay (2008, 2020, 2022); MinMax slider.
- **Math companion:** Rockafellar-Uryasev LP, CDaR formulation, MinMax aversion parameter.
- **MS box:** art 220 (canonical drawdown control).
- **Notebook:** CVaR LP with cvxpy; MinMax drawdown overlay; stress replay.

### Lesson 20: Transaction costs and cost-aware rebalancing
- **Demos:** cost slider (proportional + impact); turnover vs Sharpe trade-off; no-trade region polygon.
- **Math companion:** linear cost LP, square-root impact SOCP, Garleanu-Pedersen optimal trading.
- **MS box:** art 91, 366.
- **Notebook:** cost-aware MV with cvxpy; rebalance frequency optimisation.

### Lesson 21: Volatility targeting
- **Demos:** target vol slider, half-life slider, equity curve before/after, drawdown comparison.
- **Math companion:** EWMA vol formal; vol drag intuition; interaction with momentum.
- **MS box:** art 5 (canonical), art 245 (vol target effect on equity Sharpe).
- **Notebook:** vol target a single asset; combine with TSMOM signal; cost-aware version.

### Lesson 22: Kelly criterion
- **Demos:** Kelly fraction slider; terminal wealth Monte Carlo; probability of 50% drawdown.
- **Math companion:** log-utility derivation; multi-asset Kelly = $\Sigma^{-1} \mu$; fractional Kelly link to MV.
- **MS box:** MS implicitly uses fractional Kelly via vol targeting.
- **Notebook:** simulate Kelly path; full vs fractional comparison; discuss leverage limits.

### Lesson 24: Factor models for risk and alpha
- **Demos:** Fama-French 5-factor regression; statistical PCA factors; factor risk decomposition pie chart.
- **Math companion:** $\Sigma = B \Omega B' + D$, statistical vs fundamental factors, Bai-Ng criterion.
- **MS box:** art 47 (sectoral macro), art 74 (latent factors).
- **Notebook:** FF5 decomposition; PCA factors; portfolio risk attribution.

### Lesson 25: Mandate constraints and tracking error
- **Demos:** TE budget slider; sector cap toggles; binding-constraint highlight.
- **Math companion:** active MV formulation, Grinold-Kahn fundamental law, TE budget SOCP.
- **MS box:** standard mandate practice; art 15 closest analog.
- **Notebook:** mandate-constrained portfolio with cvxpy; TE attribution.

### Lesson 26: Signal blending and Grinold's law
- **Demos:** signal stack composer (toggle 4-5 signals); IC time series; orthogonalisation toggle.
- **Math companion:** Grinold's law derivation, breadth, signal correlation correction.
- **MS box:** art 28, 36, 39, 50, 25, 49 (the heart of MS).
- **Notebook:** blend signals on FX; orthogonalise; IR comparison.

### Lesson 23: Backtesting with CPCV
- **Demos:** walk-forward vs k-fold vs CPCV; Sharpe distribution from CPCV paths; deflated Sharpe vs trials.
- **Math companion:** purged k-fold formal, CPCV path enumeration, embargo design.
- **MS box:** art 50, 204.
- **Notebook:** implement CPCV; deflated Sharpe; bootstrap CI.

### Lesson 27: Regime-aware allocation
- **Demos:** HMM regime classifier on returns + VIX; regime-conditional allocation; static vs conditional Sharpe.
- **Math companion:** HMM Baum-Welch high-level, regime-conditional moments.
- **MS box:** art 89, 111, 136, 76, 220.
- **Notebook:** fit HMM with hmmlearn; conditional 60/40; cycle conditional.

### Lesson 29: Capstone, cross-asset macro lab
- **The big one.** Combines every lesson. Universe, signals, blending, optimisation, vol target, drawdown, costs, backtest, attribution.
- **Demos:** full pipeline with toggleable layers; signal family attribution; regime conditional Sharpe table.
- **MS box:** art 3 (the flagship), art 39 (the pipeline).
- **Notebook:** the capstone notebook (integrative).

---

## Build conventions for the next agent

1. Read `dashboard_building_guide.md` first.
2. Open `lesson_05_markowitz.html` and `lesson_07_risk_budgeting.html` as reference implementations of the canonical layout.
3. For the JavaScript demos: copy the math utilities (linspace, mat-vec, inv, normPdf, normInv) verbatim. The interactive widget pattern is the same.
4. Each lesson should match the structure of Lessons 5 through 8: glossary, 5 to 6 concept sections, 1 to 3 live demos, MS in-practice box, math companion (5+ subsections), 5 coding exercises, 3 self-test questions.
5. Update `README.md` to add each new file to the table.

## Suggested cadence

Build 2 to 4 lessons per work session. Aim for one full module (4 lessons) per week. At 2 lessons per session, the remaining 17 = 8 to 9 sessions = roughly 6 to 8 weeks of part-time work. This matches the 8-week curriculum's intended teaching pace.

When ready to build the next batch, say "build Lessons 9 and 10" or "begin Module C". I will produce the next pair at the same production quality.
