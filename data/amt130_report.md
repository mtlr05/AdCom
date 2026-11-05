# AMT-130: a historical prior from FDA advisory committee votes

4 November 2026

## Summary

uniQure's AMT-130 is a gene therapy for Huntington's disease. The company has said that the U.S. Food and Drug Administration (FDA) accepted its biologics license application for accelerated approval, granted priority review, and set a target decision date of 1 May 2027, and that an advisory committee meeting is planned and not yet dated. Those statements come from uniQure releases on 2 and 4 November 2026. They are company statements until an FDA letter is in hand. The orphan-drug designation is an FDA record: designation 525216, dated 27 September 2017, for an adeno-associated virus serotype 5 therapy that delivers a microRNA aimed at the huntingtin gene. Orphan designation is for a disease that affects fewer than 200,000 people in the United States.

The historical set is the 116 meetings from 4 November 2016 through 2026 at which a committee asked an approval or benefit-risk question and the final FDA action is known. A favourable vote means more yes votes than no votes. On these 116 meetings, 78 votes were favourable and 80 products were later approved. The rates are 0.67 and 0.69. The Jeffreys interval, a range from the counts alone, runs from 0.58 to 0.75 for the vote and from 0.60 to 0.77 for approval. Given a favourable vote, 72 of 78 products were approved. Given an unfavourable vote, 8 of 38 were approved. Of the 116 votes, 101 come from FDA minutes or transcripts and 15 from press reports. Of the 116 outcomes, 49 come from an FDA document, 34 from openFDA, the agency's public file of drug-application records, 27 from press reports, and 6 from a Securities and Exchange Commission filing or another company document.

Six facts known before the meeting were tested one at a time. A meeting was dropped only when that one fact was unrecorded. The test is Fisher's exact test on the two-by-two table of the factor against the outcome. The p-values are two-sided and are not adjusted for the six factors. Orphan status is the factor that comes in under 0.05 for both outcomes. An orphan product was favourable in 34 of 40 meetings, against 43 of 75 for the other products (p = 0.003), and was approved in 33 of 40, against 46 of 75 (p = 0.022). Cell and gene therapy is the next result: all 8 of those meetings were favourable, against 70 of 108 (p = 0.052), and all 8 were approved, against 72 of 108 (p = 0.056). Priority review, the biologics center, a neurology committee, and an initial application stay above 0.05 on this test. Priority review is the nearest of those four for the vote, at p = 0.064 on the 92 meetings with a recorded review type, and it has no association with approval (39 of 46 priority-review products were approved, and 41 of 46 standard-review products).

The combined model then puts orphan status and cell and gene therapy in together, on the 115 meetings with a settled orphan label. Every cell-and-gene-therapy meeting in this set is also an orphan product. The effect size is the penalized log-odds, the weight a logistic model gives the factor after a penalty pulls extreme weights back toward zero. Zero means no association. A positive weight means more of the outcome. Orphan status moves from 1.17 on its own to 1.06 in the combined model for the vote, and from 0.90 to 0.78 for approval. Cell and gene therapy moves from 1.15 to 0.79 for the vote, and from 1.11 to 0.85 for approval. Inside the 40 orphan meetings, the further split by cell and gene therapy has p = 0.32 for the vote (8 of 8 against 26 of 32) and p = 0.31 for approval (8 of 8 against 25 of 32). Orphan status among the other meetings stays under 0.05 for the vote (26 of 32 against 43 of 75, p = 0.026) and moves to p = 0.12 for approval (25 of 32 against 46 of 75).

The tests keep orphan status for the vote. They do not keep cell and gene therapy as a second factor. The two-factor fit is still reported, because that pair is AMT-130's profile and because the one-at-a-time result for cell and gene therapy sits on the 0.05 line. For a product with both labels the penalized fit gives 0.90 for a favourable vote and 0.89 for eventual approval. The bootstrap intervals, from 400 resamples of the meetings, run from 0.84 to 0.94 and from 0.83 to 0.93. The eight matching meetings were all favourable and all approved, and the interval computed from those eight alone runs from 0.74 to 1.00. The orphan-only fit, which is the fit the tests support, gives 0.82 (bootstrap 0.72 to 0.90) and 0.80 (0.68 to 0.89), from 34 of 40 and 33 of 40.

