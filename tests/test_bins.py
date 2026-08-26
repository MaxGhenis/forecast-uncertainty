import pytest

from forecast_uncertainty.bins import (
    contiguous_ecb_intervals,
    parse_ecb_header,
    us_bin_scheme,
)


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("TN1_0", (None, -1.0)),
        ("T0_0", (None, 0.0)),
        ("FN1_0TN0_6", (-1.0, -0.6)),
        ("FN0_2T0_2", (-0.2, 0.2)),
        ("F0_0T0_4", (0.0, 0.4)),
        ("F4_0", (4.0, None)),
    ],
)
def test_ecb_header_parser(header, expected):
    assert parse_ecb_header(header) == expected


def test_ecb_effective_edges_follow_adjacent_one_decimal_grid():
    literal = [
        parse_ecb_header(name)
        for name in ["TN0_8", "FN0_7TN0_3", "FN0_2T0_2", "F0_3T0_7", "F0_8"]
    ]

    assert contiguous_ecb_intervals(literal) == (
        (None, -0.7),
        (-0.7, -0.2),
        (-0.2, 0.3),
        (0.3, 0.8),
        (0.8, None),
    )


@pytest.mark.parametrize(
    ("variable", "year", "quarter", "name", "bins"),
    [
        ("prgdp", 1968, 4, "prgdp_1968q4_1973q1", 15),
        ("prgdp", 1981, 3, "prgdp_1981q3_1991q4", 6),
        ("prgdp", 1992, 1, "prgdp_1992q1_2009q1", 10),
        ("prgdp", 2009, 2, "prgdp_2009q2_2020q1", 11),
        ("prgdp", 2020, 2, "prgdp_wide_2020q2_2024q1", 11),
        ("prgdp", 2024, 2, "prgdp_2024q2_present", 11),
        ("prpgdp", 1985, 2, "prpgdp_1985q2_1991q4", 6),
        ("prpgdp", 2014, 1, "prpgdp_2014q1_present", 10),
        ("prunemp", 2020, 2, "prunemp_wide_2020q2_2024q1", 10),
        ("prccpi", 2007, 1, "prccpi_2007q1_present", 10),
    ],
)
def test_us_bin_eras(variable, year, quarter, name, bins):
    scheme = us_bin_scheme(variable, year, quarter)
    assert scheme.name == name
    assert len(scheme.intervals) == bins


def test_seed_scheme_midpoints_are_unchanged():
    assert us_bin_scheme("prgdp", 1992, 1).midpoints == pytest.approx(
        (6.45, 5.45, 4.45, 3.45, 2.45, 1.45, 0.45, -0.55, -1.55, -2.45)
    )
