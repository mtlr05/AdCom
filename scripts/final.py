import pandas as pd,numpy as np,json,re,datetime,os
M=pd.read_pickle('meetings.pkl'); G=pd.read_pickle('gaps.pkl'); X=pd.read_pickle('excluded.pkl')
# ---- legacy merge (PCNS/CTGTAC hand-verified rows from earlier build)
ROOT=os.environ.get('ADCOM_ROOT',os.getcwd())
LEGACY_XLSX=os.environ.get('ADCOM_LEGACY_XLSX',os.path.join(ROOT,'inputs','adcom_dataset.xlsx') if os.path.exists(os.path.join(ROOT,'inputs','adcom_dataset.xlsx')) else '/workspace/adcom/out/adcom_dataset.xlsx')
CGT_CSV=os.environ.get('ADCOM_CGT_CSV',os.path.join(ROOT,'inputs','cgt_check.csv') if os.path.exists(os.path.join(ROOT,'inputs','cgt_check.csv')) else '/workspace/adcom/cgt_check/cgt_check.csv')
L=pd.read_excel(LEGACY_XLSX,'pivotal_only')
leg=[]
for _,r in L.iterrows():
    k=(r.committee,str(r.meeting_date)[:10])
    hit=M[(M.committee==k[0])&(M.meeting_date==k[1])]
    rec=dict(meeting_date=k[1],committee=r.committee,app=str(r.application_number),brand=r.product_brand,generic=r.product_generic,product_text=r.product_brand,
        question_text=r.question_text,vote_yes=r.vote_yes,vote_no=r.vote_no,vote_abstain=r.vote_abstain,voting_member_count=(r.vote_yes or 0)+(r.vote_no or 0)+(r.vote_abstain or 0),
        adcom='favourable' if r.vote_yes>r.vote_no else ('tie' if r.vote_yes==r.vote_no else 'unfavourable'),
        final_action='approved' if str(r.fda_action).startswith('approv') else str(r.fda_action),final_action_date=str(r.fda_action_date)[:10],
        review_priority=r.review_priority,orphan_designation_any=r.orphan_designated_indication,orphan_verification='legacy dataset: '+str(r.orphan_source),
        minutes_url=r.sources,meeting_type='supplemental' if 'suppl' in str(r.application_type).lower() or str(r.application_type).startswith('s') else 'initial application',
        CNS=r.committee=='PCNS',CGT=r.committee=='CTGTAC',center=r.center,decision_source=r.fda_action_source,source='legacy verified-vote row (out/adcom_dataset.xlsx)',pivotal_rule='legacy: analyst-chosen pivotal question')
    if len(hit)==0: leg.append(rec)
    else:
        i=hit.index[0]
        for f in ['final_action','final_action_date','review_priority','orphan_designation_any','orphan_verification','brand']:
            if str(M.at[i,f]) in ('unverified','','nan','None') and str(rec[f]) not in ('nan',''): M.at[i,f]=rec[f]; M.at[i,'source']=str(M.at[i,'source'])+f'; {f} from legacy'
M=pd.concat([M,pd.DataFrame(leg)],ignore_index=True)
# cgt_check adcom rows not present
C=pd.read_csv(CGT_CSV)
for _,r in C[C.adcom_held.astype(str).str.startswith('Y')].iterrows():
    dt=str(r.meeting_date)[:10]
    if ((M.meeting_date==dt)).any(): continue
    m=re.findall(r'\d+',str(r.votes_yes_no_abst))
    if len(m)<2: X.loc[len(X)]=dict(committee=r.committee,meeting_date=dt,reason='CGT check: adcom held, no product vote ('+str(r.notes)[:120]+')',minutes_url=r.evidence_url,n_votes=0,first_question=''); continue
    y,n=int(m[0]),int(m[1]); a=int(m[2]) if len(m)>2 else 0
    M.loc[len(M)]=dict(meeting_date=dt,committee=r.committee,product_text=r['product'],brand=r['product'],vote_yes=y,vote_no=n,vote_abstain=a,voting_member_count=y+n+a,adcom='favourable' if y>n else 'unfavourable',
        final_action='approved' if 'pprov' in str(r.fda_action) and 'reject' not in str(r.fda_action).lower() else str(r.fda_action),final_action_date=str(r.action_date),minutes_url=r.evidence_url,CGT=True,CNS=False,center='CBER',
        meeting_type='initial application',orphan_designation_any=str(r.orphan),source='cgt_check row (SBRA/minutes/press; see notes): '+str(r.notes)[:150],pre_2010=dt<'2010',pivotal_rule='cgt_check: efficacy/approval question')
