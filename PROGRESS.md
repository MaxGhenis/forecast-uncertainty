# Progress

## State

Build brief 2 is in progress. The repository handoff and interactive plan have
been read. Work is split between the two pipeline corrections, full-matrix data
generation, and the dependency-free SVG interface. Per the brief's final
instruction, all changes will remain uncommitted.

## Done

- Read `SOL_REPORT.md` and `interactive/PLAN.md` completely.
- Confirmed the prior pipeline's documented HICPX realization gap and synthetic
  zero-coverage treatment of the invalid UNEMP10 download.
- Confirmed the existing interactive is a three-view Q1 US real-GDP seed mockup.
- Recorded and preserved unrelated pre-existing untracked lane-note files.

## Next

- Load the local ECB core-HICP realization file in parallel with headline HICP,
  extend calibration flags and actual-only accounting, and update tests.
- Remove all UNEMP10 pipeline/download/README/coverage references and delete the
  invalid HTML workbook.
- Rebuild all outputs and pass the full pipeline test suite.
- Generate a compact full-matrix `interactive/data.js` from `outputs/`.
- Wire live controls, both decomposition measures, quarterly-round behavior,
  calibration, consensus fan, and the new term-structure view.
- Validate static behavior, size/schema invariants, themes, tooltips, and tables.
- Write `INTERACTIVE_REPORT.md` with audited counts, decisions, and honest gaps.
