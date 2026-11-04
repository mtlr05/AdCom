# AMT-130: favourable adcom and FDA approval

Historical rates among products that already had a product-approval vote. The model does not see the external-control analysis, the 48-month cUHDRS result, or accelerated approval. A small R-squared means the pre-meeting labels explain little of the vote.

AMT-130 vector: orphan Y (OOPD 525216, 27 Sep 2017, AAV5 microRNA to huntingtin, uniQure), priority review (uniQure, 2 and 4 Nov 2026, company release), CGT, CBER, initial BLA. CNS is predicted both ways because the committee is not set. CNS in this table means the committee was PCNS or PDAC.

Validity: recomputed 2x2 cells match `two_by_two.csv`. Approval-question rows: 116. With a final outcome: 116. Vote source among approval-question rows: {'FDA': 101, 'press': 15}. Outcome source: {'FDA': 49, 'FDA (openFDA)': 34, 'press': 27, 'SEC/company': 6}. Priority still unverified: 31. Orphan still `review`: 2 (dropped from models that use orphan). Final vs 1-year label disagreements: 13 of 68 rows that have both.

R-squared is Nagelkerke pseudo-R-squared. AIC keeps the smaller model when extra factors do not help. The intercept prior is Normal(0, 2.5); other coefficients Normal(0, 1). Unpenalized fits with a coefficient past 8 are marked separated and are not used as a probability.

## Kept models, CNS off

| Screen | Factors | n | Nagelkerke R2 | AIC | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |
|---|---|---:|---:|---:|---:|---|---:|---|
| P(favourable) approval-question votes | priority | 92 | 0.077 | 90.4 | 0.87 | 0.79–0.94 | 46 (41) | 0.89 (0.78–0.96) |
| P(favourable) approval-question votes | orphan+priority | 91 | 0.082 | 91.7 | 0.88 | 0.77–0.96 | 27 (23) | 0.85 (0.69–0.95) |
| P(favourable) approval-question votes | priority+initial | 92 | 0.079 | 92.3 | 0.88 | 0.80–0.94 | 35 (32) | 0.91 (0.79–0.98) |
| P(favourable) approval-question votes | orphan+priority+initial | 91 | 0.085 | 93.5 | 0.89 | 0.78–0.96 | 22 (19) | 0.86 (0.68–0.96) |
| P(favourable) approval-question votes | orphan+CNS+cber+initial | 115 | 0.154 | 142.5 | 0.87 | 0.76–0.94 | 6 (6) | 0.96 (0.67–1.00) |
| P(FDA final approval) | priority | 92 | 0.008 | 74.9 | 0.85 | 0.76–0.93 | 46 (39) | 0.85 (0.72–0.93) |
| P(FDA final approval) | priority+initial | 92 | 0.034 | 75.6 | 0.87 | 0.78–0.95 | 35 (31) | 0.88 (0.75–0.96) |
| P(FDA final approval) | orphan+priority | 91 | 0.010 | 76.5 | 0.84 | 0.72–0.93 | 27 (22) | 0.81 (0.64–0.93) |
| P(FDA final approval) | orphan+priority+initial | 91 | 0.041 | 76.9 | 0.86 | 0.75–0.94 | 22 (19) | 0.86 (0.68–0.96) |
| P(FDA final approval) | orphan+CNS+cber+initial | 115 | 0.113 | 143.3 | 0.85 | 0.73–0.93 | 6 (6) | 0.96 (0.67–1.00) |
| P(FDA final approval | vote) | vote | 116 | 0.585 | 85.4 | 0.89 | 0.82–0.93 | 78 (72) | 0.92 (0.85–0.97) |
| P(FDA final approval | vote) | initial+vote | 116 | 0.589 | 86.8 | 0.88 | 0.81–0.93 | 58 (53) | 0.91 (0.82–0.97) |
| P(FDA final approval | vote) | cber+vote | 116 | 0.587 | 87.1 | 0.92 | 0.87–0.95 | 9 (9) | 0.98 (0.76–1.00) |
| P(FDA final approval | vote) | orphan+vote | 115 | 0.584 | 87.2 | 0.90 | 0.82–0.95 | 34 (32) | 0.94 (0.82–0.99) |
| P(FDA final approval | vote) | CNS+cber+initial+vote | 116 | 0.591 | 90.5 | 0.91 | 0.85–0.95 | 7 (7) | 0.97 (0.71–1.00) |

## Same models, CNS on (joint PCNS)

