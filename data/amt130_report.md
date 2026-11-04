# AMT-130: a historical prior from FDA advisory committee votes

4 November 2026

## Summary

uniQure's AMT-130 is a gene therapy for Huntington's disease. The company has said that the U.S. Food and Drug Administration (FDA) accepted its biologics license application for accelerated approval, granted priority review, and set a target decision date of 1 May 2027, and that an advisory committee meeting is planned and not yet dated. Those statements come from uniQure releases on 2 and 4 November 2026. They are company statements until an FDA letter is in hand. The product's orphan-drug designation is an FDA record: designation 525216, dated 27 September 2017, for an adeno-associated virus serotype 5 therapy that delivers a microRNA aimed at the huntingtin gene.

This report uses earlier product-approval votes as a historical prior for two questions. How often has a committee voted in favour of a product with labels like these? How often has the FDA later approved it? The table holds 156 meetings from 4 November 2016 through July 2026 at which a committee voted on approval of a specific product.

On the 116 meetings that asked an approval or benefit-risk question and have a known final outcome, 78 votes were favourable and 80 products were later approved. The rates are 0.67 and 0.69. They count every such meeting. They do not drop a meeting whose review type is unverified, and they do not require priority review. Given a favourable vote, 72 of 78 products were approved. Given an unfavourable vote, 8 of 38 were approved. The Jeffreys interval for the favourable-vote rate runs from 0.58 to 0.75, and the interval for the approval rate runs from 0.60 to 0.77.

Models that set priority review to yes are fit on the 92 of these meetings that have a recorded review type. They return probabilities of about 0.87 to 0.89 for a favourable vote and 0.84 to 0.87 for eventual approval, when the meeting is not held by either of the two neurology committees defined in the method. On those same 92 meetings, priority review does not improve a model of approval. The criterion moves from 73.2 to 74.9, and the R-squared is 0.01. Standard review was followed by approval in 41 of 46 meetings, and priority review in 39 of 46. The higher approval figure is the rate in the subset with a recorded review type.

The labels explain little of who is approved. The strongest association in the table is between the committee's vote and the FDA's later action. Priority review has a modest association with a favourable vote: on the 92 meetings with a recorded review type, 41 of 46 priority-review products were favourable, against 33 of 46 with standard review, and the R-squared is 0.08. The table has no column for the strength of the clinical evidence, for the use of an external control group, or for accelerated approval. A high historical rate is the rate among products the FDA has already chosen to bring to a committee.

## Introduction

An FDA advisory committee is a panel of outside experts. The panel votes. The agency decides. For a new drug or biologic, the vote that matters in this project is the one that asks whether the product should be approved, or whether its benefits outweigh its risks. A favourable vote means more yes votes than no votes. Abstentions are recorded and are not counted as yes votes.

AMT-130 has not had that meeting. The date and the committee are unset. The practical question is what the last decade of similar meetings implies before the briefing book exists, and again after the vote exists. The answer is a prior, in the ordinary sense of a base rate from past cases. It is not a forecast that folds in the Huntington's data package.

The work had three parts. The first was a search for product-approval votes that the table had missed. The second was a lookup of every model factor that was still blank, unverified, or ambiguous. The third was a comparison of every combination of those factors, followed by a prediction from the few combinations that fit best. A value was changed only when a public source supported the change. A missing record was not treated as a rejection, and it was not treated as evidence that a designation was absent.

The meeting file, the search log, the factor log, and the model output sit beside this report. This document is the explanation of what was done and what the numbers mean.

## Method

### The meeting table

Each row is one advisory committee meeting and one product, from 4 November 2016 through 2026, where the committee took a vote on approval of that product. The vote recorded is the pivotal vote: the last question at that meeting, for that product, that asks about approval, licensure, or whether benefits outweigh risks. Questions about what to do before approval, about labeling, about a risk program, or about a dose are not used as the pivotal vote. If no approval question was asked, the table uses the first effectiveness question, and the row is flagged so that choice is visible.

The FDA's later action is recorded in two ways. The final action is the latest known decision, so an application that received a complete response letter and was approved years later counts as approved. A complete response letter is the FDA's letter saying the application is not approved in its current form. The one-year action asks whether the product was approved within 365 days of the meeting. Withdrawn and pending applications are not counted as approved. Pending and unverified outcomes are left out of the vote-by-outcome counts and are counted separately.

The comparisons that follow drop four kinds of rows. A meeting that was superseded by a later vote on the same product is dropped. A tie is dropped. One meeting on Lynparza, coded as favourable only inside a genetic subgroup, is dropped because it is not a plain yes or no. An outcome that is still pending or unverified is left out of the likelihood and is counted.

Before any model was fit, the analysis set was checked against the published four-cell counts of vote by outcome. The cells matched. Those counts, for the final action, are the ones below. Each column is one combination of the committee vote and the FDA's later action.

| Group | Favourable, approved | Favourable, not approved | Unfavourable, approved | Unfavourable, not approved | Meetings in the count | Left out as unverified or pending |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| All pivotal votes | 90 | 6 | 10 | 43 | 150 | 1 |
| Approval or benefit-risk questions only | 72 | 6 | 8 | 30 | 116 | 0 |
| Rare disease, orphan designation for the indication | 40 | 2 | 2 | 11 | 55 | 1 |
| Rare disease and priority review | 29 | 1 | 1 | 8 | 39 | 0 |
| Cell and gene therapy | 10 | 0 | 0 | 1 | 11 | 1 |

