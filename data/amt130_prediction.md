# AMT-130: favourable adcom and FDA approval

Historical rates among products that already had a product-approval vote. The model does not see the external-control analysis, the 48-month cUHDRS result, or accelerated approval. A small R-squared means the pre-meeting labels explain little of the vote.

AMT-130 vector: orphan Y (OOPD 525216, 27 Sep 2017, AAV5 microRNA to huntingtin, uniQure), priority review (uniQure, 2 and 4 Nov 2026, company release), CGT, CBER, initial BLA. CNS is predicted both ways because the committee is not set. CNS in this table means the committee was PCNS or PDAC.

Validity: recomputed 2x2 cells match `two_by_two.csv`. Approval-question rows: 116. With a final outcome: 116. Vote source among approval-question rows: {'FDA': 101, 'press': 15}. Outcome source: {'FDA': 49, 'FDA (openFDA)': 34, 'press': 27, 'SEC/company': 6}. Priority still unverified: 45. Orphan still `review`: 2 (dropped from models that use orphan). Final vs 1-year label disagreements: 13 of 68 rows that have both.

R-squared is Nagelkerke pseudo-R-squared. AIC keeps the smaller model when extra factors do not help. The intercept prior is Normal(0, 2.5); other coefficients Normal(0, 1). Unpenalized fits with a coefficient past 8 are marked separated and are not used as a probability.

## Kept models, CNS off

| Screen | Factors | n | Nagelkerke R2 | AIC | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |
|---|---|---:|---:|---:|---:|---|---:|---|
| P(favourable) approval-question votes | priority | 85 | 0.115 | 74.1 | 0.90 | 0.83–0.95 | 43 (40) | 0.93 (0.83–0.98) |
| P(favourable) approval-question votes | priority+initial | 85 | 0.141 | 74.7 | 0.92 | 0.86–0.96 | 32 (31) | 0.96 (0.86–1.00) |
| P(favourable) approval-question votes | orphan+priority | 84 | 0.133 | 74.8 | 0.92 | 0.84–0.98 | 25 (23) | 0.91 (0.77–0.98) |
| P(favourable) approval-question votes | orphan+priority+initial | 84 | 0.159 | 75.4 | 0.93 | 0.87–0.98 | 20 (19) | 0.94 (0.79–0.99) |
| P(favourable) approval-question votes | priority+CGT+cber+initial | 85 | 0.161 | 77.6 | 0.96 | 0.92–0.98 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval) | priority+initial | 85 | 0.131 | 53.7 | 0.92 | 0.86–0.98 | 32 (30) | 0.93 (0.81–0.99) |
| P(FDA final approval) | orphan+priority+initial | 84 | 0.135 | 55.4 | 0.93 | 0.85–0.98 | 20 (19) | 0.94 (0.79–0.99) |
| P(FDA final approval) | priority | 85 | 0.013 | 56.5 | 0.89 | 0.81–0.96 | 43 (38) | 0.88 (0.76–0.95) |
| P(FDA final approval) | priority+CGT+cber+initial | 85 | 0.149 | 56.9 | 0.95 | 0.92–0.98 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval) | orphan+priority+CGT+cber+initial | 84 | 0.153 | 58.6 | 0.95 | 0.91–0.98 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval | vote) | vote | 116 | 0.585 | 85.4 | 0.89 | 0.82–0.93 | 78 (72) | 0.92 (0.85–0.97) |
| P(FDA final approval | vote) | initial+vote | 116 | 0.589 | 86.8 | 0.88 | 0.81–0.93 | 58 (53) | 0.91 (0.82–0.97) |
| P(FDA final approval | vote) | cber+vote | 116 | 0.587 | 87.1 | 0.92 | 0.87–0.95 | 9 (9) | 0.98 (0.76–1.00) |
| P(FDA final approval | vote) | orphan+vote | 115 | 0.584 | 87.2 | 0.90 | 0.82–0.95 | 34 (32) | 0.94 (0.82–0.99) |
| P(FDA final approval | vote) | CNS+cber+initial+vote | 116 | 0.591 | 90.5 | 0.91 | 0.85–0.95 | 7 (7) | 0.97 (0.71–1.00) |

