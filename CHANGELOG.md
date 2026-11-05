# CHANGELOG

## 2026-11-05 — estimated clocks, three unverified left
- A missing day is the 15th. A stated goal is used, including an expected date. A complete-response date is the goal only when it lands on one anniversary. Each basis says `(calculated)` and states the estimate. Log: `data/unapproved_priority_search_2026-11-05.csv`.
- Eleven more rows set to STANDARD: Hydexor (both cycles), MNK-812, vernakalant, oxycodegol, tanezumab, sintilimab, poziotinib, NurOwn, ITCA 650, and condoliase. Nicotine mouth spray, Tookad, and AR19 stay unverified.
- Priority 81, standard 72, unverified 3. All, Common, Rare, Rare + priority, CGT, and the approval-only cells are unchanged, so the chart filenames stay at v8 / v5 / v6. The Standard row is 32 / 3 / 8 / 26 (n=69). The factor screen was rerun, and a four-factor model (orphan, priority, opioid, cell and gene therapy) was added beside the screen-selected pair.

## 2026-11-05 — PDUFA clock for the remaining unverified rows
- The clock is measured from the initial submission. An NME or original BLA is 8 months from submission for priority and 12 months from submission for standard. A non-NME is 6 and 10 months from submission. The basis says `(calculated)`. A Class 2 clock, an extended goal, and a sponsor forecast are not used. Log: `data/unapproved_priority_search_2026-11-05.csv`.
- Ten rows set to STANDARD: Rexista (both cycles), sirukumab, Waylivra, Buvaya, ALKS 5461, sotagliflozin NDA 210934 (both cycles), roxadustat, and gefapixant. Fourteen stay unverified.
- Priority 81, standard 61, unverified 14. All, Common, Rare, Rare + priority, CGT, and the approval-only cells are unchanged, so the chart filenames stay at v8 / v5 / v6. The Standard row is 32 / 1 / 8 / 17 (n=58). The factor screen was not rerun.