Votes in the full table of 156 rows come from FDA minutes or transcripts for 137 rows and from press reports for 19. Outcomes come from an FDA document or openFDA, the agency's public file of drug-application records, for 112 rows, from press reports for 38, and from a Securities and Exchange Commission filing or another company document for 6. Press-sourced rows are real records with a weaker source. They are not described here as FDA-verified.

### Data sources

The meeting list began as FDA advisory committee notices in the Federal Register. Votes were taken from FDA minutes, voting results, and transcripts, with press and company filings used only where the minutes could not be recovered. Approval dates and review type for drugs came from openFDA. Orphan status came from the FDA orphan-drug designation list kept by the Office of Orphan Products Development. A published count of meetings from 2016 to 2021, Daval and colleagues in JAMA Health Forum in 2023, was used as a completeness check. That paper publishes committee-year totals, not a list of meetings.

Two further searches were run for this report, because a second pass through the Federal Register would have repeated the original build.

The first search read FDA advisory committee calendars and the past-meeting pages of the human-drug and biologics committees, including archived pages, from 4 November 2016 through 4 November 2026. Each date and committee was compared with the meeting table, with the list of meetings seen and set aside, and with the list of meetings that still lacked a usable vote. That last list is empty. Extra attention went to the cellular and gene-therapy committee, the two neurology committees, joint meetings, and the years 2022 through 2026, which the Daval count does not cover.

The second search was the Securities and Exchange Commission's full-text filing system, EDGAR, for current reports that mention an advisory committee vote and a tally. A filing by itself was not enough to add a row. A row was added only when a public source gave the date, the committee, the product or application number, the wording of the pivotal question, and a yes and no tally, with a link.

The calendar comparison produced 271 dated items. Of those, 129 were already in the meeting table and 91 were already on the exclusion list. The rest were joint meetings already stored under the lead committee, a second day of a meeting already stored, pharmacy-compounding meetings, class or policy discussions, or pages that named no application and no tally. One product meeting was set aside on purpose: sulopenem, on 9 September 2024, had an application number, and the FDA minutes show that the committee was not asked to vote.

One row qualified and was added. Solithromycin, for community-acquired bacterial pneumonia, was reviewed by the Antimicrobial Drugs Advisory Committee on 4 November 2016 under new drug application 209006. The same vote covered the intravenous application 209007. The FDA transcript records the benefit-risk question as 7 yes and 6 no. The sponsor's annual report to the Securities and Exchange Commission records a complete response letter on 29 December 2016 and states that the review was a priority review because the product was a qualified infectious disease product. The orphan-drug list has no row for solithromycin. The indication is a common infection, so orphan status is no. The vote source is the FDA transcript. The outcome and the priority designation are from the company filing.

Daval and colleagues counted 164 meetings for 2016 to 2021. After the start date of this table, pharmacy-compounding meetings, and joint meetings filed under another committee, about 19 of those published counts remain unmatched. Daval does not list the meetings, so those 19 cannot be identified one by one. They were not filled by adding rows. The model does not wait on them.

### Factors that were still open

Every cell that the model might use, and that was unverified, ambiguous, or blank, was looked up. A cell was changed only when the source named the designation for the submission the committee actually reviewed. The priority attached to an original application was not copied onto a supplement or a resubmission. A decision date was not used to infer priority review, because a short clock is not the same statement as a priority designation.

Six priority values were filled.

| Product | Meeting | Application | New value | Source |
| --- | --- | --- | --- | --- |
| Ryoncil | 13 Aug 2020 | 125706 | Priority | FDA review memo. The memo says the application was filed as a priority review on 30 March 2020, and that is the application the committee reviewed. |
| Quizartinib | 14 May 2019 | 212166 | Priority | Daiichi Sankyo release, 21 November 2018. Press. |
| Omburtamab | 28 Oct 2022 | 761176 | Priority | Y-mAbs release, 31 May 2022. Press. |
| Omecamtiv mecarbil | 13 Dec 2022 | 216401 | Standard | A secondary write-up of Cytokinetics' 4 February 2022 acceptance notice. |
| Midomafetamine | 4 Jun 2024 | 215455 | Priority | Lykos release. Press. |
| Darzalex Faspro, high-risk smoldering myeloma | 20 May 2025 | 761145, supplement 029 | Standard | openFDA tags that supplement as standard. FDA minutes identify the supplement the committee reviewed. |

A second pass, on 4 November 2026, read the acceptance notice, the FDA briefing or review memo, or the company filing for every remaining unverified priority cell. Fourteen values were filled. Eight come from an FDA document: Rebyota standard, Abrysvo for adults 60 and older priority, Arexvy priority, Abrysvo in pregnancy priority, the Carvykti and Abecma 2024 supplements standard, mFLUSIVA priority, and intravenous tramadol standard. Two come from a Securities and Exchange Commission filing: Bayer's ciprofloxacin dry powder priority, stated in Aradigm's quarterly report, and bardoxolone standard. Four come from a company release: Translarna standard, Linhaliq priority, retifanlimab priority, and carbetocin priority. Each sentence names the submission the committee reviewed. The Carvykti and Abecma values are the supplements on the 15 March 2024 agenda, not the original licenses.

