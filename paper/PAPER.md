# What do forecasters say they don't know?

Elicited macroeconomic uncertainty across two surveys, six decades, and the
horizons where it stops.

Working title. Alternatives for Max:

1. What do forecasters say they don't know? (question form, the seed)
2. What forecasters say they don't know (statement form)
3. Stated uncertainty: the macroeconomic distributions forecasters report,
   1968–2026
4. The uncertainty forecasters report
5. Elicited uncertainty and the horizons where elicitation stops

Authors: Max Ghenis [+ TBD]. Target venue open — Review of Income and Wealth
fits the measurement framing (IARIW's journal); alternatives: International
Journal of Forecasting (the natural home for SPF density work), Journal of
Economic Perspectives (if the panorama framing dominates the methods).

---

## Abstract (draft)

Professional forecasters state their own uncertainty four times a year. Since
1968 the US Survey of Professional Forecasters has collected probability
distributions — not just point forecasts — for output growth and inflation,
and the ECB's survey has done the same for the euro area since 1999. We pool
every reported histogram by the law of total variance, decomposing total
uncertainty into the average forecaster's stated uncertainty and the
disagreement between forecasters, for every variable, horizon, and survey
round. Three findings organize the panorama. Stated uncertainty is stable:
pooled next-year US growth uncertainty averaged 1.26 points over 1992–2020
and stands at 1.36 in 2026. Disagreement — the visible spread between
forecasters — carries a median 18% of total variance; the invisible
within-forecaster share carries the rest. The distributions are honest on
average (a ±1σ band covered 70% of outcomes over 33 years) and fail in
clusters, missing six straight years around the late-1990s productivity boom
and the pandemic in both directions. Density elicitation stops three to five
years out. Published estimates of AI's growth effects span roughly 0.1 to 30
percentage points a year (Shenk 2026; Cunningham 2025) at exactly the
horizons no survey asks about, and we show what asking would take. An
interactive companion tracks every series.
[NEEDS-SOL: confirm cross-variable/EA versions of facts 1–2 hold before
"every variable" phrasing ships.]

---

## 1. Introduction

Job: the elicitation-gap hook, then the contribution list. Open with the
2026 fact pair (computed): forecasters put a 0.40-point interquartile range
on next year's US growth and a 0.20-point IQR on the next decade's — the
ten-year answer is tighter than the one-year answer, and no one asked the
ten-year question as a distribution. Then the AI contrast: the published
range of decade-scale growth effects runs from under 0.1pp a year (Acemoglu
2024; CBO per Cunningham 2025) through ~1.5pp (Briggs and Kodnani 2023) and
0.07–1.24pp within one framework (Aghion and Bunel 2024) to above 30pp
(Davidson 2021; Erdil and Besiroglu 2023) — compiled at 0.1–30pp/yr by
Shenk (2026) and Cunningham (2025), almost entirely as point estimates — a
debate conducted outside the instruments that measure stated uncertainty.
The one large elicitation, Karger et al. (2026, FRI + Chicago Fed), is a
one-off collecting medians and two quantiles, and it confirms the pattern:
the disagreement is about economic impact, not capability arrival.

Contributions (draft list, confirm against LITREVIEW verdict):
1. The panorama: every density variable, horizon, and round of both
   surveys, one construction, 1968–2026.
2. The 2020s update: the inflation surge, the bin-scheme changes, and what
   they did to measured uncertainty.
3. Cross-Atlantic comparison on identical measures, including the ECB's
   longer-term (4–5 year) densities, which have no US counterpart.
4. Calibration of the pooled distributions against realizations, and where
   the misses cluster.
5. The elicitation gap: a documented inventory of where density elicitation
   stops, against where the growth debate now lives.
6. A live interactive publishing every series.

Positioning (from LITREVIEW.md, all citations verified): the decomposition
is Wallis (2005) and Boero, Smith and Wallis (2008), first posed on these
histograms by Zarnowitz and Lambros (1987); the histogram machinery follows
Engelberg, Manski and Williams (2009); the fixed-event conversion is Ganics,
Rossi and Sekhposyan (2024); the calibration template runs from Diebold,
Tay and Wallis (1999) through Clements (2014). Nearest antecedents:
D'Amico and Orphanides (2008) — the US long series, inflation only, ending
2008; Clements, Rich and Tracy (2022) — both surveys, in prose, no new
series; Allayioti et al. (2024) — the ECB's own 25-year retrospective, one
survey. The paper is the assembled object none of them built: every density
variable, both surveys, decomposed and calibration-checked through 2026,
with a live interactive — and the elicitation-gap argument, which the
corpus shows unmade.

## 2. The elicitation landscape

Job: the inventory table — who asks forecasters for distributions, about
what, how far out. Draftable now from FACTS.md (survey structure blocks):

| Survey | Density variables | Density horizons | Since |
|---|---|---|---|
| US SPF (Philadelphia Fed) | output growth, GDP price inflation | current + next year (to 2009Q1); current…+3 (2009Q2–) | 1968Q4 (nominal GNP era; real GNP 1981Q3; real GDP 1992Q1) |
| US SPF | core CPI, core PCE (Q4/Q4) | current + next year | 2007Q1 |
| US SPF | unemployment rate | current…+3 | 2009Q2 |
| US SPF | recession probability (decline in real GDP) | current + 4 quarters | 1968Q4 |
| US SPF | 10-year growth, CPI, PCE, unemployment | POINT only — no density | 1991–1992 era [NEEDS-SOL: exact starts] |
| ECB SPF | HICP, real GDP growth, unemployment | current/next calendar year; rolling 1y + 2y; longer-term (4y in Q1/Q2 rounds, 5y in Q3/Q4; Q1-only in early years) | 1999Q1 |
| ECB SPF | core HICP | same structure | 2017Q1 |

Prose to carry: the asymmetry. The US survey is longer; the euro-area survey
asks further out. Nobody asks beyond five years, and the US stops at three.
The rest of the landscape (verified in LITREVIEW.md §5): the NY Fed's SCE
elicits household densities to three years (a five-year inflation question
since 2022); Consensus Economics elicits by-range probabilities at one year
and publishes its 5–10 year forecasts as points; Livingston (since 1946),
Blue Chip, and the FOMC's SEP are point products — the SEP's fans come from
historical errors, not elicited beliefs. The two partial precedents at long
horizons are one-offs: Christensen, Gillingham and Nordhaus (2018, expert
quantiles on growth to 2100) and Karger et al. (2026). The claim the
inventory supports: no survey anywhere regularly elicits probability
distributions over ten-year-ahead growth. Bin history for the US densities
(SPF documentation): 15 bins at the 1968Q4 origin, 6 from 1981Q3, 10 from
1992Q1, 11 from 2009Q2, with changes in 2020Q2 and 2024Q2.

## 3. Measures

Job: the construction, stated once, used everywhere. Draft (evidence in
hand):

Each forecaster attaches probabilities to bins. We place each bin's mass at
its midpoint, give open tails the width of the adjacent bin, keep responses
whose probabilities sum to within two points of 100, and renormalize. For
forecaster i, the histogram yields a mean m_i and a variance v_i. The law
of total variance splits the pooled mixture:

    total variance = E[v_i] + Var(m_i)

The first term is the average uncertainty forecasters state individually;
the second is disagreement, the only term visible in point-forecast data.
We report the square roots, the between share, and quantiles of the pooled
mixture. The interquartile range of the mixture doubles as a robustness
measure: bin-scheme changes move midpoint-based SDs mechanically, and the
2020Q2 US bin widening is the worked example [PENDING-SOL: magnitude].

Fixed-event structure: targets are calendar years, so a "next year"
forecast made in Q1 and one made in Q4 differ in horizon by three quarters.
We treat (round, target) pairs explicitly and show within-year shrinkage
rather than averaging over it. [PENDING-SOL: shrinkage profile.]

## 4. Five stylized facts

Each fact gets a figure from the pipeline and a paragraph. Status:

1. **Stated uncertainty is stable — and its 2021 spike decayed fast.**
   Next-year US growth: 1.24pp pooled SD in 1992, 1.26 average through
   2020, 2.10 peak in 2021, 1.36 by 2026 (COMPUTED). [PENDING-SOL: same
   series for inflation, unemployment, and the euro area.]
2. **Disagreement is the small share.** Median 18% of total variance
   (decile range 12–32%, max 41% in 2009) for US next-year growth
   (COMPUTED). The spread you can see in point forecasts understates
   stated uncertainty roughly threefold. [PENDING-SOL: does the share stay
   small across variables, horizons, and the EA?]
3. **The term structure of stated uncertainty is flat where it exists —
   and the point-forecast term structure inverts.** The 10-year IQR (0.20)
   sits below the next-year IQR (0.40) in 2026 (COMPUTED). [PENDING-SOL:
   within-density term structure h=0…3 US, 1y/2y/longer ECB; where does
   stated uncertainty peak?]
4. **The distributions are calibrated on average and fail in regimes.**
   69.7% one-sigma coverage over 33 years; misses: 1996–2001 (six straight,
   five upside then the 2001 bust), 2008–09, 2020–21 (COMPUTED). The
   average is textbook; the errors are not independent draws.
5. **The euro area asks the question the US doesn't — and the answer moved
   after 2021.** The ECB longer-term density series (4–5 years out)
   [PENDING-SOL: level 1999–2026, post-2021 shift; this is the fact the
   whole AI section leans on, so it ships only with computed numbers].

## 5. The elicitation gap

Job: put the AI growth debate against the inventory. Beats, citations
verified (LITREVIEW.md §5): the 0.1–30pp/yr published range and its
anchors (Acemoglu low, Goldman mid, Aghion–Bunel spread-within-framework,
Davidson/Erdil–Besiroglu high, Epoch's GATE model whose own authors
disclaim quantitative reliability); Karger et al. (2026) as the flagship
elicitation — medians and two quantiles, once; Chow, Halperin and Mazlish
(2026) extracting long-horizon growth beliefs from asset prices precisely
because no survey elicits them; Cunningham (2025) independently noting the
missing distributions. The observation the paper owns: the instruments that
would discipline this debate exist, run quarterly, have 50 years of
calibration record — and stop at year three (US) or five (EA). Tone check:
state the gap; do not scold the surveys.

## 6. What better elicitation would look like

Job: constructive close. Candidate beats (design, not advocacy): extend one
existing survey block to a 10-year density on growth; bins wide enough to
be honest about tails (the 2020 US widening as precedent); score and
publish calibration the way section 4 does; pair each long-horizon density
with the respondent's AI-adoption assumption so the growth debate becomes
decomposable. [Draft after facts 3 and 5 are in.]

## 7. Conclusion

One page. The 2026 pair again — 0.40 next year, 0.20 for the decade — now
with the whole panorama behind it.

---

## Figures (planned, all from `outputs/`)

1. Total pooled uncertainty over time, all variables, both surveys (fact 1)
2. Decomposition: within vs between shares (fact 2)
3. Term structure: stated uncertainty by horizon, US and EA (fact 3)
4. Calibration: consensus ± total band vs realizations, misses flagged
   (fact 4)
5. ECB longer-term series 1999–2026 (fact 5)
6. The elicitation gap: horizons with densities vs the AI-estimate range
   (the one original diagram; design in the interactive first)