exm=M.meeting_type.astype(str).str.startswith('EXCLUDE')
for _,r in M[exm].iterrows(): X.loc[len(X)]=dict(committee=r.committee,meeting_date=r.meeting_date,reason='marketed product, notice names no new/supplemental application (safety/other): '+str(r.get('brand','')),minutes_url=r.minutes_url,n_votes=1,first_question=str(r.question_text)[:300])
M=M[~exm].copy()
dup=M.duplicated(['meeting_date','app'])&M.app.astype(str).str.len().gt(3)
M=M[~dup].copy()
M['pre_2010']=M.meeting_date<'2010-01-01'
M['year']=M.meeting_date.str[:4]
# ---- known fixes
def fix(cond,**kw):
    for k,v in kw.items(): M.loc[cond,k]=v
b=M.brand.astype(str).str.lower()+' '+M.product_text.astype(str).str.lower()
fix(b.str.contains('amyvid|florbetapir'),action_at_1yr='not approved within 1 yr',final_action='approved',final_action_date='2012-04-06',notes='Fix1: CRL 2011, approved 2012-04-06; 1-yr=not approved, final=approved')
fix(b.str.contains('lemtrada|alemtuzumab'),meeting_type='initial application',notes='Fix2: Lemtrada coded as initial MS application (Daval-consistent); BLA 103948 is Campath supplement-type in records - flagged')
rely=b.str.contains('relyvrio|amx0035|sodium phenylbutyrate')&(M.meeting_date<'2022-06-01')
fix(rely,replaced_by_later_meeting=True,notes='Fix3: superseded by 2022-09-07 PCNS vote; excluded from concordance')
M['replaced_by_later_meeting']=M.get('replaced_by_later_meeting',False).fillna(False).astype(bool)
# action_at_1yr fill
def a1(r):
    if str(r.get('action_at_1yr')) not in ('nan','None',''): return r['action_at_1yr']
    if r['final_action']=='approved':
        try: return 'approved' if (datetime.date.fromisoformat(str(r['final_action_date'])[:10])-datetime.date.fromisoformat(r['meeting_date'])).days<=365 else 'not approved within 1 yr'
        except: return 'unverified'
    return 'unverified' if str(r['final_action'])in('unverified','nan') else 'not approved within 1 yr'
