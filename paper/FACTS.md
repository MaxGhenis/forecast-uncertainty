# Ground-truth sheet

Every claim the paper may state, with its verification status. Writers cite
nothing outside this sheet plus LITREVIEW.md (verified citations only).
Status codes: COMPUTED (this repo, this session), DOC (read in the survey
documentation in `data/docs/`), PENDING-SOL (awaiting the full pipeline),
PENDING-LIT (awaiting the verified lit review). Unresolved items carry
`[NEEDS …]` markers in the draft; resolve, never delete.

## The construction

- Law of total variance on reported histograms: total pooled variance =
  mean within-forecaster variance + between-forecaster variance
  (disagreement). Midpoint mass per bin; open tails get the adjacent bin's
  width. Rows kept when |Σprobs − 100| < 2, renormalized. COMPUTED (seed
  pipeline, `data/docs/seed_spf_density_pipeline.py`).

## US SPF — computed series (next-year PRGDP, Q1 rounds, 1992–2026)

- Total pooled SD: 1.24pp in 1992; mean 1.26pp over 1992–2020; peak 2.10pp
  in 2021; 1.36pp in 2026. COMPUTED.
- Disagreement share of total variance: median 0.18, decile range
  0.12–0.32, max 0.41 (2009). Average individual SD ≈ 0.89 × total SD.
  COMPUTED.
- ±1σ (total) coverage of realized annual-average real GDP growth: 23 of 33
  target years, 69.7% (theory: 68%). COMPUTED.
- Missed targets: 1996, 1997, 1998, 1999, 2000 (all upside), 2001
  (downside), 2008, 2009 (downside), 2020 (downside), 2021 (upside) — six
  consecutive misses 1996–2001, then only regime shifts. COMPUTED.
  NOTE: supersedes the earlier "five straight" phrasing; 2001 also missed.
- 2026 Q1: next-year consensus median 1.83%, IQR 0.40pp; 10-year average
  annual (RGDP10, point forecasts) median 2.1%, IQR 0.20pp. The decade
  answer is tighter than the next-year answer. COMPUTED.

## US SPF — survey structure

- Density variables and start dates: PRGDP/PRPGDP histograms back to 1968Q4
  (output concept changes: nominal GNP → real GNP 1981Q3 → real GDP 1992Q1;
  bin schemes in documentation Table 7); PRCCPI and PRCPCE (Q4/Q4 core CPI
  and core PCE growth) since 2007Q1; PRUNEMP since 2009Q2; RECESS
  (probability of a decline in real GDP, current + next four quarters).
  DOC (`data/docs/spf-documentation.txt` lines 59–90, 639–652, Table 7).
- Density horizons: current and next year only, until 2009Q2; current
  through +3 years after (PRGDP extension stated at line 66–69; PRPGDP and
  PRUNEMP block structure consistent with 4 target years by column count —
  PENDING-SOL for the doc-exact statement per variable).
- 2020Q2–2024Q1: much wider PRGDP bins (16+ … below −12); mechanically
  inflates measured SDs. DOC (Table 7) + seed. Magnitude of the mechanical
  effect: PENDING-SOL (IQR vs SD divergence).
- 10-year variables (RGDP10, CPI10, PCE10, UNEMP10) are single point
  forecasts — no densities at any horizon beyond +3. COMPUTED (file
  structure) + DOC.

## ECB SPF — survey structure

- Microdata: 111 quarterly rounds, 1999Q1–2026Q3, published openly.
  COMPUTED (files in `data/raw/ecb_spf/`).
- Density variables: HICP inflation, core HICP (since 2017Q1), real GDP
  growth, unemployment rate. DOC (dataset description, line 407 for core).
- Horizons: current year, next year(, year after next — PENDING-SOL);
  rolling 1y and 2y ahead of latest data; and a longer-term calendar year —
  four years ahead in Q1/Q2 rounds, five years ahead in Q3/Q4 rounds; in
  early years the longer-term question ran only in Q1 rounds. DOC
  (description lines 54–95, 105–113). Never call it a flat "five-year"
  series.
- Bin edges are encoded in the data column headers (`F0_0T0_4` styles) —
  scheme changes are self-describing. COMPUTED (2021Q2.csv inspected).

## Pending computation (sol lane)

- All-variable, all-horizon, all-round measures for both surveys;
  term structure of stated uncertainty; within-year fixed-event shrinkage;
  ECB longer-term series level and post-2021 shift; calibration per
  variable; disagreement share across variables; bin-change mechanics.

## Pending literature (workflow)

- Every citation. The AI-growth published range ("0.1–30pp/yr").
- The claim that no survey anywhere regularly elicits ~10-year-ahead growth
  densities (confirm or find the counterexample).
- Novelty verdict per component.

## Prohibitions

- No fabricated mechanisms; no numbers not on this sheet or in LITREVIEW.md.
- No process narration or review history in the paper.
- Realizations are latest-vintage: state as a scope limit, flat and active.
- Uncertainty ≠ disagreement is the founding distinction of this
  literature (Zarnowitz–Lambros) — the paper never conflates the terms.
- Nothing publishes without Max.
