# Orphan natural-history page

This directory is one project. The advisory-committee dataset in the rest of the repository is the other. They do not share a pipeline. `run_all.sh` does not build this page, and editing this page does not change `adcom_full_pivotal.csv`.

`index.html` is the only copy of the page. Row edits go there. There is no copy step.

## What the page is

One row per product whose efficacy package used a natural-history cohort for an orphan indication. The page started from Jahanshahi et al. (approvals through 2019) and Vaghela et al. (non-oncologic orphan NDAs and BLAs through October 2022), plus a short manual list. A later product is added only when it matches the class below.

Numbers come from an FDA letter, review, label, or snapshot. Company figures stay labeled as company data. The Supportive label on the page is not a second inclusion rule. Voxzogo is the pattern for a natural-history cohort that contextualized a randomized trial.

## The class

This is the only full statement of the class. The page points here. Do not keep a second copy in a skill or in a looser line on the page.

Jahanshahi’s kept class is retrospectively collected natural history: subject-level data from a natural history study, existing medical records, or a previously conducted registry, used to support a pivotal study. They separated that from published data with no subject-level dataset, from an arm of a previous clinical study, and from a patient’s own baseline. They also left out natural-history material used only to choose an endpoint or to interpret nonclinical work.

Vaghela’s kept class, among non-oncologic orphan NDAs and BLAs, is natural history, including a registry cohort or a retrospective historical control, used to compare or contextualize efficacy. They put retrospective medical chart reviews in a different bucket (Dojolvi, Diacomit, Mepsevii, Luxturna), and this page drops that bucket. They put an external control taken from another study in a third bucket (vutrisiran), and this page drops that too.

The page then applies one further cut to both extracts: the cohort is the untreated course of the disease. Tepadina and pretomanid are labeled retrospective natural history in Jahanshahi and stay excluded, because the historical patients had received another treatment. Oncology stays out, as Vaghela set it aside. Orphan designation for the indication stays required.

A prospective observational study with subject-level untreated patients is in the class. Nulibry is already a row of that pattern. A literature rate or a performance threshold with no subject-level dataset is not.

## How a row is added

Start from the FDA lists, not from names already on the page. Take every original approval from 1 November 2022 through the day of the edit:

- CDER novel-drug approval pages for each year, plus that year’s “new” page if the annual table lags a this-week approval.
- CBER biological-product approvals for the same years.
- The openFDA complete-response set, because a rejection is not on the approval list.
- The CBER real-world-evidence table and the LEADER 3D case studies, as a cross-check, not as the list.

Read the label’s clinical-studies section, or the approval letter if the label is not posted yet. Keep a product only when that text shows the class above. Write one line per product to `screen_log.csv`: name, date, source URL, and `row`, `already listed`, or `not this class`, with a short reason. A product with no line was not screened.

The screen through 19 November 2026 is in `screen_log.csv`. It covers the CDER novel tables (November 2022 through 18 November 2026), the CBER BLA tables for 2023 through 2026, Hemgenix for November 2022, and 89 application numbers in the openFDA complete-response file dated 1 January 2025 through 19 November 2026 (100 letters, last updated 18 November 2026). It does not cover every efficacy supplement. The one supplement in this pass is Brineura for children under 3, because that product was already in the table.

For each new row, confirm orphan designation and that the product is absent from this project’s meeting files (`data/adcom_full_pivotal.csv` and `data/excluded.csv`). AdCom “No” uses the sentence already used for Viltepso and Voxzogo. Cite an FDA letter, review, label, or snapshot for every number.

## Deploy

Vercel’s root directory for this project is `natural-history`. `vercel.json` in this directory is the only Vercel config. The page is `index.html`, so `/` serves it. There is no deploy step in the dataset pipeline. If an existing Vercel project still uses the repository root or `site/`, change its root directory to `natural-history` before the next deploy.