![Figure 1. Penalized log-odds for a favourable vote and for later FDA approval. A circle is the factor on its own, and the number beside the name is how many meetings record it. A square, drawn just below the circle, is the same factor inside the model that contains orphan status and cell and gene therapy, fit on the 115 meetings with a settled orphan label. The line is a bootstrap 95 percent interval. A positive value means more of the outcome. Priority review uses the 92 meetings with a recorded review type.](../charts/amt130_factor_compare.png)

After the vote is known, the association is much stronger than any pre-meeting label. A model that uses the vote and nothing else puts the chance of eventual approval at 0.89 after a favourable vote and at 0.29 after an unfavourable vote. The bootstrap intervals run from 0.82 to 0.93 and from 0.19 to 0.42.

## Introduction

An FDA advisory committee votes. The agency decides. The vote that matters here is the one that asks whether a specific product should be approved, or whether its benefits outweigh its risks. AMT-130 has not had that meeting. The date and the committee are unset. The practical question is what the last decade of similar meetings implies before the briefing book exists, and again after the vote exists. The answer is a base rate from past cases. It does not fold in the Huntington's data package.

This version of the calculation asks four questions in order. Which of the pre-meeting factors is associated with the vote, and with later approval? How large is that association when each factor is taken on every meeting that records it? What happens to the size and the test when orphan status and cell and gene therapy are put in one model? How does that combined result compare with the one-at-a-time result?

A missing record was not treated as a rejection, and it was not treated as evidence that a designation was absent. The meeting file, the factor log, and the model output sit beside this report.

## Method

### The meetings

Each row of the meeting table is one advisory committee meeting and one product, from 4 November 2016 through 2026, where the committee took a vote on approval of that product. The vote recorded is the pivotal vote: the last question at that meeting, for that product, that asks about approval, licensure, or whether benefits outweigh risks. The comparisons drop a meeting that was superseded by a later vote on the same product, a tie, and the Lynparza meeting that was favourable only inside a genetic subgroup. An outcome that is still pending or unverified is left out of the likelihood.

The main set is the approval or benefit-risk questions. A second pass, in the appendix, uses every pivotal vote, including questions that asked only about effectiveness. Before the models were fit, the analysis set was checked against the published four-cell counts. The cells matched. For the final action, which counts a later approval as approved, the approval-question cells are 72 favourable and approved, 6 favourable and not approved, 8 unfavourable and approved, and 30 unfavourable and not approved.

The final action is the latest known decision. A complete response letter followed by approval years later counts as approved. The one-year action asks whether the product was approved within 365 days of the meeting. That label is missing for 48 of the 116 approval questions. It is a sensitivity in the appendix, because it is an outcome rather than a fact known before the meeting, and because it was not filled in from a missing record.

### The six factors

Each factor is coded yes or no.

Orphan status means the product had an FDA orphan-drug designation for the indication reviewed at the meeting. One approval question, Darzalex Faspro for high-risk smoldering myeloma on 20 May 2025, is still marked "review" because the designation text does not settle that indication. Models that use orphan status leave it out. The other open orphan cell, Tudriqev, is an effectiveness question and is outside the main set.

Priority review means the FDA had granted priority review for the submission the committee reviewed, as against a standard review. Thirty-one cells in the whole table remain unverified. Twenty-four of them are in the main set of 116. A model that uses this factor drops those 24. A short clock, a fast-track grant, or the priority review of an earlier cycle was not treated as a designation for the submission under review.

Cell and gene therapy means the meeting was held by the Cellular, Tissue, and Gene Therapies Advisory Committee, or the product was one of four cell therapies reviewed at another committee: Kymriah, Ryoncil, Carvykti, and Abecma. This factor is recorded on every row.

The central nervous system factor means the meeting was held by the Peripheral and Central Nervous System Drugs Advisory Committee or by the Psychopharmacologic Drugs Advisory Committee. A neurologic disease reviewed by the gene-therapy committee is coded as not in this group. The factor is recorded on every row. AMT-130 is a treatment for a brain disease, and the committee that will review it has not been named. The two models in the results do not contain this factor, so the unset committee does not move their probabilities.

Center means the application sits at the Center for Biologics Evaluation and Research, as against the Center for Drug Evaluation and Research. Initial application means a first license or approval application, as against a supplement to a product already on the market. Both are recorded on every row. AMT-130 is an initial biologics license application at the biologics center, and it is a cell and gene therapy with orphan status and, on the company's account, priority review.

### One factor at a time, then the combined model

For each factor, the correlation and the test use every meeting that records that factor and has a known outcome. The correlation is the phi coefficient, the ordinary correlation between two yes-or-no columns. The test is Fisher's exact test. Where the unpenalized logistic fit stays finite, the appendix also gives the likelihood-ratio test against a model with no factors. That second test is on the same meetings. The two tests answer slightly different questions, and the results say so when they disagree.