| Screen | Factors | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |
|---|---|---:|---|---:|---|
| P(favourable) approval-question votes | priority | 0.87 | 0.79–0.94 | 46 (41) | 0.89 (0.78–0.96) |
| P(favourable) approval-question votes | orphan+priority | 0.88 | 0.77–0.96 | 27 (23) | 0.85 (0.69–0.95) |
| P(favourable) approval-question votes | priority+initial | 0.88 | 0.80–0.94 | 35 (32) | 0.91 (0.79–0.98) |
| P(favourable) approval-question votes | orphan+priority+initial | 0.89 | 0.78–0.96 | 22 (19) | 0.86 (0.68–0.96) |
| P(favourable) approval-question votes | orphan+CNS+cber+initial | 0.93 | 0.82–0.98 | 0 (0) | n/a (n/a–n/a) |
| P(FDA final approval) | priority | 0.85 | 0.76–0.93 | 46 (39) | 0.85 (0.72–0.93) |
| P(FDA final approval) | priority+initial | 0.87 | 0.78–0.95 | 35 (31) | 0.88 (0.75–0.96) |
| P(FDA final approval) | orphan+priority | 0.84 | 0.72–0.93 | 27 (22) | 0.81 (0.64–0.93) |
| P(FDA final approval) | orphan+priority+initial | 0.86 | 0.75–0.94 | 22 (19) | 0.86 (0.68–0.96) |
| P(FDA final approval) | orphan+CNS+cber+initial | 0.91 | 0.77–0.97 | 0 (0) | n/a (n/a–n/a) |
| P(FDA final approval | vote) | vote | 0.89 | 0.82–0.93 | 78 (72) | 0.92 (0.85–0.97) |
| P(FDA final approval | vote) | initial+vote | 0.88 | 0.81–0.93 | 58 (53) | 0.91 (0.82–0.97) |
| P(FDA final approval | vote) | cber+vote | 0.92 | 0.87–0.95 | 9 (9) | 0.98 (0.76–1.00) |
| P(FDA final approval | vote) | orphan+vote | 0.90 | 0.82–0.95 | 34 (32) | 0.94 (0.82–0.99) |
| P(FDA final approval | vote) | CNS+cber+initial+vote | 0.92 | 0.86–0.96 | 0 (0) | n/a (n/a–n/a) |

CNS off, the kept models give P(favourable) from 0.87 to 0.89 and P(FDA final approval), not conditioning on the vote, from 0.84 to 0.87.

Conditioning on the vote, P(approve | favourable) runs from 0.88 to 0.92, and P(approve | unfavourable) from 0.28 to 0.37.
The marginal, each model's P(favourable) times P(approve | favourable) plus the unfavourable term, runs from 0.67 to 0.82. The low end is a vote model whose paired stage-1 model does not include priority or CGT, so that end is not the AMT-130 covariate profile.

Best stable pre-meeting model for a favourable vote: orphan+CNS+cber+initial, Nagelkerke R2 0.154. That is a small share of the variation. Most of the association in this table is between the vote and the later FDA action, and the covariates are regulatory labels, not the data package.

Stratum column: Jeffreys beta-binomial on the rows that match AMT-130 on the factors in that model. A stratum under about 8 rows is a count, not a forecast. `final` counts a later approval as approved.

## Sensitivities

All pivotal votes (not only approval/benefit-risk questions), the 1-year FDA action on the same kept factor sets, and a linear meeting-year term on those sets. Year is centered at 2020 and predicted at 2026. These rows are not in the range above.

