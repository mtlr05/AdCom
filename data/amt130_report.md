# AMT-130: a historical prior from FDA advisory committee votes

4 November 2026

## Summary

uniQure's AMT-130 is a gene therapy for Huntington's disease. The company has said that the U.S. Food and Drug Administration (FDA) accepted its biologics license application for accelerated approval, granted priority review, and set a target decision date of 1 May 2027, and that an advisory committee meeting is planned and not yet dated. Those statements come from uniQure releases on 2 and 4 November 2026. They are company statements until an FDA letter is in hand. The orphan-drug designation is an FDA record: designation 525216, dated 27 September 2017. Orphan designation is for a disease that affects fewer than 200,000 people in the United States. The wording of the committee's question is unset, so the rates below pool approval questions and effectiveness questions.

The meeting table holds 156 rows. The base count is 150, after dropping 4 ties, 1 meeting superseded by a later vote on the same product, and the Lynparza meeting that was favourable only inside a genetic subgroup. Of those 150, 116 asked about approval, licensure, or whether benefits outweigh risks, and 25 asked about effectiveness. Those 141 are the meetings in this calculation. Nine asked about a label, a delay, applicability to U.S. patients, or a surrogate marker. They are listed in the appendix and stay out of the rates. One of the 141, deramiocel on 29 July 2026, has no final action yet. It stays in the vote count and drops out of the approval count, which uses 140 meetings.

On the 141, 92 votes were favourable. The rate is 0.65, and the Jeffreys interval, a range from the counts alone, runs from 0.57 to 0.73. On the 140, 95 products were later approved. The rate is 0.68, and the interval runs from 0.60 to 0.75. A favourable vote means more yes votes than no votes. Given a favourable vote, 86 of 92 products were approved. Given an unfavourable vote, 9 of 48 were approved. Of the 141 votes, 125 come from FDA minutes or transcripts and 16 from press reports. Of the 140 outcomes, 57 come from an FDA document, 44 from openFDA, the agency's public file of drug-application records, 33 from press reports, and 6 from a Securities and Exchange Commission filing or another company document.

Six facts known before the meeting were tested one at a time, and an opioid column was added as a seventh. A meeting was dropped only when that one fact was unrecorded. The test is Fisher's exact test on the two-by-two table. The p-values are two-sided and are not adjusted for the seven factors. For the vote, two factors come in under 0.05. An orphan product was favourable in 40 of 51 meetings, against 50 of 88 (p = 0.011). An opioid was favourable in 5 of 15, against 87 of 126 (p = 0.009). Priority review was favourable in 57 of 68, against 31 of 48 with standard review (p = 0.027), on the 116 meetings with a recorded review type. Cell and gene therapy was favourable in 10 of 12, against 82 of 129 (p = 0.22). The biologics center, a neurology committee, and an initial application stay above 0.05.

For eventual approval, opioid is the factor that comes in under 0.05: 5 of 15 against 90 of 125 (p = 0.006). Orphan status is the next: 39 of 50 against 54 of 88 (p = 0.059). Priority review has no association with approval on the meetings where it is recorded (56 of 67 against 39 of 48, p = 0.81).

Filling the blank review types in as standard, and then as priority, does not give the same answer. On the vote, the blanks-as-standard comparison is 57 of 68 against 35 of 73 (p < 0.001), and the blanks-as-priority comparison is 61 of 93 against 31 of 48 (p = 1.00). On approval the first comparison is p = 0.0001 and the second reverses the direction (p = 0.021). Priority review is left out of the joint model. The joint model is orphan status and opioid. On the vote, the coefficients are 0.75 and -0.90, and each drop-one p-value is 0.04. AMT-130 is not an opioid, so that model is evaluated with opioid set to no. It gives 0.77 for a favourable vote and 0.77 for eventual approval, the same figures as orphan status alone, from cells of 40 of 51 and 39 of 50.

