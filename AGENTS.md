# AGENTS.md: how `adcom_full_pivotal.csv` / `adcom_full.xlsx` was built

Audience: any agent or person who needs to rebuild, audit, extend, or correct this dataset.
Location: this repo. Scripts in `scripts/`, data (and the pipeline working directory) in `data/`, charts in `charts/`. Run `./run_all.sh`.
Last updated: 2026-11-04.

## 1. What the dataset is

One row per FDA advisory committee (adcom) meeting x product, for meetings from **2016-11-04 to 2026**, where the committee took a vote on **approval of a specific product** (initial application or supplement). The row records the committee's **pivotal vote** and what the FDA did afterwards. Purpose: estimate the probability that an adcom is favourable and that the FDA follows it, by stratum (rare vs common disease, priority vs standard review, CNS, cell/gene therapy), as a prior for uniQure's AMT-130.

Main outputs:
- `adcom_full_pivotal.csv` (155 rows; sheet `meetings_pivotal` in `adcom_full.xlsx`). The main table.
- `excluded.csv` (170 rows, each with a reason). Meetings that were seen but have no product approval vote.
- `gaps.csv`. Product meetings found in the Federal Register with no usable vote (currently 0 open gaps).
- `two_by_two.csv`. Vote vs FDA outcome counts by subset. Final outcome and 1-year outcome.
- `coverage_vs_daval.csv`, `daval_shortfall_explained.csv`. Completeness check against Daval et al.
- `REPORT.md`. Counts by committee and verification rates. `README.md`. Short change log.
- Charts: `four.py` / `four_pct.py` / `four_cgt.py` build the four 2x2 charts (all drugs, and CGT only) from the CSV.
- Charts (current): `charts/all_2x2_counts_v4.png`, `charts/all_2x2_pct_v4.png`, `charts/cgt_2x2_pct_v4.png` (all pivotal votes) and `charts/*_approvalonly_v5.png` (vote_type == approval/benefit-risk only). Older `*_v2/_v3` and `four_2x2*.png` are superseded.
- CGT tables built from the CSV by `cgt_tables.py`: `charts/cgt_validation_table_v4.pdf`, `charts/cgt_priority_review_table_v4.pdf` (12 CGT rows). The hand-built `cgt_*_table.pdf` (val.py, 9 rows) are superseded.
- `check_consistency.py` asserts CSV, xlsx, two_by_two.csv and chart inputs agree.

Never overwrite `adcom_full_pivotal.csv` blindly. Backup before the 2026-11-04 orphan fix: `adcom_full_pivotal.bak_before_orphan_fix.csv`. Note that `final.py` regenerates the CSV from scratch; **All corrections now live in code** (`cur.py` writes `curated.csv` and `field_overrides.csv`; `final.py` applies field overrides last). Never edit the CSV by hand. Backup before the 2026-11-04 corrections: `adcom_full_pivotal.bak_2026-11-04_pre_corrections.csv`.

## 2. Definitions used

- **Pivotal vote**: the last vote question at that meeting for that product that explicitly asks about approval, licensure, or benefit-risk ("benefits outweigh risks"). Excluded wording: "prior to approval", post-marketing, labeling, REMS, restriction, dose. If there is no such question, the first effectiveness question is used; failing that, the first vote (flagged `pivotal_rule`). The rule applied to each row is in column `pivotal_rule`.
- **Favourable** = yes > no. Abstentions are recorded but not counted as yes. **Ties are excluded** from the 2x2s (4 meetings).
- **Superseded meetings** (`replaced_by_later_meeting=True`) are excluded from the 2x2s. Example: Relyvrio's first vote was replaced by the Sept 2022 vote.
- **FDA outcome**: `final_action` (latest known decision, so a CRL followed by approval years later counts as approved) and `action_at_1yr` (approved within 365 days of the meeting). Withdrawn or pending is not "approved". Pending and unverified outcomes are left out of the 2x2s and counted in the "unverified" figure.
- **Rare disease** = `orphan_for_indication == Y`: the product has FDA orphan drug designation (US prevalence under 200,000) **for the indication reviewed at the meeting**, per FDA's orphan database (OOPD). `orphan_designation_any` is the looser product-level flag.
- **Priority vs standard**: `review_priority` (`PRIORITY`, `STANDARD`, or `unverified`).
- **CNS** = committees PCNS and PDAC. **CGT** = committee CTGTAC **or** one of the cell therapies reviewed elsewhere: Kymriah 125646, Ryoncil 125706, Carvykti 125746, Abecma 125736 (`CGT_APPS` in `final.py`). Rebyota (fecal microbiota, VRBPAC) is not CGT.
- **Center** (`center`, with `center_basis`): set per product in `final.py`: CTGTAC/VRBPAC rows and `CBER_APPS` are CBER; an application listed in Drugs@FDA/openFDA (CDER products only), a 761xxx BLA, or an NDA is CDER.
- **vote_type**: `approval/benefit-risk`, `effectiveness-only`, or `restriction/other` (restriction, deferral, surrogate, endpoint, applicability, labeling). Rule on the last VOTE question in `final.py` plus curated overrides in `cur.py` (`vote_type_basis` says which). The approval-only 2x2s use only `approval/benefit-risk`.