The effect size is the coefficient from logistic regression with a penalty. The penalty matches a normal prior with standard deviation 2.5 on the intercept and standard deviation 1 on each factor. The same penalty is used for a factor on its own and for a factor inside a larger model, so the coefficients can be compared. The unpenalized coefficient is reported only when it stays below 8 in absolute value. Past that point the fit has separated: some combination of the factors lines up with a column of identical outcomes, and the unpenalized weight runs off.

The combined model contains orphan status and cell and gene therapy. That pair is the candidate suggested by the one-at-a-time screen, and it is the pair that matches AMT-130 among the factors that do not require a recorded review type. It is fit on the 115 meetings with a settled orphan label. Cell and gene therapy is complete, so adding it drops no further meeting.

All eight cell-and-gene-therapy meetings in this set were successes, so the unpenalized combined fit separates and a likelihood-ratio p-value for that model is not available. The incremental test is therefore Fisher's exact test in the rows where the other factor does not already decide the split. Cell and gene therapy occurs only among the orphan products, so its incremental test is the two-by-two table inside those 40 meetings. Orphan status does not vary inside the eight, so its incremental test is the two-by-two table among the other meetings. A wider model, with the remaining factors added, is in the appendix. It is penalized for the same reason.

Nagelkerke's R-squared summarizes how much of the yes-or-no outcome the factors pick up. Zero means they do no better than the overall rate. It is a pseudo R-squared, not the R-squared of a straight line. Models that drop different meetings are not ranked against each other by the Akaike information criterion, because that criterion is a sum over meetings and a smaller sample makes it smaller even when the fit is no better.

Two intervals are reported. The bootstrap resamples the meetings 400 times with a fixed seed, refits the penalized model, and takes the 2.5th and 97.5th percentiles. The stratum interval ignores the regression and uses only the meetings that match the factor pattern. With k successes in n meetings it is a Jeffreys interval. When n is under about eight, that interval is the description of the cell, and the logistic probability is borrowing strength from other meetings.

AMT-130 enters the orphan model as orphan yes, and the two-factor model as orphan yes and cell and gene therapy yes. The neurology-committee factor is absent from both.

## Results

### Which factors clear the test

The table gives each factor on its own meetings. "Yes" is the count when the factor is present. "No" is the count when it is absent. The log-odds is the penalized coefficient. The last column is the two-sided Fisher p-value.

| Factor | Meetings | Yes | No | Correlation | Log-odds | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Favourable vote | | | | | | |
| Orphan status | 115 | 34/40 | 43/75 | 0.28 | 1.17 | 0.003 |
| Cell and gene therapy | 116 | 8/8 | 70/108 | 0.19 | 1.14 | 0.052 |
| Priority review | 92 | 41/46 | 33/46 | 0.22 | 0.90 | 0.064 |
| Biologics center | 116 | 9/10 | 69/106 | 0.15 | 0.84 | 0.16 |
| Neurology committees | 116 | 8/10 | 70/106 | 0.08 | 0.45 | 0.49 |
| Initial application | 116 | 58/89 | 20/27 | -0.08 | -0.32 | 0.49 |
| Eventual approval | | | | | | |
| Orphan status | 115 | 33/40 | 46/75 | 0.22 | 0.90 | 0.022 |
| Cell and gene therapy | 116 | 8/8 | 72/108 | 0.18 | 1.10 | 0.056 |
| Priority review | 92 | 39/46 | 41/46 | -0.07 | -0.23 | 0.76 |
| Biologics center | 116 | 9/10 | 71/106 | 0.14 | 0.79 | 0.17 |
| Neurology committees | 116 | 8/10 | 72/106 | 0.07 | 0.39 | 0.72 |
| Initial application | 116 | 59/89 | 21/27 | -0.11 | -0.43 | 0.34 |

Orphan status is the clear result. Its likelihood-ratio p-values, from the unpenalized fit on the same 115 meetings, are 0.002 for the vote and 0.016 for approval. The R-squared is 0.11 for the vote and 0.07 for approval. That is a real association and a small share of the variation.

Cell and gene therapy is next, and its unpenalized fit does not stay finite, because the yes-group has no failures. The Fisher p-values are 0.052 and 0.056. The penalized log-odds are about the same size as orphan's. The correlation is smaller, 0.19 and 0.18, because the factor is present at only 8 meetings.

