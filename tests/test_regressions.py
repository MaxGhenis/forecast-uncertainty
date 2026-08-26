from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from forecast_uncertainty.build import add_recession_realizations, aggregate_density
from forecast_uncertainty.ecb_spf import parse_ecb_round
from forecast_uncertainty.realizations import (
    calibration_table,
    load_ecb_realizations,
    load_us_realizations,
)
from forecast_uncertainty.us_spf import LONGRUN_VARIABLES, parse_us_density

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "tests" / "fixtures" / "seed"


@pytest.fixture(scope="module")
def prgdp_measures():
    measures, _ = aggregate_density(parse_us_density("PRGDP"))
    return measures


def test_next_year_q1_prgdp_matches_seed(prgdp_measures):
    expected = pd.read_csv(SEED / "spf_uncertainty_disagreement.csv")
    actual = prgdp_measures[
        (prgdp_measures["quarter"] == 1)
        & (prgdp_measures["horizon_class"] == "next_year")
    ].set_index("year")
    aligned = actual.loc[expected["YEAR"]]

    np.testing.assert_allclose(
        aligned["within_sd"], expected["within_sd"], rtol=0, atol=1e-9
    )
    np.testing.assert_allclose(
        aligned["disagreement"], expected["dis"], rtol=0, atol=1e-9
    )
    np.testing.assert_allclose(
        aligned["total_sd"], expected["total"], rtol=0, atol=1e-9
    )
    np.testing.assert_allclose(
        aligned["share_between"], expected["share_between"], rtol=0, atol=1e-9
    )


def test_next_year_q1_prgdp_calibration_flags_match_seed(prgdp_measures):
    expected = pd.read_csv(SEED / "spf_errors.csv")
    calibration = calibration_table(prgdp_measures, load_us_realizations())
    actual = calibration[
        (calibration["quarter"] == 1) & (calibration["horizon_class"] == "next_year")
    ].set_index(["year", "target_year"])
    assert len(actual) == len(expected)
    keys = pd.MultiIndex.from_frame(expected[["YEAR", "target"]])
    aligned = actual.loc[keys]

    np.testing.assert_allclose(aligned["realized"], expected["g"], rtol=0, atol=1e-12)
    np.testing.assert_allclose(aligned["error"], expected["err"], rtol=0, atol=1e-12)
    assert aligned["inside_1sd"].astype(bool).tolist() == expected["inside"].tolist()


def test_documented_round_coverage_and_core_starts():
    ecb_paths = sorted((ROOT / "data" / "raw" / "ecb_spf").glob("*.csv"))
    assert len(ecb_paths) == 111
    assert ecb_paths[0].stem == "1999Q1"
    assert ecb_paths[-1].stem == "2026Q3"

    prccpi = parse_us_density("PRCCPI")
    rounds = prccpi[["year", "quarter"]].drop_duplicates()
    assert len(rounds) == 79
    assert tuple(rounds.iloc[0]) == (2007, 1)
    assert tuple(rounds.iloc[-1]) == (2026, 3)

    point_only = parse_ecb_round(ROOT / "data" / "raw" / "ecb_spf" / "2016Q4.csv")
    core_point_only = point_only[point_only["variable"] == "hicpx"]
    assert not core_point_only.empty
    assert core_point_only["probability"].isna().all()

    first_density = parse_ecb_round(ROOT / "data" / "raw" / "ecb_spf" / "2017Q1.csv")
    assert (
        first_density.loc[first_density["variable"] == "hicpx", "probability"]
        .notna()
        .any()
    )


def test_hicpx_realizations_support_calendar_and_rolling_calibration():
    realizations = load_ecb_realizations()
    core = realizations[realizations["variable"] == "hicpx"].set_index("target_period")

    assert len(core) == 377
    assert core.loc["2024Dec", "realized"] == pytest.approx(2.7)
    assert core.loc["2024Dec", "observation_status"] == "A"
    assert core.loc["2025", "realized"] == pytest.approx(2.425)
    assert core.loc["2025", "observation_status"] == "A+E"

    forecasts = pd.DataFrame(
        [
            {
                "survey": "ecb",
                "variable": "hicpx",
                "target_period": target,
                "mean": 2.5,
                "total_sd": 1.0,
                "q05": 1.0,
                "q95": 4.0,
            }
            for target in ("2024Dec", "2025")
        ]
    )
    calibration = calibration_table(forecasts, realizations)

    assert calibration["target_period"].tolist() == ["2024Dec", "2025"]
    estimated = calibration["observation_status"].str.contains("E", na=False)
    assert estimated.tolist() == [False, True]