## 3. Data sources (all public)

| Need | Source | How accessed |
|---|---|---|
| List of meetings and the products on each agenda | Federal Register API `federalregister.gov/api/v1/documents.json`, FDA advisory committee notices, 2000 to 2026 | `fr.py` (half-year queries, `fr/`), then `fr_items.py` / `parse_fr.py` (parse agenda text for NDA/BLA numbers) |
| Votes | FDA minutes, voting results, transcripts (PDFs), on fda.gov `/media/<id>/download`, committee pages, Wayback Machine, and Archive-It for older material | `minutes.py`, `minutes_pre09.py`, `ait.py`/`ait2.py`, `mscan.py` + `ingest_media.py` (scans fda.gov media IDs), `dl.py` (download + `pdftotext`), `ocr.py` for scanned PDFs |
| CDER approvals, priority vs standard | openFDA `api.fda.gov/drug/drugsfda.json` | `ofda.py`, `outq.py` (cached in `ofda/`). **Does not cover CBER biologics** |
| Rejections | openFDA CRL database `api.fda.gov/transparency/crl.json` (2025 onward) | `crl_all.json`, used in `enrich.py` |
| CBER approvals and review type | FDA approval letters, SBRAs, CBER approved-products pages | by hand; letters in `ltr/` |
| Orphan status | FDA OOPD export | `oopd_all.csv` (8,000+ rows of orphan designations, **a lookup table, not adcom meetings**) |
| Completeness benchmark | Daval et al., JAMA Health Forum 2023 (PMC10329213), eTable 1 | `daval_etable1.csv`, `daval_table2.csv` |
| Fallback for votes and outcomes | Company press releases, SEC filings (8-K, 6-K), news | only via `cur.py`; each row has `curated_source` and is tiered as "press" in the verification columns |

## 4. Pipeline (run order)

1. **Meeting discovery**: `fr.py` downloads FDA advisory committee notices. `parse_fr.py` and `fr_items.py` extract date, committee, and each NDA/BLA on the agenda into `fr_items.json` (one item per date and application number).
2. **Find the minutes**: the minutes scripts collect links to minutes/voting-results PDFs from committee pages and archives, and `mscan.py` scans FDA media IDs for ones not linked. `dl.py` downloads and converts to text. `ocr.py` handles scanned PDFs. Older meetings fall back to Wayback copies.
3. **Extract votes** (`build.py` with `votes.py`): regexes pull vote tallies (yes, no, abstain) and the question text. A vote is attached to a product by **product names that appear in the vote question**. This matters for multi-product meetings. Pivotal question selection follows section 2. Output: `rows_raw.pkl` (every vote), `gaps.pkl` (no usable vote), `excluded.pkl` (not a product approval vote: safety, policy, class, device, EUA, cancellations).
4. **Attach outcomes** (`enrich.py`): look up the application in openFDA. If an original approval exists on or after the meeting, the outcome is approved with its date. A later CRL in the CRL database means not approved. Supplements are **left unverified** unless sourced elsewhere, because openFDA does not say which indication a supplement covers. **Nothing is inferred from the absence of a record.**
5. **Orphan status** (`orphan_ind.py`): match product names to OOPD, only designations dated before the decision. If the designation text shares at least 2 keywords with the meeting's indication, it is Y. A 1-keyword match is "review". Otherwise N ("designation for other indication" or "no designation for ingredient"). 26 weak matches were then adjudicated by hand (`orphan_adj.csv`).
6. **Curation** (`cur.py`): hand-sourced overrides: drops (cancelled meetings, duplicates, class votes), added rows (meetings the parser missed), corrected vote tallies and question mappings, sourced outcomes (press, SEC, FDA letters), priority review values. Each curated row has `curated_source`.
7. **Assemble and compute** (`final.py`): merge the earlier hand-verified rows (`inputs/adcom_dataset.xlsx`, or env `ADCOM_LEGACY_XLSX`; falls back to `/workspace/adcom/out/adcom_dataset.xlsx`) and the CGT existence check (`inputs/cgt_check.csv` or env `ADCOM_CGT_CSV`), remove duplicates and marketed-product meetings, apply `cur.py`, fill `review_priority` from openFDA (original or supplement), compute `two_by_two.csv`, `coverage_vs_daval.csv`, write the CSV/XLSX.
8. **Report** (`report.py`): `REPORT.md`.
9. **Consistency + charts**: `check_consistency.py`, then `four.py`, `four_pct.py`, `four_cgt.py`, `cgt_tables.py` (into `charts/`, env `CHART_DIR`).

