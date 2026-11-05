"""
Data targets for the OG-PHL steady-state dashboard, and the function that
computes the matching model moments from a solved ``SS_vars.pkl``.

Every target carries its source; the same numbers are pinned against the
packaged parameters in ``tests/test_taxes.py`` and
``tests/test_remittances.py``. Ratios are to GDP. Revenue shares are the
OECD Revenue Statistics in Asia and the Pacific 2025 (Philippines, 2023)
plus the BESF/BTr non-tax lines the calibration captures. Fiscal rows
first, then external, production and households.
"""

import numpy as np

# moment: (target, source)
TARGETS = {
    # Fiscal: revenue by instrument
    "PIT/Y": (0.0312, "OECD Revenue Statistics Asia-Pacific 2025, PHL 2023"),
    "payroll/Y": (0.0278, "SSC, OECD Revenue Statistics 2025, PHL 2023"),
    "CIT/Y": (
        0.0420,
        "CIT 2.90 + BTr income from government capital ~1.00 + "
        "unallocable income taxes 0.30 (OECD 2023; BESF)",
    ),
    "cons tax/Y": (
        0.0794,
        "VAT + excises + customs 7.39 (OECD 2023) + fees and charges "
        "0.55 (BESF non-tax)",
    ),
    "wealth tax/Y": (
        0.0132,
        "property-type taxes: RPT, DST, LGU levies (OECD 'other taxes' "
        "less estate)",
    ),
    "bequest tax/Y": (0.0007, "estate tax collections, BIR"),
    "r_gov": (
        0.020,
        "BTr FY2024: interest P763.3bn on ~P15.3tn average debt, less "
        "~3% expected inflation",
    ),
    "D/Y": (0.60, "debt_ratio_ss: MTFF program anchor"),
    # Spending
    "TR/Y": (0.0448, "alpha_T: social transfers, DBM/BESF"),
    "I_g/Y": (0.052, "alpha_I: public infrastructure program, MTFF/BESF"),
    # External
    "K_f/K": (0.20, "BSP International Investment Position, inward share"),
    "RM/Y": (
        0.0812,
        "BSP 2025 personal remittances US$39.62bn (BPM6), the household "
        "income measure; the published 7.3% ratio is the narrower cash "
        "measure",
    ),
    # Production and households (no binding target yet: beta/delta still sit
    # at inherited defaults; a PWT capital-output anchor is the open
    # calibration item, see the ZAF 0.3.0 baseline for the pattern)
    "B/Y[0] anchor": (
        2.783,
        "initial_wealth_ratio: household wealth to GDP, 2025 "
        "(transition-initial target, not a steady-state moment)",
    ),
}


def ss_moments(ss):
    """
    Model side of every dashboard row from a solved steady state.

    Args:
        ss (dict): a solved ``SS_vars.pkl``

    Returns:
        m (dict): model moments, keyed like ``TARGETS``, plus untargeted
            ratios
    """
    Y = float(np.squeeze(ss["Y"]))

    def sc(key):
        return float(np.sum(ss[key]))

    C = sc("C")
    nx = Y - C - sc("I_total") - sc("I_g") - sc("G")
    m = {
        "PIT/Y": sc("iit_revenue") / Y,
        "payroll/Y": sc("payroll_tax_revenue") / Y,
        "CIT/Y": sc("business_tax_revenue") / Y,
        "cons tax/Y": sc("cons_tax_revenue") / Y,
        "wealth tax/Y": sc("wealth_tax_revenue") / Y,
        "bequest tax/Y": sc("bequest_tax_revenue") / Y,
        "total tax/Y": sc("total_tax_revenue") / Y,
        "r_gov": sc("r_gov"),
        "D/Y": sc("D") / Y,
        "D_f/D": sc("D_f") / sc("D") if sc("D") else np.nan,
        "G/Y": sc("G") / Y,
        "TR/Y": sc("TR") / Y,
        "I_g/Y": sc("I_g") / Y,
        "pensions/Y": sc("agg_pension_outlays") / Y,
        "K_f/K": sc("K_f") / sc("K"),
        "RM/Y": sc("RM") / Y,
        "NX/Y": nx / Y,
        "K/Y": sc("K") / Y,
        "(I+I_g)/Y": (sc("I_total") + sc("I_g")) / Y,
        "C/Y purch.": (C + sc("cons_tax_revenue")) / Y,
        "B/Y": sc("B") / Y,
        "BQ/Y": sc("BQ") / Y,
        "r": sc("r"),
        "factor": sc("factor"),
    }
    return m
