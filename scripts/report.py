import pandas as pd
M=pd.read_csv('adcom_full_pivotal.csv',dtype=str).fillna('')
X=pd.read_csv('excluded.csv',dtype=str).fillna('')
T=pd.read_csv('two_by_two.csv'); E=pd.read_csv('daval_shortfall_explained.csv'); R=pd.read_csv('reconcile_vs_out.csv')
L=[]; p=L.append
p('# FDA AdCom pivotal-vote dataset: final report (scope 2016-11-04 to 2026)\n')
p(f'Generated {pd.Timestamp.now():%Y-%m-%d %H:%M} ET. Files are in the data root (this folder). Main table: adcom_full_pivotal.csv / adcom_full.xlsx ({len(M)} product-meeting rows). Excluded sheet: excluded.csv ({len(X)} rows, each with a reason). Gaps: 0.\n')
p('## Counts by committee\n'); bc=M.groupby('committee').agg(rows=('app','size'),press_votes=('vote_source_tier',lambda s:(s=="press").sum()),outcome_press_or_company=('outcome_source_tier',lambda s:s.isin(["press","SEC/company"]).sum())).sort_values('rows',ascending=False); p(bc.to_markdown()+'\n')
p('## Verification rate by field\n')
for c,lab in [('vote_source_tier','Vote'),('outcome_source_tier','Final outcome'),('orphan_for_indication','Orphan status for the indication'),('priority_basis','Review priority basis')]:
    v=M[c].value_counts(); p(f'**{lab}**: '+', '.join(f'{k} {n} ({n/len(M):.0%})' for k,n in v.items())+'\n')