Rerun: `python3 cur.py && python3 final.py && python3 report.py && python3 four.py && python3 four_pct.py && python3 four_cgt.py && python3 cgt_tables.py && python3 check_consistency.py` (fast, offline apart from cached files). The crawl stages are slow and rate-limited (fda.gov, Wayback, Archive-It); their outputs are cached under `pdf/`, `txt/`, `html/`, `ofda/`, `fr/`. Full pipeline scripts must be run in the order above.

## 5. Verification columns

`verified_vote` / `vote_source_tier`: FDA minutes/transcripts (136 of 155) vs press (19). `verified_outcome` / `outcome_source_tier`: FDA document or openFDA (112), press (38), SEC/company (5). `verified_orphan`, `orphan_indication_basis`, `priority_basis` say how each label was derived. When quoting results, always report these tiers; do not present press-sourced rows as FDA-verified.

## 6. Completeness check against Daval

Daval lists 164 meetings for 2016 to 2021. We account for 86 product-vote rows plus 39 excluded meetings, and 20 of Daval's 2016 meetings fall before our 2016-11-04 cutoff. That leaves **19 unexplained**: 7 pharmacy-compounding meetings, a net 6 from joint meetings filed under another committee, and about 6 unidentified. Daval publishes counts only, not a meeting list, so a row-by-row match is not possible. Our totals cannot be proven complete; they are consistent with his within those 19.

## 7. Headline results (2016-11-04 to 2026; final outcome; ties, superseded and unverified outcomes excluded)

Counts as AA / AR / RA / RR (first letter adcom: A favourable or R unfavourable, second letter FDA approved or rejected), after the 2026-11-04 corrections:

| Subset | All pivotal votes | Approval/benefit-risk votes only |
|---|---|---|
| All | 90 / 5 / 10 / 43 (n=148, 1 pending) | 72 / 5 / 8 / 30 (n=115) |
| Common (orphan N) | 48 / 3 / 8 / 32 | 39 / 3 / 7 / 25 |
| Rare (orphan Y) | 40 / 2 / 2 / 11 (1 pending) | 32 / 2 / 1 / 5 |
| Rare + priority | 28 / 1 / 1 / 2 | 22 / 1 / 0 / 1 |
| CGT (12 rows) | 10 / 0 / 0 / 1 (deramiocel pending) | 8 / 0 / 0 / 0 |

2 rows are orphan `review` (Darzalex Faspro SMM, Tudriqev) and appear only in "All". Cells are small. FDA tends to convene adcoms when it is uncertain (selection bias), "final" counts later approvals, and some outcomes and votes rest on press.

## 8. Known issues (open)

