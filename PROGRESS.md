# Progress

## State

Build brief 3 is complete. Exact distribution scores, strictly expanding
benchmarks, `outputs/scores.csv`, the URL-wired Scores view, and
`SCORES_REPORT.md` are implemented, regenerated, and independently audited. Per
this brief's explicit instruction, no commits were created and the finished tree
remains uncommitted.

## Done

- Read `SOL_REPORT.md` and `INTERACTIVE_REPORT.md` completely before inspecting
  implementation details.
- Recorded the pre-existing unrelated changes to `paper/PAPER.md` and
  `lane3-note.md`; neither will be touched.
- Reconciled the contradictory commit instructions in favor of the task-specific
  “commit nothing” and “leave the tree uncommitted” requirements.
- Traced the respondent-density aggregation, concept-safe realization join,
  output build, compact interactive bundle, renderers, and URL-hash state.
- Fixed the no-lookahead convention: a target is usable only when its annual,
  quarterly, or monthly completion quarter is strictly before the forecast
  round; benchmark histories use the longest compatible local series.
- Confirmed the compact Scores view needs only nine emitted fields and should
  keep `data.js` comfortably below 1.2 MB at the existing four-significant-digit
  rounding.
- Recorded the original 1,080-byte CSS token block SHA-256
  (`acd919a4fe11dd8e737168379518c8fa32468c4372007834a63edd160cf6b69b`)
  for byte-identity verification.
- Implemented exact segment-integrated histogram CRPS, right-continuous PIT,
  seven pinball losses, empirical-sample CRPS, and Gaussian CRPS, including
  degenerate point-mass support and shared quantile construction.
- Added tests against dense numerical integration, the Monte Carlo energy
  identity, point-mass and Uniform closed forms, the integrated-pinball identity,
  response filtering, benchmark formulas, period cutoffs, and future-data
  invariance.
- Added full-history realization loading and minimum-10 expanding climatology and
  prior-error Gaussian benchmarks with explicit history counts and nullable skill.
- Rebuilt a 3,070-row `outputs/scores.csv` matching calibration exactly; all
  distribution scores are finite, pooled CRPS never exceeds average-individual
  CRPS, and PIT lies in `[0, 1]`.
- Added the Scores tab, compact score data, three palette-ordered lines, null-gap
  handling, tooltip/table/legend behavior, and URL-hash dispatch.
- Regenerated `interactive/data.js` at 800,301 bytes (66.7% of its 1.2 MB budget)
  with all 38 score combinations and full source-schema assertions.
- Wrote the requested per-horizon, pooling, tail-cluster, PIT, benchmark-gap,
  judgment-call, and validation analysis to `SCORES_REPORT.md`.
- Audited all 76 Scores states (38 combinations times Q1/all), including hash
  round-trips, tooltips, tables, null gaps, and fair duplicate-round aggregation.
- Passed the full 74-test suite, Ruff format/check, deterministic data generation,
  JavaScript syntax, token-integrity, source/output reconstruction, and
  working-tree audits.

## Next

- Review the uncommitted implementation and report.