## Same models, CNS on (joint PCNS)

| Screen | Factors | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |
|---|---|---:|---|---:|---|
| P(favourable) approval-question votes | priority | 0.90 | 0.83–0.95 | 43 (40) | 0.93 (0.83–0.98) |
| P(favourable) approval-question votes | priority+initial | 0.92 | 0.86–0.96 | 32 (31) | 0.96 (0.86–1.00) |
| P(favourable) approval-question votes | orphan+priority | 0.92 | 0.84–0.98 | 25 (23) | 0.91 (0.77–0.98) |
| P(favourable) approval-question votes | orphan+priority+initial | 0.93 | 0.87–0.98 | 20 (19) | 0.94 (0.79–0.99) |
| P(favourable) approval-question votes | priority+CGT+cber+initial | 0.96 | 0.92–0.98 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval) | priority+initial | 0.92 | 0.86–0.98 | 32 (30) | 0.93 (0.81–0.99) |
| P(FDA final approval) | orphan+priority+initial | 0.93 | 0.85–0.98 | 20 (19) | 0.94 (0.79–0.99) |
| P(FDA final approval) | priority | 0.89 | 0.81–0.96 | 43 (38) | 0.88 (0.76–0.95) |
| P(FDA final approval) | priority+CGT+cber+initial | 0.95 | 0.92–0.98 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval) | orphan+priority+CGT+cber+initial | 0.95 | 0.91–0.98 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval | vote) | vote | 0.89 | 0.82–0.93 | 78 (72) | 0.92 (0.85–0.97) |
| P(FDA final approval | vote) | initial+vote | 0.88 | 0.81–0.93 | 58 (53) | 0.91 (0.82–0.97) |
| P(FDA final approval | vote) | cber+vote | 0.92 | 0.87–0.95 | 9 (9) | 0.98 (0.76–1.00) |
| P(FDA final approval | vote) | orphan+vote | 0.90 | 0.82–0.95 | 34 (32) | 0.94 (0.82–0.99) |
| P(FDA final approval | vote) | CNS+cber+initial+vote | 0.92 | 0.86–0.96 | 0 (0) | n/a (n/a–n/a) |

CNS off, the kept models give P(favourable) from 0.90 to 0.96 and P(FDA final approval), not conditioning on the vote, from 0.89 to 0.95.

Conditioning on the vote, P(approve | favourable) runs from 0.88 to 0.92, and P(approve | unfavourable) from 0.28 to 0.37.
The marginal, each model's P(favourable) times P(approve | favourable) plus the unfavourable term, runs from 0.67 to 0.82. The low end is a vote model whose paired stage-1 model does not include priority or CGT, so that end is not the AMT-130 covariate profile.

Best stable pre-meeting model for a favourable vote: priority+CGT+cber+initial, Nagelkerke R2 0.161. That is a small share of the variation. Most of the association in this table is between the vote and the later FDA action, and the covariates are regulatory labels, not the data package.

Stratum column: Jeffreys beta-binomial on the rows that match AMT-130 on the factors in that model. A stratum under about 8 rows is a count, not a forecast. `final` counts a later approval as approved.

## Sensitivities

All pivotal votes (not only approval/benefit-risk questions), the 1-year FDA action on the same kept factor sets, and a linear meeting-year term on those sets. Year is centered at 2020 and predicted at 2026. These rows are not in the range above.