Priority review is the one place the two tests disagree. On the 92 meetings with a recorded review type, the Fisher p-value for the vote is 0.064 and the likelihood-ratio p-value is 0.033. The R-squared is 0.08. For approval the same factor has a correlation of -0.07, a log-odds of -0.23, and a Fisher p-value of 0.76. Standard review was followed by approval in 41 of 46 meetings, and priority review in 39 of 46. The Fisher test is the one applied to every factor. Priority review does not clear it, and it is left out of the combined model. Putting it in would also drop the 24 meetings with no recorded review type. Four of those 24 votes were favourable, and none of the 24 products was approved.

The biologics center, the neurology committees, and an initial application have Fisher p-values from 0.16 to 0.72. Their bootstrap intervals in Figure 1 cross zero. An initial application leans the other way: 58 of 89 initial applications had a favourable vote, against 20 of 27 supplements.

### The two factors together

On the 115 meetings, the penalized combined model gives the coefficients below. The one-at-a-time column for cell and gene therapy uses these same 115 meetings. Leaving out the one unsettled orphan row changes that coefficient from 1.14 to 1.15 for the vote and from 1.10 to 1.11 for approval.

| Factor | Vote, alone | Vote, combined | Approval, alone | Approval, combined |
| --- | ---: | ---: | ---: | ---: |
| Orphan status | 1.17 | 1.06 | 0.90 | 0.78 |
| Cell and gene therapy | 1.15 | 0.79 | 1.11 | 0.85 |

Orphan's vote coefficient barely moves, and the incremental test stays under 0.05 (p = 0.026). Orphan's approval coefficient moves from 0.90 to 0.78, and the incremental test moves from p = 0.022 to p = 0.12. The eight cell-and-gene-therapy approvals were part of the one-at-a-time approval result for orphan status. Set beside the other orphan products, that result is 25 of 32 against 46 of 75.

Cell and gene therapy's coefficient shrinks by about a third, and the incremental p-values are 0.32 and 0.31. The shrinkage has a simple source. All eight meetings are orphan products, and all eight sit at the biologics center. Counted on its own, cell and gene therapy is credited with eight favourable, approved meetings. Counted beside orphan status, those eight are already inside the orphan group, where 26 of the other 32 votes were also favourable and 25 of 32 products were also approved. The gap is 8 of 8 against about 26 of 32. It is too small for the test.

The unpenalized combined fit separates, so there is no likelihood-ratio p-value to set beside the one-at-a-time likelihood-ratio tests. Figure 1 shows the bootstrap intervals on the penalized coefficients. In the combined model the vote intervals run from 0.28 to 1.81 for orphan status and from 0.37 to 1.18 for cell and gene therapy. The approval intervals run from 0.04 to 1.61 and from 0.37 to 1.26.

### What the two fits give for AMT-130

The orphan model is the one the tests support. The two-factor model is the candidate that adds the next factor. Both set the included labels to yes. Neither uses priority review or the neurology committees.

| Model | Outcome | Probability | Bootstrap 95% | Matching meetings | Interval for that cell |
| --- | --- | ---: | --- | ---: | --- |
| Orphan status | Favourable vote | 0.82 | 0.72-0.90 | 34/40 | 0.72-0.93 |
| Orphan status | Eventual approval | 0.80 | 0.68-0.89 | 33/40 | 0.69-0.92 |
| Both factors | Favourable vote | 0.90 | 0.84-0.94 | 8/8 | 0.74-1.00 |
| Both factors | Eventual approval | 0.89 | 0.83-0.93 | 8/8 | 0.74-1.00 |

Adding cell and gene therapy raises the fitted probabilities by about 0.08 and 0.09. The matching cell shrinks from 40 meetings to 8, and the interval on those 8 runs from 0.74 to 1.00. The logistic interval is narrower because the penalty shares strength with the other orphan meetings. For a cell of eight with no failures, the wider interval is the one that describes the cell. All eight votes come from FDA minutes or transcripts. Four of the eight outcomes come from an FDA document or openFDA, and four from press reports. The meetings are listed in the appendix.

Once the vote is known, the pre-meeting labels add little. The vote-only model has an R-squared of 0.58. Eventual approval is 0.89 after a favourable vote (72 of 78; Jeffreys 0.85 to 0.97) and 0.29 after an unfavourable vote (8 of 38; Jeffreys 0.11 to 0.36). There is no unfavourable cell-and-gene-therapy vote in this set, so a two-factor model of approval given an unfavourable vote would be predicting into an empty cell. That fit is left in the appendix.

