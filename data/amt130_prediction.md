# AMT-130: favourable adcom and FDA approval

Historical rates among products that already had a product-approval vote. The model does not see the external-control analysis, the 48-month cUHDRS result, or accelerated approval. A small R-squared means the pre-meeting labels explain little of the vote.

AMT-130 vector: orphan Y (OOPD 525216, 27 Sep 2017, AAV5 microRNA to huntingtin, uniQure), priority review (uniQure, 2 and 4 Nov 2026, company release), CGT, CBER, initial BLA. CNS is predicted both ways because the committee is not set. CNS in this table means the committee was PCNS or PDAC.

Validity: recomputed 2x2 cells match `two_by_two.csv`. Approval-question rows: 116. With a final outcome: 116. Vote source among approval-question rows: {'FDA': 101, 'press': 15}. Outcome source: {'FDA': 49, 'FDA (openFDA)': 34, 'press': 27, 'SEC/company': 6}. Priority still unverified: 3. Orphan still `review`: 2 (dropped from models that use orphan). Final vs 1-year label disagreements: 13 of 68 rows that have both.

R-squared is Nagelkerke pseudo-R-squared. AIC keeps the smaller model when extra factors do not help. The intercept prior is Normal(0, 2.5); other coefficients Normal(0, 1). Unpenalized fits with a coefficient past 8 are marked separated and are not used as a probability.

## Kept models, CNS off

| Screen | Factors | n | Nagelkerke R2 | AIC | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |
|---|---|---:|---:|---:|---:|---|---:|---|
| P(favourable) approval-question votes | orphan+priority+opioid+CNS | 112 | 0.261 | 127.6 | 0.86 | 0.76–0.94 | 28 (24) | 0.85 (0.70–0.95) |
| P(favourable) approval-question votes | priority+opioid+CNS | 113 | 0.235 | 128.6 | 0.82 | 0.73–0.89 | 45 (37) | 0.82 (0.69–0.91) |
| P(favourable) approval-question votes | orphan+priority+opioid | 112 | 0.227 | 128.9 | 0.87 | 0.78–0.95 | 30 (26) | 0.86 (0.71–0.95) |
| P(favourable) approval-question votes | orphan+priority+opioid+CNS+cber | 112 | 0.264 | 129.2 | 0.89 | 0.79–0.96 | 7 (7) | 0.97 (0.71–1.00) |
| P(favourable) approval-question votes | orphan+priority+opioid+CNS+cber+initial | 112 | 0.264 | 131.2 | 0.89 | 0.77–0.96 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval) | priority+opioid+CNS | 113 | 0.193 | 128.1 | 0.79 | 0.68–0.88 | 45 (35) | 0.78 (0.64–0.88) |
| P(FDA final approval) | orphan+priority+opioid+CNS | 112 | 0.203 | 128.6 | 0.83 | 0.69–0.92 | 28 (23) | 0.82 (0.65–0.93) |
| P(FDA final approval) | priority+opioid+CNS+cber | 113 | 0.204 | 129.1 | 0.86 | 0.69–0.93 | 9 (8) | 0.87 (0.59–0.99) |
| P(FDA final approval) | priority+opioid | 113 | 0.154 | 129.6 | 0.81 | 0.70–0.88 | 50 (40) | 0.80 (0.67–0.89) |
| P(FDA final approval) | orphan+priority+opioid+CNS+cber+initial | 112 | 0.211 | 131.8 | 0.87 | 0.75–0.94 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval | vote) | priority+opioid+vote | 113 | 0.621 | 79.9 | 0.90 | 0.84–0.94 | 42 (40) | 0.95 (0.86–0.99) |
| P(FDA final approval | vote) | priority+vote | 113 | 0.601 | 80.6 | 0.90 | 0.83–0.94 | 45 (43) | 0.95 (0.86–0.99) |
| P(FDA final approval | vote) | priority+opioid+CNS+vote | 113 | 0.629 | 80.8 | 0.90 | 0.83–0.94 | 37 (35) | 0.94 (0.84–0.99) |
| P(FDA final approval | vote) | priority+opioid+cber+vote | 113 | 0.623 | 81.6 | 0.92 | 0.86–0.96 | 8 (8) | 0.97 (0.74–1.00) |
| P(FDA final approval | vote) | priority+opioid+CNS+cber+initial+vote | 113 | 0.632 | 84.3 | 0.91 | 0.85–0.96 | 6 (6) | 0.96 (0.67–1.00) |

## Same models, CNS on (joint PCNS)

