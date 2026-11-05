"""
Tests of the income gradients in fertility and mortality. No model solve.
"""

import inspect

import numpy as np
import pytest

from ogphl import income
from ogphl.demographic_gradients import (
    adult_mortality_tilts,
    demographic_gradients,
)


def test_dhs_tilts_are_the_2022_philippine_values():
    """Fertility and infant mortality tilts are the Philippines' DHS 2022
    wealth-quintile slopes (EAPD-DRB/Demographic-Gradients), per percentile
    point."""
    g = demographic_gradients(20, 80, 320, 2025, 0.0313)
    assert g["fert_gradient"] == pytest.approx(-0.986426 / 100, rel=1e-5)
    assert g["infmort_gradient"] == pytest.approx(-1.603953 / 100, rel=1e-5)


def test_adult_mortality_follows_the_income_rule():
    """No Philippine census measurement: the adult tilt is the library's
    income rule at GNI per head ($4,470 in 2024) plus the age-band offsets,
    and it steepens with income up to the rule's $10,000 cap."""
    t = adult_mortality_tilts(4470.0)
    base = 1.291 - 0.2443 * np.log(4470.0)
    assert t[(15, 29)] == pytest.approx(base - 0.407)
    assert t[(60, 74)] == pytest.approx(base + 0.3972)
    capped = adult_mortality_tilts(1e6)[(15, 29)]
    assert capped == pytest.approx(adult_mortality_tilts(1e4)[(15, 29)])
    assert capped < t[(15, 29)]


def test_mortality_gradient_shape_and_ages():
    """By period and single age; zero at age 0 (infant mortality has its own
    gradient) and at 75 and over (outside the rule's age bands)."""
    m = demographic_gradients(20, 80, 320, 2025, 0.0313)["mort_gradient"]
    assert m.shape == (400, 100)
    assert np.all(m[:, 0] == 0) and np.all(m[:, 75:] == 0)
    assert np.all(m[:, 15:75] < 0)


def test_earnings_gini_target_is_the_2023_income_gini():
    """The e-matrix tilt targets the World Bank PIP 2023 income Gini, the same
    income concept as the US reference (41.5), not the consumption Gini."""
    default = inspect.signature(income.get_e_interp).parameters[
        "gini_to_match"
    ]
    assert default.default == 39.3


def test_earnings_age_shape_is_the_nta_ratio():
    """The US earnings curves are reshaped by the ratio of the Philippine to
    the US NTA labour-income profile (2015 vs the nearest US year, 2011),
    normalised over ages 20-64 and held flat from 72. Philippine labour
    income peaks at 39 against 49 in the US."""
    f = income.get_age_shape_factor(20, 80)
    assert f.shape == (80,)
    assert f[0] == pytest.approx(2.011, abs=0.005)
    assert f[45] == pytest.approx(0.543, abs=0.005)
    assert np.all(f[52:] == f[52])
    phl = income._load_nta_profile("PHL")
    assert max(phl) == 2015
    assert 20 + int(np.nanargmax(phl[2015][20:80])) == 39