![Figure 1. Penalized log-odds for a favourable vote and for later FDA approval. A circle is the factor on its own, using every meeting that records it. A square is the same factor inside the model that contains orphan status and opioid, fit on the meetings that record both. Priority review is a circle only. The line is a bootstrap 95 percent interval. A positive value means more of the outcome. The vote panel uses 141 meetings. The approval panel uses 140. Orphan status is missing for 2 of them. Priority review is missing for 25.](../charts/amt130_factor_compare.png)

For an orphan product that is not an opioid, the penalized fit gives 0.77 for a favourable vote and 0.77 for eventual approval. The bootstrap intervals run from 0.65 to 0.87 and from 0.66 to 0.87. The matching cells are 40 of 51 and 39 of 50, and the intervals on those cells run from 0.66 to 0.88 and from 0.65 to 0.88. None of the orphan products in those cells is an opioid. A three-factor model adds cell and gene therapy and reads AMT-130 as an orphan gene therapy that is not an opioid. It gives 0.80 and 0.84, on cells of 9 of 11 and 9 of 10. After the vote is known, a model with the vote alone puts eventual approval at 0.90 after a favourable vote and at 0.26 after an unfavourable vote.

## Introduction

An FDA advisory committee votes. The agency decides. AMT-130 has not had that meeting. The date, the committee, and the wording of the question are unset. A question about effectiveness is a plausible pivotal question, and so is a question about approval or benefit against risk. The calculation uses both. The answer is a base rate from past cases. It does not fold in the Huntington's data package.

The order is the same as before. Which factors are associated with the vote, and with later approval, when each factor keeps every meeting that records it? What happens to the size and the test when the factors that clear the screen are put in one model? The meeting file and the model output sit beside this report.

## Method

Each row is one advisory committee meeting and one product, from 4 November 2016 through 2026, where the committee took a vote on that product. The vote recorded is the pivotal vote. The base count of 150 drops a superseded meeting, a tie, and the Lynparza subgroup vote. An outcome that is still pending is left out of the approval likelihood and kept in the vote count. Deramiocel is that pending row. Its effectiveness vote was 3 yes and 9 no.

The nine meetings left out of the 141 asked a narrower question: a dose in the label, whether to wait for another trial, whether a foreign trial applies to U.S. patients, or whether a surrogate marker is reasonably likely to predict benefit. Those are real meetings. They are a different question from whether the product works or should be approved. The final action counts a later approval as approved. The one-year action, approval within 365 days, is a sensitivity in the appendix.

Seven factors are coded yes or no. Orphan status means an FDA orphan designation for the indication reviewed. Two cells stay marked "review" and drop out of models that use this factor: Darzalex Faspro for high-risk smoldering myeloma, and Tudriqev. Priority review means the original application's designation. A supplement or a later cycle takes that original designation when a source names it, and stays blank when no source names the original cycle. A blank drops out of models that use this factor and stays in models that do not. Opioid means an active moiety is an opioid agonist. Every row is yes or no. The fifteen opioid meetings inside the 141 are the ones that are not a tie. Cell and gene therapy means the Cellular, Tissue, and Gene Therapies Advisory Committee, or Kymriah, Ryoncil, Carvykti, or Abecma. The neurology factor means the Peripheral and Central Nervous System Drugs Advisory Committee or the Psychopharmacologic Drugs Advisory Committee. Center means the Center for Biologics Evaluation and Research. Initial application means a first license, as against a supplement. AMT-130 is an initial biologics application at the biologics center, a cell and gene therapy, with orphan status and, on the company's account, priority review. It is not an opioid. The committee is unset. The models below that omit the neurology factor do not move when that assignment is made.

The correlation is the phi coefficient, the ordinary correlation between two yes-or-no columns. The one-at-a-time test is Fisher's exact test. Where the unpenalized logistic fit stays finite, the appendix also gives the likelihood-ratio p-value. The effect size throughout is the penalized coefficient. The penalty matches a normal prior with standard deviation 2.5 on the intercept and standard deviation 1 on each factor. The same penalty is used alone and in a combined model.