M['action_at_1yr']=M.apply(a1,axis=1)
M['approved_final']=M.final_action.astype(str).str.startswith('approved').where(~M.final_action.astype(str).isin(['unverified','nan','pending','Pending']))
M['approved_1yr']=(M.action_at_1yr=='approved').where(M.action_at_1yr!='unverified')
M=M.sort_values(['meeting_date','committee']).reset_index(drop=True)
# ---- curated overrides (manual, sourced) ----
M['curated_source']='';M['curated_adcom']=''
if os.path.exists('curated.csv'):
    C=pd.read_csv('curated.csv',dtype=str).fillna(''); M=M.astype(object)
    for _,c in C.iterrows():
        sel=(M.meeting_date==c.meeting_date)&(M.committee==c.committee)
        if c.get('app',''): sel&=M.app.astype(str).str.lstrip('0').str.contains(c.app.lstrip('0'),regex=False)
        if c.action=='drop':
            X=pd.concat([X,pd.DataFrame([dict(meeting_date=c.meeting_date,committee=c.committee,app=c.app,reason='curated: '+c.notes+' | '+c.curated_source)])],ignore_index=True)
            M=M[~sel]; continue
        if c.action!='add' and sel.sum()==0:
            print('CURATED UNMATCHED',c.meeting_date,c.committee,c.app); continue
        if c.action=='add' and c.app:
            _ex=(M.meeting_date==c.meeting_date)&(M.app.astype(str).str.lstrip('0')==c.app.lstrip('0'))
            if _ex.any():
                sel=_ex; M.loc[sel,'committee']=c.committee; M.loc[sel,'source']=M.loc[sel,'source'].astype(str)+' + curated'
                c=c.copy(); c['action']='override'
        if c.action=='add':
            _ni=(M.index.max()+1) if len(M) else 0; M.loc[_ni]={k:'' for k in M.columns}; sel=M.index==_ni
            M.loc[sel,['meeting_date','committee','app']]=[c.meeting_date,c.committee,c.app]
            M.loc[sel,'source']='curated'
        for k in ['brand','generic','meeting_type','question_text','vote_yes','vote_no','vote_abstain','adcom','action_at_1yr','final_action','final_action_date','decision_source','review_priority','orphan_designation_any','orphan_match','minutes_url','notes']:
            if k in c and c[k]!='': M.loc[sel,k]=c[k]
        if c.get('final_action',''): M.loc[sel,'decision_source']='curated: '+(c.get('decision_source','') or c.curated_source)
        if c.get('vote_yes',''): M.loc[sel,'pivotal_rule']='curated: '+c.get('pivotal_note','analyst-chosen approval question')
        if c.get('review_priority',''): M.loc[sel,'review_priority']=c.review_priority
        if c.get('vote_yes','') or c.action=='add': M.loc[sel,'curated_source']=c.curated_source
        if c.get('adcom',''): M.loc[sel,'curated_adcom']=c.adcom
    for k in ['vote_yes','vote_no','vote_abstain']: M[k]=pd.to_numeric(M[k],errors='coerce')
    M['CNS']=M.committee.isin(['PCNS','PDAC','PDAC+PCNS']); M['CGT']=M.committee.str.contains('CTGTAC')
    M['year']=M.meeting_date.str[:4]; M['pre_2010']=M.meeting_date<'2010-01-01'
    M=M.sort_values(['meeting_date','committee']).reset_index(drop=True)
WINDOW='2016-11-04'
OLD=M[M.meeting_date<WINDOW].copy(); M=M[M.meeting_date>=WINDOW].copy()
M['action_at_1yr']=M.apply(a1,axis=1)
_vy=pd.to_numeric(M.vote_yes,errors='coerce'); _vn=pd.to_numeric(M.vote_no,errors='coerce')
M['adcom']=np.where(M.curated_adcom.astype(str)!='',M.curated_adcom,np.where(_vy.isna(),M.adcom,np.where(_vy>_vn,'favourable',np.where(_vy==_vn,'tie','unfavourable'))))
M['voting_member_count']=_vy.fillna(0)+_vn.fillna(0)+pd.to_numeric(M.vote_abstain,errors='coerce').fillna(0)
M['approved_final']=M.final_action.astype(str).str.lower().str.startswith('approved').where(~M.final_action.astype(str).str.lower().isin(['unverified','nan','pending','']))
M['approved_1yr']=(M.action_at_1yr=='approved').where(~M.action_at_1yr.isin(['unverified','pending']))
if os.path.exists('curated.csv'):
    def _cov(r):
        for _,c in C.iterrows():
            try: dd=abs((datetime.date.fromisoformat(str(r.meeting_date))-datetime.date.fromisoformat(c.meeting_date)).days)
            except: continue
            if dd<=3 and c.app and str(r.app).lstrip('0')==c.app.lstrip('0'): return True
        return False
    G=G[~G.apply(_cov,axis=1)] if len(G) else G
