(Chap_MacroCalib)=
# Calibration of Macroeconomic Parameters

## Economic Assumptions

### Start year

The model's initial period is **2025** (`start_year`), a calibration decision rather than a default: the start year should be the most recent year the calibration can *observe*, not a projection year. 2025 is the last complete year, and the anchors line up with it directly — the remittance level is the observed 2025 personal-remittance ratio, the sovereign-rate anchor uses FY 2024–2025 interest actuals, and `initial_debt_ratio` $= 0.60$ matches the debt ratio at the *start* of 2025 (end-2024: 60.7%, BTr), where a 2026 start would require ~0.62. The remaining data vintages (OECD taxes 2023, PWT capital 2023, FIES incomes 2023) sit one year closer to the start than they would under a 2026 start. The demographic arrays regenerate for the chosen start year via `ogphl.update_baseline_demographics`, which also rebuilds the demographics-derived remittance parameters.

### Productivity growth

As the rate of labor-augmenting technological change, $g_y$, we use 3.13% — the average annual growth rate of World Bank GDP per person employed (constant 2021 PPP dollars, `SL.GDP.PCAP.EM.KD`) for the Philippines over 2000–2019, computed by `ogphl.macro_params` and baked into the packaged parameters. The pre-pandemic window is used deliberately to avoid COVID-era volatility distorting the steady-state productivity target; the Penn World Table 11 gives 3.24% over the same window, a close cross-check.

The series is output *per person employed*, not per capita, because $g_y$ is the growth of labor productivity: the model's demographics already generate the rising share of the population at work (the Philippine demographic dividend), so per-capita growth — 3.71%, the value this calibration previously used — counted that dividend twice. With the steady state's long-run population growth of −0.56% (UN projections), total long-run GDP growth is 2.6% a year. That is below the 6–7% the government's Medium-Term Fiscal Framework projects for the coming years; the steady state describes the long run, not the convergence decades. Long-run growth also enters the fiscal block: the debt-stabilizing primary balance at the 0.60 debt target is $-0.35\%$ of GDP.

### GDP at market prices

Every ratio in this calibration is a share of GDP at market prices, the GDP the Philippine data are published against, and the model is scored on the same basis. That takes one conversion, because OG-Core's output $Y$ is not market-price GDP. Households pay $(1+\tau^c)$ times the producer price of consumption and the tax goes to the government, so the consumption tax is collected on top of $Y$: $Y$ is the sum of factor incomes, and GDP at market prices is $Y$ plus consumption-tax revenue. This is the standard mapping between a model with consumption taxes and the national accounts ({cite}`Prescott:2004`, following {cite}`MendozaRazinTesar:1994`, whose consumption tax rate is defined on consumption at pre-tax prices, as OG-Core's is). With consumption taxes at 7.94% of market-price GDP, market-price GDP is $1/(1-0.0794) = 1.086$ times $Y$. The 2018 social accounting matrix gives the same ratio independently: market-price GDP is 1.089 times the sum of factor incomes.

Two things follow. The dashboard in `ogphl/targets.py` divides every model ratio by $Y$ plus the consumption tax before comparing it with the data. And the parameters that OG-Core multiplies by its own $Y$ (transfers $\alpha_T$, spending $\alpha_G$, public investment $\alpha_I$, remittances $\alpha_{RM}$, the debt ratios, initial household wealth and initial public capital) are the data share times 1.086, so that each one is the published share of market-price GDP. The raw model output tables report ratios to $Y$, so they read about 8.6% above the published figures: debt of 0.652 of $Y$ is the 0.60 of GDP the program anchors.

This matters for the Philippines and not for OG-USA, whose consumption tax is 1%. Before the conversion every fiscal ratio in this calibration ran 7–8% below its data target on the market-price basis, the capital stock 3.32 times GDP instead of 3.59, and the capital share counted product taxes as capital income (see {ref}`Chap_FirmCalib`).

## Open Economy Parameters

### Foreign holding of government debt in the initial period