The joint model is every factor that clears 0.05 for the vote, after a sensitivity on priority review. That sensitivity fills the blank review types once as standard and once as priority. Priority review enters the joint model only when those two fills agree and the recorded-review sample does not remove another factor's association. They do not agree, so the joint model is orphan status and opioid. Orphan status plus cell and gene therapy is reported beside it. On this set the unpenalized fit of that pair stays finite, because two cell-and-gene-therapy votes were unfavourable.

The bootstrap resamples the meetings 400 times with a fixed seed. The stratum interval is a Jeffreys interval on the meetings that match the factor pattern. When that cell is small, its interval is the description of the cell.

## Results

### One factor at a time

"Yes" is the count when the factor is present. "No" is the count when it is absent. The last column is the Fisher p-value.

| Factor | Meetings | Yes | No | Correlation | Log-odds | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Favourable vote | | | | | | |
| Opioid | 141 | 5/15 | 87/126 | -0.23 | -1.13 | 0.009 |
| Orphan status | 139 | 40/51 | 50/88 | 0.22 | 0.88 | 0.011 |
| Priority review | 116 | 57/68 | 31/48 | 0.22 | 0.88 | 0.027 |
| Biologics center | 141 | 15/18 | 77/123 | 0.15 | 0.78 | 0.11 |
| Cell and gene therapy | 141 | 10/12 | 82/129 | 0.12 | 0.67 | 0.22 |
| Initial application | 141 | 71/110 | 21/31 | -0.03 | -0.11 | 0.83 |
| Neurology committees | 141 | 11/19 | 81/122 | -0.06 | -0.29 | 0.61 |
| Eventual approval | | | | | | |
| Opioid | 140 | 5/15 | 90/125 | -0.26 | -1.23 | 0.006 |
| Biologics center | 140 | 15/17 | 80/123 | 0.16 | 0.92 | 0.093 |
| Cell and gene therapy | 140 | 10/11 | 85/129 | 0.14 | 0.89 | 0.10 |
| Orphan status | 138 | 39/50 | 54/88 | 0.17 | 0.69 | 0.059 |
| Priority review | 115 | 56/67 | 39/48 | 0.03 | 0.15 | 0.81 |
| Initial application | 140 | 73/109 | 22/31 | -0.04 | -0.14 | 0.83 |
| Neurology committees | 140 | 12/19 | 83/121 | -0.04 | -0.19 | 0.61 |

Opioid and orphan status clear 0.05 for the vote. Opioid also clears it for approval. The fifteen opioid meetings are the opioid rows that are not a tie. Five of them were favourable, and five were later approved. Those are not the same five: one favourable vote was followed by a complete response, and one unfavourable vote was followed by approval. Priority review's 116 leave out 25 votes with no recorded review type. On the 140 with a final action, those 25 include 4 favourable votes, no approvals, and 8 opioids. The R-squared is 0.07 for opioid on the vote and 0.08 on approval, and 0.07 for orphan status and for priority review on the vote. Cell and gene therapy's vote interval in Figure 1 crosses zero. The two unfavourable votes in that group are NurOwn, 1 yes and 17 no, with the application later withdrawn, and deramiocel, 3 yes and 9 no, still pending. Both were effectiveness questions.

For approval, the Fisher test and the likelihood-ratio test disagree at two rows that the Fisher test does not carry forward. Orphan status has Fisher p = 0.059 and likelihood-ratio p = 0.041. The biologics center has Fisher p = 0.093 and likelihood-ratio p = 0.038. Opioid's likelihood-ratio p-value on approval is 0.004. Priority review's approval coefficient on the recorded meetings is 0.15.

### Why priority review is not in the joint model

The recorded-review comparison for the vote is 57 of 68 against 31 of 48 (p = 0.027, log-odds 0.88). Coding every blank as standard review gives 57 of 68 against 35 of 73 (p < 0.001, log-odds 1.49). Coding every blank as priority review gives 61 of 93 against 31 of 48 (p = 1.00, log-odds 0.05). For approval the same two fills are p = 0.0001 (log-odds 1.29) and p = 0.021 (log-odds -0.85). The second fill reverses the direction. The 25 meetings with a final action and no recorded review type had no approvals, so coding them as standard review puts those failures in the standard arm. The result is not identified. Restricting to the recorded-review meetings also removes the vote associations for orphan status and for opioid. Priority review stays out of the joint model.

