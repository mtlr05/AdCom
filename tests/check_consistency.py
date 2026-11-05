"""Asserts the CSV, xlsx, two_by_two.csv and the chart inputs agree. Run from the data root (scripts dir on sys.path)."""
import os,sys,pandas as pd
sys.path.insert(0,os.environ.get('ADCOM_SCRIPTS','.'))
from chart2x2 import load,tables
CH=os.environ.get('CHART_DIR','charts'); fails=[]
def ok(c,msg): (None if c else fails.append(msg)); print(('PASS ' if c else 'FAIL ')+msg)
M=pd.read_csv('adcom_full_pivotal.csv',dtype=str).fillna('')
X=pd.read_excel('adcom_full.xlsx','meetings_pivotal',dtype=str).fillna('')
ok(len(M)==len(X),f'row count csv {len(M)} == xlsx {len(X)}')
for c in ['meeting_date','app','adcom','final_action','orphan_for_indication','review_priority','center','CGT','vote_type']:
    ok(list(M[c])==[str(v) for v in X[c]],f'column {c} identical csv vs xlsx')
ok(set(M.orphan_for_indication)<= {'Y','N','review','unverified'},'orphan values in {Y,N,review,unverified}')
ok((M.center.isin(['CDER','CBER'])).all(),'center filled CDER/CBER on every row')
ok(set(M.opioid)<= {'Y','N'},'opioid is Y or N on every row')
ok((M.opioid!='').all(),'opioid has no blank')
ok((M[M.CGT=='True'].center=='CBER').all(),'all CGT rows are CBER')
ok(M[M.committee.str.contains('CTGTAC')].CGT.eq('True').all(),'all CTGTAC rows flagged CGT')
FO=pd.read_csv('field_overrides.csv',dtype=str).fillna('')
for _,o in FO.iterrows():
    r=M[(M.meeting_date==o.meeting_date)&(M.app.str.lstrip('0')==o.app.lstrip('0'))]
    ok(len(r)==1 and r.iloc[0][o.field]==o.value,f'override applied {o.meeting_date} {o.app} {o.field}')
man=FO[FO.field.isin(['orphan_for_indication','review_priority','brand'])]
ok((man.source.str.contains('http')).all(),'every manual orphan/priority/brand change cites a URL')
T=pd.read_csv('two_by_two.csv'); T=T[T.outcome=='final'].set_index('subset')
key={'1) Common diseases (not orphan)':'Common (orphan N)','2) Rare diseases (orphan)':'Rare (orphan Y)','3) Rare and priority review':'Rare + priority','4) Aggregate (all)':'All'}
for ap,pre in [(False,''),(True,'Approval-only: ')]:
    res=tables(load(approval_only=ap)[1])
    for k,sub in key.items():
        if ap: sub={'Common (orphan N)':'Approval-only: Common','Rare (orphan Y)':'Approval-only: Rare','Rare + priority':'Approval-only: Rare + priority','All':'Approval-only: All'}[sub]
        t=T.loc[sub]; r=res[k]
        ok((r['AA'],r['AR'],r['RA'],r['RR'])==(t.FavApproved,t.FavNotApproved,t.UnfavApproved,t.UnfavNotApproved),f'chart cells == two_by_two [{sub}]')
for ap,sub in [(False,'CGT (CTGTAC + CAR-T/MSC)'),(True,'Approval-only: CGT')]:
    r=tables(load(cgt=True,approval_only=ap)[1])['4) Aggregate (all)']; t=T.loc[sub]
    ok((r['AA'],r['AR'],r['RA'],r['RR'])==(t.FavApproved,t.FavNotApproved,t.UnfavApproved,t.UnfavNotApproved),f'CGT chart cells == two_by_two [{sub}]')
X2=pd.read_excel('adcom_full.xlsx','2x2'); ok(len(X2)==len(pd.read_csv('two_by_two.csv')) and (X2.FavApproved.values==pd.read_csv('two_by_two.csv').FavApproved.values).all(),'xlsx 2x2 sheet == two_by_two.csv')
csvt=os.path.getmtime('adcom_full_pivotal.csv')
for f in ['all_2x2_counts_v8.png','all_2x2_pct_v8.png','cgt_2x2_pct_v5.png','all_2x2_counts_approvalonly_v8.png','all_2x2_pct_approvalonly_v8.png','cgt_2x2_pct_approvalonly_v6.png','cgt_validation_table_v5.pdf','cgt_priority_review_table_v5.pdf']:
    p=os.path.join(CH,f); ok(os.path.exists(p) and os.path.getmtime(p)>=csvt,f'{f} exists and is newer than CSV')
print('FAILURES:',len(fails)); sys.exit(1 if fails else 0)