Thirty-one priority cells stay unverified. The acceptance notice for those products gives an action date, or names fast track, and does not say priority or standard review. A short clock was not treated as a designation. The original priority review of Columvi, deramiocel, and Tudriqev was not copied onto the supplement or the resubmission the committee reviewed. NurOwn's briefing does not name a review type. The 17 September 2021 Comirnaty booster row has no application number, and no source names a review type for that booster. The basis column records the page that was checked.

The four newly coded priority reviews that are also orphan for the indication are Bayer's ciprofloxacin powder, Linhaliq, retifanlimab, and carbetocin. All four votes were unfavourable, and none of those applications was approved. They are why the rare-disease-and-priority row above is 29, 1, 1 and 8, on 39 meetings, where it had been 29, 1, 1 and 4, on 35. Thirty of the 39 were approved. On the approval-question subset the same two ciprofloxacin products move the count from 22, 1, 0 and 2, on 25 meetings, to 22, 1, 0 and 4, on 27. Twenty-two of the 27 were approved.

Two orphan cells stay marked for review, which means the designation text does not settle the indication the committee discussed. Darzalex Faspro on 20 May 2025 was reviewed for high-risk smoldering multiple myeloma. The orphan designation on file is for multiple myeloma, and it does not name the smoldering indication. Tudriqev, on 30 July 2026, has no orphan-drug row under that name, under vusolimogene oderparepvec, or under RP1. The absence of a row was not coded as "not orphan." Both cells stay "review," and any model that uses orphan status leaves them out.

Meeting type needed no change. Every row is already an initial application or a supplement. The ambiguous Lemtrada meeting that had been flagged in earlier work falls outside this window.

### What the model uses

Six facts are known before the meeting, or are fixed by the kind of meeting. Each is coded yes or no.

Orphan status means the product had an FDA orphan-drug designation for the indication reviewed at the meeting. Orphan designation is for a disease that affects fewer than 200,000 people in the United States. Rows still marked "review" drop out of models that use this factor, and they stay in models that do not.

Priority review means the FDA had granted priority review for the submission the committee reviewed, as against a standard review. Rows still unverified drop out of models that use this factor, and they stay in models that do not.

Cell and gene therapy means the meeting was held by the Cellular, Tissue, and Gene Therapies Advisory Committee, or the product was one of four cell therapies reviewed at another committee: Kymriah, Ryoncil, Carvykti, and Abecma. Rebyota, a fecal microbiota product, is not in this group.

The central nervous system factor means the meeting was held by the Peripheral and Central Nervous System Drugs Advisory Committee or by the Psychopharmacologic Drugs Advisory Committee. A neurologic disease reviewed by another committee, including a gene-therapy committee, is coded as not in this group. AMT-130 is a treatment for a brain disease, and the committee that will review it has not been named, so every model that contains this factor is reported twice.

Center means the application sits at the Center for Biologics Evaluation and Research, as against the Center for Drug Evaluation and Research. AMT-130 is a biologic and is coded at the biologics center.

Initial application means a first license or approval application, as against a supplement to a product already on the market. AMT-130 is an initial biologics license application.

The wording of the vote is used as a filter, not as a seventh yes-or-no factor. The main results use only questions about approval, licensure, or benefit against risk. A second pass uses every pivotal vote, including questions that asked only about effectiveness.

The committee vote itself is used only in the second stage, when the outcome is FDA approval. Favourable means yes votes exceed no votes.

Calendar year was not part of the full grid. It was added, as a straight line centered on 2020, only to the models the grid had already kept, and it was evaluated at 2026. The year 2026 is inside the years the table already contains.

### How the models were fit

Every subset of the six factors was fit twice: once for a favourable vote, and once for eventual FDA approval. A third screen added the vote as a factor in the approval model. With six yes-or-no factors there are 64 subsets in each screen, including the model with no factors.

The fit is logistic regression. The probability of a yes outcome is a smooth S-shaped function of a weighted sum of the factors. The weights were estimated with a penalty that pulls them toward zero. The penalty matches a normal prior with standard deviation 2.5 on the intercept and standard deviation 1 on each factor. The same model was also fit with no penalty. If that unpenalized fit failed to converge, or if any weight exceeded 8 in absolute value, the fit was marked as separated. A separated fit can look precise while the data in a small cell are all successes or all failures. Separated fits are reported in the screen and are not used as a probability.

Fit is summarized by Nagelkerke's R-squared. This is a pseudo R-squared for a yes-or-no outcome. Zero means the factors do no better than a single overall rate. One would mean a perfect fit. It is not the R-squared of a straight line through a cloud of points. McFadden's R-squared, a simpler ratio of log likelihoods, is stored beside it in the output file. Models are ranked by the Akaike information criterion, which charges a model for each extra factor. A factor that does not improve the fit enough raises the criterion, and the smaller model is preferred. The criterion is computed from the unpenalized fit when that fit is stable.