### Orphan status and opioid together

This is the pair the vote screen produced, on the meetings that record orphan status. The fit uses 139 vote meetings and 138 approval meetings. On those meetings, before the factors are combined, orphan status is 40 of 51 against 50 of 88 (p = 0.011, log-odds 0.88) and opioid is 5 of 15 against 85 of 124 for the vote (p = 0.010, log-odds -1.11).

| Factor | Vote, alone | Vote, combined | Approval, alone | Approval, combined |
| --- | ---: | ---: | ---: | ---: |
| Orphan status | 0.88 | 0.75 | 0.69 | 0.53 |
| Opioid | -1.11 | -0.90 | -1.21 | -1.06 |

The vote drop-one p-values are 0.045 for orphan status and 0.044 for opioid. The criterion is 177.5 for orphan status alone and 175.5 with opioid, so the second factor earns its place on the vote. The joint bootstrap intervals run from 0.08 to 1.52 and from -1.69 to -0.13. For approval, opioid's drop-one p-value is 0.016 and orphan's is 0.18. The approval bootstrap interval for orphan status crosses zero. Figure 1 shows the squares on these two factors.

### Orphan status, opioid, and cell and gene therapy

This is the two-factor model with cell and gene therapy added. It uses the same 139 vote meetings and 138 approval meetings, because opioid and cell and gene therapy are filled on every row and the only rows dropped are the two orphan cells marked "review." Tudriqev is one of those two, and it is a cell and gene therapy, so the class count inside this fit is 9 of 11 for the vote and 9 of 10 for approval. The one-at-a-time count of 10 of 12 keeps Tudriqev. On these meetings, before the factors are combined, the vote log-odds are 0.88 for orphan status, -1.11 for opioid, and 0.61 for cell and gene therapy (9 of 11 against 81 of 128, p = 0.33).

| Factor | Vote, alone | Vote, combined | Approval, alone | Approval, combined |
| --- | ---: | ---: | ---: | ---: |
| Orphan status | 0.88 | 0.71 | 0.69 | 0.45 |
| Opioid | -1.11 | -0.89 | -1.21 | -1.06 |
| Cell and gene therapy | 0.61 | 0.21 | 0.83 | 0.57 |

The vote drop-one p-values are 0.081 for orphan status, 0.044 for opioid, and 0.75 for cell and gene therapy. The criterion is 175.5 for orphan status and opioid, and 177.4 with the third factor, so the third factor does not earn its place on the vote. The bootstrap intervals are 0.02 to 1.50, -1.68 to -0.12, and -0.66 to 1.09. For approval the drop-one p-values are 0.38, 0.016, and 0.27, and the criterion moves from 170.2 to 171.0. The approval bootstrap intervals are -0.22 to 1.21, -1.87 to -0.27, and -0.34 to 1.26. The cell-and-gene-therapy interval crosses zero on both outcomes. Among orphan products, the class is 9 of 11 against 31 of 40 for the vote (p = 1.00) and 9 of 10 against 30 of 40 for approval (p = 0.42).

### Orphan status and cell and gene therapy together

This pair leaves opioid out. On the 139 vote meetings the coefficients are 0.84 for orphan status and 0.22 for cell and gene therapy. The drop-one p-values are 0.021 and 0.75. The criterion is 177.5 for orphan status alone and 179.4 with the second factor. On the 138 approval meetings the coefficients are 0.61 and 0.58, and the drop-one p-values are 0.13 and 0.27.

### What the fits give for AMT-130

