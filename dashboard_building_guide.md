# Dashboard Building Guide

**Audience:** future me (Claude, or whichever agent picks this up).
**Purpose:** how to build interactive HTML teaching dashboards in the style of Module A (Lessons 01 to 03 in this folder). Read this once before starting any new lesson dashboard so you do not re-derive the decisions.

This document describes the conventions, patterns, and common pitfalls. The file `lesson_01_returns_stylised_facts.html` is the canonical reference implementation; when in doubt, check it.

---

## 1. Format and philosophy

- **Single-file HTML pages.** One file per lesson. Opens in any modern browser.
- **No build step.** No npm, no webpack, no transpiler. Plain HTML, CSS, and ES6.
- **No Python required to view.** All interactivity is JavaScript. Companion notebooks (`module_X_exercises.ipynb`) are separate.
- **Bottom-up teaching.** Every concept is introduced from first principles, with one or two prior-lesson dependencies stated explicitly.
- **Manipulable demos throughout.** A page without a slider is a slide deck. The whole point of HTML over slides is interactivity.
- **No em-dashes anywhere.** Project rule. Use commas, colons, parentheses, or " to ".

---

## 2. File location and naming

All lessons live in:

```
C:\Users\ryant\Documents\Big Brain\Areas\Global Macro\Teaching Materials\Portfolio Dashboards\
```

Naming convention:

- `lesson_NN_<short_slug>.html` for the dashboard.
- `module_X_exercises.ipynb` for the coding companion (one per module, not per lesson).
- `dashboard_building_guide.md` (this file).
- `README.md` for the folder index.

`NN` is a zero-padded two-digit number that matches the lesson number in `Portfolio Construction Master Plan.md` (e.g. Lesson 5 is `lesson_05_markowitz.html`).

---

## 3. Standard section template

Every lesson has the following sections in this order. Skip a section only if it genuinely does not apply.

1. **Title and subtitle.** `<h1>` with the lesson number and topic. `<p class="subtitle">` with one sentence of "what you will get out of this".
2. **Table of contents.** Anchored to section IDs `#s1`, `#s2`, etc. Use a `<div class="toc">`.
3. **Section 0: Reading the controls.** Glossary of every slider, dropdown, and toggle used on the page. Explain each one in math and intuition.
4. **Sections 1 to N: concept sections.** Build from definitions to the climax. Each section has prose, formulas, and (usually) a live demo.
5. **Optional deep dive.** Zoom in on one parameter or concept that needs more depth (see the df deep dive in Lesson 1).
6. **Mathematical companion.** Derivations, proofs, formal statements. This is where the textbook-style heavy math lives.
7. **Coding exercises (extras).** 3-5 prompts with code snippets. Reference the notebook for fully scaffolded versions.
8. **Self test.** 3 questions: one conceptual, one coding, one numerical.
9. **Nav block.** Prev/next links.
10. **Scripts.** All JavaScript at the bottom of `<body>`.

---

## 4. CSS template

The same CSS goes at the top of every lesson. Copy verbatim. Never restyle from scratch.