## 2026-11-05 — priority search for unapproved products
- Searched the 27 rows whose review type was unverified. Each is unapproved, so Drugs@FDA has no original submission. The search looked at the FDA briefing for that meeting, then a sponsor SEC filing, then a company press release, including releases that were never filed. Log: `data/unapproved_priority_search_2026-11-05.csv`.
- Three rows set to PRIORITY from an FDA document: stannsoporfin (3 May 2018, NDA 209904), obeticholic acid for NASH (19 May 2023, NDA 212833), and the original Comirnaty BLA (the 17 Sep 2021 meeting is a booster supplement; the row's application cell stays blank). All three votes were unfavourable and the products were not approved. They are orphan N, so the rare-and-priority 2x2 does not change.
- Priority 81, standard 51, unverified 24. All, Common, Rare, Rare + priority, CGT, and the approval-only cells are unchanged, so the chart filenames stay at v8 / v5 / v6. The Priority row in `two_by_two.csv` is now 58 / 2 / 2 / 15 (n=78, 1 pending): the three new rows are unfavourable and not approved. The factor screen was not rerun.

## 2026-11-04 — opioid column and initial-review priority
- `opioid` is Y or N on every row. Y means an active moiety is an opioid agonist. Sixteen rows are Y. Naloxone, samidorphan alone, and lofexidine are N.
- `review_priority` is the original application's designation. Supplements take openFDA's original submission when it names one. Cited original cycles set Remoxy (2008 10-K, SEC), Carvykti (Legend 6-K, SEC), Abecma (FDA clinical review), Columvi (openFDA original submission), Darzalex Faspro (FDA multi-discipline review, still standard), deramiocel and Tudriqev (company announcements of the original BLA; press).
- 2x2 (AA/AR/RA/RR, final): All, Common, Rare, and the CGT aggregate unchanged. Rare+priority 29/1/1/8 -> 32/1/1/8 (n=42, 1 pending). Approval-only Rare+priority 22/1/0/4 -> 25/1/0/4 (n=30). Priority 78, standard 51, unverified 27. Charts `*_v8`, CGT `cgt_2x2_pct_v5.png` and `cgt_2x2_pct_approvalonly_v6.png`, CGT tables `*_v5.pdf`.
- The factor screen adds opioid. A sensitivity that fills blank review types as standard, and again as priority, does not agree, so priority review is not in the joint model. The vote screen carries orphan status and opioid.

## 2026-11-04 — exhaustive priority search
- Fourteen `review_priority` values set where a source names the designation for the submission the committee reviewed. Eight are FDA documents (Rebyota, Abrysvo 60+, Arexvy, Abrysvo maternal, Carvykti sBLA, Abecma sBLA, mFLUSIVA, tramadol IV). Two are SEC filings (Bayer ciprofloxacin dry powder, via Aradigm's 10-Q; bardoxolone). Four are press (Translarna, Linhaliq, retifanlimab, carbetocin).
- Thirty-one priority cells stay unverified. The search note is in `priority_basis`. Orphan `review` is unchanged (Darzalex Faspro SMM, Tudriqev). `action_at_1yr` stays unverified on 63 rows.
- 2x2 (AA/AR/RA/RR, final): All, Common, Rare, and CGT unchanged. Rare+priority 29/1/1/4 -> 29/1/1/8. Approval-only Rare+priority 22/1/0/2 -> 22/1/0/4. All-drug charts rebuilt as `*_v7`.

## 2026-11-04 — missing-row search and priority lookups
- Solithromycin (AMDAC 2016-11-04, NDA 209006) added. FDA transcript: benefit-risk 7-6. SEC 10-K: CRL 29 Dec 2016 and priority review. Orphan N. Search log in `data/missing_row_search.csv` (one added row; sulopenem 2024-09-09 had no vote).
- Six `review_priority` values set from a cited source (Ryoncil, quizartinib, omburtamab, omecamtiv, midomafetamine, Darzalex Faspro S-029). 45 stay unverified. Log: `data/factor_verification.csv`.
- 2x2 (AA/AR/RA/RR, final): All 90/6/10/43; Common 48/4/8/32; Rare 40/2/2/11; Rare+priority 29/1/1/4; CGT 10/0/0/1; Approval-only All 72/6/8/30; Approval-only Rare+priority 22/1/0/2. All-drug charts are `*_v6`.

## 2026-11-04 — corrections + handover
- All corrections moved into code (`cur.py` -> `curated.csv` + `field_overrides.csv`; applied last in `final.py`). Previously 7 orphan fixes and 32 center values existed only as CSV edits.
- Orphan audit of 155 rows (`orphan_audit_2026-11-04.csv`): 20 value changes + 4 basis-only fixes. NurOwn -> Y.
- CGT definition extended to Kymriah, Ryoncil, Carvykti, Abecma (12 rows). Center derived per product with `center_basis`.
- New columns: `center_basis`, `vote_type`, `vote_type_basis`. New 2x2 subsets: Rare + priority, Approval-only (All/Common/Rare/Rare + priority/CGT).
- CGT review priority written with source URLs; Deramiocel/Tudriqev noted as resubmissions.
- Ryoncil/Carvykti/Abecma: brand filled; votes already from FDA minutes (8-2 with note; 11-0; 8-3).
- Charts rebuilt as `*_v4` (all votes) and `*_approvalonly_v5`; CGT tables `*_v4.pdf` now generated from the CSV (`cgt_tables.py`).
- `check_consistency.py`, `run_all.sh`, relative/configurable input paths (`data/inputs/`, env `ADCOM_LEGACY_XLSX`, `ADCOM_CGT_CSV`, `CHART_DIR`).
- 2x2 before -> after (AA/AR/RA/RR): All 90/5/10/43 -> 90/5/10/43; Common 46/3/5/32 -> 48/3/8/32; Rare 38/2/5/10 -> 40/2/2/11; Rare+priority 25/1/1/2 -> 28/1/1/2; CGT 7/0/0/1 -> 10/0/0/1.

## Earlier (see AGENTS.md / REPORT.md)
- Gap resolution (68 -> 0), outcome sourcing, orphan_for_indication, curated add-row index bug fix (121 -> 155 rows).