| Model | Outcome | Probability | Bootstrap 95% | Matching meetings | Interval for that cell |
| --- | --- | ---: | --- | ---: | --- |
| Orphan status | Favourable vote | 0.77 | 0.65-0.87 | 40/51 | 0.66-0.88 |
| Orphan status | Eventual approval | 0.77 | 0.66-0.86 | 39/50 | 0.65-0.88 |
| Orphan, not an opioid | Favourable vote | 0.77 | 0.65-0.87 | 40/51 | 0.66-0.88 |
| Orphan, not an opioid | Eventual approval | 0.77 | 0.66-0.87 | 39/50 | 0.65-0.88 |
| Orphan, not an opioid, cell and gene therapy | Favourable vote | 0.80 | 0.62-0.92 | 9/11 | 0.53-0.96 |
| Orphan, not an opioid, cell and gene therapy | Eventual approval | 0.84 | 0.69-0.92 | 9/10 | 0.62-0.99 |
| Orphan and cell and gene therapy | Favourable vote | 0.80 | 0.62-0.91 | 9/11 | 0.53-0.96 |
| Orphan and cell and gene therapy | Eventual approval | 0.84 | 0.69-0.92 | 9/10 | 0.62-0.99 |

AMT-130 is not an opioid. The two-factor model is read at opioid set to no, and the probability sits on the orphan-only figure because none of the orphan products in that cell is an opioid. The three-factor model sets cell and gene therapy to yes as well. The probability moves to 0.80 and 0.84. The matching cells are 9 of 11 and 9 of 10, the same cells as orphan status plus cell and gene therapy with opioid left out. NurOwn is the approval failure. Deramiocel is the extra unfavourable vote, and it has no final action. Tudriqev is the cell-and-gene-therapy meeting left out of both cells because its orphan label is still "review." All ten completed cell-and-gene-therapy votes in the orphan cell come from FDA minutes or transcripts. Two of the ten outcomes come from an FDA document, four from openFDA, and four from press reports.

Once the vote is known, the pre-meeting labels add little. The vote-only model has an R-squared of 0.64. Eventual approval is 0.90 after a favourable vote and 0.26 after an unfavourable vote. The bootstrap intervals run from 0.85 to 0.94 and from 0.17 to 0.36.

## Discussion

Adding the 25 effectiveness questions changes the cell-and-gene-therapy count from a run of favourable votes to 10 of 12. NurOwn and deramiocel are the two unfavourable votes, and both were effectiveness questions. That is why a model fit on approval questions only made the class look separate from everything else, and why the same factor has a Fisher p-value of 0.22 once those questions are included. Ryoncil, also an effectiveness question, was favourable and was approved in 2024 after a complete response in 2020. Tudriqev was favourable and approved, and it stays out of the orphan models because the designation text does not settle the indication.

Opioid is the new association, and it runs against approval. Five of fifteen opioid meetings were favourable, and five of fifteen were approved. The products are oxycodone, hydrocodone, buprenorphine, tramadol, sufentanil, oliceridine, and oxycodegol, including buprenorphine for opioid use disorder and for depression. The column is filled for every meeting, so the estimate does not depend on dropping a blank.

Priority review still clears 0.05 for the vote on the 116 meetings with a recorded original designation. That association does not survive the sensitivity. The 25 meetings with no recorded review type and a final action had 4 favourable votes and no approvals, and 8 of them are opioids. Calling those blanks standard review assigns the failures to standard review and makes priority look stronger. Calling them priority review removes the vote association and reverses the approval association. The flag is also now the original application's designation, including where the committee reviewed a supplement or a resubmission. Twenty-seven cells in the whole table remain unverified, 25 of them inside the 141.

The biologics center is the other near result for approval, at Fisher p = 0.093. In a model with orphan status, opioid, cell and gene therapy, the biologics center, the neurology committees, and an initial application, the opioid vote coefficient is -0.86 and the biologics-center coefficient is 0.50. The cell-and-gene-therapy vote coefficient is -0.08. The neurology committees lean slightly the other way on this wider set (11 of 19 favourable). No cell-and-gene-therapy meeting in the table was held by either of those committees.