## Discussion

The one-at-a-time rule and the combined model answer different questions, and for orphan status they almost agree on the vote. The coefficient moves from 1.17 to 1.06, and the test stays under 0.05. For approval they agree less. The one-at-a-time p-value of 0.022 uses the eight cell-and-gene-therapy approvals as part of the orphan result. The combined comparison sets those eight aside, and the remaining orphan association, 25 of 32 against 46 of 75, has p = 0.12. A reader who wants one factor for both outcomes still has orphan status as the only factor under 0.05 on its own. A reader who wants the approval association to survive the combined model does not have that result.

Cell and gene therapy looks almost as large as orphan status when it is counted alone, and smaller once they are together. The same pattern appears for the biologics center, whose one-at-a-time vote coefficient is 0.84. In the appendix model that enters orphan status, cell and gene therapy, the biologics center, the neurology committees, and an initial application together, that coefficient falls to 0.34. Those labels describe the same handful of meetings. None of the eight was a meeting of either neurology committee.

Priority review is the factor that changes the sample. The 24 dropped meetings are mostly initial applications for common diseases that were voted down and not approved. The 92 that remain have a higher base rate: 74 favourable votes and 80 approvals, against 78 and 80 on all 116. Inside those 92, priority review separates the vote somewhat and does not separate approval. On the 91 meetings that record both orphan status and review type, a model with all six factors pulls the orphan vote coefficient down to 0.06. That is a change of sample, and it is why each one-at-a-time coefficient was computed before any meeting was dropped for a different factor's blank cell. The two-factor model does not make that drop.

The vote remains the strong association. An R-squared of 0.11 for orphan status, and 0.58 for the vote itself, is the scale of this table. The final action and the one-year action disagree on 13 of the 68 approval questions that have both labels. On those 68, 45 products were approved within a year, 42 of 53 after a favourable vote and 3 of 15 after an unfavourable vote. Most of the eight cell-and-gene-therapy meetings have no one-year label. The appendix refit uses two of them, one approved within a year and one not. That is a count of two, and it is not a rate for AMT-130.

Two readings of the wider set belong with these results. On every pivotal vote, not only the approval questions, orphan status still clears 0.05 for the vote (42 of 55 against 52 of 92, p = 0.021), and the biologics center does too (15 of 17, p = 0.032). Cell and gene therapy does not (10 of 11, p = 0.098). The single unfavourable cell-and-gene-therapy vote on that wider set is NurOwn. The incremental test of cell and gene therapy inside the orphan meetings is p = 0.42. The approval-question set remains the main result, because that is the question AMT-130's meeting would be asked.

The FDA calls an advisory committee when the decision is uncertain enough to want one. Products that are approved without a meeting do not appear. The 0.67 and 0.69 figures are rates among products that reached a vote. The orphan rates, 34 of 40 and 33 of 40, are rates inside that selected set. The table has no column for the strength of the clinical evidence, for an external control group, or for accelerated approval. Two products with the same orphan label can have very different evidence. Fifteen of the 116 votes and 33 of the 116 outcomes rest on press or company documents. The eight-meeting cell splits four and four on the outcome source. A press-sourced row is a real record with a weaker source.

Six factors were tested. The p-values above are not adjusted for that. Orphan's vote result, at 0.003, is the one that would still clear a strict adjustment. The approval result at 0.022, and every result near 0.05, would not.

## Conclusions

On the 116 approval or benefit-risk questions with a known final outcome, the chance of a favourable vote is 0.67 (78 of 116) and the chance of eventual approval is 0.69 (80 of 116). Given a favourable vote, 72 of 78 were approved. Given an unfavourable vote, 8 of 38 were approved. The vote-only model puts those conditional chances at 0.89 and 0.29.

Taken one at a time, on the meetings that record the factor, orphan status is the factor that clears a two-sided Fisher test at 0.05 for both outcomes: 34 of 40 against 43 of 75 for the vote (p = 0.003), and 33 of 40 against 46 of 75 for approval (p = 0.022). The penalized log-odds are 1.17 and 0.90. Cell and gene therapy is next, at 8 of 8, with p = 0.052 and p = 0.056. Priority review, the biologics center, a neurology committee, and an initial application do not clear 0.05. Priority review's likelihood-ratio p-value for the vote is 0.033 on the 92 meetings with a recorded review type, and its Fisher p-value is 0.064. Its approval association is a correlation of -0.07.