| Screen | Factors | CNS | n | Nagelkerke R2 | AIC | P |
|---|---|---:|---:|---:|---:|---:|
| sensitivity all-pivotal P(favourable) | priority | 0 | 120 | 0.035 | 133.9 | 0.81 |
| sensitivity all-pivotal P(favourable) | priority | 1 | 120 | 0.035 | 133.9 | 0.81 |
| sensitivity all-pivotal P(favourable) | priority+CNS | 0 | 120 | 0.057 | 134.0 | 0.83 |
| sensitivity all-pivotal P(favourable) | priority+CNS | 1 | 120 | 0.057 | 134.0 | 0.73 |
| sensitivity all-pivotal P(favourable) | orphan+priority | 0 | 119 | 0.038 | 135.1 | 0.81 |
| sensitivity all-pivotal P(favourable) | orphan+priority | 1 | 119 | 0.038 | 135.1 | 0.81 |
| sensitivity all-pivotal P(favourable) | orphan+priority+CNS | 0 | 119 | 0.062 | 135.1 | 0.82 |
| sensitivity all-pivotal P(favourable) | orphan+priority+CNS | 1 | 119 | 0.062 | 135.1 | 0.72 |
| sensitivity all-pivotal P(favourable) | orphan+priority+CNS+initial | 0 | 119 | 0.071 | 136.4 | 0.83 |
| sensitivity all-pivotal P(favourable) | orphan+priority+CNS+initial | 1 | 119 | 0.071 | 136.4 | 0.73 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+CNS+initial | 0 | 119 | 0.093 | 114.0 | 0.84 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+CNS+initial | 1 | 119 | 0.093 | 114.0 | 0.73 |
| sensitivity all-pivotal P(FDA final approval) | priority+initial | 0 | 120 | 0.043 | 114.2 | 0.84 |
| sensitivity all-pivotal P(FDA final approval) | priority+initial | 1 | 120 | 0.043 | 114.2 | 0.84 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+initial | 0 | 119 | 0.062 | 114.3 | 0.82 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+initial | 1 | 119 | 0.062 | 114.3 | 0.82 |
| sensitivity all-pivotal P(FDA final approval) | priority+CNS+initial | 0 | 120 | 0.062 | 114.7 | 0.86 |
| sensitivity all-pivotal P(FDA final approval) | priority+CNS+initial | 1 | 120 | 0.062 | 114.7 | 0.78 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+initial+vote | 0 | 120 | 0.675 | 56.3 | 0.94 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+initial+vote | 1 | 120 | 0.675 | 56.3 | 0.94 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+initial+vote | 0 | 119 | 0.686 | 56.9 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+initial+vote | 1 | 119 | 0.686 | 56.9 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+vote | 0 | 120 | 0.645 | 58.0 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+vote | 1 | 120 | 0.645 | 58.0 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+CNS+initial+vote | 0 | 120 | 0.676 | 58.2 | 0.94 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+CNS+initial+vote | 1 | 120 | 0.676 | 58.2 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+CNS+initial+vote | 0 | 119 | 0.689 | 58.6 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+CNS+initial+vote | 1 | 119 | 0.689 | 58.6 | 0.91 |
| sensitivity 1-year approval | priority | 0 | 61 | 0.045 | 72.3 | 0.80 |
| sensitivity 1-year approval | priority | 1 | 61 | 0.045 | 72.3 | 0.80 |
| sensitivity 1-year approval | priority+initial | 0 | 61 | 0.146 | 69.8 | 0.82 |
| sensitivity 1-year approval | priority+initial | 1 | 61 | 0.146 | 69.8 | 0.82 |
| sensitivity 1-year approval | orphan+priority | 0 | 60 | 0.046 | 71.6 | 0.83 |
| sensitivity 1-year approval | orphan+priority | 1 | 60 | 0.046 | 71.6 | 0.83 |
| sensitivity 1-year approval | orphan+priority+initial | 0 | 60 | 0.106 | 71.0 | 0.83 |
| sensitivity 1-year approval | orphan+priority+initial | 1 | 60 | 0.106 | 71.0 | 0.83 |
| sensitivity 1-year approval | orphan+CNS+cber+initial | 0 | 67 | 0.128 | 88.4 | 0.68 |
| sensitivity 1-year approval | orphan+CNS+cber+initial | 1 | 67 | 0.128 | 88.4 | 0.82 |
| sensitivity 1-year approval | vote | vote | 0 | 68 | 0.320 | 73.1 | 0.76 |
| sensitivity 1-year approval | vote | vote | 1 | 68 | 0.320 | 73.1 | 0.76 |
| sensitivity 1-year approval | vote | initial+vote | 0 | 68 | 0.337 | 74.1 | 0.76 |
| sensitivity 1-year approval | vote | initial+vote | 1 | 68 | 0.337 | 74.1 | 0.76 |
| sensitivity 1-year approval | vote | cber+vote | 0 | 68 | 0.334 | 74.3 | 0.69 |
| sensitivity 1-year approval | vote | cber+vote | 1 | 68 | 0.334 | 74.3 | 0.69 |
| sensitivity 1-year approval | vote | orphan+vote | 0 | 67 | 0.342 | 71.9 | 0.79 |
| sensitivity 1-year approval | vote | orphan+vote | 1 | 67 | 0.342 | 71.9 | 0.79 |
| sensitivity 1-year approval | vote | CNS+cber+initial+vote | 0 | 68 | 0.360 | 76.6 | 0.68 |
| sensitivity 1-year approval | vote | CNS+cber+initial+vote | 1 | 68 | 0.360 | 76.6 | 0.77 |

Year term versus the same model without it (AIC; lower is better):

- P(favourable), priority: AIC 90.4 without year, 91.2 with year (Nagelkerke 0.097, stable=True).
- P(favourable), orphan+priority: AIC 91.7 without year, 92.1 with year (Nagelkerke 0.108, stable=True).
- P(favourable), priority+initial: AIC 92.3 without year, 93.2 with year (Nagelkerke 0.097, stable=True).
- P(favourable), orphan+priority+initial: AIC 93.5 without year, 94.0 with year (Nagelkerke 0.109, stable=True).
- P(favourable), orphan+CNS+cber+initial: AIC 142.5 without year, 143.4 with year (Nagelkerke 0.165, stable=True).
- P(FDA final approval), priority: AIC 74.9 without year, 76.8 with year (Nagelkerke 0.008, stable=True).
- P(FDA final approval), priority+initial: AIC 75.6 without year, 77.5 with year (Nagelkerke 0.034, stable=True).
- P(FDA final approval), orphan+priority: AIC 76.5 without year, 78.5 with year (Nagelkerke 0.010, stable=True).
- P(FDA final approval), orphan+priority+initial: AIC 76.9 without year, 78.9 with year (Nagelkerke 0.041, stable=True).
- P(FDA final approval), orphan+CNS+cber+initial: AIC 143.3 without year, 145.3 with year (Nagelkerke 0.113, stable=True).

Sources for the AMT-130 vector: orphan, OOPD 525216 in `oopd_all.csv`; priority review, uniQure releases of 2 Nov 2026 and 4 Nov 2026 (company, secondary) until an FDA letter is in hand.
