"""Generate the static interactive's compact full-matrix data bundle.

The browser receives positional rows, with their field names recorded once in
``DATA.fields``.  This keeps every selectable survey-variable-horizon series
while avoiding repeated JSON keys and staying within the static-page budget.

Run: uv run --no-sync python interactive/gen_data.py
"""

from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
OUT = Path(__file__).resolve().parent / "data.js"
SIZE_BUDGET = 1_200_000

SOURCE_PATHS = {
    "measures": OUTPUTS / "measures.csv",
    "calibration": OUTPUTS / "calibration.csv",
    "longrun_points": OUTPUTS / "longrun_points.csv",
}

MEASURE_FIELDS = [
    "survey",
    "variable",
    "year",
    "quarter",
    "horizon_class",
    "horizon_years",
    "n",
    "mean",
    "median",
    "within_sd",
    "disagreement",
    "total_sd",
    "share_between",
    "iqr",
    "q25",
    "q75",
]
CALIBRATION_FIELDS = [
    "survey",
    "variable",
    "year",
    "quarter",
    "horizon_class",
    "horizon_years",
    "consensus",
    "realized",
    "total_sd",
    "q05",
    "q95",
    "inside_1sd",
    "inside_pooled_90",
]
LONGRUN_FIELDS = [
    "survey",
    "variable",
    "year",
    "quarter",
    "n",
    "median",
    "iqr",
]

SURVEYS = [
    {"id": "us", "label": "US SPF"},
    {"id": "ecb", "label": "ECB SPF"},
]
VARIABLES = {
    "us": [
        {"id": "PRGDP", "label": "Real GDP growth"},
        {"id": "PRPGDP", "label": "GDP price inflation"},
        {"id": "PRUNEMP", "label": "Unemployment rate"},
        {"id": "PRCCPI", "label": "Core CPI"},
        {"id": "PRCPCE", "label": "Core PCE"},
    ],
    "ecb": [
        {"id": "rgdp", "label": "Real GDP growth"},
        {"id": "unemp", "label": "Unemployment rate"},
        {"id": "hicp", "label": "HICP"},
        {"id": "hicpx", "label": "Core HICP"},
    ],
}
HORIZONS = {
    "us": [
        ("current_year", "Current year"),
        ("next_year", "Next year"),
        ("year_after_next", "+2 years"),
        ("three_years_ahead", "+3 years"),
    ],
    "ecb": [
        ("current_year", "Current year"),
        ("next_year", "Next year"),
        ("year_after_next", "Year after next"),
        ("rolling_1y", "Rolling 1 year"),
        ("rolling_2y", "Rolling 2 years"),
        ("longer_term", "Longer term"),
    ],
}
US_FULL_HORIZONS = tuple(horizon for horizon, _ in HORIZONS["us"])
US_SHORT_HORIZONS = US_FULL_HORIZONS[:2]
ECB_HORIZONS = tuple(horizon for horizon, _ in HORIZONS["ecb"])
EXPECTED_HORIZONS = {
    **{
        ("us", variable["id"]): (
            US_FULL_HORIZONS
            if variable["id"] in {"PRGDP", "PRUNEMP"}
            else US_SHORT_HORIZONS
        )
        for variable in VARIABLES["us"]
    },
    **{("ecb", variable["id"]): ECB_HORIZONS for variable in VARIABLES["ecb"]},
}
EXPECTED_COMBOS = {
    (survey, variable, horizon)
    for (survey, variable), horizons in EXPECTED_HORIZONS.items()
    for horizon in horizons
}
EXPECTED_LONGRUN_COMBOS = {("us", "CPI10"), ("us", "PCE10"), ("us", "RGDP10")}


def significant(value: Any, digits: int = 4) -> int | float | str | bool | None:
    """Return JSON-safe values, rounding floating-point values significantly."""
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (bool, str)):
        return value
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"Non-finite numeric value: {value!r}")
    rounded = float(f"{number:.{digits}g}")
    if rounded == 0:
        return 0
    return int(rounded) if rounded.is_integer() else rounded