For each outcome the screen records the four stable models with the best criterion, plus the single stable model with the highest R-squared if the criterion had not already kept it. That is a cap of about five models per outcome. The ranking mixes models fit on different meetings. A model that includes priority review drops every meeting whose review type is unverified, and the criterion, being a sum of meeting-level terms, is then smaller partly because fewer meetings enter the sum. The results therefore start from the rates on the full approval-question set. The models the criterion kept are reported after that. Priority review is also compared with a model that has no factors on the same meetings, which puts the two fits on one scale.

Two intervals are reported, and they answer different questions. The bootstrap interval resamples the meetings 400 times, refits the penalized model, and takes the 2.5th and 97.5th percentiles of the predicted probability. The seed is fixed, so the interval can be rebuilt. The stratum interval ignores the regression and looks only at the meetings that match AMT-130 on the factors in that model. With k successes in n such meetings, the interval is a Jeffreys interval, which is the 2.5th and 97.5th percentiles of a beta distribution with parameters 0.5 plus k and 0.5 plus n minus k. When n is under about eight, that interval is the honest description, and the logistic probability is borrowing strength from meetings that match on only some of the labels.

The main probabilities use the final action, so a later approval counts. The same kept factor sets were refit on the one-year action as a sensitivity. The all-pivotal-vote screen is a second sensitivity. Neither sensitivity is folded into the headline range.

AMT-130 enters every model as orphan yes, priority review, cell and gene therapy, biologics center, and initial application. The neurology-committee factor is set to no and to yes whenever the model contains it.

## Results

The validity check passed: the meetings used in the model reproduce the published vote-by-outcome counts. The main set is the 116 approval or benefit-risk questions that have a final outcome. Of those votes, 101 come from FDA minutes or transcripts and 15 from press reports. Of those outcomes, 83 come from an FDA document or openFDA, 27 from press reports, and 6 from a company or Securities and Exchange Commission filing. Thirty-one priority cells in the whole table remain unverified. Of the 116 meetings in the main set, 24 have no verified review type, so a model that uses priority review is fit on the other 92. The two orphan cells still marked "review" drop out of models that use orphan status. Among the 68 approval-question meetings that have both a final action and a one-year action, the two labels disagree 13 times.

### Base rates

The rates below use all 116 meetings. A meeting stays in the count when its review type is unverified. Priority review is not set to yes.

| Outcome | Meetings | Events | Rate | Jeffreys 95% |
| --- | ---: | ---: | ---: | --- |
| Favourable vote | 116 | 78 | 0.67 | 0.58 to 0.75 |
| Eventual approval | 116 | 80 | 0.69 | 0.60 to 0.77 |
| Approval, given a favourable vote | 78 | 72 | 0.92 | 0.85 to 0.97 |
| Approval, given an unfavourable vote | 38 | 8 | 0.21 | 0.11 to 0.36 |

The penalized logistic intercept matches these rates at two decimals: 0.67 for a favourable vote and 0.69 for eventual approval. The bootstrap intervals run from 0.59 to 0.75 and from 0.61 to 0.77.

Among stable models that do not use priority review, the criterion prefers orphan status alone. An orphan product, which is AMT-130's designation, has a fitted chance of 0.82 of a favourable vote and 0.80 of eventual approval. Those fits use 115 meetings. One orphan cell still marked "review" is left out. The matching cells are 34 favourable votes out of 40, and 33 approvals out of 40.

| Outcome | Meetings | R-squared | Probability | Bootstrap 95% | Matching meetings (successes) | Interval for that cell |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| Favourable vote | 115 | 0.11 | 0.82 | 0.72 to 0.90 | 40 (34) | 0.85 (0.72 to 0.94) |
| Eventual approval | 115 | 0.07 | 0.80 | 0.68 to 0.89 | 40 (33) | 0.82 (0.69 to 0.92) |

The 24 meetings with no verified review type account for much of the gap between these rates and the higher figures below. Four of the 24 votes were favourable, and none of the 24 products was later approved. The 92 meetings with a recorded review type include 74 favourable votes and 80 approvals.

### Chance of a favourable vote, with priority review set to yes

The screen ranked by the criterion keeps four models that include priority review, and one model without it that has the highest R-squared. Adding orphan status or an initial application raises R-squared by a small amount and does not improve the criterion by enough to displace priority review alone. The highest R-squared is 0.15, from orphan status, the neurology-committee factor, the biologics center, and an initial application, fit on 115 meetings. That is a small share of the variation in the vote. Its matching cell is six meetings, all favourable.

The criterion on the priority rows sums 92 meetings, and the criterion for the full set sums 116, so the two numbers answer different samples. On the same 92 meetings, a model with no factors has a criterion of 93.0, and the priority-review model has a criterion of 90.4. Priority review does improve that comparison. The R-squared is 0.08. Forty-one of 46 priority-review meetings were favourable, against 33 of 46 standard-review meetings.