if os.path.exists('gap_excl.csv'):
    GE=pd.read_csv('gap_excl.csv',dtype=str).fillna('')
    def _ge(r):
        for _,e in GE.iterrows():
            try: dd=abs((datetime.date.fromisoformat(str(r.meeting_date))-datetime.date.fromisoformat(e.meeting_date)).days)
            except: continue
            if dd<=1 and str(r.committee).split('+')[0] in e.committee+'+'+str(r.committee) and (not e.app or not str(r.app) or str(r.app).lstrip('0')==e.app.lstrip('0')): return e.reason+' | '+e.source
        return ''
    if len(G):
        _r=G.apply(_ge,axis=1); mv=G[_r!=''].copy(); mv['reason']='gap resolved: '+_r[_r!='']
        X=pd.concat([X,mv],ignore_index=True); G=G[_r=='']
if len(G):
    _k=set(zip(M.meeting_date.astype(str),M.app.astype(str).str.lstrip('0')))
    G=G[~G.apply(lambda r:(str(r.meeting_date),str(r.app).lstrip('0')) in _k,axis=1)]
G=G[G.meeting_date.astype(str)>=WINDOW]; X=X[X.meeting_date.astype(str)>=WINDOW] if len(X) else X
# Solithromycin 2016-11-04 was filed under excluded as "no NDA/BLA". The transcript
# (fda.gov/media/102423) is a product benefit-risk vote, now a curated pivotal row.
if len(X):
    X=X[~((X.meeting_date.astype(str)=='2016-11-04')&(X.committee.astype(str)=='AMDAC')&(X.reason.astype(str).str.startswith('no NDA/BLA')))].copy()
# verification flags
def _tier(x):
    x=str(x); l=x.lower()
    if not x or x in('unverified','nan'): return 'unverified'
    if 'press' in l: return 'press'
    if 'sec.gov' in l or 'sec 8-k' in l or 'company' in l: return 'SEC/company'
    if 'fda' in l or 'minutes' in l or 'federalregister' in l: return 'FDA'
    if 'http' in l: return 'press'
    return 'other'
import orphan_ind
_o=orphan_ind.run(M.fillna('').astype(str)); M['orphan_for_indication']=[x[0] for x in _o]; M['orphan_indication_basis']=[x[1] for x in _o]
if os.path.exists('orphan_adj.csv'):
    for _,o in pd.read_csv('orphan_adj.csv',dtype=str).fillna('').iterrows():
        s_=(M.meeting_date==o.meeting_date)&(M.app.astype(str)==o.app)
        M.loc[s_,'orphan_for_indication']=o.orphan_for_indication; M.loc[s_,'orphan_indication_basis']=o.note
_leg=M.source.astype(str).str.contains('legacy|cgt_check')&M.orphan_designation_any.astype(str).str.upper().str[:1].isin(['Y','N'])
M.loc[_leg,'orphan_for_indication']=M.loc[_leg,'orphan_designation_any'].astype(str).str.upper().str[:1]; M.loc[_leg,'orphan_indication_basis']='hand-verified (legacy out/ or cgt_check)'
# review priority from openFDA when missing
import json as _j,re as _re
def _prio(r):
    p=str(r.review_priority).upper()
    if p in ('PRIORITY','STANDARD'): return p,'existing'
    fn='ofda/'+str(r.app).lstrip('0').zfill(6)+'.json'
    if not str(r.app).strip('0') or not os.path.exists(fn): return 'unverified','no openFDA record (BLA at CBER or unapproved)'
    d=_j.load(open(fn)); subs=d.get('submissions',[])
    m=_re.search(r'S-0*(\d+)',str(r.final_action))
    if m:
        for s in subs:
            if s['submission_type']=='SUPPL' and s['submission_number']==m.group(1) and s.get('review_priority') in('PRIORITY','STANDARD'): return s['review_priority'],'openFDA supplement S-'+m.group(1)
    if 'supplement' not in str(r.meeting_type).lower():
        for s in subs:
            if s['submission_type']=='ORIG' and s.get('review_priority') in('PRIORITY','STANDARD'): return s['review_priority'],'openFDA ORIG'
    return 'unverified','supplement not matched in openFDA'
