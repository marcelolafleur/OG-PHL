(Chap_GovCalib)=
# Calibration of Government Parameters

## Government Transfers as a Share of GDP

We calibrate Philippine government spending on transfer programs as a percent of GDP as $\alpha_T=[0.0448]$, using World Bank World Development Indicators data for 2023.

## Government Spending as a Share of GDP

The Department of Budget and Management (DBM), Budget of Expenditures and Sources of Financing (BESF) for FY 2026, Table A2 ([source](https://www.dbm.gov.ph/wp-content/uploads/BESF/BESF2026/A2.pdf)) forecasts total federal disbursements as a percent of GDP in 2026, 2027, and 2028 as 21.5%, 20.8%, and 20.6%, respectively. To get the portion that is net of transfers, we subtract off the calibrated share of spending on transfers $\alpha_T=[0.0448]$ from each. This gives our calibration for government spending net of transfers as a percent of GDP for 2026, 2027, and 2028 as $\alpha_G=[0.1702, 0.1632, 0.1612]$.


### Government spending on infrastructure as a share of GDP

We calibrate the vector $\alpha_I=[0.051, 0.051, 0.052]$. These values are forecasts for 2026, 2027, and 2028, taken directly from the "Infrastructure Program (Disbursements), Percent of GDP" row of the DBM, BESF for FY 2026, Table A2 ([source](https://www.dbm.gov.ph/wp-content/uploads/BESF/BESF2026/A2.pdf)).

## Public pensions

The Philippines has three public pension schemes: the Social Security System (SSS) for private-sector workers, the Government Service Insurance System (GSIS) for civil servants, and the uniformed-service pensions paid from the national budget's Pension and Gratuity Fund. Together they paid about 2.28% of GDP in benefits: SSS ₱257.4 billion in 2023 (1.06% of GDP), GSIS ₱179.9 billion in 2024 (0.68%), and the Pension and Gratuity Fund ₱143.0 billion in the 2024 General Appropriations Act (0.54%). The OECD's *Pensions at a Glance Asia/Pacific 2024* reports 7.7% of GDP for public pension spending without a breakdown; it cannot be reconciled with the paying institutions' own totals, which this calibration uses. (Earlier versions of the calibration switched pensions off entirely, with the US benefit formula's rates set to zero, while the payroll tax collected the contributions.)

The model uses OG-Core's defined-benefit system with the SSS rules (Republic Act 11199; OECD *Pensions at a Glance Asia/Pacific 2024*):

- **Pension age** 60 (`retirement_age`), after a career of 40 years (`yr_contrib`).
- **Benefit rate** `alpha_db` = 0.0217 per year of contribution. The SSS benefit is 20% of average monthly earnings plus 2% for each credited year beyond ten, which over a 40-year career is 80%, almost exactly 2% a year; it is paid 13 times a year, so $0.02 \times 13/12$.
- **Earnings base** the average of the last five years (`avg_earn_num_years` = 5). The SSS pays on the greater of the last five years' average or the career average; salary credits are nominal and unindexed, so the last five years is the larger in practice.
- **Coverage** by lifetime-income group, `replacement_rate_adjust` = $[0, 0, 0.5, 1, 1, 1, 1] \times 1.073$: the formal groups draw a pension (about 36% of the employed contribute to SSS or GSIS), and the informal groups do not. The scale also carries generosity, so it may exceed one: the SSS formula is the base, but GSIS and uniformed-service pensions (54% of spending) pay more (GSIS reaches 90% replacement), and the formula's flat ₱1,000 and ₱300 components (about 8% of average earnings) are not modeled.

The scale is set so outlays match spending, but at the right point in time. OG-Core pays every retiree as if the system had always existed, so its steady state is a *mature* system in the long-run population, while today's 2.28% comes from a young population. The steady-state target is therefore today's spending times the rise in covered retirees per worker between 2025 and the steady state, 3.06 (from the model's own population arrays, weighted by coverage, since the covered groups live longer): 6.97% of GDP. Outlays at the start of the transition are checked against today's 2.28% on the solved transition path.

**A long-run fiscal consequence.** With tax rates held at today's collections, a mature pension system in an aged population squeezes the rest of the budget. In the steady state the budget rule sets government consumption to about 3% of GDP, against 14.7% today. That is the model's answer to the question "current tax and pension policy, forever, in the long-run population"; it is not a fitting error, and the pension rates are deliberately not shrunk to avoid it. Raising contributions or adjusting benefits are natural reform scenarios to study against this baseline.