In the combined model the orphan vote coefficient is 1.06, beside 1.17 on its own, and the incremental test stays at p = 0.026. The orphan approval coefficient is 0.78, beside 0.90, and the incremental test is p = 0.12. Cell and gene therapy's coefficients fall from 1.15 to 0.79 and from 1.11 to 0.85, and the incremental tests inside the orphan meetings are p = 0.32 and p = 0.31. The second factor does not clear the test once orphan status is in the model.

The probabilities the tests support, for an orphan product, are 0.82 for a favourable vote and 0.80 for eventual approval, from 34 of 40 and 33 of 40. The two-factor probabilities, for a product that is also a cell and gene therapy, are 0.90 and 0.89. They rest on 8 of 8 meetings, and the interval on those eight runs from 0.74 to 1.00. Orphan status is taken from FDA designation 525216. Priority review is a company statement and is not a factor in these probabilities. The clinical evidence is outside this calculation.

## Suggested improvements

Thirty-one priority cells are still unverified, 24 of them in the main set. The page checked for each one is named in the factor log. A value should be entered only when a source names priority or standard review for the submission the committee reviewed.

The Darzalex Faspro cell for high-risk smoldering myeloma, and the Tudriqev cell, should be set to yes or no only if a source settles the indication. The absence of an orphan-drug row was not coded as "not orphan."

A sourced column for accelerated approval, for a resubmission as against a first cycle, and for an external control would address the largest hole in the factor list. Those columns would have to be built one row at a time, under the same rule: no inference from a missing record.

The one-year action is unverified on 48 of the 116 approval questions. It was left unverified on purpose. Press-only tallies that are still thin should be checked against minutes where a tally exists. The residual of about 19 meetings against the Daval count for 2016 to 2021 is a difference in published totals. That paper does not list the meetings, and closing the gap by adding rows would invent them.

## Appendix. One factor at a time, with the second test

The likelihood-ratio p-value is from the unpenalized logistic fit against a model with no factors, on the same meetings. It is blank where that fit separates. R-squared is Nagelkerke's, and for a separated fit it is computed from the penalized likelihood, so it is not on the same scale as the stable rows.

| Factor | Meetings | R-squared | Likelihood-ratio p | Stable |
| --- | ---: | ---: | ---: | --- |
| Favourable vote | | | | |
| Orphan status | 115 | 0.11 | 0.002 | Yes |
| Cell and gene therapy | 116 | 0.05 | | No |
| Priority review | 92 | 0.08 | 0.033 | Yes |
| Biologics center | 116 | 0.04 | 0.079 | Yes |
| Neurology committees | 116 | 0.01 | 0.35 | Yes |
| Initial application | 116 | 0.01 | 0.38 | Yes |
| Eventual approval | | | | |
| Orphan status | 115 | 0.07 | 0.016 | Yes |
| Cell and gene therapy | 116 | 0.05 | | No |
| Priority review | 92 | 0.01 | 0.54 | Yes |
| Biologics center | 116 | 0.03 | 0.099 | Yes |
| Neurology committees | 116 | 0.01 | 0.41 | Yes |
| Initial application | 116 | 0.02 | 0.25 | Yes |

The criterion is not used to rank these rows. Priority review's row has fewer meetings, and a criterion summed over fewer meetings is not comparable with a criterion summed over 116.

## Appendix. More than two factors

These coefficients are penalized. The unpenalized fit separates in both models, because the cell-and-gene-therapy cell has no failures. The five-factor model drops only the one orphan cell marked "review" (115 meetings). The six-factor model also drops every meeting with no recorded review type (91 meetings).

| Factor | Vote, five factors | Approval, five factors | Vote, six factors | Approval, six factors |
| --- | ---: | ---: | ---: | ---: |
| Orphan status | 1.09 | 0.82 | 0.06 | -0.29 |
| Cell and gene therapy | 0.68 | 0.73 | 0.56 | 0.52 |
| Priority review | | | 0.80 | -0.27 |
| Biologics center | 0.34 | 0.32 | 0.64 | 0.59 |
| Neurology committees | 0.63 | 0.56 | 0.66 | 0.66 |
| Initial application | -0.36 | -0.46 | 0.22 | 0.58 |

The biologics-center vote coefficient falls from 0.84 on its own to 0.34 beside orphan status and cell and gene therapy. On the 91-meeting sample the orphan vote coefficient falls to 0.06. The initial-application coefficient changes sign between the two samples. The 24 meetings that the six-factor model drops include 23 initial applications, 4 favourable votes, no approvals, 1 orphan product, and no cell or gene therapy.