_p=M.apply(_prio,axis=1); M['review_priority']=[x[0] for x in _p]; M['priority_basis']=[x[1] for x in _p]
# ===== 2026-11-04 corrections: center, CGT, vote_type, field overrides (applied last) =====
CBER_APPS={'125646':'KYMRIAH tisagenlecleucel (CAR-T, CBER OTP)','125706':'RYONCIL remestemcel-L (MSC therapy, CBER OTP)','125746':'CARVYKTI cilta-cel (CAR-T, CBER OTP)','125736':'ABECMA ide-cel (CAR-T, CBER OTP)'}
CGT_APPS={'125646','125706','125746','125736'}
def _center(r):
    a=str(r.app).lstrip('0').split('/')[0]
    if str(r.committee) in ('CTGTAC','VRBPAC'): return 'CBER','CBER committee ('+str(r.committee)+')'
    if a in CBER_APPS: return 'CBER',CBER_APPS[a]
    fn='ofda/'+a.zfill(6)+'.json'
    if a and os.path.exists(fn) and _j.load(open(fn)).get('submissions'): return 'CDER','listed in Drugs@FDA/openFDA (CDER-regulated products only)'
    if a and len(a)==6 and a.startswith('761'): return 'CDER','761xxx BLA number series is CDER-assigned'
    if a and not a.startswith('125'): return 'CDER','NDA (CDER)'
    return 'CDER','CDER committee; no CBER product identified'
_c=M.apply(_center,axis=1); M['center']=[x[0] for x in _c]; M['center_basis']=[x[1] for x in _c]
M['CGT']=M.committee.astype(str).str.contains('CTGTAC')|M.app.astype(str).str.lstrip('0').isin(CGT_APPS)
def _vt(q):
    q=str(q).lower(); k=q.rfind('vote:'); q=q[k:] if k>=0 else q
    if re.search(r'restrict|be delayed|deferred|prior to a final regulatory|applicab|reliably interpreted|surrogate|reasonably likely to predict|in label',q): return 'restriction/other'
    eff=re.search(r'effective|effectiveness|efficacy|clinical benefit|improves|clinically meaningful',q)
    br=re.search(r'benefit.{0,40}risk|risk.{0,10}benefit|outweigh|safety|approv|licensure|support (its )?use',q)
    if eff and not br: return 'effectiveness-only'
    return 'approval/benefit-risk'
M['vote_type']=M.question_text.map(_vt); M['vote_type_basis']='rule on question_text'
M['orphan_pre_override']=M.orphan_for_indication.astype(str)
if os.path.exists('field_overrides.csv'):
    for _,o in pd.read_csv('field_overrides.csv',dtype=str).fillna('').iterrows():
        s_=(M.meeting_date.astype(str)==o.meeting_date)&(M.app.astype(str).str.lstrip('0')==o.app.lstrip('0'))
        if s_.sum()!=1: print('FIELD OVERRIDE UNMATCHED',o.meeting_date,o.app,o.field,s_.sum()); continue
        M.loc[s_,o.field]=o.value
        if o.field=='vote_type': M.loc[s_,'vote_type_basis']='curated: '+o.source
        if o.field=='center': M.loc[s_,'center_basis']='curated: '+o.source
    _ch=M[M.orphan_pre_override!=M.orphan_for_indication.astype(str)]
    _fo=pd.read_csv('field_overrides.csv',dtype=str).fillna(''); _fo=_fo[_fo.field=='orphan_indication_basis']
    aud=[]
    for _,o in _fo.iterrows():
        s_=(M.meeting_date.astype(str)==o.meeting_date)&(M.app.astype(str).str.lstrip('0')==o.app.lstrip('0'))
        r=M[s_].iloc[0]; aud.append(dict(meeting_date=r.meeting_date,committee=r.committee,app=r.app,brand=r.brand or r.product_text,old=r.orphan_pre_override,new=r.orphan_for_indication,changed=r.orphan_pre_override!=r.orphan_for_indication,basis=r.orphan_indication_basis,source=o.source))
    pd.DataFrame(aud).to_csv('orphan_audit_2026-11-04.csv',index=False)