The vote remains the strong association. An R-squared of about 0.10 for orphan status and opioid together, and 0.64 for the vote itself, is the scale of this table. The final action and the one-year action disagree on 14 of the 81 meetings that have both labels. On those 81, 54 products were approved within a year. The one-year screen does not clear 0.05 for any factor. The FDA calls a committee when the decision is uncertain enough to want one. The 0.65 and 0.68 figures are rates among products that reached a vote. The table has no column for the strength of the evidence, for an external control, or for accelerated approval. Sixteen of the 141 votes and 39 of the 140 outcomes rest on press or company documents.

## Conclusions

Of 150 pivotal meetings, 141 asked an approval, benefit-risk, or effectiveness question. The chance of a favourable vote on those 141 is 0.65 (92 of 141). The chance of eventual approval on the 140 with a final action is 0.68 (95 of 140). Given a favourable vote, 86 of 92 were approved. Given an unfavourable vote, 9 of 48 were approved. The vote-only model puts those conditional chances at 0.90 and 0.26.

Taken one at a time, opioid and orphan status clear a Fisher test at 0.05 for the vote: 5 of 15 against 87 of 126 (p = 0.009), and 40 of 51 against 50 of 88 (p = 0.011). Priority review is 57 of 68 against 31 of 48 (p = 0.027) on the 116 meetings with a recorded original designation. Cell and gene therapy is 10 of 12 (p = 0.22). For approval, opioid clears the Fisher test, 5 of 15 against 90 of 125 (p = 0.006). Orphan status is 39 of 50 against 54 of 88 (p = 0.059). Priority review is 56 of 67 against 39 of 48 (p = 0.81).

The sensitivity on the blank review types does not agree with itself, so priority review is not in the joint model. In the model with orphan status and opioid, the vote coefficients are 0.75 and -0.90, and both drop-one p-values are 0.04. AMT-130 is not an opioid. That model, read at opioid set to no, gives 0.77 and 0.77, from cells of 40 of 51 and 39 of 50. Adding cell and gene therapy moves those coefficients to 0.71, -0.89, and 0.21. The third factor's drop-one p-value is 0.75, and the criterion rises from 175.5 to 177.4. Read as an orphan gene therapy that is not an opioid, the three-factor model gives 0.80 and 0.84, from cells of 9 of 11 and 9 of 10.

Orphan status is taken from FDA designation 525216. Priority review is a company statement, and it is not a term in the model used for the probability. The clinical evidence is outside this calculation. Nine meetings with a narrower question are outside the 141.

## Suggested improvements

Review type is still unverified for 25 of the 141 votes. The flag is the original application's review type, and a value should be entered only when a source names priority or standard review for that original application. The page checked for each remaining blank is named in the factor log.

Darzalex Faspro for high-risk smoldering myeloma, and Tudriqev, should be set to yes or no only if a source settles the indication. Deramiocel's final action is open until the agency decides. The one-year label is thin on this set and was left unverified where no source dated the action.

A sourced column for accelerated approval, for a resubmission, and for an external control would address the largest hole in the factor list. The residual of about 19 meetings against the Daval count for 2016 to 2021 is a difference in published totals. That paper does not list the meetings.

## Appendix. The second test

The likelihood-ratio p-value is from the unpenalized logistic fit on the same meetings. R-squared is Nagelkerke's.

| Factor | Meetings | R-squared | Likelihood-ratio p |
| --- | ---: | ---: | ---: |
| Favourable vote | | | |
| Opioid | 141 | 0.07 | 0.008 |
| Orphan status | 139 | 0.07 | 0.009 |
| Priority review | 116 | 0.07 | 0.018 |
| Biologics center | 141 | 0.03 | 0.069 |
| Cell and gene therapy | 141 | 0.02 | 0.15 |
| Neurology committees | 141 | 0.00 | 0.47 |
| Initial application | 141 | 0.00 | 0.74 |
| Eventual approval | | | |
| Opioid | 140 | 0.08 | 0.004 |
| Orphan status | 138 | 0.04 | 0.041 |
| Biologics center | 140 | 0.04 | 0.038 |
| Cell and gene therapy | 140 | 0.04 | 0.060 |
| Priority review | 115 | 0.00 | 0.75 |
| Neurology committees | 140 | 0.00 | 0.64 |
| Initial application | 140 | 0.00 | 0.67 |