p(f"Review priority values: {M.review_priority.value_counts().to_dict()}. The three unverified rows are nicotine mouth spray, Tookad, and AR19. Their submission and goal dates do not pick one anniversary.\n")
p(f"1-year outcome: {M.action_at_1yr.value_counts().to_dict()}. 'unverified' at 1 year means the approval date is known only to the month, or the decision is still pending inside the window.\n")
p('## 2x2 tables: adcom vote vs FDA outcome (ties and superseded meetings removed; unverified counts shown)\n'); p(T.to_markdown(index=False)+'\n')
p('## Corrections 2026-11-04\n'); A=pd.read_csv('orphan_audit_2026-11-04.csv',dtype=str).fillna(''); p(A[['meeting_date','brand','app','old','new','basis']].to_markdown(index=False)+'\n'); p('vote_type counts: '+str(M.vote_type.value_counts().to_dict())+'. center: '+str(M.center.value_counts().to_dict())+'. CGT rows: '+str((M.CGT=='True').sum())+'.\n')
p('## Still press-only votes (no FDA minutes or transcript found)\n'); p(M[M.vote_source_tier=='press'][['meeting_date','committee','brand','generic','vote_yes','vote_no']].to_markdown(index=False)+'\n')
p('Teplizumab: an FDA review (761183Orig1s000OtherR) confirms that "the majority" voted favourably, which supports the direction of the vote but not the exact count. Romosozumab, Descovy and tanezumab: FDA review PDFs were image-only or did not contain the tally.\n')
p('## Outcomes sourced from press or company statements only\n'); p(M[M.outcome_source_tier.isin(['press','SEC/company'])][['meeting_date','brand','generic','final_action','final_action_date']].to_markdown(index=False)+'\n')
p('## Orphan status: unresolved\n'); p(M[M.orphan_for_indication.isin(['review','unverified'])][['meeting_date','committee','app','brand','product_text']].to_markdown(index=False)+'\n')
p('''## Decisions on the wrong-question rows (item 4)
- Tavneos 2021-05-06: switched to the benefit-risk vote, 10-8 (FDA minutes). The efficacy vote was 9-9.
- Ocaliva 2024-09-13: switched to the benefit-risk vote, 1-10-3 (media/182630). The clinical-benefit vote was 1-13.
- Zelnorm 2018-10-17: kept 11-1 ("reintroduction supported").
- Entresto 2020-12-15: kept 12-1 ("ANY indication").
- Lynparza 2023-04-28: kept 11-1, but this was a vote to restrict the indication, not an approve/reject vote. Flagged as favourable-restricted.
- Lumakras 2023-10-05: kept 2-10 as a proxy. The only vote was on whether PFS could be interpreted. Flagged.
- Aduhelm 2020-11-06: pivotal set to 0-10-1 (final question, Study 302 as primary evidence). Q1 was 1-8-2 and is noted on the row (media/145690).

## Reconciliation with the hand-verified data (out/, 2016-11 onward)
''')
p(R.to_markdown(index=False)+'\n')
p('- Leqembi is present (app 761269). It shows as MISSING above only because of the "/S-001" suffix in the key.\n- Translarna: the minutes give A:0 / B:10 / C:1. We code C ("sufficient to conclude effective") as yes, which gives 1-10. The out/ data treats C as an abstain, giving 0-10-1. This is a coding choice, not a data error.\n- PCNS: all 8 present (Translarna, Epidiolex, Aduhelm, Relyvrio x2, Qalsody, Leqembi, Kisunla), plus the joint Rexulti PDAC+PCNS row. CGT: Luxturna, Skysona, Zynteglo, Elevidys, NurOwn, Lantidra, deramiocel and Tudriqev (now added: 10-3, FDA SBRA media/194230) are present, and Kymriah, Ryoncil, Carvykti and Abecma are flagged CGT (12 CGT rows).\n')
p('## Shortfall vs Daval, 2016-2021 (daval_shortfall_explained.csv has one row per year x committee)\n')
g=E.groupby('committee')[['daval_meetings','ours_product_vote_rows','ours_excluded','pre_window_2016','residual_shortfall','residual_after_prewindow']].sum(); p(g.to_markdown()+'\n')
p(f'''Totals: Daval {E.daval_meetings.sum()} meetings. We have {E.ours_product_vote_rows.sum()} product-vote rows and {E.ours_excluded.sum()} excluded meetings. {E.pre_window_2016.sum()} of Daval's 2016 meetings fall before 2016-11-04, outside our scope. That leaves a net {E.residual_after_prewindow.sum()} unexplained.
- PCAC accounts for 7: compounding-list meetings, not NDA/BLA approvals.
- AADPAC/DSaRM joint meetings are attributed differently: AADPAC is +16 and DSaRM is -10 (net 6).
- The remainder (roughly 6-10, mostly ODAC, EMDAC and AAC) has not been identified meeting by meeting. Daval publishes counts only, not a meeting list, so a true row-by-row match is not possible. Likely causes are multi-day meetings counted per day and class or policy sessions with no NDA/BLA in the Federal Register notice.
''')
p('''## What changed this stage
- Fixed a bug in final.py where curated "add" rows overwrote existing rows (index collision). This raised the row count from 121 to 155. Curated rows that duplicated an existing meeting/app are now merged instead of added.
- All 68 gap meetings resolved:
  - 30 gap meetings became rows (gap_votes.csv: 12 FDA-sourced, the rest press).
  - About 32 were moved to excluded with a reason (gap_excl.csv: no vote, cancelled, class review, IND, duplicate).
  - The remaining gaps duplicated existing rows.
- All 38 unverified outcomes are now sourced. Supplements are matched by supplement number in openFDA and checked against the FDA approval letter text (ltr/). CBER outcomes come from FDA BLA approval lists and letters. The rest are press or company statements, flagged as such.
- Added orphan_for_indication: OOPD designation keyword-matched to the indication, hand-verified values carried over from legacy rows, and 26 weak matches adjudicated (orphan_adj.csv).
- Added vote_source_tier and outcome_source_tier columns.

## Not done / caveats
- Press votes (list above) could not be confirmed against FDA documents. The fda.gov committee pages return 404, and the review PDFs found were image-only.
- The waiter loops chained after mscan/ait matched their own command lines and could never finish, so they were killed. mscan.py (144000–196000) has since finished, but the 118000–144000 range and ait2 never ran. With gaps at 0, those runs are optional. The pipeline was rerun manually.
- Pre-2016-11 rows stay in sheet pre_2016-11_not_curated and were not worked further.
''')
open('REPORT.md','w').write('\n'.join(L))