def test_generated_hicpx_calibration_coverage():
    calibration = pd.read_csv(ROOT / "outputs" / "calibration.csv")
    core = calibration[
        (calibration["survey"] == "ecb") & (calibration["variable"] == "hicpx")
    ]

    assert len(core) == 176
    assert (int(core["inside_1sd"].sum()), int(core["inside_pooled_90"].sum())) == (
        106,
        128,
    )

    actual_only = core[~core["observation_status"].str.contains("E", na=False)]
    assert len(actual_only) == 156
    assert (
        int(actual_only["inside_1sd"].sum()),
        int(actual_only["inside_pooled_90"].sum()),
    ) == (90, 108)


def test_generated_scores_match_calibration_and_flag_benchmark_windows():
    calibration = pd.read_csv(ROOT / "outputs" / "calibration.csv")
    scores = pd.read_csv(ROOT / "outputs" / "scores.csv")

    assert len(scores) == len(calibration) == 3070
    assert scores.columns[: len(calibration.columns)].tolist() == list(
        calibration.columns
    )
    pd.testing.assert_frame_equal(
        scores[list(calibration.columns)], calibration, check_dtype=False
    )

    distribution_columns = [
        "crps_pooled",
        "crps_individual_mean",
        "pinball_05",
        "pinball_10",
        "pinball_25",
        "pinball_50",
        "pinball_75",
        "pinball_90",
        "pinball_95",
        "pit",
    ]
    assert scores[distribution_columns].notna().all().all()
    assert scores[distribution_columns[:-1]].ge(0.0).all().all()
    assert scores["pit"].between(0.0, 1.0).all()
    assert (scores["crps_pooled"] <= scores["crps_individual_mean"] + 1e-10).all()

    for name in ("climatology", "gaussian"):
        benchmark = scores[f"crps_{name}"]
        eligible = scores[f"n_{name}"] >= 10
        assert benchmark.notna().equals(eligible)
        expected_skill = 1.0 - scores["crps_pooled"] / benchmark
        np.testing.assert_allclose(
            scores.loc[eligible, f"skill_vs_{name}"],
            expected_skill.loc[eligible],
            rtol=0.0,
            atol=1e-12,
        )
        assert scores.loc[~eligible, f"skill_vs_{name}"].isna().all()


def test_documented_longrun_point_configuration():
    assert LONGRUN_VARIABLES == ("RGDP10", "CPI10", "PCE10")


def test_calibration_excludes_us_gnp_concepts():
    forecasts = pd.DataFrame(
        [
            {
                "survey": "us",
                "variable": "PRGDP",
                "concept": concept,
                "target_year": 1992,
                "mean": 2.0,
                "total_sd": 1.0,
                "q05": 0.0,
                "q95": 4.0,
            }
            for concept in ("nominal_gnp", "real_gnp", "real_gdp")
        ]
        + [
            {
                "survey": "us",
                "variable": "PRPGDP",
                "concept": concept,
                "target_year": 1992,
                "mean": 2.0,
                "total_sd": 1.0,
                "q05": 0.0,
                "q95": 4.0,
            }
            for concept in ("gnp_implicit_deflator", "gdp_implicit_deflator")
        ]
    )
    realizations = pd.DataFrame(
        [
            {
                "survey": "us_spf",
                "variable": variable,
                "target_period": "1992",
                "realized": 2.5,
            }
            for variable in ("prgdp", "prpgdp")
        ]
    )

    calibration = calibration_table(forecasts, realizations)

    assert calibration[["variable", "concept"]].to_records(index=False).tolist() == [
        ("PRGDP", "real_gdp"),
        ("PRPGDP", "gdp_implicit_deflator"),
    ]


def test_recession_realizations_require_chain_weighted_gdp_concept():
    forecasts = pd.DataFrame(
        [
            {
                "survey": "us",
                "variable": "RECESS",
                "concept": concept,
                "year": 1996,
                "quarter": 1,
                "target_period": "1996Q1",
                "mean_probability": 25.0,
            }
            for concept in ("fixed_weighted_real_gdp", "chain_weighted_real_gdp")
        ]
    )
    realizations = pd.DataFrame(
        [
            {
                "survey": "us_spf",
                "variable": "recess",
                "target_period": "1996Q1",
                "realized": 0.0,
                "source": "test",
            }
        ]
    )

    scored = add_recession_realizations(forecasts, realizations)

    assert scored.loc[0, ["realized", "source"]].isna().all()
    assert scored.loc[1, "realized"] == 0.0
    assert scored.loc[1, "source"] == "test"