These rows are not ranked against each other by a criterion. Priority review's row sums fewer meetings.

## Appendix. More than two factors

The model without priority review drops the two orphan cells marked "review." The unpenalized fit is stable. The model with priority review also drops every blank review type. Its unpenalized fit separates, and those coefficients are the penalized ones.

| Factor | Vote, without priority | Approval, without priority | Vote, all seven | Approval, all seven |
| --- | ---: | ---: | ---: | ---: |
| Orphan status | 0.69 | 0.43 | -0.16 | -0.49 |
| Opioid | -0.86 | -1.02 | -0.57 | -0.51 |
| Cell and gene therapy | -0.08 | 0.27 | 0.08 | 0.54 |
| Priority review | | | 0.90 | 0.21 |
| Biologics center | 0.50 | 0.58 | 0.62 | 0.84 |
| Neurology committees | -0.10 | 0.00 | -0.52 | -0.59 |
| Initial application | -0.05 | -0.03 | 0.39 | 0.77 |

On the recorded-review sample the orphan vote coefficient is about zero and the priority coefficient stays near 0.9. That sample is the one the sensitivity rejected. A year term, added to the orphan-and-opioid model and evaluated as a line centered at 2020, moves the criterion from 172.3 to 171.5 for the vote and from 170.2 to 171.4 for approval. It is not added.

## Appendix. Approval within one year

Eighty-one of the 140 meetings with a final action also have a one-year label. Fifty-four of the 81 were approved within a year. The two labels disagree 14 times. No one-at-a-time Fisher test clears 0.05. The p column is that test.

| Factor | Meetings | Yes | No | Correlation | Log-odds | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Orphan status | 79 | 22/30 | 31/49 | 0.10 | 0.38 | 0.46 |
| Priority review | 74 | 30/37 | 24/37 | 0.18 | 0.66 | 0.19 |
| Initial application | 81 | 52/75 | 2/6 | 0.20 | 0.85 | 0.092 |
| Neurology committees | 81 | 10/13 | 44/68 | 0.10 | 0.41 | 0.53 |
| Opioid | 81 | 3/6 | 51/75 | -0.10 | -0.43 | 0.39 |
| Cell and gene therapy | 81 | 2/4 | 52/77 | -0.08 | -0.35 | 0.60 |
| Biologics center | 81 | 2/4 | 52/77 | -0.08 | -0.35 | 0.60 |

The orphan-only probability on this outcome is 0.72 (bootstrap 0.57 to 0.85), from 22 of 30. The orphan-and-opioid probability, with opioid set to no, is the same 0.72, from the same 22 of 30.

## Appendix. Approval given the vote

The model with the vote and no pre-meeting factor is stable, uses the 140 meetings with a final action, and has an R-squared of 0.64.

| Vote | Probability | Bootstrap 95% | Meetings | Interval for that cell |
| --- | ---: | --- | ---: | --- |
| Favourable | 0.90 | 0.85-0.94 | 86/92 | 0.87-0.97 |
| Unfavourable | 0.26 | 0.17-0.36 | 9/48 | 0.10-0.31 |

Adding orphan status and opioid leaves the favourable-vote probability at 0.90. The matching cell among orphan products that are not opioids is 38 of 40. The unfavourable cell in that group is 1 of 10. Adding cell and gene therapy puts the favourable-vote probability at 0.93, on a cell of 9 of 9, and the unfavourable probability at 0.35. That unfavourable cell is one meeting, NurOwn, which was not approved.

## Appendix. Cell and gene therapy meetings

These rows are in the 141. Tudriqev is in the vote and approval counts and drops out of any model that uses orphan status. Deramiocel is in the vote count only.