| Screen | Factors | CNS | n | Nagelkerke R2 | AIC | P |
|---|---|---:|---:|---:|---:|---:|
| sensitivity all-pivotal P(favourable) | priority+initial | 0 | 106 | 0.088 | 108.1 | 0.87 |
| sensitivity all-pivotal P(favourable) | priority+initial | 1 | 106 | 0.088 | 108.1 | 0.87 |
| sensitivity all-pivotal P(favourable) | priority | 0 | 106 | 0.055 | 108.5 | 0.85 |
| sensitivity all-pivotal P(favourable) | priority | 1 | 106 | 0.055 | 108.5 | 0.85 |
| sensitivity all-pivotal P(favourable) | orphan+priority+initial | 0 | 105 | 0.100 | 108.8 | 0.89 |
| sensitivity all-pivotal P(favourable) | orphan+priority+initial | 1 | 105 | 0.100 | 108.8 | 0.89 |
| sensitivity all-pivotal P(favourable) | orphan+priority | 0 | 105 | 0.069 | 109.1 | 0.87 |
| sensitivity all-pivotal P(favourable) | orphan+priority | 1 | 105 | 0.069 | 109.1 | 0.87 |
| sensitivity all-pivotal P(favourable) | orphan+priority+CGT+CNS+cber+initial | 0 | 105 | 0.133 | 112.4 | 0.95 |
| sensitivity all-pivotal P(favourable) | orphan+priority+CGT+CNS+cber+initial | 1 | 105 | 0.133 | 112.4 | 0.93 |
| sensitivity all-pivotal P(FDA final approval) | priority+initial | 0 | 106 | 0.154 | 79.5 | 0.91 |
| sensitivity all-pivotal P(FDA final approval) | priority+initial | 1 | 106 | 0.154 | 79.5 | 0.91 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+initial | 0 | 105 | 0.159 | 80.9 | 0.91 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+initial | 1 | 105 | 0.159 | 80.9 | 0.91 |
| sensitivity all-pivotal P(FDA final approval) | priority+CNS+initial | 0 | 106 | 0.163 | 81.0 | 0.91 |
| sensitivity all-pivotal P(FDA final approval) | priority+CNS+initial | 1 | 106 | 0.163 | 81.0 | 0.88 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+CNS+initial | 0 | 105 | 0.169 | 82.3 | 0.91 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+CNS+initial | 1 | 105 | 0.169 | 82.3 | 0.88 |
| sensitivity all-pivotal P(FDA final approval) | priority+CGT+CNS+cber+initial | 0 | 106 | 0.178 | 84.0 | 0.95 |
| sensitivity all-pivotal P(FDA final approval) | priority+CGT+CNS+cber+initial | 1 | 106 | 0.178 | 84.0 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+initial+vote | 0 | 106 | 0.637 | 45.9 | 0.95 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+initial+vote | 1 | 106 | 0.637 | 45.9 | 0.95 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+initial+vote | 0 | 105 | 0.636 | 47.9 | 0.95 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+initial+vote | 1 | 105 | 0.636 | 47.9 | 0.95 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+CNS+initial+vote | 0 | 106 | 0.637 | 47.9 | 0.95 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+CNS+initial+vote | 1 | 106 | 0.637 | 47.9 | 0.95 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+CGT+cber+initial+vote | 0 | 106 | 0.639 | 49.7 | 0.97 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+CGT+cber+initial+vote | 1 | 106 | 0.639 | 49.7 | 0.97 |
| sensitivity all-pivotal P(FDA final approval | vote) | CGT+CNS+cber+initial+vote | 0 | 149 | 0.646 | 107.8 | 0.94 |
| sensitivity all-pivotal P(FDA final approval | vote) | CGT+CNS+cber+initial+vote | 1 | 149 | 0.646 | 107.8 | 0.94 |
| sensitivity 1-year approval | priority+initial | 0 | 61 | 0.146 | 69.8 | 0.82 |
| sensitivity 1-year approval | priority+initial | 1 | 61 | 0.146 | 69.8 | 0.82 |
| sensitivity 1-year approval | orphan+priority+initial | 0 | 60 | 0.106 | 71.0 | 0.83 |
| sensitivity 1-year approval | orphan+priority+initial | 1 | 60 | 0.106 | 71.0 | 0.83 |
| sensitivity 1-year approval | priority | 0 | 61 | 0.045 | 72.3 | 0.80 |
| sensitivity 1-year approval | priority | 1 | 61 | 0.045 | 72.3 | 0.80 |
| sensitivity 1-year approval | priority+CGT+cber+initial | 0 | 61 | 0.164 | 72.9 | 0.71 |
| sensitivity 1-year approval | priority+CGT+cber+initial | 1 | 61 | 0.164 | 72.9 | 0.71 |
| sensitivity 1-year approval | orphan+priority+CGT+cber+initial | 0 | 60 | 0.131 | 73.9 | 0.73 |
| sensitivity 1-year approval | orphan+priority+CGT+cber+initial | 1 | 60 | 0.131 | 73.9 | 0.73 |
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
| sensitivity year P(favourable) | priority+year | 0 | 85 | 0.176 | 72.7 | 0.77 |
| sensitivity year P(favourable) | priority+year | 1 | 85 | 0.176 | 72.7 | 0.77 |
| sensitivity year P(favourable) | priority+initial+year | 0 | 85 | 0.191 | 73.9 | 0.81 |
| sensitivity year P(favourable) | priority+initial+year | 1 | 85 | 0.191 | 73.9 | 0.81 |
| sensitivity year P(favourable) | orphan+priority+year | 0 | 84 | 0.208 | 72.6 | 0.80 |
| sensitivity year P(favourable) | orphan+priority+year | 1 | 84 | 0.208 | 72.6 | 0.80 |
| sensitivity year P(favourable) | orphan+priority+initial+year | 0 | 84 | 0.226 | 73.6 | 0.83 |
| sensitivity year P(favourable) | orphan+priority+initial+year | 1 | 84 | 0.226 | 73.6 | 0.83 |
| sensitivity year P(favourable) | priority+CGT+cber+initial+year | 0 | 85 | 0.212 | 76.6 | 0.89 |
| sensitivity year P(favourable) | priority+CGT+cber+initial+year | 1 | 85 | 0.212 | 76.6 | 0.89 |

