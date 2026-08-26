"""SPF density-forecast pipeline (built 2026-08-25, IARIW session).

Computes forecaster-level uncertainty, disagreement, and total pooled
uncertainty (law of total variance) from the Philadelphia Fed SPF
individual probability forecasts (PRGDP), plus realized-error calibration.

Data: https://www.philadelphiafed.org/-/media/frbp/assets/surveys-and-data/
  survey-of-professional-forecasters/data-files/files/individual_prgdp.xlsx
Realized growth: FRED A191RL1A225NBEA (annual-avg real GDP growth, BEA).

Bin schemes from SPF documentation Table 7 (verified from the PDF):
- 1992Q1-2009Q1: 10 bins/target year, 2 target years (cols 1-10 current, 11-20 next)
- 2009Q2-2020Q1: 11 bins, 4 target years (1-11, 12-22, 23-33, 34-44)
- 2020Q2-2024Q1: 11 WIDE bins (16+ ... <-12) - COVID widening; inflates SDs mechanically
- 2024Q2-:       11 intermediate bins (9+ ... <-5.1)
Open tails get midpoint = boundary +/- half the adjacent bin width.

Per Q1 round (fixed horizon: next-year target):
  weights W_i = probs/100 per forecaster (rows with |sum-100|<2 kept)
  m_i = sum(W_i * mid); v_i = sum(W_i * mid^2) - m_i^2
  uncertainty (within) = sqrt(mean(v_i));  disagreement (between) = sd(m_i)
  TOTAL = sqrt(mean(v_i) + var(m_i))   # law of total variance, mixture pooling
  (same construction as ~/llm-econ-beliefs: Var = E[Var|run] + Var(E|run))

Calibration: consensus mean forecast (mean of m_i) vs realized; coverage of
+/- total was 70% over 33 years (theory 68%); misses cluster in regime shifts
(1996-2000 five straight +2pp, 2009 -4.9, 2020 -3.8, 2021 +4.6).

Outputs used for the IARIW social set: spf_uncertainty_disagreement.csv,
spf_errors.csv, spf_nextyear_consensus.csv, spf_rgdp10_dispersion.csv.
NOTE: PRGDP also carries year+2 and year+3 blocks since 2009Q2 (term
structure of uncertainty - unexploited). PRPGDP/PRUNEMP/PRCCPI/PRCPCE/RECESS
are the other density variables. ECB SPF has 1y/2y/5y densities (growth,
HICP, unemployment) - not yet pulled.
"""
import pandas as pd, numpy as np

def mids_from(e):
    out = []
    for lo, hi in e:
        if hi is None: w = e[1][1] - e[1][0]; out.append(lo + w/2)
        elif lo is None: w = e[-2][1] - e[-2][0]; out.append(hi - w/2)
        else: out.append((lo + hi)/2)
    return out

S1 = mids_from([(6,None),(5,5.9),(4,4.9),(3,3.9),(2,2.9),(1,1.9),(0,0.9),(-1,-0.1),(-2,-1.1),(None,-2)])
S2 = mids_from([(6,None),(5,5.9),(4,4.9),(3,3.9),(2,2.9),(1,1.9),(0,0.9),(-1,-0.1),(-2,-1.1),(-3,-2.1),(None,-3)])
S3 = mids_from([(16,None),(10,15.9),(7,9.9),(4,6.9),(2.5,3.9),(1.5,2.4),(0,1.4),(-3,-0.1),(-6,-3.1),(-12,-6.1),(None,-12)])
S4 = mids_from([(9,None),(7,8.9),(5.5,6.9),(4,5.4),(2.5,3.9),(1.5,2.4),(0,1.4),(-1.5,-0.1),(-3,-1.6),(-5.1,-3.1),(None,-5.1)])

def era_nextyear(y):
    """(column range, midpoints) for the NEXT-YEAR block of a Q1-year-y survey."""
    if y <= 2009: return (range(11, 21), S1)
    if y <= 2020: return (range(12, 23), S2)
    if y <= 2024: return (range(12, 23), S3)
    return (range(12, 23), S4)

def round_stats(P, mids):
    """P: (n_forecasters, n_bins) raw percent probs; returns dict of measures."""
    P = P[~np.isnan(P).all(axis=1)]; P = np.nan_to_num(P)
    P = P[np.abs(P.sum(axis=1) - 100) < 2]
    W = P / P.sum(axis=1, keepdims=True)
    m = (W * mids).sum(axis=1)
    v = (W * mids**2).sum(axis=1) - m**2
    within = v.mean(); between = m.var(ddof=1)
    return dict(n=len(P), mean=m.mean(), median=np.median(m),
                within_sd=np.sqrt(within), dis=m.std(ddof=1),
                total=np.sqrt(within + between),
                share_between=between/(within+between))