| Factors | Meetings | R-squared | Probability | Bootstrap 95% | Matching meetings (favourable) | Interval for that cell |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| Priority | 92 | 0.08 | 0.87 | 0.79 to 0.94 | 46 (41) | 0.89 (0.78 to 0.96) |
| Orphan, priority | 91 | 0.08 | 0.88 | 0.77 to 0.96 | 27 (23) | 0.85 (0.69 to 0.95) |
| Priority, initial application | 92 | 0.08 | 0.88 | 0.80 to 0.94 | 35 (32) | 0.91 (0.79 to 0.98) |
| Orphan, priority, initial application | 91 | 0.09 | 0.89 | 0.78 to 0.96 | 22 (19) | 0.86 (0.68 to 0.96) |
| Orphan, neurology committee, biologics center, initial application | 115 | 0.15 | 0.87 | 0.76 to 0.94 | 6 (6) | 0.96 (0.67 to 1.00) |

The first four probabilities run from 0.87 to 0.89. They are the chance for a product with priority review, inside the 92 meetings that have a recorded review type. They are a different quantity from the 0.67 rate on all 116 meetings. The last row does not set priority review. Its matching cell is six meetings, and the interval on that cell runs from 0.67 to 1.00. The logistic interval is narrower because the model borrows strength from the larger pattern. For a cell this small, the wider interval is the one that describes the cell itself.

The four priority models do not contain the neurology-committee factor, so those probabilities are the same if the meeting is later assigned to one of those two committees. The last model does contain it. Switching that factor on moves its probability from 0.87 to 0.93, and the matching cell is empty.

### Chance of FDA approval, before the vote is known

On all 116 meetings the approval rate is 0.69, from the base-rate table. The screen keeps four models that include priority review and one, with the highest R-squared, that does not. On the 92 meetings with a recorded review type, a model with no factors has a criterion of 73.2. Adding priority review raises the criterion to 74.9, so the factor does not earn its place. The R-squared is 0.01. Eighty of those 92 products were approved. Standard review accounts for 41 of 46, and priority review for 39 of 46. The predicted probability of 0.85 for a priority-review product is the rate in this subset. The highest R-squared among the kept models is 0.11.

| Factors | Meetings | R-squared | Probability | Bootstrap 95% | Matching meetings (approved) | Interval for that cell |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| Priority | 92 | 0.01 | 0.85 | 0.76 to 0.93 | 46 (39) | 0.85 (0.72 to 0.93) |
| Priority, initial application | 92 | 0.03 | 0.87 | 0.78 to 0.95 | 35 (31) | 0.88 (0.75 to 0.96) |
| Orphan, priority | 91 | 0.01 | 0.84 | 0.72 to 0.93 | 27 (22) | 0.81 (0.64 to 0.93) |
| Orphan, priority, initial application | 91 | 0.04 | 0.86 | 0.75 to 0.94 | 22 (19) | 0.86 (0.68 to 0.96) |
| Orphan, neurology committee, biologics center, initial application | 115 | 0.11 | 0.85 | 0.73 to 0.93 | 6 (6) | 0.96 (0.67 to 1.00) |

Across the four priority models the probability of eventual approval runs from 0.84 to 0.87. That range sits with 80 approvals out of 92 meetings that have a recorded review type. The six-meeting cell in the last row is all approvals, and its own interval runs from 0.67 to 1.00. The four priority models do not contain the neurology-committee factor. The last model does, and switching it on leaves no matching meeting.

### Chance of FDA approval, after the vote is known

Every model this screen kept leaves priority review out. The raw counts are in the base-rate table: 72 approvals out of 78 favourable votes, and 8 approvals out of 38 unfavourable votes. Adding the vote raises R-squared to about 0.59. The criterion prefers a model that uses the vote and little else. The penalized fits put the chance of eventual approval at 0.88 to 0.92 after a favourable vote, and at 0.28 to 0.37 after an unfavourable vote. The first row, which uses the vote alone, shrinks the raw rates of 0.92 and 0.21 toward one half, to 0.89 and 0.29.

| Factors besides the vote | R-squared | If the vote is favourable | If the vote is unfavourable | Marginal probability | Bootstrap 95%, favourable case | Matching meetings if favourable (approved) |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| None | 0.58 | 0.89 | 0.29 | 0.69 | 0.82 to 0.93 | 78 (72) |
| Initial application | 0.59 | 0.88 | 0.28 | 0.67 | 0.81 to 0.93 | 58 (53) |
| Biologics center | 0.59 | 0.92 | 0.37 | 0.82 | 0.87 to 0.95 | 9 (9) |
| Orphan | 0.58 | 0.90 | 0.34 | 0.80 | 0.82 to 0.95 | 34 (32) |
| Neurology committee, biologics center, initial application | 0.59 | 0.91 | 0.35 | 0.79 | 0.85 to 0.95 | 7 (7) |

The marginal probability multiplies the model's own chance of a favourable vote by the chance of approval given a favourable vote, and adds the matching term for an unfavourable vote. It runs from 0.67 to 0.82. The low end comes from the first two rows, whose paired model of the vote does not include priority review or cell and gene therapy. That end is the historical base rate of a favourable vote, applied to AMT-130's approval equation. It is not the probability from AMT-130's full set of labels. The high end is the biologics-center model, whose matching cell is 9 approvals out of 9.

If the neurology-committee factor in the last row is switched on, the favourable-vote probability moves from 0.91 to 0.92 and the matching cell is empty. No meeting in the table was both a cell or gene therapy at the biologics center and a meeting of either neurology committee. That probability is an extrapolation.