```css
:root {
  --bg: #fafbfc; --fg: #1a202c; --muted: #4a5568;
  --primary: #2b6cb0; --accent: #c05621;
  --card: #fff; --border: #e2e8f0;
  --insight: #fffbea; --insight-border: #f59e0b;
  --code-bg: #1a202c; --code-fg: #e2e8f0;
  --demo-bg: #f7fafc;
}
* { box-sizing: border-box; }
body {
  font-family: 'Helvetica Neue', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  max-width: 920px; margin: 0 auto; padding: 2rem;
  line-height: 1.65; color: var(--fg); background: var(--bg);
}
h1 { font-size: 2.1rem; color: var(--primary); margin-bottom: 0.2rem; }
.subtitle { color: var(--muted); font-size: 1.05rem; margin-bottom: 2rem; }
h2 { color: var(--primary); border-bottom: 2px solid var(--border); padding-bottom: 0.4rem; margin-top: 3rem; }
h3 { color: var(--accent); margin-top: 2rem; }
.toc { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 1rem 1.5rem; margin: 1.5rem 0; }
.demo { background: var(--demo-bg); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem 1.4rem; margin: 1.5rem 0; }
.controls { display: flex; flex-wrap: wrap; gap: 1.2rem; align-items: flex-end; margin-bottom: 1rem; }
.control { display: flex; flex-direction: column; min-width: 130px; }
.control label { font-size: 0.85rem; color: var(--muted); font-weight: 600; margin-bottom: 0.3rem; }
.control input[type="range"] { width: 180px; }
.value { font-family: 'JetBrains Mono', 'Courier New', monospace; color: var(--accent); font-weight: 600; }
.plot { background: white; border-radius: 6px; padding: 0.5rem; }
.insight { background: var(--insight); border-left: 4px solid var(--insight-border); padding: 0.8rem 1.2rem; margin: 1.2rem 0; border-radius: 0 6px 6px 0; }
.formula { background: #ebf4ff; padding: 0.6rem 1rem; border-radius: 6px; margin: 0.8rem 0; border-left: 3px solid var(--primary); }
code { background: var(--code-bg); color: var(--code-fg); padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.88em; font-family: 'JetBrains Mono', 'Courier New', monospace; }
pre { background: var(--code-bg); color: var(--code-fg); padding: 1rem 1.2rem; border-radius: 6px; overflow-x: auto; font-size: 0.88em; line-height: 1.5; }
pre code { background: none; padding: 0; }
.selftest { background: #ebf8ff; border: 1px solid #63b3ed; border-radius: 8px; padding: 1rem 1.5rem; margin: 2rem 0; }
.stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin: 0.8rem 0; }
.stat { display: flex; justify-content: space-between; padding: 0.3rem 0.6rem; background: white; border-radius: 4px; border: 1px solid var(--border); }
.stat-label { color: var(--muted); }
.stat-value { font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.nav { display: flex; justify-content: space-between; margin: 3rem 0 1rem; padding-top: 1rem; border-top: 1px solid var(--border); color: var(--muted); }
.nav a { color: var(--primary); text-decoration: none; }
```

The colour palette is intentional: soft blue primary for headings, warm orange accent for highlights, pale yellow for "insight" boxes, dark slate for code blocks. Do not change these without good reason. Consistency across lessons matters.

---

## 5. CDN dependencies

