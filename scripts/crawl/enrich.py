import pandas as pd,json,os,re,datetime
R=pd.read_pickle('rows_raw.pkl'); G=pd.read_pickle('gaps.pkl'); X=pd.read_pickle('excluded.pkl')
P=R[R.pivotal_question].copy()
OO=pd.read_csv('oopd_all.csv',dtype=str).fillna('')
OO['g']=OO['Generic Name'].str.lower(); OO['t']=OO['Trade Name'].str.lower()
def D(s):
    try: return datetime.date.fromisoformat(str(s)[:10])
    except: return None
def ymd(s): return f'{s[:4]}-{s[4:6]}-{s[6:8]}' if s else ''
out=[]
CRL={}
for c in json.load(open('crl_all.json')):
    for a in re.findall(r'\d{5,6}',str(c.get('application_number',''))):
        m,d_,y=c['letter_date'].split('/'); CRL.setdefault(a.lstrip('0'),[]).append((f'{y}-{m}-{d_}','https://download.open.fda.gov/crl/'+c['file_name'],c.get('approval_status','')))
def crl_after(app,md):
    L=sorted(x for x in CRL.get(app.lstrip('0'),[]) if md and D(x[0]) and D(x[0])>=md-datetime.timedelta(days=30))
    return L[0] if L else None
for _,r in P.iterrows():
    r=r.to_dict(); md=D(r['meeting_date']); app=str(r['app'] or '')
    d={}
    for k in {app,app.zfill(6),app.lstrip('0')}:
        fn=f'ofda/{k}.json'
        if app and os.path.exists(fn):
            x=json.load(open(fn))
            if x: d=x; break
    r.update(brand='',generic='',review_priority='unverified',action_at_1yr='unverified',final_action='unverified',final_action_date='',decision_source='')
    if d:
        pr=d.get('products',[{}])[0]; r['brand']=pr.get('brand_name',''); r['generic']=';'.join(a.get('name','') for a in pr.get('active_ingredients',[]))
        subs=d.get('submissions',[]); r['application_number']=d.get('application_number'); r['decision_source']='openFDA drugsfda '+d.get('_q','')
        orig=[s for s in subs if s.get('submission_type')=='ORIG' and s.get('submission_status')=='AP']
        od=D(ymd(orig[0]['submission_status_date'])) if orig else None
        if orig: r['review_priority']=orig[0].get('review_priority','unverified')
        cand=None
        if od and md and od>=md-datetime.timedelta(days=30): cand=od
        elif od and md and od<md:  # app already approved
            if r['meeting_type']!='supplemental' and not re.search(r'supplement|new indication|proposed (?:for|indication)|efficacy supplement',str(r['fr_snippet']),re.I):
                r['meeting_type']='EXCLUDE: marketed product, no new application in notice (safety/other)'
            else: r['meeting_type']='supplemental'
            ss=sorted([D(ymd(s['submission_status_date'])) for s in subs if s.get('submission_type')=='SUPPL' and s.get('submission_class_code')=='EFFICACY' and s.get('submission_status')=='AP' and D(ymd(s['submission_status_date']))>=md])
            cand=None; r['suppl_candidate_approval']=ss[0].isoformat() if ss else ''
            if ss: r['review_priority']=next((s.get('review_priority') for s in subs if D(ymd(s.get('submission_status_date','')))==ss[0]),r['review_priority'])
            r['decision_source']+=' | supplemental: first EFFICACY supplement approved after meeting (heuristic; indication not checked)'
        if cand:
            r['final_action']='approved'; r['final_action_date']=cand.isoformat()
            r['action_at_1yr']='approved' if (cand-md).days<=365 else 'not approved within 1 yr'
        elif r['meeting_type']=='supplemental':
            r['final_action']='unverified'; r['action_at_1yr']='unverified'; r['decision_source']+=' | supplemental outcome NOT verified (openFDA does not give indication per supplement)'
        else:
            c=crl_after(app,md)
            if c: r['final_action']='CRL (not approved as of 2026-11)'; r['final_action_date']=c[0]; r['action_at_1yr']='not approved within 1 yr'; r['decision_source']+=' | openFDA CRL letter '+c[1]
            else: r['final_action']='unverified'; r['action_at_1yr']='unverified'; r['decision_source']+=' | no ORIG approval and no CRL in openFDA; needs manual check'
    if not d and app and r['meeting_type']!='supplemental':
        c=crl_after(app,md)
        if c: r['final_action']='CRL (no approval found as of 2026-11)'; r['final_action_date']=c[0]; r['action_at_1yr']='not approved within 1 yr'; r['decision_source']='openFDA CRL letter '+c[1]+' (CRL database; later approval under another app # not excluded)'
        else: r['decision_source']='no openFDA drugsfda record and no openFDA CRL for app '+app+'; needs manual check'
    # orphan
    SALT='hydrochloride|mesylate|sodium|potassium|acetate|sulfate|maleate|citrate|tartrate|phosphate|succinate|fumarate|bromide|chloride|calcium|hydrobromide|besylate|tosylate|injection|tablets|extended|release|capsules|solution|for|and|oral|topical|ophthalmic|suspension|dihydrate|monohydrate|hcl|disodium|magnesium'
    names=[x for x in re.split(r'[;,/ ()]+',(r['generic'] or r['product_text'] or '').lower()) if len(x)>=6 and not re.fullmatch(SALT,x)][:1]
    hits=OO[OO.g.apply(lambda g:any(re.search(r'\b'+re.escape(n),g) for n in names))] if names else OO.iloc[0:0]
    if len(hits): hits=hits[hits['Date Designated'].apply(lambda s:(D(f'{s[6:10]}-{s[0:2]}-{s[3:5]}') or datetime.date(2100,1,1))<= (md or datetime.date(2100,1,1)))]
    r['orphan_designation_any']='Y' if len(hits) else ('N' if names else 'unverified')
    r['orphan_match']='' if not len(hits) else '; '.join((hits['Generic Name']+' | '+hits['Orphan Designation']+' | '+hits['Date Designated']).head(4))
    r['orphan_verification']='OOPD export name match (indication NOT checked; fuzzy)' if len(hits) else ('OOPD export: no designation for ingredient name before meeting' if names else 'no product name')
    r['CNS']=r['committee'] in ('PCNS','PDAC'); r['CGT']=r['committee']=='CTGTAC'
    r['center']='CBER' if r['committee'] in ('CTGTAC','VRBPAC','BPAC','APAC','BRMAC') else 'CDER'
    f=r['favourable']; r['adcom']='tie' if f=='tie' else ('favourable' if f else 'unfavourable')
    r['concordant_final']=('' if f=='tie' or r['final_action']=='unverified' else ((r['final_action']=='approved')==bool(f)))
    r['source']='automated (FR+FDA minutes+openFDA)'
    out.append(r)
M=pd.DataFrame(out); M.to_pickle('meetings.pkl'); print(len(M)); print(M.adcom.value_counts()); print(M.final_action.value_counts())
