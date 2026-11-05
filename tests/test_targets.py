"""
Tests of the steady-state dashboard targets. No model solve.
"""

import numpy as np

from ogphl.targets import TARGETS, ss_moments

SS_KEYS = [
    "Y",
    "C",
    "I_total",
    "I_g",
    "G",
    "iit_revenue",
    "payroll_tax_revenue",
    "business_tax_revenue",
    "cons_tax_revenue",
    "wealth_tax_revenue",
    "bequest_tax_revenue",
    "total_tax_revenue",
    "r_gov",
    "D",
    "D_f",
    "TR",
    "K_f",
    "K",
    "RM",
    "B",
    "BQ",
    "r",
    "factor",
]


def test_every_target_has_a_value_and_a_source():
    for name, (value, source) in TARGETS.items():
        assert np.isfinite(value), name
        assert isinstance(source, str) and source.strip(), name


def test_steady_state_targets_have_model_moments():
    """Every steady-state target has a matching model moment; the
    initial-wealth anchor is a transition-path target, read elsewhere."""
    ss = {k: np.array(1.0) for k in SS_KEYS}
    moments = ss_moments(ss)
    for name in TARGETS:
        if name.endswith("anchor"):
            continue
        assert name in moments, name