## Appendix. Every pivotal vote

This pass adds effectiveness questions to the approval questions. The known-outcome count is 149. One further pivotal row is still pending. Orphan models use 147 meetings. The two-factor fit is stable on this wider set, because one cell-and-gene-therapy vote was unfavourable: NurOwn, on 27 September 2023, an effectiveness question, with the application later withdrawn.

| Factor | Meetings | Yes, favourable | No, favourable | Fisher p | Log-odds | Yes, approved | No, approved | Fisher p | Log-odds |
| --- | ---: | --- | --- | ---: | ---: | --- | --- | ---: | ---: |
| Orphan status | 147 | 42 of 55 | 52 of 92 | 0.021 | 0.80 | 42 of 55 | 56 of 92 | 0.071 | 0.64 |
| Cell and gene therapy | 149 | 10 of 11 | 86 of 138 | 0.098 | 0.98 | 10 of 11 | 90 of 138 | 0.10 | 0.91 |
| Priority review | 120 | 54 of 66 | 37 of 54 | 0.13 | 0.62 | 54 of 66 | 45 of 54 | 1.00 | -0.06 |
| Biologics center | 149 | 15 of 17 | 81 of 132 | 0.032 | 1.03 | 15 of 17 | 85 of 132 | 0.057 | 0.94 |
| Neurology committees | 149 | 12 of 20 | 84 of 129 | 0.80 | -0.17 | 13 of 20 | 87 of 129 | 0.80 | -0.08 |
| Initial application | 149 | 73 of 114 | 23 of 35 | 1.00 | -0.05 | 76 of 114 | 24 of 35 | 1.00 | -0.06 |

Inside the orphan meetings the cell-and-gene-therapy split is 9 of 10 against 33 of 45, and the Fisher p-value is 0.42 for both the vote and approval. Orphan status among the other meetings has p = 0.063 for the vote. The two-factor penalized probabilities for a product with both labels are 0.84 for a favourable vote (bootstrap 0.70 to 0.92) and 0.84 for approval (0.69 to 0.92). The matching cell is 9 of 10, and its own interval runs from 0.62 to 0.99.

On this wider set the biologics center clears 0.05 for the vote. That result is not in the main model. The main set is the approval question, which is the question at issue, and on that set the biologics center is 9 of 10 with p = 0.16.

## Appendix. Approval within one year

Sixty-eight of the 116 approval questions have a one-year label. Forty-five of the 68 were approved within a year. The final action and the one-year action disagree on 13 of these 68. The one-at-a-time tests are below. The p column is Fisher's exact test. None clears 0.05.

| Factor | Meetings | Yes | No | Correlation | Log-odds | p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Orphan status | 67 | 18/23 | 27/44 | 0.17 | 0.62 | 0.18 |
| Cell and gene therapy | 68 | 1/2 | 44/66 | -0.06 | -0.22 | 1.00 |
| Priority review | 61 | 23/28 | 22/33 | 0.18 | 0.62 | 0.24 |
| Biologics center | 68 | 1/2 | 44/66 | -0.06 | -0.22 | 1.00 |
| Neurology committees | 68 | 7/8 | 38/60 | 0.17 | 0.71 | 0.25 |
| Initial application | 68 | 43/62 | 2/6 | 0.22 | 0.85 | 0.17 |

The two meetings with both a cell-and-gene-therapy label and a one-year label are Zynteglo, approved within a year, and Lantidra, not approved within a year. The two-factor refit on the 67 meetings with a settled orphan label is stable. Its coefficients are 0.64 for orphan status and -0.37 for cell and gene therapy. The fitted probability for a product with both labels is 0.69, with a bootstrap interval from 0.44 to 0.89, and the matching cell is 1 of 2. The orphan-only probability on this outcome is 0.76 (bootstrap 0.61 to 0.87), from 18 of 23, with a cell interval from 0.59 to 0.91. A year term was not added. The one-year label is too thin, for this factor, to support one.

## Appendix. Approval given the vote

The model with the vote and no pre-meeting factor is stable, uses all 116 meetings, and has an R-squared of 0.58.

| Vote | Probability | Bootstrap 95% | Meetings | Interval for that cell |
| --- | ---: | --- | ---: | --- |
| Favourable | 0.89 | 0.82-0.93 | 72/78 | 0.85-0.97 |
| Unfavourable | 0.29 | 0.19-0.42 | 8/38 | 0.11-0.36 |

