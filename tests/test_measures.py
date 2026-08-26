import numpy as np
import pytest

from forecast_uncertainty.measures import filter_probability_rows, round_stats


def test_law_of_total_variance_identity():
    probabilities = np.array(
        [
            [20.0, 80.0, 0.0],
            [0.0, 40.0, 60.0],
            [50.0, 0.0, 50.0],
        ]
    )
    stats = round_stats(probabilities, [-1.0, 0.0, 2.0])

    assert stats["total_sd"] ** 2 == pytest.approx(
        stats["within_sd"] ** 2 + stats["disagreement"] ** 2
    )
    assert stats["share_between"] == pytest.approx(
        stats["disagreement"] ** 2 / stats["total_sd"] ** 2
    )


def test_sum_filter_is_strict_and_fills_partial_nan_with_zero():
    probabilities = np.array(
        [
            [50.0, 50.0, np.nan],
            [49.0, 49.0, 0.0],
            [51.0, 51.0, 0.0],
            [np.nan, np.nan, np.nan],
            [20.0, 40.0, 39.5],
        ]
    )

    weights, counts = filter_probability_rows(probabilities)

    assert counts == {
        "rows_total": 5,
        "rows_all_nan": 1,
        "rows_nonempty": 4,
        "rows_kept": 2,
        "rows_dropped": 2,
    }
    np.testing.assert_allclose(weights.sum(axis=1), 1.0)


def test_pooled_quantiles_are_uniform_within_bins_and_report_iqr():
    probabilities = np.array([[25.0, 50.0, 25.0], [25.0, 50.0, 25.0]])
    intervals = [(None, 0.0), (0.0, 1.0), (1.0, None)]

    stats = round_stats(probabilities, [-0.5, 0.5, 1.5], intervals)

    assert stats["q25"] == pytest.approx(0.0)
    assert stats["q50"] == pytest.approx(0.5)
    assert stats["q75"] == pytest.approx(1.0)
    assert stats["iqr"] == pytest.approx(1.0)