def _require_columns(frame: pd.DataFrame, columns: list[str], source: Path) -> None:
    missing = set(columns).difference(frame.columns)
    assert not missing, f"{source} is missing required columns: {sorted(missing)}"


def _combo_set(frame: pd.DataFrame) -> set[tuple[str, str, str]]:
    return {
        (str(survey), str(variable), str(horizon))
        for survey, variable, horizon in frame[
            ["survey", "variable", "horizon_class"]
        ].itertuples(index=False, name=None)
    }


def _options(measures: pd.DataFrame) -> dict[str, Any]:
    expected_variables = {
        (survey, item["id"]) for survey, items in VARIABLES.items() for item in items
    }
    emitted_variables = set(
        measures[["survey", "variable"]].itertuples(index=False, name=None)
    )
    assert emitted_variables == expected_variables, (
        "Variable labels and measures.csv differ: "
        f"missing={sorted(expected_variables - emitted_variables)}, "
        f"unexpected={sorted(emitted_variables - expected_variables)}"
    )

    horizons: dict[str, list[dict[str, str]]] = {}
    for survey, variable in sorted(emitted_variables):
        available = set(
            measures.loc[
                (measures["survey"] == survey) & (measures["variable"] == variable),
                "horizon_class",
            ]
        )
        expected = set(EXPECTED_HORIZONS[(survey, variable)])
        assert available == expected, (
            f"Horizon matrix differs for {survey}|{variable}: "
            f"missing={sorted(expected - available)}, "
            f"unexpected={sorted(available - expected)}"
        )
        ordered = [
            {"id": horizon, "label": label}
            for horizon, label in HORIZONS[survey]
            if horizon in expected
        ]
        assert ordered, f"No selectable horizons for {survey}|{variable}"
        assert {item["id"] for item in ordered} == available, (
            f"Unlabelled horizons for {survey}|{variable}: "
            f"{sorted(available - {item['id'] for item in ordered})}"
        )
        horizons[f"{survey}|{variable}"] = ordered

    return {"surveys": SURVEYS, "variables": VARIABLES, "horizons": horizons}


def _measure_rows(frame: pd.DataFrame) -> list[list[Any]]:
    return [
        [
            row.survey,
            row.variable,
            int(row.year),
            int(row.quarter),
            row.horizon_class,
            significant(row.horizon_years),
            int(row.n),
            significant(row.mean),
            significant(row.median),
            significant(row.within_sd),
            significant(row.disagreement),
            significant(row.total_sd),
            significant(row.share_between),
            significant(row.iqr),
            significant(row.q25),
            significant(row.q75),
        ]
        for row in frame.itertuples(index=False)
    ]


def _calibration_rows(frame: pd.DataFrame) -> list[list[Any]]:
    return [
        [
            row.survey,
            row.variable,
            int(row.year),
            int(row.quarter),
            row.horizon_class,
            significant(row.horizon_years),
            significant(row.consensus_mean),
            significant(row.realized),
            significant(row.total_sd),
            significant(row.q05),
            significant(row.q95),
            bool(row.inside_1sd),
            bool(row.inside_pooled_90),
        ]
        for row in frame.itertuples(index=False)
    ]


def _longrun_rows(frame: pd.DataFrame) -> list[list[Any]]:
    return [
        [
            row.survey,
            row.variable,
            int(row.year),
            int(row.quarter),
            int(row.n),
            significant(row.median),
            significant(row.iqr),
        ]
        for row in frame.itertuples(index=False)
    ]


def _assert_series(
    frame: pd.DataFrame,
    combos: set[tuple[str, str, str]],
    name: str,
) -> None:
    sizes = frame.groupby(["survey", "variable", "horizon_class"], observed=True).size()
    empty = [combo for combo in sorted(combos) if int(sizes.get(combo, 0)) == 0]
    assert not empty, f"Empty {name} series: {empty}"


