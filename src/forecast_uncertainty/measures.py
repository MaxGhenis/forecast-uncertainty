"""Pure statistical functions for reported forecast histograms."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np

QUANTILES = (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)


def finite_intervals(
    intervals: Sequence[tuple[float | None, float | None]],
) -> np.ndarray:
    """Replace open tails by one adjacent-bin width and return ascending bounds."""
    if not intervals:
        raise ValueError("At least one interval is required")

    ordered = sorted(
        intervals,
        key=lambda bounds: -np.inf if bounds[0] is None else bounds[0],
    )
    finite_widths = [
        upper - lower
        for lower, upper in ordered
        if lower is not None and upper is not None and upper > lower
    ]
    if not finite_widths:
        raise ValueError("An adjacent closed interval is required for open tails")

    output: list[tuple[float, float]] = []
    for index, (lower, upper) in enumerate(ordered):
        if lower is None:
            width = _nearest_width(ordered, index, direction=1)
            lower = float(upper) - width
        elif upper is None:
            width = _nearest_width(ordered, index, direction=-1)
            upper = float(lower) + width
        if upper <= lower:
            raise ValueError(f"Invalid interval: {(lower, upper)}")
        output.append((float(lower), float(upper)))
    return np.asarray(output, dtype=float)


def _nearest_width(
    intervals: Sequence[tuple[float | None, float | None]],
    index: int,
    direction: int,
) -> float:
    cursor = index + direction
    while 0 <= cursor < len(intervals):
        lower, upper = intervals[cursor]
        if lower is not None and upper is not None and upper > lower:
            return float(upper - lower)
        cursor += direction
    raise ValueError("Open tail has no adjacent closed interval")


def bin_midpoints(
    intervals: Sequence[tuple[float | None, float | None]],
) -> np.ndarray:
    """Return midpoints, using the adjacent-bin-width convention for open tails."""
    bounds = finite_intervals(intervals)
    return bounds.mean(axis=1)


def pooled_quantiles(
    weights: np.ndarray,
    intervals: Sequence[tuple[float | None, float | None]],
    quantiles: Iterable[float] = QUANTILES,
) -> dict[str, float]:
    """Quantiles of the mean histogram, with mass uniform inside each bin."""
    probabilities = np.asarray(weights, dtype=float)
    if probabilities.ndim == 2:
        probabilities = probabilities.mean(axis=0)
    if probabilities.ndim != 1 or probabilities.size != len(intervals):
        raise ValueError("Weights and intervals have incompatible shapes")
    total = probabilities.sum()
    if not np.isfinite(total) or total <= 0:
        return {_quantile_name(q): np.nan for q in quantiles}
    probabilities = probabilities / total

    raw_order = np.argsort(
        [-np.inf if lower is None else lower for lower, _ in intervals]
    )
    bounds = finite_intervals(intervals)
    probabilities = probabilities[raw_order]
    cumulative = np.cumsum(probabilities)
    result: dict[str, float] = {}
    for quantile in quantiles:
        q = float(quantile)
        if not 0 <= q <= 1:
            raise ValueError(f"Invalid quantile: {q}")
        index = min(int(np.searchsorted(cumulative, q, side="left")), len(bounds) - 1)
        mass = probabilities[index]
        prior = cumulative[index - 1] if index else 0.0
        lower, upper = bounds[index]
        fraction = 0.0 if mass <= 0 else (q - prior) / mass
        result[_quantile_name(q)] = float(lower + np.clip(fraction, 0, 1) * (upper - lower))
    return result


def _quantile_name(quantile: float) -> str:
    return f"q{round(100 * quantile):02d}"


def filter_probability_rows(probabilities: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Apply the survey response filter and normalize retained rows to one."""
    values = np.asarray(probabilities, dtype=float)
    if values.ndim != 2:
        raise ValueError("Probabilities must be a two-dimensional array")
    all_nan = np.isnan(values).all(axis=1)
    nonempty = values[~all_nan]
    filled = np.nan_to_num(nonempty, nan=0.0)
    sums = filled.sum(axis=1)
    valid = np.abs(sums - 100.0) < 2.0
    kept = filled[valid]
    if kept.size:
        kept = kept / kept.sum(axis=1, keepdims=True)
    counts = {
        "rows_total": int(len(values)),
        "rows_all_nan": int(all_nan.sum()),
        "rows_nonempty": int(len(nonempty)),
        "rows_kept": int(valid.sum()),
        "rows_dropped": int((~valid).sum()),
    }
    return kept, counts


def round_stats(
    probabilities: np.ndarray,
    midpoints: Sequence[float],
    intervals: Sequence[tuple[float | None, float | None]] | None = None,
) -> dict[str, float | int]:
    """Compute within, between, total, and pooled-distribution statistics."""
    mids = np.asarray(midpoints, dtype=float)
    values = np.asarray(probabilities, dtype=float)
    if values.ndim != 2 or values.shape[1] != mids.size:
        raise ValueError("Probabilities and midpoints have incompatible shapes")
    weights, counts = filter_probability_rows(values)
    result: dict[str, float | int] = {"n": counts["rows_kept"], **counts}
    if not len(weights):
        result.update(
            {
                "mean": np.nan,
                "median": np.nan,
                "within_sd": np.nan,
                "disagreement": np.nan,
                "total_sd": np.nan,
                "share_between": np.nan,
            }
        )
        if intervals is not None:
            result.update({_quantile_name(q): np.nan for q in QUANTILES})
            result["iqr"] = np.nan
        return result

    individual_means = (weights * mids).sum(axis=1)
    individual_variances = (weights * mids**2).sum(axis=1) - individual_means**2
    individual_variances = np.maximum(individual_variances, 0.0)
    within_variance = float(individual_variances.mean())
    between_variance = (
        float(individual_means.var(ddof=1)) if len(individual_means) > 1 else np.nan
    )
    total_variance = within_variance + between_variance
    result.update(
        {
            "mean": float(individual_means.mean()),
            "median": float(np.median(individual_means)),
            "within_sd": float(np.sqrt(within_variance)),
            "disagreement": float(np.sqrt(between_variance)),
            "total_sd": float(np.sqrt(total_variance)),
            "share_between": (
                float(between_variance / total_variance)
                if total_variance > 0
                else np.nan
            ),
        }
    )
    if intervals is not None:
        quantile_values = pooled_quantiles(weights, intervals)
        result.update(quantile_values)
        result["iqr"] = quantile_values["q75"] - quantile_values["q25"]
    return result