M['verified_vote']=np.where(M.curated_source.astype(str)!='','curated: '+M.curated_source.astype(str),np.where(M.source.astype(str).str.startswith('automated'),'parsed from FDA minutes (regex); pivotal question by rule',np.where(M.source.astype(str).str.startswith('legacy'),'read from FDA minutes (legacy)', 'cgt_check: see source')))
M['verified_outcome']=np.where(M.final_action.astype(str).isin(['unverified','nan','']),'unverified',np.where(M.decision_source.astype(str).str.startswith('curated'),M.decision_source.astype(str),np.where(M.decision_source.astype(str).str.contains('openFDA absence'),'openFDA absence-based (weaker)',np.where(M.decision_source.astype(str).str.contains('openFDA'),'openFDA',np.where(M.final_action.astype(str)=='unverified','unverified','legacy/cgt_check (mixed: memory/press flagged there)')))))
M['vote_source_tier']=M.verified_vote.map(_tier); M['outcome_source_tier']=np.where(M.verified_outcome=='unverified','unverified',np.where(M.verified_outcome.str.startswith('openFDA'),'FDA (openFDA)',M.verified_outcome.map(_tier)))
M['verified_orphan']=M.orphan_verification.fillna('unverified')
cols=['meeting_date','year','committee','center','app','brand','generic','product_text','meeting_type','pre_2010','question_text','vote_yes','vote_no','vote_abstain','voting_member_count','adcom','pivotal_rule','polarity_check',
 'action_at_1yr','final_action','final_action_date','decision_source','review_priority','orphan_designation_any','orphan_match','CNS','CGT','replaced_by_later_meeting','n_products_same_meeting',
 'minutes_url','minutes_title','fr_notice','fr_snippet','orphan_for_indication','orphan_indication_basis','priority_basis','center_basis','vote_type','vote_type_basis','verified_vote','vote_source_tier','verified_outcome','outcome_source_tier','verified_orphan','source','curated_source','notes']
for c in cols:
    if c not in M: M[c]=''
M=M[cols]; OLD=OLD[[c for c in cols if c in OLD]]
# ---- 2x2
M['replaced_by_later_meeting']=M.replaced_by_later_meeting.map(lambda v: v is True or str(v)=='True')
S=M[(~M.replaced_by_later_meeting)&(M.adcom!='tie')]
def two(df,col):
    d=df[df[col].notna()]
    t=pd.crosstab(d.adcom,d[col].map({True:'FDA approved',False:'FDA not approved'}))
    return t
tabs=[]
subs={'All':S,'Rare (orphan Y)':S[S.orphan_for_indication.astype(str).str.upper().str.startswith('Y')],'Common (orphan N)':S[S.orphan_for_indication.astype(str).str.upper().str.startswith('N')],
'Priority':S[S.review_priority.astype(str).str.upper().str.startswith('PRI')],'Standard':S[S.review_priority.astype(str).str.upper().str.startswith('STA')],'CNS (PCNS/PDAC)':S[S.CNS==True],'CGT (CTGTAC + CAR-T/MSC)':S[S.CGT==True],'Rare + priority':S[S.orphan_for_indication.astype(str).str.upper().str.startswith('Y')&S.review_priority.astype(str).str.upper().str.startswith('PRI')],
'Approval-only: All':S[S.vote_type=='approval/benefit-risk'],'Approval-only: Common':S[(S.vote_type=='approval/benefit-risk')&S.orphan_for_indication.astype(str).str.upper().str.startswith('N')],'Approval-only: Rare':S[(S.vote_type=='approval/benefit-risk')&S.orphan_for_indication.astype(str).str.upper().str.startswith('Y')],'Approval-only: Rare + priority':S[(S.vote_type=='approval/benefit-risk')&S.orphan_for_indication.astype(str).str.upper().str.startswith('Y')&S.review_priority.astype(str).str.upper().str.startswith('PRI')],'Approval-only: CGT':S[(S.vote_type=='approval/benefit-risk')&(S.CGT==True)],
'2016-11-04..2021 (Daval overlap)':S[S.meeting_date<='2021-12-31']}
for name,df in subs.items():
    for col,lab in [('approved_final','final'),('approved_1yr','1yr')]:
        pass