| Screen | Factors | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |
|---|---|---:|---|---:|---|
| P(favourable) approval-question votes | orphan+priority+opioid+CNS | 0.94 | 0.85–0.97 | 2 (2) | 0.90 (0.33–1.00) |
| P(favourable) approval-question votes | priority+opioid+CNS | 0.90 | 0.82–0.95 | 5 (5) | 0.96 (0.62–1.00) |
| P(favourable) approval-question votes | orphan+priority+opioid | 0.87 | 0.78–0.95 | 30 (26) | 0.86 (0.71–0.95) |
| P(favourable) approval-question votes | orphan+priority+opioid+CNS+cber | 0.95 | 0.88–0.98 | 0 (0) | n/a (n/a–n/a) |
| P(favourable) approval-question votes | orphan+priority+opioid+CNS+cber+initial | 0.95 | 0.87–0.98 | 0 (0) | n/a (n/a–n/a) |
| P(FDA final approval) | priority+opioid+CNS | 0.89 | 0.79–0.94 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval) | orphan+priority+opioid+CNS | 0.92 | 0.82–0.97 | 2 (2) | 0.90 (0.33–1.00) |
| P(FDA final approval) | priority+opioid+CNS+cber | 0.93 | 0.81–0.97 | 0 (0) | n/a (n/a–n/a) |
| P(FDA final approval) | priority+opioid | 0.81 | 0.70–0.88 | 50 (40) | 0.80 (0.67–0.89) |
| P(FDA final approval) | orphan+priority+opioid+CNS+cber+initial | 0.94 | 0.85–0.98 | 0 (0) | n/a (n/a–n/a) |
| P(FDA final approval | vote) | priority+opioid+vote | 0.90 | 0.84–0.94 | 42 (40) | 0.95 (0.86–0.99) |
| P(FDA final approval | vote) | priority+vote | 0.90 | 0.83–0.94 | 45 (43) | 0.95 (0.86–0.99) |
| P(FDA final approval | vote) | priority+opioid+CNS+vote | 0.93 | 0.88–0.96 | 5 (5) | 0.96 (0.62–1.00) |
| P(FDA final approval | vote) | priority+opioid+cber+vote | 0.92 | 0.86–0.96 | 8 (8) | 0.97 (0.74–1.00) |
| P(FDA final approval | vote) | priority+opioid+CNS+cber+initial+vote | 0.95 | 0.90–0.97 | 0 (0) | n/a (n/a–n/a) |

CNS off, the kept models give P(favourable) from 0.82 to 0.89 and P(FDA final approval), not conditioning on the vote, from 0.79 to 0.87.

Conditioning on the vote, P(approve | favourable) runs from 0.90 to 0.92, and P(approve | unfavourable) from 0.30 to 0.40.
The marginal, each model's P(favourable) times P(approve | favourable) plus the unfavourable term, runs from 0.78 to 0.86. The low end is a vote model whose paired stage-1 model does not include priority or CGT, so that end is not the AMT-130 covariate profile.

Best stable pre-meeting model for a favourable vote: orphan+priority+opioid+CNS+cber+initial, Nagelkerke R2 0.264. That is a small share of the variation. Most of the association in this table is between the vote and the later FDA action, and the covariates are regulatory labels, not the data package.

Stratum column: Jeffreys beta-binomial on the rows that match AMT-130 on the factors in that model. A stratum under about 8 rows is a count, not a forecast. `final` counts a later approval as approved.

## Sensitivities

All pivotal votes (not only approval/benefit-risk questions), the 1-year FDA action on the same kept factor sets, and a linear meeting-year term on those sets. Year is centered at 2020 and predicted at 2026. These rows are not in the range above.