def _mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC).isoformat(
        timespec="seconds"
    )


def main() -> None:
    measures_raw = pd.read_csv(SOURCE_PATHS["measures"])
    calibration = pd.read_csv(SOURCE_PATHS["calibration"])
    longrun = pd.read_csv(SOURCE_PATHS["longrun_points"])

    measure_source_fields = MEASURE_FIELDS
    calibration_source_fields = [
        "survey",
        "variable",
        "year",
        "quarter",
        "horizon_class",
        "horizon_years",
        "consensus_mean",
        "realized",
        "total_sd",
        "q05",
        "q95",
        "inside_1sd",
        "inside_pooled_90",
    ]
    _require_columns(measures_raw, measure_source_fields, SOURCE_PATHS["measures"])
    _require_columns(
        calibration, calibration_source_fields, SOURCE_PATHS["calibration"]
    )
    _require_columns(longrun, LONGRUN_FIELDS, SOURCE_PATHS["longrun_points"])
    for column in ("inside_1sd", "inside_pooled_90"):
        assert pd.api.types.is_bool_dtype(calibration[column]), (
            f"Calibration flag {column} must contain booleans"
        )

    # The documented early US target exceptions have no class and cannot power
    # a horizon control. Keep their exclusion explicit in bundle provenance.
    unclassified = int(measures_raw["horizon_class"].isna().sum())
    measures = measures_raw.dropna(subset=["horizon_class"]).copy()

    # Early ECB Q1 files legitimately contain both four- and five-year
    # longer-term targets in the same round (SOL_REPORT.md, term structure).
    identity_fields = [
        "survey",
        "variable",
        "year",
        "quarter",
        "horizon_class",
        "horizon_years",
    ]
    assert not measures[MEASURE_FIELDS].isna().any().any(), (
        "Selectable measure rows contain missing view fields"
    )
    assert not calibration[calibration_source_fields].isna().any().any(), (
        "Calibration rows contain missing view fields"
    )
    assert not longrun[LONGRUN_FIELDS].isna().any().any(), (
        "Long-run rows contain missing view fields"
    )
    assert not measures.duplicated(identity_fields).any(), (
        "Duplicate measure round rows"
    )
    assert not calibration.duplicated(identity_fields).any(), (
        "Duplicate calibration round rows"
    )

    options = _options(measures)
    measure_combos = _combo_set(measures)
    option_combos = {
        (survey, variable, item["id"])
        for key, items in options["horizons"].items()
        for survey, variable in [key.split("|", maxsplit=1)]
        for item in items
    }
    assert measure_combos == EXPECTED_COMBOS, (
        "Measure series and expected 38-combo matrix differ: "
        f"missing={sorted(EXPECTED_COMBOS - measure_combos)}, "
        f"unexpected={sorted(measure_combos - EXPECTED_COMBOS)}"
    )
    assert option_combos == EXPECTED_COMBOS, (
        "Control options and expected 38-combo matrix differ: "
        f"missing={sorted(EXPECTED_COMBOS - option_combos)}, "
        f"unexpected={sorted(option_combos - EXPECTED_COMBOS)}"
    )
    calibration_combos = _combo_set(calibration)
    assert calibration_combos == EXPECTED_COMBOS, (
        "Calibration series and expected 38-combo matrix differ: "
        f"missing={sorted(EXPECTED_COMBOS - calibration_combos)}, "
        f"unexpected={sorted(calibration_combos - EXPECTED_COMBOS)}"
    )
    _assert_series(measures, EXPECTED_COMBOS, "measure")
    _assert_series(calibration, EXPECTED_COMBOS, "calibration")

    longrun_combos = set(
        longrun[["survey", "variable"]].itertuples(index=False, name=None)
    )
    assert longrun_combos == EXPECTED_LONGRUN_COMBOS, (
        "Long-run source series differ: "
        f"missing={sorted(EXPECTED_LONGRUN_COMBOS - longrun_combos)}, "
        f"unexpected={sorted(longrun_combos - EXPECTED_LONGRUN_COMBOS)}"
    )
    longrun_sizes = longrun.groupby(["survey", "variable"], observed=True).size()
    assert all(int(longrun_sizes.get(combo, 0)) > 0 for combo in longrun_combos), (
        "Empty long-run series"
    )

    survey_rank = {item["id"]: index for index, item in enumerate(SURVEYS)}
    variable_rank = {
        (survey, item["id"]): index
        for survey, items in VARIABLES.items()
        for index, item in enumerate(items)
    }
    horizon_rank = {
        (survey, horizon): index
        for survey, items in HORIZONS.items()
        for index, (horizon, _) in enumerate(items)
    }

    def sort_matrix(frame: pd.DataFrame) -> pd.DataFrame:
        ranked = frame.assign(
            _survey=frame["survey"].map(survey_rank),
            _variable=[
                variable_rank[(survey, variable)]
                for survey, variable in frame[["survey", "variable"]].itertuples(
                    index=False, name=None
                )
            ],
            _horizon=[
                horizon_rank[(survey, horizon)]
                for survey, horizon in frame[["survey", "horizon_class"]].itertuples(
                    index=False, name=None
                )
            ],
        )
        return ranked.sort_values(
            [
                "_survey",
                "_variable",
                "_horizon",
                "horizon_years",
                "year",
                "quarter",
            ]
        ).drop(columns=["_survey", "_variable", "_horizon"])

    measures = sort_matrix(measures)
    calibration = sort_matrix(calibration)
    longrun = longrun.sort_values(["survey", "variable", "year", "quarter"])

    source_files = [
        {"path": str(path.relative_to(ROOT)), "modified_utc": _mtime(path)}
        for path in SOURCE_PATHS.values()
    ]
    build_date = max(item["modified_utc"] for item in source_files)[:10]
    manifest = {
        "measures": {"combos": len(measure_combos), "rows": len(measures)},
        "calibration": {
            "combos": len(calibration_combos),
            "rows": len(calibration),
        },
        "longrun_points": {"combos": len(longrun_combos), "rows": len(longrun)},
        "excluded_unclassified_measure_rows": unclassified,
    }
    data = {
        "meta": {
            "source": (
                "Philadelphia Fed Survey of Professional Forecasters and "
                "ECB Survey of Professional Forecasters; latest-vintage "
                "realizations documented in outputs/calibration.csv."
            ),
            "source_files": source_files,
            "generated_from": "outputs/ via interactive/gen_data.py",
            "build_date": build_date,
            "rounding": "four significant digits",
            "manifest": manifest,
        },
        "fields": {
            "measures": MEASURE_FIELDS,
            "calibration": CALIBRATION_FIELDS,
            "longrun_points": LONGRUN_FIELDS,
        },
        "options": options,
        "measures": _measure_rows(measures),
        "calibration": _calibration_rows(calibration),
        "longrun_points": _longrun_rows(longrun),
    }

    payload = (
        "const DATA="
        + json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
        + ";\n"
    )
    byte_count = len(payload.encode("utf-8"))
    assert byte_count <= SIZE_BUDGET, (
        f"data.js is {byte_count:,} bytes; budget is {SIZE_BUDGET:,} bytes"
    )
    OUT.write_text(payload, encoding="utf-8")

    print(
        "manifest: "
        f"measures {len(measure_combos)} combos × {len(measures):,} rows; "
        f"calibration {len(calibration_combos)} combos × {len(calibration):,} rows; "
        f"longrun {len(longrun_combos)} combos × {len(longrun):,} rows"
    )
    print(f"wrote {OUT} ({byte_count:,} bytes; budget {SIZE_BUDGET:,})")


if __name__ == "__main__":
    main()
