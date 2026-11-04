# DATA_DICTIONARY: data/adcom_full_pivotal.csv (= sheet meetings_pivotal)

| Column | Meaning |
|---|---|
| `meeting_date` | Meeting date (ISO). Key with app. |
| `year` | Year of meeting. |
| `committee` | FDA advisory committee acronym (joint meetings joined with +). |
| `center` | CDER or CBER, per product (see center_basis). |
| `app` | NDA/BLA number (may carry /S-xxx supplement suffix; blank for a few curated rows). |
| `brand` | Brand name (blank if unapproved/unknown). |
| `generic` | Generic/established name. |
| `product_text` | Product text as parsed from the FR notice/minutes. |
| `meeting_type` | initial application or supplemental. |
| `pre_2010` | Always False in this window. |
| `question_text` | Text of the pivotal vote question (may contain surrounding minutes text). |
| `vote_yes` | Yes votes on the pivotal question. |
| `vote_no` | No votes. |
| `vote_abstain` | Abstentions. |
| `voting_member_count` | yes+no+abstain. |
| `adcom` | favourable (yes>no), unfavourable, tie, or favourable (restricted...) (Lynparza 2023). Polarity is flipped for defer/delay questions (pivotal_note in curated.csv). |
| `pivotal_rule` | How the pivotal question was chosen (rule or curated). |
| `polarity_check` | Automated flag that question polarity was checked. |
| `action_at_1yr` | approved / not approved within 1 yr / unverified. |
| `final_action` | Latest known FDA decision; starts with "approved" when approved (later approvals count). |
| `final_action_date` | Date of final_action (may be month only). |
| `decision_source` | Source of final_action. |
| `review_priority` | PRIORITY / STANDARD / unverified. |
| `orphan_designation_any` | Looser product-level orphan flag from legacy data. |
| `orphan_match` | OOPD rows matched by name (diagnostic). |
| `CNS` | True for PCNS/PDAC. |
| `CGT` | True for CTGTAC rows and Kymriah, Ryoncil, Carvykti, Abecma. |
| `replaced_by_later_meeting` | True if superseded by a later meeting for the same application (excluded from 2x2). |
| `n_products_same_meeting` | Number of products voted at the same meeting. |
| `minutes_url` | FDA minutes/voting results URL used. |
| `minutes_title` | Title of the minutes link. |
| `fr_notice` | Federal Register notice URL. |
| `fr_snippet` | Agenda text from the FR notice. |
| `orphan_for_indication` | Y (OOPD designation for the reviewed indication, dated before decision), N, review (ambiguous), unverified. Defines Rare. |
| `orphan_indication_basis` | Why orphan_for_indication has its value; "corrected 2026-11-04 on audit" for audited rows. |
| `priority_basis` | Source of review_priority (openFDA ORIG/supplement, URL, or reason unverified). |
| `center_basis` | Why center has its value. |
| `vote_type` | approval/benefit-risk, effectiveness-only, or restriction/other. |
| `vote_type_basis` | rule on question_text, or curated: reason. |
| `verified_vote` | How the vote was verified. |
| `vote_source_tier` | FDA or press. |
| `verified_outcome` | How the outcome was verified. |
| `outcome_source_tier` | FDA, FDA (openFDA), SEC/company, press, unverified. |
| `verified_orphan` | Legacy orphan verification note (product-level). |
| `source` | Which pipeline branch produced the row (automated, curated, legacy, cgt_check). |
| `curated_source` | URL/description of the manual source when curated. |
| `notes` | Free-text notes. |

## data/two_by_two.csv
| Column | Meaning |
|---|---|
| subset | Row filter (All, Rare (orphan Y), Common (orphan N), Priority, Standard, CNS, CGT, Rare + priority, Approval-only: ..., Daval overlap) |
| outcome | final (final_action) or 1yr (action_at_1yr) |
| n | rows with a known outcome (includes non-binary adcom codes) |
| FavApproved / FavNotApproved / UnfavApproved / UnfavNotApproved | AA / AR / RA / RR cells |
| outcome_unverified | rows with unverified/pending outcome |

## data/field_overrides.csv
meeting_date, app, field, value, source: field-level corrections written by cur.py, applied last by final.py.

## data/orphan_audit_2026-11-04.csv
meeting_date, committee, app, brand, old (pipeline value before override), new, changed, basis, source.

## data/excluded.csv / gaps.csv
committee, meeting_date, reason, minutes_url, n_votes, first_question (+ app/product fields where known).