| Screen | Factors | CNS | n | Nagelkerke R2 | AIC | P |
|---|---|---:|---:|---:|---:|---:|
| sensitivity all-pivotal P(favourable) | orphan+priority+opioid | 0 | 145 | 0.142 | 181.5 | 0.79 |
| sensitivity all-pivotal P(favourable) | orphan+priority+opioid | 1 | 145 | 0.142 | 181.5 | 0.79 |
| sensitivity all-pivotal P(favourable) | priority+opioid | 0 | 147 | 0.138 | 181.5 | 0.77 |
| sensitivity all-pivotal P(favourable) | priority+opioid | 1 | 147 | 0.138 | 181.5 | 0.77 |
| sensitivity all-pivotal P(favourable) | priority+opioid+cber | 0 | 147 | 0.146 | 182.5 | 0.83 |
| sensitivity all-pivotal P(favourable) | priority+opioid+cber | 1 | 147 | 0.146 | 182.5 | 0.83 |
| sensitivity all-pivotal P(favourable) | orphan+priority+opioid+cber | 0 | 145 | 0.147 | 182.8 | 0.84 |
| sensitivity all-pivotal P(favourable) | orphan+priority+opioid+cber | 1 | 145 | 0.147 | 182.8 | 0.84 |
| sensitivity all-pivotal P(favourable) | orphan+priority+opioid+CGT+CNS+cber+initial | 0 | 145 | 0.149 | 188.6 | 0.84 |
| sensitivity all-pivotal P(favourable) | orphan+priority+opioid+CGT+CNS+cber+initial | 1 | 145 | 0.149 | 188.6 | 0.83 |
| sensitivity all-pivotal P(FDA final approval) | priority+opioid | 0 | 147 | 0.115 | 177.7 | 0.77 |
| sensitivity all-pivotal P(FDA final approval) | priority+opioid | 1 | 147 | 0.115 | 177.7 | 0.77 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+opioid | 0 | 145 | 0.115 | 178.3 | 0.78 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+opioid | 1 | 145 | 0.115 | 178.3 | 0.78 |
| sensitivity all-pivotal P(FDA final approval) | priority+opioid+cber | 0 | 147 | 0.121 | 179.0 | 0.83 |
| sensitivity all-pivotal P(FDA final approval) | priority+opioid+cber | 1 | 147 | 0.121 | 179.0 | 0.83 |
| sensitivity all-pivotal P(FDA final approval) | priority+opioid+CGT | 0 | 147 | 0.118 | 179.3 | 0.82 |
| sensitivity all-pivotal P(FDA final approval) | priority+opioid+CGT | 1 | 147 | 0.118 | 179.3 | 0.82 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+opioid+CGT+CNS+cber+initial | 0 | 145 | 0.123 | 185.3 | 0.83 |
| sensitivity all-pivotal P(FDA final approval) | orphan+priority+opioid+CGT+CNS+cber+initial | 1 | 145 | 0.123 | 185.3 | 0.84 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+opioid+vote | 0 | 147 | 0.673 | 95.9 | 0.92 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+opioid+vote | 1 | 147 | 0.673 | 95.9 | 0.92 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+vote | 0 | 147 | 0.662 | 96.1 | 0.92 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+vote | 1 | 147 | 0.662 | 96.1 | 0.92 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+opioid+vote | 0 | 145 | 0.672 | 97.4 | 0.91 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+opioid+vote | 1 | 145 | 0.672 | 97.4 | 0.91 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+opioid+initial+vote | 0 | 147 | 0.673 | 97.8 | 0.92 |
| sensitivity all-pivotal P(FDA final approval | vote) | priority+opioid+initial+vote | 1 | 147 | 0.673 | 97.8 | 0.92 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+opioid+CGT+CNS+cber+initial+vote | 0 | 145 | 0.674 | 105.0 | 0.93 |
| sensitivity all-pivotal P(FDA final approval | vote) | orphan+priority+opioid+CGT+CNS+cber+initial+vote | 1 | 145 | 0.674 | 105.0 | 0.93 |
| sensitivity 1-year approval | priority+opioid+CNS | 0 | 67 | 0.161 | 84.6 | 0.80 |
| sensitivity 1-year approval | priority+opioid+CNS | 1 | 67 | 0.161 | 84.6 | 0.86 |
| sensitivity 1-year approval | orphan+priority+opioid+CNS | 0 | 66 | 0.159 | 84.6 | 0.83 |
| sensitivity 1-year approval | orphan+priority+opioid+CNS | 1 | 66 | 0.159 | 84.6 | 0.89 |
| sensitivity 1-year approval | priority+opioid+CNS+cber | 0 | 67 | 0.170 | 86.1 | 0.76 |
| sensitivity 1-year approval | priority+opioid+CNS+cber | 1 | 67 | 0.170 | 86.1 | 0.83 |
| sensitivity 1-year approval | priority+opioid | 0 | 67 | 0.150 | 83.2 | 0.82 |
| sensitivity 1-year approval | priority+opioid | 1 | 67 | 0.150 | 83.2 | 0.82 |
| sensitivity 1-year approval | orphan+priority+opioid+CNS+cber+initial | 0 | 66 | 0.195 | 86.7 | 0.77 |
| sensitivity 1-year approval | orphan+priority+opioid+CNS+cber+initial | 1 | 66 | 0.195 | 86.7 | 0.85 |
| sensitivity 1-year approval | vote | priority+opioid+vote | 0 | 67 | 0.322 | 75.2 | 0.83 |
| sensitivity 1-year approval | vote | priority+opioid+vote | 1 | 67 | 0.322 | 75.2 | 0.83 |
| sensitivity 1-year approval | vote | priority+vote | 0 | 67 | 0.313 | 73.8 | 0.82 |
| sensitivity 1-year approval | vote | priority+vote | 1 | 67 | 0.313 | 73.8 | 0.82 |
| sensitivity 1-year approval | vote | priority+opioid+CNS+vote | 0 | 67 | 0.327 | 76.9 | 0.82 |
| sensitivity 1-year approval | vote | priority+opioid+CNS+vote | 1 | 67 | 0.327 | 76.9 | 0.86 |
| sensitivity 1-year approval | vote | priority+opioid+cber+vote | 0 | 67 | 0.338 | 76.2 | 0.77 |
| sensitivity 1-year approval | vote | priority+opioid+cber+vote | 1 | 67 | 0.338 | 76.2 | 0.77 |
| sensitivity 1-year approval | vote | priority+opioid+CNS+cber+initial+vote | 0 | 67 | 0.363 | 78.6 | 0.76 |
| sensitivity 1-year approval | vote | priority+opioid+CNS+cber+initial+vote | 1 | 67 | 0.363 | 78.6 | 0.82 |
| sensitivity year P(favourable) | orphan+priority+opioid+CNS+year | 0 | 112 | 0.289 | 126.8 | 0.77 |
| sensitivity year P(favourable) | orphan+priority+opioid+CNS+year | 1 | 112 | 0.289 | 126.8 | 0.88 |
| sensitivity year P(favourable) | priority+opioid+CNS+year | 0 | 113 | 0.261 | 128.1 | 0.72 |
| sensitivity year P(favourable) | priority+opioid+CNS+year | 1 | 113 | 0.261 | 128.1 | 0.84 |
| sensitivity year P(favourable) | orphan+priority+opioid+year | 0 | 112 | 0.257 | 127.9 | 0.78 |
| sensitivity year P(favourable) | orphan+priority+opioid+year | 1 | 112 | 0.257 | 127.9 | 0.78 |
| sensitivity year P(favourable) | orphan+priority+opioid+CNS+cber+year | 0 | 112 | 0.296 | 128.1 | 0.82 |
| sensitivity year P(favourable) | orphan+priority+opioid+CNS+cber+year | 1 | 112 | 0.296 | 128.1 | 0.91 |
| sensitivity year P(favourable) | orphan+priority+opioid+CNS+cber+initial+year | 0 | 112 | 0.296 | 130.1 | 0.82 |
| sensitivity year P(favourable) | orphan+priority+opioid+CNS+cber+initial+year | 1 | 112 | 0.296 | 130.1 | 0.91 |

