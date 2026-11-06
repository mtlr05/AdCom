# Four-factor model: predicted probability and the rate in that cell

The model is the penalized logistic regression on orphan status, priority review, opioid, and cell and gene therapy. **Predicted** is that model's probability for the pattern. **Observed, fit** is the share of meetings with the outcome among the meetings used to estimate the model. Compare those two columns. **In the fit** is that count. **Observed** counts every meeting with the same pattern and a recorded outcome. That count includes restriction questions, ties, and a meeting a later one replaced.

A favourable vote is the committee's pivotal vote, coded 1 or 0. Approval means `final_action` begins with "approved." A pending or unverified action is left out. The vote model uses 136 meetings. The approval model uses 135, because deramiocel has no final action.

## Favourable vote

| Predicted | Pattern | All meetings | Observed | In the fit | Observed, fit |
| --- | --- | ---: | ---: | ---: | ---: |
| 84.1% | Orphan, priority, cell/gene therapy | 8/9 | 88.9% | 8/9 | 88.9% |
| 82.3% | Orphan, priority | 25/35 | 71.4% | 23/29 | 79.3% |
| 75.9% | Priority | 23/30 | 76.7% | 22/28 | 78.6% |
| 65.4% | Orphan, standard, cell/gene therapy | 1/2 | 50.0% | 1/2 | 50.0% |
| 62.5% | Orphan, standard | 8/11 | 72.7% | 8/11 | 72.7% |
| 57.2% | Priority, opioid | 3/4 | 75.0% | 3/4 | 75.0% |
| 53.0% | Standard | 23/44 | 52.3% | 22/42 | 52.4% |
| 32.4% | Standard, opioid | 2/11 | 18.2% | 2/11 | 18.2% |

## Approval

| Predicted | Pattern | All meetings | Observed | In the fit | Observed, fit |
| --- | --- | ---: | ---: | ---: | ---: |
| 87.1% | Orphan, priority, cell/gene therapy | 8/8 | 100.0% | 8/8 | 100.0% |
| 80.1% | Orphan, priority | 26/35 | 74.3% | 22/29 | 75.9% |
| 78.0% | Priority | 25/32 | 78.1% | 22/28 | 78.6% |
| 75.7% | Orphan, standard, cell/gene therapy | 1/2 | 50.0% | 1/2 | 50.0% |
| 65.1% | Orphan, standard | 8/11 | 72.7% | 8/11 | 72.7% |
| 62.2% | Standard | 29/46 | 63.0% | 27/42 | 64.3% |
| 54.4% | Priority, opioid | 3/4 | 75.0% | 3/4 | 75.0% |
| 35.6% | Standard, opioid | 3/12 | 25.0% | 2/11 | 18.2% |
