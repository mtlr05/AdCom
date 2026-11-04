# SPEC

## Unit of observation
One row per (meeting_date, application) where an FDA adcom between 2016-11-04 and 2026-12-31 voted on a question about a specific NDA/BLA. Excluded meetings (no product vote, class/policy, device, EUA, cancelled, duplicates) go to `excluded.csv` with a reason.

## Pivotal vote
Last vote question explicitly on approval/licensure/benefit-risk; else first effectiveness question; else first vote (flagged). Favourable = yes > no; ties excluded from 2x2s. Defer/delay questions are polarity-flipped. `vote_type` classifies the pivotal question.

## Outcome
`final_action` = latest known FDA decision (approved later counts as approved). Unverified/pending outcomes are excluded from 2x2 cells and counted separately. Never infer non-approval from a missing record.

## Strata
Rare = `orphan_for_indication == Y` (OOPD designation for the reviewed indication, before the decision). Common = `N`. Priority = `review_priority == PRIORITY`. CGT = CTGTAC + Kymriah, Ryoncil, Carvykti, Abecma. Approval-only = `vote_type == approval/benefit-risk`.

## Rules for changes
All corrections go in `scripts/cur.py` (`c(...)` for row-level curation, `fo(...)` / `orph(...)` for field overrides) with a source URL. Never edit CSVs by hand. Charts are saved under new filenames when the numbers change.

## Acceptance test
From a fresh clone with `pip install -r requirements.txt`:
1. `./run_all.sh` exits 0 and prints `run_all.sh: OK` and `FAILURES: 0`.
2. `data/adcom_full_pivotal.csv` has 155 rows and 47 columns; `center` is never blank; `orphan_for_indication` ∈ {Y,N,review,unverified}.
3. `data/two_by_two.csv` (outcome=final) contains: All 90/5/10/43; Common 48/3/8/32; Rare 40/2/2/11; Rare + priority 28/1/1/2; CGT 10/0/0/1; Approval-only: All 72/5/8/30; Approval-only: Rare + priority 22/1/0/1 (AA/AR/RA/RR). Any intentional change must update this list and CHANGELOG.md.
4. `charts/` contains the six `*_v4` / `*_approvalonly_v5` PNGs and the two `cgt_*_v4.pdf` tables, newer than the CSV.