![Figure 1. The top two points are the unfiltered rates on all 116 meetings: a favourable vote, and eventual approval. Each later priority row sets priority review to yes and is fit on the 92 meetings with a recorded review type. The rows that include the vote leave priority review out. Each point is the penalized logistic probability. The line is the bootstrap 95 percent interval. The neurology-committee factor is off.](../charts/amt130_prediction_forest.png)

## Discussion

The rate on all 116 approval questions is 0.67 for a favourable vote and 0.69 for eventual approval. The figures near 0.87 come from models that set priority review to yes. Those models are fit on the 92 meetings with a recorded review type, and 80 of those 92 were later approved. Within those 92, priority review does not improve the approval model: the criterion rises from 73.2 to 74.9, and the R-squared is 0.01. Standard review was followed by approval in 41 of 46 meetings, and priority review in 39 of 46. The high approval rate is the rate among meetings whose review type was recorded. The 24 meetings with no verified review type include 4 favourable votes and no later approvals, and leaving them out lifts the average.

The vote is the factor that separates outcomes. An unfavourable vote is associated with a chance of eventual approval near one in three in the kept models. A favourable vote is associated with a chance near nine in ten. That gap is visible in the four-cell counts. Of 116 approval questions with a known final action, 72 were favourable and later approved, 6 were favourable and not approved, 8 were unfavourable and later approved, and 30 were unfavourable and not approved.

Two readings of "approved" diverge, and the divergence matters for a decision date. The final action counts a later approval. Ryoncil is the clearest example in this table: the committee voted in 2020, the FDA issued a complete response, and the product was approved in 2024. The final action is approved. The one-year action is not approved. Across the approval-question rows that have both labels, they disagree 13 times out of 68. On the 68 meetings with a one-year label, 45 were approved within a year, 42 of 53 after a favourable vote and 3 of 15 after an unfavourable vote. Refitting the priority-conditioned approval models on that one-year action gives a range of 0.80 to 0.83 before the vote is known, and about 0.69 to 0.79 given a favourable vote. Those refits still set priority review to yes. For a target date such as 1 May 2027, the one-year reading is the closer analogue of the first decision. The final-action reading answers a different question, which is whether the product is approved eventually.

The cell that matches AMT-130 on orphan status, an initial application, and priority review has 22 approval-question meetings, 19 of them approved. The logistic probability on that row is 0.86, and the interval computed from those 22 meetings runs from 0.68 to 0.96. The six-meeting cell in the last approval row, which does not require priority review, is all approvals, and its own interval runs from 0.67 to 1.00. A cell of six is a count. It is a weak basis for a percentage.

The committee assignment can still move a prediction, and it cannot move it with any matching history. Huntington's disease is a disease of the brain. In this table the neurology factor records the name of the committee, and the gene-therapy products were reviewed elsewhere. If the FDA seats AMT-130 at the gene-therapy committee, or at a cancer committee that has reviewed other cell therapies, the factor is off and the main tables apply. If the FDA seats it at the Peripheral and Central Nervous System Drugs Advisory Committee, the factor is on, and any model that needs a gene-therapy meeting of that committee is predicting into an empty cell.

A year term, evaluated at 2026, does not improve the criterion for the kept models. For the priority-review model of the vote the criterion moves from 90.4 to 91.2. The same term does not improve the approval models. The year 2026 is already represented in the table, through July 2026.

What the model cannot see is the part a briefing book would be about. AMT-130's development has been discussed publicly in terms of an external control comparison and a 48-month result on the composite Unified Huntington's Disease Rating Scale, and the company has said the application is for accelerated approval. None of those facts is a column. Accelerated approval appears only as a feature of particular past votes, such as the Elevidys benefit-risk question, and it was not coded as its own factor. Two products with the same orphan, priority, and cell-therapy labels can have very different evidence. This prior treats them as exchangeable.

The source mix cuts the same way. Fifteen of the 116 approval-question votes, and 33 of the 116 outcomes, rest on press or company documents rather than an FDA record. The solithromycin row that this round added is an FDA transcript for the vote and a company annual report for the rejection and the priority designation. The historical rate is a rate in a table with that mix of sources.

Selection sits underneath the base rate. The FDA calls an advisory committee when the decision is uncertain enough to want one. Products that sail through do not appear. The 0.67 and 0.69 figures are rates among products that reached a vote. They are silent on products that never reached a committee. The figures near 0.87 further restrict that set to meetings with a recorded review type and set priority review to yes.

## Conclusions

On the 116 approval or benefit-risk questions with a known final outcome, the chance of a favourable vote is 0.67 (78 of 116) and the chance of eventual approval is 0.69 (80 of 116). Every such meeting is included, whether or not its review type is recorded. Given a favourable vote, 72 of 78 were approved. Given an unfavourable vote, 8 of 38 were approved. The penalized models that use the vote put eventual approval at 0.88 to 0.92 after a favourable vote and at 0.28 to 0.37 after an unfavourable vote.