for name,df in subs.items():
    df=df.copy(); df['approved_final']=M.loc[df.index,'final_action'].astype(str).str.startswith('approved').where(~M.loc[df.index,'final_action'].astype(str).isin(['unverified','nan','']) & ~M.loc[df.index,'final_action'].astype(str).str.lower().str.startswith('pending'))
    df['approved_1yr']=(df.action_at_1yr=='approved').where(~df.action_at_1yr.astype(str).isin(['unverified','','nan']) & ~df.action_at_1yr.astype(str).str.startswith('pending'))
    for col,lab in [('approved_final','final'),('approved_1yr','1yr')]:
        d=df[df[col].notna()]
        g=lambda a,b:int(((d.adcom==a)&(d[col]==b)).sum())
        tabs.append(dict(subset=name,outcome=lab,n=len(d),FavApproved=g('favourable',True),FavNotApproved=g('favourable',False),UnfavApproved=g('unfavourable',True),UnfavNotApproved=g('unfavourable',False),
            outcome_unverified=int(df[col].isna().sum())))
T=pd.DataFrame(tabs)
# ---- coverage vs Daval
D=pd.read_csv('daval_etable1.csv').set_index('year')
cov=[]
for y in [y for y in D.index if y>=2016]:
    for c in D.columns:
        ours=M[(M.year==str(y))&(M.committee==c)].meeting_date.nunique()
        gap=G[(G.meeting_date.astype(str).str[:4]==str(y))&(G.committee==c)].meeting_date.nunique()
        ex=X[(X.meeting_date.astype(str).str[:4]==str(y))&(X.committee==c)].meeting_date.nunique() if len(X) else 0
        cov.append(dict(year=y,committee=c,daval_all_meetings=int(D.at[y,c]),ours_product_vote_meetings=ours,ours_product_meetings_in_gaps=gap,ours_excluded_nonproduct=ex,ours_total_accounted=ours+gap+ex,shortfall_vs_daval=int(D.at[y,c])-(ours+gap+ex)))
CV=pd.DataFrame(cov)
bycom=M.groupby('committee').size().rename('meetings').to_frame()
os.makedirs('out',exist_ok=True)
M.to_csv('adcom_full_pivotal.csv',index=False)
G.to_csv('gaps.csv',index=False); X.to_csv('excluded.csv',index=False); CV.to_csv('coverage_vs_daval.csv',index=False); T.to_csv('two_by_two.csv',index=False)
with pd.ExcelWriter('adcom_full.xlsx') as w:
    M.to_excel(w,sheet_name='meetings_pivotal',index=False); T.to_excel(w,sheet_name='2x2',index=False); CV.to_excel(w,sheet_name='coverage_vs_daval',index=False)
    CV.groupby('committee')[['daval_all_meetings','ours_product_vote_meetings','ours_product_meetings_in_gaps','ours_excluded_nonproduct','shortfall_vs_daval']].sum().to_excel(w,sheet_name='coverage_by_committee')
    G.to_excel(w,sheet_name='gaps',index=False); OLD.to_excel(w,sheet_name='pre_2016-11_not_curated',index=False); X.to_excel(w,sheet_name='excluded',index=False); bycom.to_excel(w,sheet_name='by_committee')
print(len(M),'meetings'); print(bycom.T.to_string()); print(T.to_string())
print('gaps',len(G),G.reason.value_counts().to_dict()); print('excluded',len(X))
print(CV.groupby('committee')[['daval_all_meetings','ours_product_vote_meetings','ours_product_meetings_in_gaps']].sum().to_string())
print('vote tier',M.vote_source_tier.value_counts().to_dict()); print('outcome tier',M.outcome_source_tier.value_counts().to_dict())
print('verif outcome',M.verified_outcome.value_counts().to_dict()); print('orphan_ind',M.orphan_for_indication.value_counts().to_dict()); print('prio',M.review_priority.value_counts().to_dict())