The path of foreign holding of domestic debt is endogenous, but the initial period stock of debt held by foreign investors is exogenous. We set this parameter, `initial_foreign_debt_ratio`, to 0.2, based on the Bureau of the Treasury (BTr) Debt Indicator report for Q4 2025 ([source](https://www.treasury.gov.ph/wp-content/uploads/2026/02/Debt-Indicator-December-2025.pdf)).

### Foreign purchases of newly issued debt

We set $\zeta_D = 0.2$. This is calibrated to equal `initial_foreign_debt_ratio` above, on the assumption that the foreign share of newly issued debt matches the foreign share of the existing stock.

### Foreign holdings of excess capital

We set $\zeta_K = 0.172$. This parameter governs the share of the gap between domestically-supplied capital and the capital demanded at the world interest rate that foreign investors fill, so it is effectively the degree of openness of the capital account at the margin. It is a *marginal* fill share, not a directly measured quantity, so we calibrate it by the level it produces: $\zeta_K = 0.172$ puts the solved steady-state foreign-owned share of the capital stock at 20%, matching the Bangko Sentral ng Pilipinas International Investment Position. With the return on capital at 8.3% against a 5% world rate, the capital that would be demanded at the world rate exceeds what Philippine households own, and foreigners filling about a sixth of that gap supply a fifth of the capital stock. The normalized Chinn-Ito capital-account openness index (roughly 0.4, [Chinn-Ito index](https://web.pdx.edu/~ito/Chinn-Ito_website.htm)) measures legal openness rather than this share, and is not a target. $\zeta_K$ is tuned jointly with the discount factor (see {ref}`Chap_HouseholdCalib`): together they set private capital and its foreign share, and they moved together when the capital share and the GDP basis were corrected (the previous pair was 0.0705 with a return on capital of 11.4%). Re-validate the solved foreign share after any tax-side or saving-side change.

It also restores a domestic-capital buffer the transition needs: at $\zeta_K = 0.9$ domestic capital ($K_d = B - D_d$) is only ~4% of the stock, so the $K_d \geq 0$ constraint binds along the path and the resource constraint fails to close; at 0.4 it clears.

### World interest rate

The small-open-economy block prices foreign capital and foreign debt at an exogenous world interest rate, `world_int_rate_annual`. We set it to 5% — a global risk-free rate of about 4% plus a Philippine country-risk premium of roughly 100 basis points, the Philippines being an investment-grade (BBB) sovereign. The previous 4% placeholder omits this premium, understating the supply price of foreign capital and so overstating foreign ownership of the capital stock.

### Remittances as a share of GDP

Personal remittance inflows to the Philippines are a substantial component of household income. The ratio of aggregate remittances to GDP is governed by two parameters: $\alpha_{RM,1}$ for the model's start period and $\alpha_{RM,T}$ for the long run / steady state. Both are set to 8.12% of GDP at market prices (0.0882 of the model's $Y$; see the GDP-at-market-prices section above), and the long-run value is calibrated to equal the current-period value so the calibration implies no remittance transition.

The level is *personal* remittances, the BPM6 measure of household income from abroad, which is the concept the model's $RM$ represents. Bangko Sentral ng Pilipinas (BSP) reports full-year 2025 personal remittances of US\$39.62 billion and cash remittances of US\$35.63 billion, the latter equal to 7.3% of GDP. Applying BSP's own published ratio to the personal measure gives $0.073 \times 39.62/35.63 = 8.12\%$ of GDP, using one consistent GDP denominator throughout. This sits inside the 8.0–9.0% band BSP research reports for personal remittances since 2017 {cite}`BayangosLubangco:2025`; the narrower cash series runs 7.0–8.0%, and calibrating to it understates household income from abroad by roughly a percentage point of GDP. See {doc}`households` for the measurement distinction, the growth path $g_{RM}$, and the household allocation `eta_RM`.

## Government Debt, Spending and Transfers

### Government Debt

The path of government debt is endogenous.  But the initial value is exogenous.  To avoid converting between model units and dollars, we calibrate the initial debt to GDP ratio, rather than the dollar value of the debt.  This is the model parameter $\alpha_D$.  We compute this from the ratio of publicly held debt outstanding to GDP.  Based on [a 2024Q1 report from Treasury](https://www.treasury.gov.ph/?p=64737) the value is 0.60 of GDP at market prices, which is 0.652 of the model's $Y$.

We also set the long-run (steady-state) debt-to-GDP target, `debt_ratio_ss`, to 0.60 of GDP (0.652 of $Y$), matching the initial ratio rather than the 1.10 US-style placeholder inherited from OG-Core. This keeps the fiscal closure consistent with the Philippine debt position at both ends of the transition.

```{figure} ./images/debt_ratio_ss_anchor.png
---
height: 400px
name: FigDebtRatioSSPHL
---
Philippine national-government debt-to-GDP, 2000–2025 (Bureau of the Treasury). `debt_ratio_ss` is calibrated to 0.60 — at the MTFF 60% soft ceiling and equal to the current stance, within the ~45–60% band implied by the IMF general-government measure (~57%), the MTFF target, and the World Bank's prudence range. It replaces the inherited 1.10 US-style placeholder, which sat above the entire historical range (2004 peak 71.6%; 2019 trough 39.6%). The lower anchor also shrinks the share of household saving absorbed by government debt, easing the crowding-out that had inflated the foreign-owned capital share.
```

### Aggregate transfers

Aggregate (non-Social Security) transfers to households are set as a share of GDP with the parameter $\alpha_T$. We exclude Social Security from transfers since it is modeled specifically. We set transfers to 4.48% of GDP ($\alpha_T = 0.0487$ of the model's $Y$) using World Bank World Development Indicators data for 2023. The value is computed as the product of total government expense as a share of GDP (WDI series `GC.XPN.TOTL.GD.ZS`) and the share of that expense classified as subsidies and other transfers.

### Government expenditures

Government spending on goods and services is set as a share of GDP with the parameter $\alpha_G$. It is **not** set to the observed spending share; it is set to the level consistent with the government budget, the single most consequential discipline in the fiscal calibration. All shares below are of GDP at market prices; $\alpha_G$ itself is a share of the model's output, 1.086 times larger.

For debt to hold at `debt_ratio_ss` $= \bar{d}$, the government must run a primary balance $pb^* = \frac{r_{gov} - g}{1 + g}\,\bar{d}$, where $g$ is the model's steady-state growth rate. With $r_{gov} = 2.0\%$ and $g = 2.55\%$ (3.13% productivity growth and −0.56% long-run population growth), $pb^* \approx -0.32\%$ of GDP. In the steady state OG-Core makes $G$ the residual of that identity: with revenue of 19.4% of GDP, transfers of 4.48%, public investment of 5.2% and a mature pension system paying 6.97%, government consumption is 3.2% of GDP.

Along the transition $\alpha_G$ binds for the first $t_{G1} = 20$ years, so it is a path, and it follows the government's own fiscal program where the program is data:

| Years | $\alpha_G$ (% of GDP) | Anchor |
|---|---|---|
| 2025 | 10.1 | programmed primary balance −2.51% |
| 2026 | 9.7 | −2.26% |
| 2027 | 8.7 | −1.59% |
| 2028 | 7.7 | −1.03% |
| 2029–2044 | 6.8 | debt back at 60% of GDP in 2044 |

The programmed primary balances are the national government's deficit less interest in the DBM Budget of Expenditures and Sources of Financing for FY 2026, Table A.2 (`ogphl/data/fiscal_program_PHL.csv`). Each year's value is the spending share that reproduces it given the model's own revenue and pension outlays on the solved transition, and the solved baseline lands on all four to the hundredth of a point. From 2029, when the program ends, spending holds the level that returns debt to 60% of GDP by 2044, the year before the budget rule takes over. (Holding instead the level whose average primary balance equals $pb^*$ ran surpluses early and paid debt down to 49% of GDP, because transition revenue starts high and falls.)

For comparison, the DBM's Budget of Expenditures and Sources of Financing implies a goods-and-services share of about 13% of GDP on a primary basis (FY 2026 disbursements of 21.5% of GDP less transfers and interest). The model's lower path is the consolidation the program itself plans and the cost of the transition's revenue dip (below): the program's deficit falls from 5.5% of GDP in 2025 to 4.3% in 2028. Two structural points matter for anyone recalibrating this block. OG-Core's steady-state closure makes $G$ the residual of the budget identity regardless of the input $\alpha_G$, so an inconsistent value only destabilizes the *transition*, where $\alpha_G$ binds and excess spending compounds into the debt-elastic premium. And revenue errors mask spending errors: an earlier calibration paired $\alpha_G \approx 0.17$ with a flat 20% income tax that over-collected by a factor of six; the two errors cancelled in the steady state while distorting every household decision in the model.

### Initial household wealth

OG-Core's transition path historically imposed the initial distribution of household wealth as the steady-state profile rescaled so that *aggregate* initial wealth equals its steady-state level. For the Philippines that rescale factor is 1.625 — the 2026 population is young relative to the model's stationary distribution — so every initial household received a 63% wealth windfall, which short-horizon retirees rationally consumed: a 41% one-year jump in aggregate consumption, domestic investment collapsing to ~2% of its long-run level, and a spurious debt paydown to 50% of GDP. See [OG-Core issue #1188](https://github.com/PSLmodels/OG-Core/issues/1188).

This calibration instead anchors initial wealth to data with `initial_wealth_ratio`, an OG-Core parameter since release 0.22.0. It is the target ratio of initial aggregate household wealth to *initial-period* GDP, $B(0) = $ `initial_wealth_ratio` $\times Y(0)$, and the transition solve moves $B(0)$ toward that target as it iterates, since initial GDP is itself solved for. So the parameter is the data value, 3.35 times GDP at market prices, which is 3.64 times the model's output. (An earlier version of this calibration was built against a draft of the feature, [OG-Core PR #1189](https://github.com/PSLmodels/OG-Core/pull/1189), which defined the ratio against steady-state GDP and needed a mapped value of 2.78; that draft was not merged, and under the released semantics 2.78 would have meant 2.78.) Reform runs start from the baseline's initial wealth: the initial state is history, and policy cannot change what households start with. The data target's construction, each piece from its most authoritative source:

| Piece | Value | Source |
|---|---|---|
| Total capital-output ratio | 3.97 | PWT 11, 2023, current-PPP series pair |
| less public capital stock | −0.38 | IMF ICSD/PIMA: Philippine public capital low by EM standards (~0.35–0.40 of GDP) |
| × domestically-owned share | × 0.80 | BSP IIP: ~20% of capital foreign-owned |
| + domestically-held government debt | +0.48 | BTr: 80% domestic share × 0.60 debt ratio |
| **Household wealth to GDP, 2025** | **≈ 3.35** | |

The capital-side construction is the model-consistent measure — the model forces $B(0) = K_d(0) + D_d(0)$ — and household-net-worth estimates (UBS Global Wealth Report class, ~2.3–2.6× GDP) sit below it, as expected where surveys undercount real property. The steady state, solved without targeting household wealth, holds 3.35 times GDP too: the capital stock, its foreign share and domestically-held debt that the steady state is tuned to imply the same household wealth as the initial-period data.

**What the early transition gets right and wrong.** The transition starts on the data where the data are anchored: household wealth 3.34 times GDP in 2025 (target 3.35), debt 0.598, the foreign share of capital 22% (IIP about 20%), pension outlays 2.28% and the programmed primary balance. The composition of spending in the first years is the calibration's main remaining miss:

| | 2025 | 2030 | 2035 | Steady state | Data |
|---|---|---|---|---|---|
| Household consumption (purchaser prices) | 80.8% | 73.0% | 70.2% | 77.8% | 76.1% (2024) |
| Fixed investment, private + public | 20.2% | 26.1% | 26.9% | 23.9% | 23.6% (2024) |
| Household wealth / GDP | 3.34 | 2.81 | 2.59 | 3.35 | 3.35 (anchor) |
| Foreign share of capital | 22% | 31% | 34% | 20% | ~20% (IIP) |

The model starts consuming 4.7 points of GDP more than the data and investing 3.4 points less, then swings the other way: over the first decade the working-age population grows fast, the return on capital rises from 8.0% to 9.9%, investment rises above its long-run share, and foreign capital fills a growing part of it while household wealth falls relative to a fast-growing GDP. The likely cause of the first-year gap is how initial wealth is spread across ages. OG-Core scales the steady-state age profile of wealth to hit the aggregate anchor (it has no input for initial wealth by age). The Philippine population is young, with fewer of the wealthy older households the steady-state profile is built on, so hitting the aggregate scales every age up: each household starts with more wealth than its steady-state counterpart of the same age, and consumes some of it. A wealth-by-age anchor from a Philippine household survey is the next refinement; until then, results for the first few years of a transition should be read with this in mind. Before the initial-wealth anchor, the same mechanism produced a 41% one-year jump in consumption; with it, the initial distortion is a few points.

### Fiscal paths against actuals and the program

```{figure} ./images/fiscal_paths_vs_program.png
---
height: 500px
name: FigFiscalPathsPHL
---
Baseline model transition paths, as shares of GDP at market prices, against actuals (2023–2024) and the national government's fiscal program (2025–2028), from the DBM Budget of Expenditures and Sources of Financing, Table A.2 (FY 2025 edition for 2023, FY 2026 for 2024–2028) and, for end-2024 debt, the Bureau of the Treasury; the data are in `ogphl/data/fiscal_program_PHL.csv` and the figure is drawn by `scripts/plot_fiscal_paths.py`. The primary balance is the deficit less interest. The model lands on the programmed primary balance in all four program years (−2.51, −2.26, −1.59, −1.03% of GDP); over 2029–2044 it runs between −0.31% (2029) and −1.93% (2044), and the budget rule takes over in 2045. Debt starts at 59.8% against the end-2024 actual of 60.7%, peaks at 61.8% in 2028, falls to a trough of 57.1% in 2037 and returns to 60–61.5% from 2044. Revenue is the program's national-government revenue plus a +3.78 point bridge to the model's general-government concept (the 2023 gap between OECD Revenue Statistics and Treasury revenue, mostly social security contributions and local taxes); the 2024 actual is high because it includes one-off non-tax transfers (2.3% of GDP of non-tax revenue, against 0.8–1.1% in other years). Model revenue falls from 19.6% of GDP in 2025 to a low of 18.2% in 2041 while the program's rises to 20.1% by 2028: the program embeds tax-administration gains the calibration holds constant, and transition revenue dips as consumption falls relative to GDP (see the initial household wealth section). Public investment sits on the infrastructure program (5.3, 5.1, 5.1, 5.2% of GDP).
```

### Government interest rate wedge

The interest rate the government pays on its debt, $r_{gov,t}$, generally differs from the household interest rate $r_t$ — sovereigns often borrow at lower rates than the private market because they are seen as safer borrowers, but the spread also widens with the debt burden. OG-Core captures both through:

$$r_{gov,t} = \max\Big(r_{gov,scale} \cdot r_t - r_{gov,shift} + r_{gov,DY} \cdot \tfrac{D_t}{Y_t} + r_{gov,DY2} \cdot \big(\tfrac{D_t}{Y_t}\big)^2,\; 0\Big)$$

**Level wedge.** The slope $r_{gov,scale} = 0.245$ — the pass-through of the private rate into the sovereign rate — comes from Philippine sovereign-vs-corporate yield data sourced from the IMF, following Li, Magud, Werner, and Witte (2021), [The Long-Run Impact of Sovereign Yields on Corporate Yields in Emerging Markets](https://www.imf.org/en/Publications/WP/Issues/2021/06/04/The-Long-Run-Impact-of-Sovereign-Yields-on-Corporate-Yields-in-Emerging-Markets-50224) (IMF WP/21/155). The intercept, however, is **re-anchored to the real effective rate the Philippine government actually pays on its debt stock** rather than taken from the LMWW cross-country estimate. In the model, $r_{gov}$ multiplies the entire debt stock in the debt-service line, so it is an *average* rate, and the matching data moment is interest payments over gross debt: the Bureau of the Treasury's Cash Operations Report puts FY 2024 interest payments at ₱763.3 billion ([source](https://www.treasury.gov.ph/wp-content/uploads/2025/02/COR-Press-Release-FY-2024.pdf)) on an average national-government debt stock of about ₱15.3 trillion — a 5.0% nominal effective rate — less expected inflation of about 3% (the BSP target midpoint) gives a **real effective rate of about 2.0%** (FY 2025, with interest of ₱854 billion on a larger stock, gives essentially the same rate). `r_gov_shift` is set to $-0.0140$ so the steady-state $r_{gov}$ equals that value (the stored shift includes the debt-elastic recentering described below). The raw LMWW intercept instead put the steady-state $r_{gov}$ at 5.1% real — 3 percentage points above what the Treasury pays — which overstated debt service by about 1.9% of GDP and, through the budget identity, forced model government spending that much lower. The same correction was applied in OG-ZAF for the same reason.

A consequence worth stating plainly: at $r_{gov} = 2.0\%$ real and steady-state growth $g \approx 2.55\%$, the model has $r_{gov} < g$, so the debt-stabilizing primary balance is a small *deficit* (about $-0.32\%$ of GDP) — consistent with the actual Philippine experience of stabilizing debt ratios while running primary deficits, because nominal growth exceeds the nominal effective interest rate. The actual FY 2024 primary deficit was 2.8% of GDP (BTr), so the model's steady state still embeds roughly two points of consolidation relative to the current stance.

**Debt-elastic premium.** The $r_{gov,DY}$ and $r_{gov,DY2}$ terms let the sovereign rate rise with the debt ratio — the crowding-out-via-risk channel that OG-Core and the sister country models leave off (otherwise a debt-financed reform raises debt with no feedback to borrowing cost). It is the [Schmitt-Grohé and Uribe (2003)](https://www.nber.org/system/files/working_papers/w9270/w9270.pdf) premium in convex (quadratic) form, following the fiscal-limits literature ([Bi 2012](https://www.sciencedirect.com/science/article/abs/pii/S0014292111001085); [Ghosh et al. 2013](https://www.nber.org/system/files/working_papers/w16782/w16782.pdf)). OG-PHL uses a *centered* form, $0.04\,(d_t - 0.6)^2$ with $d_t$ debt as a share of GDP at market prices — flat at the 0.60 target and steepening only as debt rises away — matching the country's stable spreads at 40–70% debt and stress only at 1980s-crisis levels. OG-Core measures debt against its own output, $D_t/Y_t = 1.086\,d_t$, so the packaged terms are $r_{gov,DY2} = 0.04/1.086^2 = 0.0339$ and $r_{gov,DY} = -0.048/1.086 = -0.0442$ (the constant is in `r_gov_shift`), which hold the steady state fixed and adds ~36 bp at $D/Y = 0.9$ and ~144 bp at 1.2 — within the emerging-market spread-to-debt range ([Jaramillo and Weber 2012](https://www.imf.org/external/pubs/ft/wp/2012/wp12198.pdf)). A conservative $r_{gov,DY2} = 0.02$ is a reasonable alternative.

Centering is what makes the premium usable along the transition. The multi-industry baseline debt path overshoots to about 1.3 times GDP early in the fiscal-adjustment window (period $t_{G1}$) before returning to 0.60, and the centered premium prices that overshoot at a plausible peak sovereign rate near 7.8%. A premium that bit at the target (vertex at zero debt) would instead compound the overshoot into a runaway debt-service feedback — toward ~1.7 and a ~16% rate. It is enabled by default.

## Validation: the steady-state dashboard

Most parameters are only weakly identified on their own, so the real test is whether the steady state they jointly produce resembles the economy. The table compares the solved steady state of the packaged calibration (the shipped example, run from an installed copy) with Philippine data; `examples/tune_ss.py` prints the same rows and `ogphl/targets.py` holds the targets and their sources. Every ratio is to GDP at market prices. The first three blocks are targeted, each by its own parameter; the last block is not, and is the independent check. The return on capital is open-economy latitude rather than a target, and the labor share equals one minus the capital share by construction with Cobb-Douglas production. The early transition, where the first years' consumption and investment shares miss, is scored in the initial household wealth section above; the fiscal paths are in the figure above.

| Moment | Model | Data | Gap | Source |
|---|---|---|---|---|
| **Fiscal** | | | | |
| Personal income tax | 3.12% | 3.12% | +0.1% | OECD Revenue Statistics Asia-Pacific 2025, PHL 2023 |
| Social security contributions | 2.78% | 2.78% | -0.0% | SSC, OECD Revenue Statistics 2025, PHL 2023 |
| CIT + BTr capital income | 4.19% | 4.20% | -0.2% | CIT 2.90 + BTr income from government capital ~1.00 + unallocable income taxes 0.30 (OECD 2023; BESF) |
| Consumption taxes + fees | 7.95% | 7.94% | +0.1% | VAT + excises + customs 7.39 (OECD 2023) + fees and charges 0.55 (BESF non-tax) |
| Property-type taxes | 1.33% | 1.32% | +0.8% | property-type taxes: RPT, DST, LGU levies (OECD 'other taxes' less estate) |
| Estate and donor taxes | 0.07% | 0.07% | +0.6% | estate tax collections, BIR |
| Transfers | 4.48% | 4.48% | -0.0% | alpha_T: social transfers, DBM/BESF |
| Public investment | 5.20% | 5.20% | -0.0% | alpha_I: public infrastructure program, MTFF/BESF |
| Pension outlays | 6.97% | 6.97% | +0.0% | today's 2.28% (SSS 1.06% 2023, GSIS 0.68% 2024, MUP fund 0.54% 2024 GAA) x 3.056, the rise in covered retirees per worker to the steady state (a mature system in the long-run population) |
| Government debt (anchor) | 0.60 | 0.60 | -0.0% | debt_ratio_ss: MTFF program anchor |
| Real rate on government debt | 2.00% | 2.00% | -0.1% | BTr FY2024: interest P763.3bn on ~P15.3tn average debt, less ~3% expected inflation |
| **External** | | | | |
| Foreign share of capital | 19.97% | 20.00% | -0.2% | BSP International Investment Position, inward share |
| Personal remittances | 8.12% | 8.12% | -0.0% | BSP 2025 personal remittances US$39.62bn (BPM6), the household income measure; the published 7.3% ratio is the narrower cash measure |
| **Production and saving** | | | | |
| Private capital | 3.59 | 3.59 | -0.1% | PWT 11 capital stock 2023 (3.97) less public capital ~0.38 (IMF ICSD); delta and beta are set to it |
| **Untargeted checks** | | | | |
| Fixed investment, private + public | 23.86% | 23.6% | | World Bank WDI 2024 (gross fixed capital formation) |
| Household consumption, purchaser prices | 77.78% | 76.1% | | World Bank WDI 2024 |
| Government consumption (budget residual) | 3.15% | 14.6% | | WDI 2024; the steady state sets G from the budget identity |
| Net exports (resource-constraint residual) | -4.79% | | | not a modelled trade sector |
| Household wealth | 3.35 | 3.35 | | initial-wealth construction, macro chapter |
| Total revenue | 19.44% | 19.43% | | OECD 2023 + captured non-tax (sum of the rows above) |
| Return on capital r | 8.32% | | | ballpark tier: open-economy latitude |
| Labor share of Y | 48.5% | 48.5% | | ILO 2023 x 1.086; equal to 1-gamma by construction at epsilon = 1 |
| Steady-state population growth | -0.56% | | | UN WPP terminal value (the steady state uses the end of the projection, not today's growth) |

Hours worked by age are scored separately in {ref}`Chap_HouseholdCalib`: the model is within 1–2% of the Labor Force Survey at every five-year band from 25 to 69.