Priority review does not improve a model of eventual approval once the comparison uses the meetings that have a recorded review type. On that subset, 80 of 92 were approved, 41 of 46 after standard review and 39 of 46 after priority review. The R-squared is 0.01. For the vote, priority review is associated with a higher favourable rate, 41 of 46 against 33 of 46, and the R-squared on those same meetings is 0.08. Models that set priority review to yes produce probabilities of about 0.87 to 0.89 for a favourable vote and 0.84 to 0.87 for eventual approval. The best R-squared among the kept pre-meeting models is 0.15, and that model does not use priority review.

The one-year action, on the 68 meetings with that label, is 45 approvals. The priority-conditioned refits of that outcome run from 0.80 to 0.83 before the vote. The orphan-and-priority-and-initial cell in the approval table has 22 meetings, 19 approved, and its own interval runs from 0.68 to 0.96.

Orphan status is taken from FDA designation 525216. Priority review is taken from the company's November 2026 releases until an FDA letter confirms it. The clinical evidence, the external control, and the accelerated-approval request are outside this calculation.

## Suggested improvements

Thirty-one priority cells are still unverified. The page checked for each one is named in the basis column. The remaining open cell-and-gene-therapy cases are NurOwn and the resubmissions of deramiocel and Tudriqev. A designation on the original application stays off the resubmission unless the source says it carried over. Carvykti and Abecma, at the 15 March 2024 supplement meetings, are now standard review, from the FDA reviews of those supplements.

The two orphan cells marked "review" should be set to yes or no only if a source settles the indication. Darzalex Faspro for high-risk smoldering myeloma, and Tudriqev, do not meet that bar today.

A sourced column for accelerated approval, for a resubmission as against a first cycle, and for the use of an external control would address the largest hole in the factor list. Those columns would have to be built from primary documents, one row at a time, under the same rule used here: no inference from a missing record.

Once the FDA names the committee and the date, the unused branch of the neurology factor can be dropped, and the year term can be evaluated at that year. If the question of interest is the first action rather than eventual approval, the one-year models should be reported beside the final-action models, not only as an appendix.

Press-only tallies that are still thin should be checked against minutes where a tally exists. The project log already flags the Tzield count, and the Skysona and Zynteglo counts, as press or incompletely confirmed.

The residual of about 19 meetings against the Daval count is a difference in published totals. Closing it requires a meeting list, which that paper does not provide. Adding rows so that the totals match would invent meetings.

Where a matching cell has fewer than about eight meetings, the Jeffreys interval should be quoted with the logistic probability. The five-meeting cell in this report is the case that makes the practice necessary.

## Appendix. Additional results

The tables in sections A, B, and C were fit before the 4 November priority fills. The refit after those fills is in `amt130_prediction.md`. On that refit, the all-pivotal models that set priority review to yes give a favourable-vote probability of about 0.81 to 0.83 and an approval probability, before the vote, of about 0.82 to 0.86. A year term does not improve the criterion. The tables below are kept so the earlier fit can be compared with that file.

The summary's opening rates are the unfiltered counts on all 116 approval questions. "Neurology committee on" means the meeting is assigned to the Peripheral and Central Nervous System Drugs Advisory Committee or the Psychopharmacologic Drugs Advisory Committee. Probabilities are from the penalized fit. R-squared is Nagelkerke's. The criterion is the Akaike information criterion, and a lower value is a better penalized fit.

### A. All pivotal votes

This pass includes effectiveness questions as well as approval and benefit-risk questions. The rows below are the earlier fit. The refit puts the favourable-vote probability at about 0.81 to 0.83 and the approval probability, before the vote, at about 0.82 to 0.86.

| Outcome | Factors | Neurology committee | Meetings | R-squared | Criterion | Probability |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Favourable vote | Priority, initial application | Off | 106 | 0.09 | 108.1 | 0.87 |
| Favourable vote | Priority | Off | 106 | 0.05 | 108.5 | 0.85 |
| Favourable vote | Orphan, priority, initial application | Off | 105 | 0.10 | 108.8 | 0.89 |
| Favourable vote | Orphan, priority | Off | 105 | 0.07 | 109.1 | 0.87 |
| Favourable vote | Orphan, priority, cell and gene therapy, neurology committee, biologics center, initial application | Off | 105 | 0.13 | 112.4 | 0.95 |
| Favourable vote | Same six factors | On | 105 | 0.13 | 112.4 | 0.93 |
| Eventual approval | Priority, initial application | Off | 106 | 0.15 | 79.5 | 0.91 |
| Eventual approval | Orphan, priority, initial application | Off | 105 | 0.16 | 80.9 | 0.91 |
| Eventual approval | Priority, neurology committee, initial application | Off | 106 | 0.16 | 81.0 | 0.91 |
| Eventual approval | Priority, neurology committee, initial application | On | 106 | 0.16 | 81.0 | 0.88 |
| Eventual approval | Orphan, priority, neurology committee, initial application | Off | 105 | 0.17 | 82.3 | 0.91 |
| Eventual approval | Orphan, priority, neurology committee, initial application | On | 105 | 0.17 | 82.3 | 0.88 |
| Eventual approval | Priority, cell and gene therapy, neurology committee, biologics center, initial application | Off | 106 | 0.18 | 84.0 | 0.95 |
| Eventual approval | Same five factors | On | 106 | 0.18 | 84.0 | 0.93 |