1. **Orphan `review`**: Darzalex Faspro 2025-05-20 (high-risk SMM vs the multiple-myeloma designation) and Tudriqev (no OOPD record found for RP1/vusolimogene). Decide and set in `cur.py`.
2. **Vote type is a judgement**: Elevidys (benefit-risk for *accelerated* approval) and Zelnorm (reintroduction supported by safety data) are coded approval/benefit-risk and flagged; VRBPAC vaccine and Rebyota pivotal questions are effectiveness questions (separate safety votes) and coded effectiveness-only.
3. **Priority review**: CBER rows Ryoncil, Carvykti, Abecma and NurOwn are `unverified` (no source checked / not found). Deramiocel and Tudriqev are `unverified` for the reviewed resubmission (priority applied to the original BLA; URLs in `priority_basis`).
4. **Ryoncil vote**: FDA minutes (media/143336) record 8-2; the minutes note one "No" voter later changed their vote, which is why press and cgt_check say 9-1. The FDA-recorded 8-2 is kept.
5. **Tzield vote count** (10-7) is unconfirmed: an FDA review confirms only that a majority voted favourably. Romosozumab, Descovy, and tanezumab FDA review PDFs were image-only or lacked the tally. Skysona and Zynteglo counts are from press only. Relyvrio was not re-verified after the final stage.
6. **Translarna** (1-10 in this dataset, 0-10-1 in the hand data): FDA minutes give A 0, B 10, C 1, and option C counts as a yes here. **Aduhelm** uses the final question (0-10-1), though Q1 was 1-8-2.
7. **Lynparza 2023-04-28** is coded "favourable (restricted to BRCAm)" and is outside every 2x2.
8. **Meetings with no row**: Ebvallo (no adcom was held), Casgevy (no voting question).
9. **Coverage**: 19 meetings unexplained against Daval (section 6). Some media-ID crawl ranges were never ingested; gaps are 0, so these are optional.
10. **Earlier artifacts superseded**: `/workspace/adcom/out/` (66 rows), `adcom_2x2.png`, `four_2x2*.png`, `*_v2/_v3.png`, hand-built `cgt_*_table.pdf`.

### Corrections log 2026-11-04 (all in `cur.py` -> `field_overrides.csv`, applied last in `final.py`)

- FIXED (was item 1): the 7 CSV-only orphan fixes (Elevidys, Waylivra, Blenrep 2025, pretomanid, Tzield, Gleolan, Ocaliva 2024-09-13) moved into code.
- FIXED (was item 2): NurOwn orphan Y (OOPD 2011-02-04).
- Orphan audit of all 155 rows against `oopd_all.csv`: see `orphan_audit_2026-11-04.csv` (old, new, basis, source). Y->N: Victoza 2017, Jatenzo, Tlando, roxadustat, Awiqli (spurious keyword matches). N->Y: Rebyota, omburtamab. review->Y: Blincyto 2018, Livtencity. review->N: Arakoda. unverified->N: 4 RSV/COVID vaccine rows. ->review: Darzalex SMM, Tudriqev. Basis text fixed: retifanlimab, Arikayce, Lantidra, Krintafel.
- FIXED (was item 3): CGT flag covers CTGTAC + Kymriah, Ryoncil, Carvykti, Abecma (12 rows).
- FIXED (was item 4): center set per product with `center_basis`; Kymriah, Ryoncil, Carvykti, Abecma are CBER; 31 formerly blank rows derived (all CDER).
- FIXED (was item 5): `vote_type` column added; approval-only chart set (`*_approvalonly_v5.png`).
- FIXED (was item 6): CGT priority written with URLs in `priority_basis`.
- FIXED (was item 9, which was stale): Ryoncil 2020, Carvykti and Abecma 2024 were already rows with FDA-minutes votes (media/143336: 8-2; media/178184: 11-0 and 8-3). Brand, center and CGT now filled.
- Hardcoded absolute input paths in `final.py` replaced by `inputs/` + env overrides.

## 9. Conventions for agents working on this dataset

- Never fabricate. If a field cannot be confirmed from a source, mark it `unverified` or "not found". Never infer "not approved" from a missing record.
- Cite a URL for every manual change (`curated_source`), and say whether the source is primary (FDA, SEC) or secondary (press).
- Do not use the OOPD file as a list of meetings.
- Disclose coverage gaps and verification tiers whenever statistics are quoted, because David has asked for complete coverage and flagged undisclosed gaps as unacceptable.
- Report counts with n and unverified totals. State when a cell is too small for a percentage to mean anything.