Always load these three in `<head>`:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
```

KaTeX renders math. Plotly draws plots. No other libraries.

If you ever need a feature beyond Plotly, look at it twice. Adding a fourth dependency breaks the "one click to view" promise. Better to write 30 lines of vanilla SVG than pull in D3.

---

## 6. Math rendering

Math goes in `$...$` for inline and `$$...$$` for display. KaTeX renders after DOMContentLoaded:

```javascript
document.addEventListener("DOMContentLoaded", () => {
  if (typeof renderMathInElement !== "undefined") {
    renderMathInElement(document.body, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
      ],
      throwOnError: false
    });
  }
});
```

The `throwOnError: false` keeps the page rendering even if a single equation has a typo. Production-grade math pages flip this to true once stable.

`<div class="formula">` is the visual container for display equations. KaTeX reads through it without issue.

---

## 7. Synthetic data: the PRNG and noise generators

Every dashboard generates its own data. The PRNG is **Mulberry32**, fast and seedable. Paste this into every script block that needs randomness:

```javascript
function mulberry32(seed) {
  return function() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
```

Standard normal via Box-Muller:

```javascript
function randn(rng) {
  let u = 0, v = 0;
  while (u === 0) u = rng();
  while (v === 0) v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}
```

Student t (df normal squareds in the chi-squared denominator):

```javascript
function randt(rng, df) {
  const z = randn(rng);
  let chi = 0;
  for (let i = 0; i < df; i++) {
    const g = randn(rng);
    chi += g * g;
  }
  return z / Math.sqrt(chi / df);
}
```

GARCH(1,1) with leverage effect:

```javascript
const sig = new Array(n); sig[0] = baseVol;
const ret = new Array(n); ret[0] = mu + sig[0] * eps[0];
for (let t = 1; t < n; t++) {
  const negImpact = (ret[t-1] < 0 ? 1 : 0);
  const arch = (alpha + Math.abs(leverage) * negImpact) * ret[t-1] * ret[t-1];
  sig[t] = Math.sqrt(omega + arch + beta * sig[t-1] * sig[t-1]);
  ret[t] = mu + sig[t] * eps[t];
}
```

For multivariate normal, use Cholesky decomposition rather than `np.linalg.cholesky` (which we do not have in the browser). Hand-roll the 2x2 case:

```javascript
// Sigma = [[a, b], [b, d]]
const La = Math.sqrt(a);
const Lba = b / La;
const Lc = Math.sqrt(d - Lba * Lba);
// Sample: x = La * z1, y = Lba * z1 + Lc * z2
```

For 3+ assets, hand-roll a generalised Cholesky loop. Or use eigendecomposition (slower but conceptually cleaner: project a standard normal vector through `V * sqrt(Lambda)`).

---

## 8. Interactive widget pattern

Every demo follows the same pattern:

```html
<div class="demo">
  <div class="controls">
    <div class="control">
      <label>Parameter name: <span class="value" id="param_v">0.5</span></label>
      <input type="range" id="param" min="0" max="1" step="0.01" value="0.5">
    </div>
    <!-- more controls -->
  </div>
  <div id="my_plot" class="plot" style="height: 400px;"></div>
  <div class="stat-grid">
    <div class="stat"><span class="stat-label">Some metric</span><span class="stat-value" id="metric_v">0</span></div>
  </div>
</div>
```

JavaScript wiring:

```javascript
function updateMyDemo() {
  const param = parseFloat(document.getElementById('param').value);
  document.getElementById('param_v').textContent = param.toFixed(2);

  // ... compute the data, the metrics ...
  document.getElementById('metric_v').textContent = computed.toFixed(3);

  Plotly.react('my_plot', [...traces...], {...layout...}, { displayModeBar: false });
}
['param', 'other_param'].forEach(id => document.getElementById(id).addEventListener('input', updateMyDemo));
updateMyDemo();
```

Three rules.

1. **`Plotly.react`, not `Plotly.newPlot`.** `react` reuses the existing plot div and is much faster on re-renders. `newPlot` recreates everything and flickers.
2. **`displayModeBar: false`** for teaching demos. The toolbar is noise.
3. **Call the update function once at the end** of script execution to draw the initial state.

---

## 9. Layout: Plotly grids and shapes

Multi-panel plots use `grid` in the layout:

```javascript
{
  grid: { rows: 2, columns: 2, pattern: 'independent' },
  ...
}
```

For markers (VaR lines on a histogram), use `shapes` and `annotations`:

```javascript
shapes: [
  { type: 'line', x0: 0, x1: 0, yref: 'paper', y0: 0, y1: 1,
    line: { color: '#dd6b20', width: 2.5, dash: 'dash' } }
],
annotations: [
  { x: 0, y: 1, yref: 'paper', text: 'VaR', showarrow: false }
]
```

`yref: 'paper'` means "the full vertical extent of the plot". Useful for vertical lines that span the whole y-axis without you computing min/max.

For 2D scatter with an overlay ellipse: stack three traces, scatter for the cloud, scatter mode 'lines' for the ellipse, scatter mode 'lines+markers' for the eigenvector arrows. Use `scaleanchor: 'y', scaleratio: 1` on the x-axis to keep the ellipse from stretching.

---

## 10. Pedagogical pattern for a concept section

Each substantive section follows the same shape:

1. **Why this matters.** One paragraph framing the problem.
2. **Definition or formula.** Inside a `<div class="formula">`.
3. **Plain-English unpacking.** A paragraph or two explaining the formula in words.
4. **Live demo.** The `<div class="demo">` block.
5. **Aha moment.** A `<div class="insight">` with bold "Aha:" or "Notice:" prefix, telling the reader what manipulation to try and what to look for.
6. **Optional Python translation.** A `<pre><code>...</code></pre>` block showing the corresponding numpy/pandas code. Three to ten lines, no more.

Example aha moment styles:
- "Drag X up. Watch Y do Z."
- "Crank X to extreme. The thing you expect happens, plus a side effect you did not."
- "Compare A vs B. The difference is exactly the term we just derived."

Always tell the reader what to try and what they will see. Never leave the demo as a "play around with this".

---

## 11. The two structural sections you must add

After the concept sections, you always add two structural sections.

**Mathematical companion.** A header `<h2 id="s_math">N. Mathematical companion: derivations and proofs</h2>`, then `<h3>` subsections with full derivations. This is where you dump the textbook-style content that does not fit naturally inline. Subsections cover: proofs of identities, formal statements of theorems with assumptions, regime conditions, connections to other lessons, edge cases.

**Coding exercises (extras).** A header `<h2 id="s_code">N. Coding exercises (extras)</h2>`, then 3 to 5 code snippets that the reader can implement. These are *unscaffolded*, unlike the notebook exercises. The reader writes them on paper or in their own environment.

The companion notebook (`module_X_exercises.ipynb`) covers the scaffolded versions. The HTML extras are bonus problems for stronger students.

---

## 12. Self-test format

Three questions. Always three.

```html
<div class="selftest">
  <h3>Question 1, conceptual</h3>
  <p>Question text.</p>
  <p><em>Hint or partial answer:</em> ...</p>
</div>

<div class="selftest">
  <h3>Question 2, coding</h3>
  <p>Question text.</p>
  <pre><code>def example_skeleton(): ...</code></pre>
</div>

<div class="selftest">
  <h3>Question 3, numerical</h3>
  <p>Question text. Compare with the dashboard or compute by hand.</p>
</div>
```

Conceptual exposes understanding. Coding requires writing 5 to 15 lines. Numerical forces the reader to verify a result with their own arithmetic.

---

## 13. Build process for a new lesson

When asked to build `lesson_NN_<topic>.html`:

1. **Read the master plan.** Open `Portfolio Construction Master Plan.md` and `Portfolio Construction Dashboard Plan.md`. Find the lesson's "topics" list and "dashboard" specification.
2. **Decide the demo set.** Each section that benefits from interactivity gets a demo. Aim for 3 to 6 demos per lesson, not more.
3. **Decide the parameter glossary.** What sliders / dropdowns / toggles will appear? Document each one in Section 0.
4. **Plan the math companion.** What 6 to 8 subsections do you need? Pick the proofs and theorems first.
5. **Copy the canonical reference.** Start from `lesson_01_returns_stylised_facts.html` (or the most similar existing lesson). Strip the section content but keep the CSS, the script utilities, and the structural sections.
6. **Fill in section by section.** Write Section 0 (glossary) first, then Sections 1 to N in order. Math companion last.
7. **Write the JavaScript demos as you go.** Section 1 demo first, test in browser, move to Section 2, etc. Do not wait until the end to wire interactivity.
8. **Cross-link to other lessons.** When a concept previews or recalls another module, name the lesson explicitly: "see Lesson 9", "previewed in Module D".
9. **Update the README.** Add the new file to the table.
10. **Update the dashboard plan if needed.** If you discover the spec is wrong, fix it.

---

## 14. Common pitfalls

- **Forgot to call the update function once at the bottom.** Sliders are wired but the initial render is blank. Always end every demo's script with `updateMyDemo();`.
- **Used `Plotly.newPlot` instead of `Plotly.react`.** Causes flicker and slowness on every slider drag.
- **KaTeX did not render.** Check that the `renderMathInElement` block is in the script, the script is at the bottom of `<body>`, and `throwOnError: false` is set.
- **Math escaped wrong.** Inside JavaScript template strings or HTML attributes, `\\` for one backslash. Inside the visible text content, use single `\`. Mismatch breaks math silently.
- **Sigma not PSD.** When sliders for sigmas and rhos are independent, the user can produce non-PSD covariance. Detect and project to nearest PSD via `eigh + clip + V Lambda V'`. Lesson 2 has the canonical example.
- **Cached state across slider changes.** If a generator is expensive, cache by a hashable key. See the `cachedKey` pattern in Lesson 3.
- **Plot height too small.** 320 to 480 pixels per plot, depending on complexity. Multi-panel grids need 600 to 800.
- **Em-dashes.** Project rule: never use them. Use commas, colons, parentheses, "to".
- **Forgotten responsive width.** `max-width: 920px; margin: 0 auto` works on desktop. Don't try to handle mobile. The use case is laptop.

---

## 15. When to deviate from the template

Almost never. The point is consistency: a reader should open Lesson 14 and feel at home from the layout alone. Deviate only when:

- The topic genuinely needs a 3D visualisation. Plotly's `scene` mode is your friend.
- The topic needs a step-by-step animation rather than a slider. Use Plotly's `animate` API or `setInterval`.
- The topic needs textual code-as-output (e.g., a regex builder). Use a `<textarea>` plus a results panel.

When you deviate, document the deviation at the top of the lesson with `<!-- DEVIATION: ... -->` so the next agent knows.

---

## 16. Companion notebook conventions

For each module, build one `module_X_exercises.ipynb`. Conventions:

- **Setup cell at top.** Imports + synthetic data generation. The whole module's exercises read from this single setup.
- **Each exercise has two cells.** Markdown with the prompt + hint, then code with `___` blanks and an `assert` to validate.
- **Exercises chain.** Later exercises call functions defined in earlier ones. This is intentional: the reader builds up a small library by the end of the module.
- **At least one bonus integrative exercise per module.** Tie multiple lessons together. Preview the next module.

See `module_a_exercises.ipynb` for the canonical example (33 exercises spanning Lessons 1, 2, 3 plus three bonus integrative problems).

---

## 17. Suggested time budget per new lesson

- Reading the master plan and deciding the demo set: 15 minutes.
- Section 0 glossary: 30 minutes.
- Each concept section (text + formula + demo + JS): 45 to 60 minutes.
- Mathematical companion: 60 minutes.
- Coding exercises section: 30 minutes.
- Self-test: 15 minutes.
- Wiring, testing, polish: 30 minutes.

For a typical 6-section lesson: 5 to 7 hours from cold to live.

---

## 18. Scaling up: the rest of Module B and beyond

After Module A's three lessons, you have 27 more to build. The plan calls for:

- **Module B (Lessons 5, 6, 8):** Markowitz core. Heavy on optimisation and convex programming. Plan to bring in Plotly's frontier visualisation.
- **Module C (Lessons 9, 10, 13):** Estimation error. Heavy on simulation: bootstraps, perturbations.
- **Module D (Lessons 11, 12, 7):** BL, robust, risk budgeting.
- **Module E (Lessons 14, 15, 16):** Risk parity family. Algorithms (HRP recursive bisection, ERC coordinate descent) need step-by-step animations.
- **Module F (Lessons 20, 21, 22):** Production. Vol targeting and Kelly need Monte Carlo.
- **Module G (Lessons 24, 25, 26):** Factor models, signal blending. The signal stack composer in Lesson 26 will be the most complex demo in the curriculum.
- **Module H (Lessons 23, 27, 29):** Validation, regime, capstone. Lesson 29 is the integration of everything.

Build in module order. Inside a module, build in lesson order. Do not skip ahead.

---

## 19. One last thing

Read `lesson_01_returns_stylised_facts.html` again before you start. Twice. The conventions are denser than this guide can capture in prose. The reference implementation is the spec.

Good luck.