Given the vote, the all-pivotal approval models sit higher than the main set, because the wider set of questions has fewer discordant outcomes. The probability of approval given a favourable vote in the kept models runs from 0.94 to 0.97 with the neurology factor off.

| Factors | Neurology committee | Meetings | R-squared | Criterion | Probability if favourable | Probability if unfavourable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Priority, initial application, vote | Off | 106 | 0.64 | 45.9 | 0.95 | 0.60 |
| Orphan, priority, initial application, vote | Off | 105 | 0.64 | 47.9 | 0.95 | 0.60 |
| Priority, neurology committee, initial application, vote | Off | 106 | 0.64 | 47.9 | 0.95 | 0.61 |
| Priority, neurology committee, initial application, vote | On | 106 | 0.64 | 47.9 | 0.95 | 0.57 |
| Priority, cell and gene therapy, biologics center, initial application, vote | Off | 106 | 0.64 | 49.7 | 0.97 | 0.69 |
| Cell and gene therapy, neurology committee, biologics center, initial application, vote | Off | 149 | 0.65 | 107.8 | 0.94 | 0.36 |
| Cell and gene therapy, neurology committee, biologics center, initial application, vote | On | 149 | 0.65 | 107.8 | 0.94 | 0.38 |

The last row has an empty matching cell. It is the same extrapolation described in the results: a gene-therapy meeting at a neurology committee has not occurred in this table.

### B. Approval within one year

These rows refit the models kept for eventual approval, using approval within 365 days of the meeting as the outcome. Meetings whose one-year action is unverified are left out. The probabilities fall relative to the final-action models.

| Factors | Neurology committee | Meetings | R-squared | Criterion | Probability |
| --- | ---: | ---: | ---: | ---: | ---: |
| Priority, initial application | Off | 61 | 0.15 | 69.8 | 0.82 |
| Orphan, priority, initial application | Off | 60 | 0.11 | 71.0 | 0.83 |
| Priority | Off | 61 | 0.05 | 72.3 | 0.80 |
| Priority, cell and gene therapy, biologics center, initial application | Off | 61 | 0.16 | 72.9 | 0.71 |
| Orphan, priority, cell and gene therapy, biologics center, initial application | Off | 60 | 0.13 | 73.9 | 0.73 |

Switching the neurology factor on does not change these five probabilities. Given a favourable vote, the one-year models give the following.

| Factors besides the vote | Neurology committee | Meetings | R-squared | Criterion | Probability |
| --- | ---: | ---: | ---: | ---: | ---: |
| None | Off | 68 | 0.32 | 73.1 | 0.76 |
| Initial application | Off | 68 | 0.34 | 74.1 | 0.76 |
| Biologics center | Off | 68 | 0.33 | 74.3 | 0.69 |
| Orphan | Off | 67 | 0.34 | 71.9 | 0.79 |
| Neurology committee, biologics center, initial application | Off | 68 | 0.36 | 76.6 | 0.68 |
| Neurology committee, biologics center, initial application | On | 68 | 0.36 | 76.6 | 0.77 |

The one-year models that include the vote have a lower R-squared than the final-action models that include the vote, about 0.32 to 0.36 as against about 0.59. Part of the association between a favourable vote and approval is an approval that arrives after the first year.

### C. A term for calendar year

Year was added only to the models already kept, as a straight line centered at 2020, and the probability was evaluated at 2026. For the favourable vote, every kept model fits better with the year term, and the probability drops.

| Factors | Criterion without year | Criterion with year | R-squared with year | Probability at 2026 | Stable |
| --- | ---: | ---: | ---: | ---: | --- |
| Priority | 74.1 | 72.7 | 0.18 | 0.77 | Yes |
| Priority, initial application | 74.7 | 73.9 | 0.19 | 0.81 | Yes |
| Orphan, priority | 74.8 | 72.6 | 0.21 | 0.80 | Yes |
| Orphan, priority, initial application | 75.4 | 73.6 | 0.23 | 0.83 | Yes |
| Priority, cell and gene therapy, biologics center, initial application | 77.6 | 76.6 | 0.21 | 0.89 | Yes |

For eventual approval the year term does not improve the criterion. One fit separates and is not used as a probability.

| Factors | Criterion without year | Criterion with year | R-squared with year | Stable |
| --- | ---: | ---: | ---: | --- |
| Priority, initial application | 53.7 | 55.6 | 0.13 | Yes |
| Orphan, priority, initial application | 55.4 | 57.2 | 0.14 | Yes |
| Priority | 56.5 | 58.0 | 0.03 | Yes |
| Priority, cell and gene therapy, biologics center, initial application | 56.9 | 60.0 | 0.12 | No |
| Orphan, priority, cell and gene therapy, biologics center, initial application | 58.6 | 60.4 | 0.16 | Yes |

### D. Where the files are

The meeting table is `adcom_full_pivotal.csv` in this folder, 156 rows. The search log is `missing_row_search.csv`. The factor lookups are `factor_verification.csv`. The model output is `amt130_prediction.csv`, with the screen of every subset in the `amt130_screen_*.csv` files. The figure is `charts/amt130_prediction_forest.png`. The fit is `scripts/amt130_predict.py`, run from this folder. Corrections to the meeting table are made in `scripts/cur.py` and applied when the table is rebuilt. The table is not edited by hand.
