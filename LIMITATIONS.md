# LIMITATIONS

- **Selection bias**: FDA convenes adcoms when uncertain; rates are not general approval probabilities. Cells are small (rare+priority, CGT): do not over-read percentages.
- **Press-sourced fields**: 19 votes and ~43 outcomes rest on press/company/SEC statements (`vote_source_tier`, `outcome_source_tier`). Tzield 10-7, Skysona and Zynteglo tallies are press-only; romosozumab, Descovy, tanezumab FDA PDFs lacked tallies.
- **Orphan**: keyword matching to OOPD plus hand adjudication; 2 rows are `review` (Darzalex Faspro SMM, Tudriqev). OOPD designations for other sponsors' products of the same ingredient are not counted (e.g. buprenorphine OUD).
- **Priority**: 50+ rows `unverified` (unapproved products, CBER biologics, untagged supplements). Ryoncil, Carvykti, Abecma, NurOwn unverified; Deramiocel/Tudriqev unverified for the resubmission reviewed.
- **Vote type** is a judgement on question wording (see `vote_type_basis`); Elevidys (accelerated-approval benefit-risk) and Zelnorm (reintroduction/safety) coded approval and flagged.
- **Ryoncil** uses FDA-recorded 8-2 although one voter reportedly changed their vote (press: 9-1).
- **Coverage**: 19 meetings vs Daval 2016-2021 unexplained; Daval gives counts only.
- **Crawl stage not reproducible offline**: `scripts/crawl/` needs fda.gov / Wayback / Archive-It / Federal Register / openFDA access; its outputs (`meetings.pkl`, caches) are shipped. Raw PDF/HTML caches (~250MB) are not shipped: see `data/cache/large_cache_manifest.csv` and `scripts/fetch_cache.py` (re-downloads the minutes for all rows; URLs in `data/cache/minutes_urls.csv`). Extracted minutes text for the rows is shipped in `data/cache/minutes_txt/`.
- `scripts/crawl/` scripts may reference absolute `/workspace/...` paths from the original environment; they were not refactored.