| Date | Committee | Product | Question | Yes-no | Vote | Final action | Orphan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 12 Jul 2017 | ODAC | Kymriah | Approval | 10-0 | Favourable | Approved | Yes |
| 12 Oct 2017 | CTGTAC | Luxturna | Approval | 16-0 | Favourable | Approved | Yes |
| 13 Aug 2020 | ODAC | Ryoncil | Effectiveness | 8-2 | Favourable | Approved in 2024 | Yes |
| 15 Apr 2021 | CTGTAC | Lantidra | Approval | 12-4 | Favourable | Approved | Yes |
| 9 Jun 2022 | CTGTAC | Skysona | Approval | 15-0 | Favourable | Approved | Yes |
| 10 Jun 2022 | CTGTAC | Zynteglo | Approval | 13-0 | Favourable | Approved | Yes |
| 12 May 2023 | CTGTAC | Elevidys | Approval | 8-6 | Favourable | Approved | Yes |
| 27 Sep 2023 | CTGTAC | NurOwn | Effectiveness | 1-17 | Unfavourable | Withdrawn | Yes |
| 15 Mar 2024 | ODAC | Carvykti | Approval | 11-0 | Favourable | Approved | Yes |
| 15 Mar 2024 | ODAC | Abecma | Approval | 8-3 | Favourable | Approved | Yes |
| 29 Jul 2026 | CTGTAC | Deramiocel | Effectiveness | 3-9 | Unfavourable | Pending | Yes |
| 30 Jul 2026 | CTGTAC | Tudriqev | Effectiveness | 10-3 | Favourable | Approved | Review |

ODAC is the Oncologic Drugs Advisory Committee. CTGTAC is the Cellular, Tissue, and Gene Therapies Advisory Committee. The ten completed orphan rows were favourable in 9 and approved in 9. NurOwn is the failure in both columns.

## Appendix. The nine meetings left out

Each pivotal question was about a label, a delay, applicability, or a surrogate, so the meeting is outside the 141.

| Date | Product | What the question asked |
| --- | --- | --- |
| 8 Mar 2018 | Xeljanz | Whether a 10 mg maintenance dose belonged in the label |
| 7 Aug 2018 | Arikayce | Coded restriction/other; the stored text is the agenda |
| 26 Feb 2019 | Xpovio | Whether approval should wait for a randomized trial |
| 9 Feb 2021 | Keytruda | Whether the decision should be deferred for more data |
| 24 Jun 2021 | Retifanlimab | Coded restriction/other |
| 10 Feb 2022 | Sintilimab | Whether another trial in U.S. patients should be required first |
| 22 Mar 2023 | Qalsody | Whether a reduction in a blood marker was reasonably likely to predict benefit |
| 5 Oct 2023 | Lumakras | Whether progression-free survival could support the application |
| 20 May 2025 | Columvi | Whether a foreign trial's population applied to U.S. patients |

Qalsody is a treatment for a neurologic disease, reviewed by a neurology committee. Its question was about a surrogate marker. It is part of the nine, and it is not in the 0.65 and 0.68 rates.

## Appendix. Where the meetings come from

The meeting list began as FDA advisory committee notices in the Federal Register. Votes were taken from FDA minutes, voting results, and transcripts, with press and company filings where the minutes could not be recovered. A published count of meetings from 2016 to 2021, Daval and colleagues in JAMA Health Forum in 2023, was the completeness check. That paper publishes committee-year totals. About 19 of those counts remain unmatched after the start date of this table, pharmacy-compounding meetings, and joint meetings filed under another committee. One row was added from that search: solithromycin, on 4 November 2016, a benefit-risk vote of 7 yes and 6 no.

The whole table has 156 rows. Votes come from FDA minutes or transcripts for 137 and from press reports for 19. Outcomes come from an FDA document or openFDA for 112, from press reports for 38, and from a company filing for 6.

## Appendix. Files

The meeting table is `adcom_full_pivotal.csv`. The four-cell counts are `two_by_two.csv`. The factor lookups are `factor_verification.csv`. This screen is `amt130_one_at_a_time.csv` and `amt130_factor_compare.json`. The figure is `charts/amt130_factor_compare.png`. The fit is `scripts/amt130_factor_compare.py`, run from this folder. Corrections to the meeting table are made in `scripts/cur.py` and applied when the table is rebuilt.