Year term versus the same model without it (AIC; lower is better):

- P(favourable), priority: AIC 74.1 without year, 72.7 with year (Nagelkerke 0.176, stable=True).
- P(favourable), priority+initial: AIC 74.7 without year, 73.9 with year (Nagelkerke 0.191, stable=True).
- P(favourable), orphan+priority: AIC 74.8 without year, 72.6 with year (Nagelkerke 0.208, stable=True).
- P(favourable), orphan+priority+initial: AIC 75.4 without year, 73.6 with year (Nagelkerke 0.226, stable=True).
- P(favourable), priority+CGT+cber+initial: AIC 77.6 without year, 76.6 with year (Nagelkerke 0.212, stable=True).
- P(FDA final approval), priority+initial: AIC 53.7 without year, 55.6 with year (Nagelkerke 0.133, stable=True).
- P(FDA final approval), orphan+priority+initial: AIC 55.4 without year, 57.2 with year (Nagelkerke 0.139, stable=True).
- P(FDA final approval), priority: AIC 56.5 without year, 58.0 with year (Nagelkerke 0.025, stable=True).
- P(FDA final approval), priority+CGT+cber+initial: AIC 56.9 without year, 60.0 with year (Nagelkerke 0.124, stable=False).
- P(FDA final approval), orphan+priority+CGT+cber+initial: AIC 58.6 without year, 60.4 with year (Nagelkerke 0.158, stable=True).

Sources for the AMT-130 vector: orphan, OOPD 525216 in `oopd_all.csv`; priority review, uniQure releases of 2 Nov 2026 and 4 Nov 2026 (company, secondary) until an FDA letter is in hand.