Adding orphan status and cell and gene therapy to that model separates the unpenalized fit. The penalized probability after a favourable vote is 0.93, and the matching cell is the same 8 of 8, with an interval from 0.74 to 1.00. After an unfavourable vote the matching cell is empty: no cell-and-gene-therapy approval question in this set was unfavourable. The penalized fit still produces a number, 0.46, and that number is an extrapolation. It is not a rate from a matching meeting.

## Appendix. The eight meetings

These are the approval or benefit-risk questions coded as cell and gene therapy with orphan status for the indication. All eight votes were favourable and all eight products were later approved. The vote source is FDA minutes or a transcript for every row.

| Date | Committee | Product | Application | Yes-no | Review type | Outcome source |
| --- | --- | --- | --- | --- | --- | --- |
| 12 Jul 2017 | ODAC | Kymriah | 125646 | 10-0 | Priority | FDA |
| 12 Oct 2017 | CTGTAC | Luxturna | 125610 | 16-0 | Priority | openFDA |
| 15 Apr 2021 | CTGTAC | Lantidra | 125734 | 12-4 | Standard | Press |
| 9 Jun 2022 | CTGTAC | Skysona | 125755 | 15-0 | Priority | openFDA |
| 10 Jun 2022 | CTGTAC | Zynteglo | 125717 | 13-0 | Priority | Press |
| 12 May 2023 | CTGTAC | Elevidys | 125781 | 8-6 | Priority | openFDA |
| 15 Mar 2024 | ODAC | Carvykti | 125746 | 11-0 | Standard | Press |
| 15 Mar 2024 | ODAC | Abecma | 125736 | 8-3 | Standard | Press |

ODAC is the Oncologic Drugs Advisory Committee. CTGTAC is the Cellular, Tissue, and Gene Therapies Advisory Committee. Carvykti and Abecma were reviewed as supplements, and the review type is the type named for those supplements. Three further cell-and-gene-therapy votes sit outside this list. Ryoncil, on 13 August 2020, was an effectiveness question and was later approved. NurOwn, on 27 September 2023, was an effectiveness question, the vote was unfavourable, and the application was withdrawn. Tudriqev, on 30 July 2026, was an effectiveness question, the vote was favourable, the product was approved, and the orphan cell remains "review." Deramiocel remains pending and is outside every count that requires a final action.

## Appendix. Where the meetings and the factor values come from

The meeting list began as FDA advisory committee notices in the Federal Register. Votes were taken from FDA minutes, voting results, and transcripts, with press and company filings used where the minutes could not be recovered. Approval dates and review type for drugs came from openFDA. Orphan status came from the FDA orphan-drug designation list. A published count of meetings from 2016 to 2021, Daval and colleagues in JAMA Health Forum in 2023, was used as a completeness check. That paper publishes committee-year totals, not a list of meetings. After the start date of this table, pharmacy-compounding meetings, and joint meetings filed under another committee, about 19 of those published counts remain unmatched. They were not filled by adding rows.

A calendar comparison for 4 November 2016 through 4 November 2026, and a search of current reports filed with the Securities and Exchange Commission, added one row. Solithromycin, for community-acquired bacterial pneumonia, was reviewed by the Antimicrobial Drugs Advisory Committee on 4 November 2016. The FDA transcript records the benefit-risk question as 7 yes and 6 no. The sponsor's annual report records a complete response letter on 29 December 2016 and states that the review was a priority review. The orphan-drug list has no row for solithromycin. The vote source is the FDA transcript. The outcome and the priority designation are from the company filing.

Priority review was filled only when a source named it for the submission the committee reviewed. The basis column records the page. Thirty-one cells stay unverified. The original priority review of a product was not copied onto a supplement or a resubmission. Two orphan cells stay marked "review," as the method describes.

The whole table has 156 rows. Votes come from FDA minutes or transcripts for 137 and from press reports for 19. Outcomes come from an FDA document or openFDA for 112, from press reports for 38, and from a company or Securities and Exchange Commission filing for 6.

## Appendix. Files

The meeting table is `adcom_full_pivotal.csv`, 156 rows. The published four-cell counts are `two_by_two.csv`. The factor lookups are `factor_verification.csv`. This report's screen is `amt130_one_at_a_time.csv` and `amt130_factor_compare.json`. The figure is `charts/amt130_factor_compare.png`. The fit is `scripts/amt130_factor_compare.py`, run from this folder. Corrections to the meeting table are made in `scripts/cur.py` and applied when the table is rebuilt. The table is not edited by hand.
