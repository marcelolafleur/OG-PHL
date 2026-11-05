# Practitioner's guide: keeping single- and multi-industry calibrations broadly compatible

Audience: anyone (human or agent) adjusting either the single-industry (M=1) or the
multi-industry (M>1) calibration of an OG-Core country model and needing the other
representation to stay in broad agreement. "Broad agreement" means: the same reform run
through both models gives the same signs and similar magnitudes in the percent-change
tables, shared data targets bind identically, and remaining gaps are known and explainable
— not mathematical equality.

This guide is written from OG-PHL but applies to any OG-Core country model
(OG-IDN, OG-ETH, OG-ZAF, ...). Each calibration keeps its own parameter file; nothing
here requires restructuring data.

## OG-Core structural facts these decisions rest on

Verified against ogcore 0.16.3 source; these are properties of OG-Core itself, not of any
country calibration.

- **The last industry (index M-1) is the numeraire and the only non-consumption
  producer.** Prices are normalized by it (`SS.py`: `new_p_m / new_p_m[-1]`), and ALL
  non-consumption final demand — private and government investment, government
  consumption, net capital outflows, remittances, foreign aid — is assigned to it
  (`SS.py` resource constraint: "M-1 industries only produce consumption goods").
  Consequence: the last industry's *nominal output share is mechanically inflated* and is
  never comparable to its value-added share in the data. Put the capital-goods-like
  industry (e.g. Manufacturing) last.
- **Consumption mapping**: `alpha_c` (length I, sums to 1) are Cobb-Douglas budget shares
  over consumption goods; `io_matrix` (I×M, rows sum to 1) maps goods to industries via
  `io_matrix.T @ C`. `tau_c` is per consumption good; `cit_rate`, `gamma`, `gamma_g`,
  `epsilon`, `Z` are per industry.
- **The composite consumption price is the unnormalized Cobb-Douglas index**
  `p_tilde = prod_i((1+tau_c_i) * p_i / alpha_c_i)^alpha_c_i` (`aggregates.get_ptilde`).
  It carries a units constant `prod_i(alpha_c_i^-alpha_c_i)` (≈2.97 for OG-PHL's five
  goods; =1 when I=1). Composite-consumption units therefore differ across
  representations, and because the utility weights `chi_n`/`chi_b` are fixed numbers,
  this units change is *behaviorally relevant*, not cosmetic.
- **The TFP level is not a free normalization in the open economy.** With the world
  interest rate as an absolute anchor, scaling all Z's changes the real wage relative to
  the world return, hence household saving vs foreign capital inflows, hence r and K_f/K.
  (In a closed economy the level would be neutral; these models are not closed.)
- **`factor` anchors both representations to the same currency data**:
  `factor = mean_income_data / model_mean_income` (`SS.py`). Since `mean_income_data`
  is shared, the two models' solved factors should come out nearly identical — this makes
  factor the best single-number diagnostic of level misalignment (OG-PHL: 179,355 vs
  179,325, a 0.02% gap).
- Value-added weights appear below as the aggregation weights. OG-Core never sees them —
  they come from the calibration data (the SAM) and are used only to build/collapse the
  per-industry parameters.

## Direction A: you trust the single-industry calibration, building/adjusting the multi

1. **Economy-wide values: copy verbatim.** Demographics, preferences, fiscal ratios
   (alpha_T, alpha_G, debt targets), open-economy dials (zeta_K, zeta_D, world rate,
   r_gov premium terms), g_y, statutory tax rates. Wherever they physically live, the
   values must be equal; any difference is a bug, not a modeling choice.
2. **Per-industry capital shares (gamma_m): keep the data's dispersion, impose the
   single's level.** Raw SAM factor shares are biased upward by self-employed mixed
   income (the Gollin problem); rescale so the VA-weighted arithmetic mean equals the
   single's gamma. The cross-industry pattern is what the SAM identifies; the level is
   better measured in the aggregate.
3. **Sector TFP (Z_m): relative values from data; the level is a weak lever — test,
   don't assume.** A common rescale of Z_m is theoretically clean (Hicks-neutral TFP:
   relative prices, gamma dispersion, and TFP ratios are all invariant; the numeraire
   *price* normalization p_M = 1 is independent). But in OG-PHL it was empirically a
   weak and wrong-signed lever for the aggregate gaps (an 11.7% level rise moved r *up*
   17bp), while the numeraire=1 convention already left `factor` matching the single's
   to 0.02% — i.e. the income level was already aligned. Keep the numeraire=1 convention
   unless a solved comparison says otherwise; the effective alignment lever is the
   utility-weight units conversion below.
4. **Convert the utility weights for the composite-consumption units change.** Because
   OG-Core's aggregator is unnormalized (see structural facts), moving from I=1 to I>1
   shrinks composite-consumption units by k = prod_i(alpha_c_i^-alpha_c_i) while chi_n
   and chi_b stay fixed numbers. FOC-invariance gives the exact conversion: scale both
   chi_n and chi_b by k^(sigma-1) in the multi-industry overlay (base file untouched).
   In OG-PHL (k=2.97, sigma=1.5, factor 1.723) this single derived constant closed
   44-80% of the r / K_f/K / B/Y / K/Y / C/Y gaps to the single-industry baseline.
   This is a units conversion, not a re-tune — the constant is derived, not fitted.
