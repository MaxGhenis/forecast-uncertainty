"""Generate interactive/data.js from pipeline outputs.

Until outputs/measures.csv exists, builds the US SPF real-GDP-growth bundle
from the validated seed series in tests/fixtures/seed/ (computed from
Philadelphia Fed SPF microdata). Once the full pipeline lands, this script
switches to outputs/ and emits every survey x variable x horizon.

Run: uv run python interactive/gen_data.py
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "tests" / "fixtures" / "seed"
OUT = Path(__file__).resolve().parent / "data.js"


def r(x, nd=3):
    return round(float(x), nd)


def main():
    unc = pd.read_csv(SEED / "spf_uncertainty_disagreement.csv")
    err = pd.read_csv(SEED / "spf_errors.csv")
    ny = pd.read_csv(SEED / "spf_nextyear_consensus.csv")
    lr = pd.read_csv(SEED / "spf_rgdp10_dispersion.csv")

    data = {
        "meta": {
            "source": (
                "Philadelphia Fed SPF individual density forecasts (PRGDP), "
                "Q1 rounds, next-year target; RGDP10 point forecasts. "
                "Computed via law-of-total-variance pooling. Realized growth: "
                "BEA annual-average real GDP growth."
            ),
            "generated_from": "tests/fixtures/seed (validated seed pipeline)",
            "surveys": ["US SPF"],
            "variables": ["Real GDP growth"],
        },
        "decomposition": [
            {
                "year": int(row.YEAR),
                "n": int(row.n),
                "within": r(row.within_sd),
                "disagreement": r(row.dis),
                "total": r(row.total),
                "share_between": r(row.share_between),
            }
            for row in unc.itertuples()
        ],
        "calibration": [
            {
                "year": int(row.target),
                "forecast": r(row.mean_fcast, 2),
                "realized": r(row.g, 1),
                "total": r(row.total),
                "inside": bool(row.inside),
            }
            for row in err.itertuples()
        ],
        "fan": {
            "next_year": [
                {
                    "year": int(row.t),
                    "median": r(row.median, 2),
                    "p25": r(row.p25, 2),
                    "p75": r(row.p75, 2),
                }
                for row in ny.itertuples()
            ],
            "ten_year": [
                {
                    "year": int(row.t),
                    "median": r(row.median, 2),
                    "p25": r(row.p25, 2),
                    "p75": r(row.p75, 2),
                }
                for row in lr.dropna(subset=["t"]).itertuples()
            ],
        },
    }
    OUT.write_text("const DATA = " + json.dumps(data) + ";\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