Year term versus the same model without it (AIC; lower is better):

- P(favourable), orphan+priority+opioid+CNS: AIC 127.6 without year, 126.8 with year (Nagelkerke 0.289, stable=True).
- P(favourable), priority+opioid+CNS: AIC 128.6 without year, 128.1 with year (Nagelkerke 0.261, stable=True).
- P(favourable), orphan+priority+opioid: AIC 128.9 without year, 127.9 with year (Nagelkerke 0.257, stable=True).
- P(favourable), orphan+priority+opioid+CNS+cber: AIC 129.2 without year, 128.1 with year (Nagelkerke 0.296, stable=True).
- P(favourable), orphan+priority+opioid+CNS+cber+initial: AIC 131.2 without year, 130.1 with year (Nagelkerke 0.296, stable=True).
- P(FDA final approval), priority+opioid+CNS: AIC 128.1 without year, 129.7 with year (Nagelkerke 0.197, stable=True).
- P(FDA final approval), orphan+priority+opioid+CNS: AIC 128.6 without year, 130.1 with year (Nagelkerke 0.208, stable=True).
- P(FDA final approval), priority+opioid+CNS+cber: AIC 129.1 without year, 130.5 with year (Nagelkerke 0.210, stable=True).
- P(FDA final approval), priority+opioid: AIC 129.6 without year, 131.1 with year (Nagelkerke 0.160, stable=True).
- P(FDA final approval), orphan+priority+opioid+CNS+cber+initial: AIC 131.8 without year, 133.1 with year (Nagelkerke 0.219, stable=True).

Sources for the AMT-130 vector: orphan, OOPD 525216 in `oopd_all.csv`; priority review, uniQure releases of 2 Nov 2026 and 4 Nov 2026 (company, secondary) until an FDA letter is in hand.