5. **What industry data don't identify: uniform at the single's value.** epsilon,
   gamma_g, cit_rate (unless sector-effective rates are actually published), tau_c,
   c_min = 0. Don't invent heterogeneity the data can't support.
6. **Pure structure needs only its identities**: alpha_c sums to 1, io_matrix rows
   sum to 1.
7. **Solver seeds: one set, in the base file, shared by both models.** The multi's
   continuation anchor (flat gamma, Z=1) is economically the shared aggregate economy
   and cold-starts from the base JSON's `initial_guess_*` seeds — the same values the
   single-industry model uses. If they are stale (they point at a steady state the
   economy no longer has), the anchor fails exactly the way the single does. The
   anchor's own solved r/TR/factor reproduce the seeds to within a few percent, so the
   multi can refresh them without ever running the single-industry example. Never give
   the overlay its own seed copy — that is a drift trap.

## Direction B: you trust the multi-industry calibration, setting the single

1. **Economy-wide values: copy verbatim** (same rule).
2. **gamma**: VA-weighted arithmetic mean of gamma_m (shares aggregate additively).
3. **Z**: decide who owns the level, then aggregate. If the multi's level is a numeraire
   convention (it usually is), do not import it — keep the single at Z=1 and treat the
   multi's level as the adjustable side. If the multi's level was genuinely anchored to
   data, set the single's Z to the VA-weighted (geometric) mean of Z_m. Exactly one
   model owns the level; two conventions produce two economies.
4. **Rates the multi differentiates: aggregate with matching weights** — output-weighted
   cit_rate, consumption-weighted tau_c, VA-weighted production parameters.
5. **Retune the single's solver guesses to its own steady state**
   (`initial_guess_r_SS`, `initial_guess_TR_SS`, `initial_guess_factor_SS`). The single
   cold-starts from these; the multi solves by continuation and barely uses them. Stale
   guesses after a recalibration make the steady state crawl or fail outright.

## The comparison dashboard (after solving both)

- **Must match exactly** (targets/policy, not outcomes): D/Y, D_f/D, tax rates,
  transfer and spending shares.
- **Should be close** (single digits %): K/Y, *nominal* consumption share
  (p_tilde·C/Y), aggregate labor L, and **factor** (see above — a large factor gap means
  a level misalignment upstream; find it before touching anything else).
- **Ballpark with a written explanation** (~1–2pp on rates, ~10–15% on ratios): r, r_p,
  K_f/K, B/Y. The multi typically sits somewhat higher on r and the foreign capital
  share; know why.
- **Never compare raw**: Y, w, C levels (different units by construction); raw C/Y in
  the multi (always use p_tilde·C/Y); the numeraire industry's nominal output share
  (mechanically inflated, see structural facts).

## Quick fault-finding

- r and K_f/K both too high in the multi → check the chi_n/chi_b units conversion first
  (Direction A rule 4); the Z level is a weak lever for this and moved r the wrong way in
  OG-PHL when tested.
- K/Y off → the gamma aggregation (weights or rescale) drifted.
- C/Y off → you compared raw C/Y, or the alpha_c/tau_c mapping changed.
- factor off → level misalignment somewhere upstream; fix that first.
- Everything off after a recalibration → shared values weren't propagated. Whenever
  economy-wide parameters change, re-solve *both* models in the same change set, and
  update any reference numbers one model's docs or examples quote about the other.
- Final acceptance: run the same reform through both and compare the percent-change
  tables — same signs, similar magnitudes.

## Status of OG-PHL against this guide (as of 2026-07-03)

Conforms on: shared economy-wide values (verified byte-identical across the two parameter
JSONs), gamma VA-mean rescale to 0.53785, uniform defaults (epsilon 1.0, gamma_g 0.05,
cit 0.25, tau_c 0.12), identities, retuned M=1 guesses, factor agreement (0.02%).
Known deviations and tested fixes (worktree experiments, 2026-07-03): as committed, the
M=8 aggregates sit off the M=1 baseline (r 0.0885 vs 0.0708, K_f/K 0.528 vs 0.257,
B/Y 2.38 vs 3.67) — cause is the composite-consumption units leak, NOT the Z level
(an 11.7% Z-level rise moved r the wrong way; falsified). Applying the derived chi
conversion (x1.7234 = k^(sigma-1), k=2.9702, sigma=1.5) moved M=8 to r 0.0808,
K_f/K 0.336, B/Y 3.29, K/Y 4.24 (vs 4.29), p_tilde*C/Y 0.496 (vs 0.510) — 44-80% of
each gap closed; residuals are composition effects; side effects: L overshoots to
-5.8% (from +7.7%) and factor drifts to 170,982 (-4.7%). Shipped on the #63 branch (2026-07-03): the chi conversion is in the multisector
overlay, computed by the builder from alpha_c with a pinning test (`497c56b`); the
retuned solver seeds are committed so the branch solves standalone (`ed3fb73`); the
example's stale reference numbers are fixed and the firms.md chapter documents the
conversion, the anchor seeding, and the corrected steady-state numbers (`4988f99`).
Still open: the example reform scenarios differ (M=1: CIT cut + debt 0.65; M=8: CIT
cut only), and the post-#68 rebase that dedups the shared commits. For the published
sources-and-methods documentation of the multi-industry calibration itself, see
`docs/book/content/calibration/firms.md` on the multi-industry branch — process and
verification guidance stays HERE, not in the book chapter.
