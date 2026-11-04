import json,re,os,datetime,collections,hashlib
import pandas as pd
from votes import extract
MON='(January|February|March|April|May|June|July|August|September|October|November|December)'
def pdate(s):
    m=re.search(MON+r'\s+(\d{1,2})(?:\s*(?:-|–|and|&|,)\s*\d{1,2})?,?\s*(\d{4})',s or '')
    if m:
        try: return datetime.date(int(m.group(3)),datetime.datetime.strptime(m.group(1),'%B').month,int(m.group(2))).isoformat()
        except: pass
    m=re.search(r'(\d{2})(\d{2})(20\d\d)',s or '')
    if m:
        try: return datetime.date(int(m.group(3)),int(m.group(1)),int(m.group(2))).isoformat()
        except: pass
    return ''
CM=[('Oncolog','ODAC'),('Peripheral and Central','PCNS'),('Psychopharm','PDAC'),('Cardio','CRDAC'),('Endocrin','EMDAC'),('Anti-Infective','AMDAC'),('Antimicrobial','AMDAC'),
('Antiviral','AVDAC'),('Arthritis','AAC'),('Anesthetic','AADPAC'),('Dermatolog','DODAC'),('Drug Safety','DSaRM'),('Gastrointestinal','GIDAC'),('Genetic Metabolic','GeMDAC'),
('Medical Imaging','MIDAC'),('Nonprescription','NDAC'),('Reproductive','BRUDAC'),('Pharmaceutical Science','PSCPAC'),('Pulmonary','PADAC'),('Cellular, Tissue','CTGTAC'),
('Vaccines and Related','VRBPAC'),('Blood Products','BPAC'),('Allergenic','APAC'),('Biological Response','BRMAC'),('Pharmacy Compounding','PCAC')]
def cab(s):
    for k,v in CM:
        if k.lower() in (s or '').lower(): return v
    return 'OTHER'
fr=json.load(open('fr_items.json'))
for i in fr: i['cab']=cab(i['committee'])
docs=[]
for fn in ['minutes_docs.json','minutes_docs_old.json','minutes_docs_new.json']:
    if os.path.exists(fn): docs+=json.load(open(fn))
if os.path.exists('fill_cdx.json'):
    for d in json.load(open('fill_cdx.json')):
        if d.get('url') and d.get('txtlen',0)>200: d['fetch']=d['url']; docs.append(d)
for fn in ['minutes_docs_ait.json','minutes_docs_ait2.json','minutes_docs_media.json']:
    if os.path.exists(fn):
        for d in json.load(open(fn)):
            if d.get('committee')=='?':
                d['committee']=cab(d['title']+' '+d['page'].replace('-',' '))
            docs.append(d)
seenf=set();docs=[d for d in docs if not (d['fetch'] in seenf or seenf.add(d['fetch']))]
pre=json.load(open('minutes_pre09.json')) if os.path.exists('minutes_pre09.json') else []
# ---- meeting docs
meet=collections.defaultdict(list)
for d in docs:
    if d['txtlen']<200: continue
    t=open(d['txt'],errors='ignore').read()
    if re.search(r'roster|agenda only',d['title'],re.I) and not re.search('minutes',d['title'],re.I): continue
    dt=d.get('meeting_date') or pdate(d['title']) or pdate(d.get('meeting','')) or pdate(d['page'].split('/')[-1].replace('-',' ')) or pdate(t[:1500])
    d['date']=dt
    meet[(d['committee'],dt)].append(d)
def rank(d):
    t=d['title'].lower()
    return (0 if 'final' in t or 'summary' in t else 1 if t.startswith('minutes') else 2 if 'quick' in t else 3)
OOPD=pd.read_csv('oopd_all.csv',dtype=str).fillna('')
OOPD['g']=OOPD['Generic Name'].str.lower()
def ofda(app):
    fn=f'ofda/{app.zfill(6)}.json'
    if not os.path.exists(fn) or os.path.getsize(fn)<6: fn=f'ofda/{app.lstrip("0")}.json'
    if app and os.path.exists(fn):
        d=json.load(open(fn)); return d or None
    return None
FAV_Q=re.compile(r'approv|benefit[- ]?risk|risk[- ]?benefit|favorabl|substantial evidence|effective',re.I)
rows=[];excluded=[];gaps=[]
STOP=set('proposed supplemental supplement application tablets injection capsules solution powder biologics license submitted indication treatment patients oral intravenous subcutaneous extended release hydrochloride sodium'.split())
def toks(p):
    t=set(w.lower() for w in re.findall(r'[A-Za-z][A-Za-z-]{4,}',p.get('name','')+' '+p.get('snippet','')[:0]))
    d=ofda(p['app'] or '') if p.get('app') else None
    if d:
        for pr in d.get('products',[])[:3]:
            t.add(pr.get('brand_name','').lower())
            for a in pr.get('active_ingredients',[]): t.update(w.lower() for w in re.findall(r'[A-Za-z]{5,}',a.get('name','')))
    m=re.search(re.escape((p['app'] or '@@')[-3:])+r'[^,]{0,40}?(?:for|,)\s*([A-Z][A-Za-z-]+)?\s*\(?([a-z][a-z-]{4,})',p.get('snippet',''))
    if m: t.update(x.lower() for x in m.groups() if x)
    return {x for x in t if x and len(x)>=5 and x not in STOP}
used_fr=set()
def apppos(text,app,name):
    ps=[m.start() for m in re.finditer(re.escape(app[-6:].lstrip('0')) if app else '@@@',text)]
    if name: ps+=[m.start() for m in re.finditer(re.escape(name[:12]),text,re.I)]
    return ps
for (c,dt),ds in sorted(meet.items(),key=lambda x:x[0][1]):
    ds=sorted(ds,key=rank); d=ds[0]
    text=re.sub(r'\s+',' ',open(d['txt'],errors='ignore').read())
    vs=extract(text)
    if not vs and len(ds)>1:
        for d2 in ds[1:]:
            t2=re.sub(r'\s+',' ',open(d2['txt'],errors='ignore').read()); v2=extract(t2)
            if v2: d,text,vs=d2,t2,v2; break
    # FR items same date +-1
    try: D=datetime.date.fromisoformat(dt)
    except: D=None
    cands=[i for i in fr if D and i['meeting_date'] and abs((datetime.date.fromisoformat(i['meeting_date'])-D).days)<=1 and (i['cab']==c or c in ('OTHER',) or i['cab']=='OTHER' or True)]
    # keep committee matches first
    def nm_(p):
        m=re.search(r'\d{3}[,]?\s*(?:\(\w+\)\s*)?([^,(]{3,60})',p['snippet'][p['snippet'].find(p['app'][-3:]) if p['app'] else 0:])
        n=m.group(1).strip() if m else ''
        return re.sub(r'^(for|of)\s+','',n,flags=re.I)
    def mention(p):
        a=(p['app'] or '').lstrip('0')
        if a and re.search(r'(?<!\d)'+re.escape(a)+r'(?!\d)',text): return True
        n=nm_(p).split()[0] if nm_(p) else ''
        return len(n)>=6 and n.lower() not in ('supplement','proposed','biologics','application','injection','tablets') and n.lower() in text.lower()
    cc=[i for i in cands if i['cab']==c or i['cab']=='OTHER']
    cm=[i for i in cc if mention(i)] or [i for i in cc if i['meeting_date']==dt]
    cm=cm or [i for i in cands if i['app'] and i['app'].lstrip('0')[-6:] in text]
    apps_txt=sorted(set(re.sub(r'[\s-]','',a) for a in re.findall(r'(?:NDA|BLA|STN)\s*#?\s*(\d{2,3}[-\s]?\d{3})',text)))
    if not cm and not apps_txt:
        excluded.append(dict(committee=c,meeting_date=dt,reason='no NDA/BLA in FR notice or minutes (non-product/general topic or unmatched)',minutes_url=d['fetch'],n_votes=len(vs),first_question=(vs[0]['question'][:300] if vs else '')))
        continue
    prods=cm if cm else [dict(app=a,snippet='',fr_url='',fr_doc='',committee='') for a in apps_txt]
    # assign votes to products by nearest preceding mention
    pos={}
    for p in prods:
        p['name']=nm_(p)
        pos[id(p)]=apppos(text,p['app'],p['name'])
    for p in prods:
        used_fr.add((p.get('fr_doc'),p['app']))
        if len(prods)==1: pv=vs
        else:
            pv=[]
            for v in vs:
                q4=v['question'][-500:].lower()
                hits=[q for q in prods if any(t in q4 for t in toks(q))]
                if len(hits)==1:
                    if hits[0] is p: pv.append(v)
                    continue
                best=max(prods,key=lambda q:max([x for x in pos[id(q)] if x<v['pos']] or [-1]))
                if best is p and max([x for x in pos[id(p)] if x<v['pos']] or [-1])>=0: pv.append(v)
        snip=p['snippet']
        supp=bool(re.search(r'supplement|sNDA|sBLA|/S-?\d|new indication|expand',snip,re.I))
        base=dict(meeting_date=dt,committee=c,app=p['app'],product_text=p['name'],fr_notice=p.get('fr_url',''),fr_snippet=snip[:500],minutes_title=d['title'],minutes_url=d['fetch'],minutes_page=d['page'],
                  meeting_type='supplemental' if supp else 'initial application',pre_2010=dt<'2010-01-01',n_vote_questions=len(pv),n_products_same_meeting=len(prods))
        if not pv:
            gaps.append(dict(base,reason='no parseable vote tally in minutes for this product (no vote held, or format not parsed)' if vs or len(text)>2000 else 'minutes text empty/scanned')); continue
        STRONG=re.compile(r'(support|recommend)\w*\s+(the\s+|its\s+|for\s+)?(accelerated\s+|marketing\s+)?approv|approv\w*\s+(of|this|for)|benefit[- /]*risk|risk[- /]*benefit|benefits?\s+outweigh|benefit\w*\b.{0,150}\boutweigh|favorabl|should\s+be\s+approved|\bbe\s+approved|recommend\w*\s+approv|support\w*\s+(the\s+)?licensure|approvab',re.I)
        BAD=re.compile(r'prior to approv|before approv|post-?approv|postmarket|lower dose|additional stud|label|REMS|restrict',re.I)
        def qt(v):
            q=v['question']; k=max(q.rfind('VOTE'),q.rfind('Vote,'),q.rfind('Voting Question'))
            q=q[k:] if k>=0 else q[-350:]
            return re.sub(r'^(VOTE:?|Vote,)\s*','',q)
        for v in pv: v['q']=qt(v)
        sc=[v for v in pv if STRONG.search(v['q']) and not BAD.search(v['q'])]
        A=[v for v in sc if re.search(r'approv|licensure',v['q'],re.I)]
        piv=A[-1] if A else (sc[0] if sc else None)
        rule='overall approval/benefit-risk question'
        if piv is None:
            EFF=re.compile(r'effectiveness|is effective|efficacy|clinical(ly)? (meaningful )?benefit|substantial evidence',re.I)
            ef=[v for v in pv if EFF.search(v['q']) and not BAD.search(v['q'])]
            if ef: piv=ef[0]; rule='no approval/benefit-risk question: first effectiveness question'
            else: piv=pv[0]; rule='no approval/effectiveness question: first vote question (flag for review)'
        for k,v in enumerate(pv):
            rows.append(dict(base,question_num=k+1,question_text=v['question'],vote_yes=v['yes'],vote_no=v['no'],vote_abstain=v['abstain'],vote_raw=v['raw'],
                 voting_member_count=v['yes']+v['no']+v['abstain'],pivotal_question=(v is piv),pivotal_rule=rule if v is piv else '',
                 favourable=('tie' if v['yes']==v['no'] else v['yes']>v['no']),polarity_check=bool(re.search(r"\bnot\b|should .*restrict|withdraw|remov",v['question'],re.I))))
cov=collections.defaultdict(list)
for r_ in rows+gaps:
    if r_.get('app'): cov[r_['app'].lstrip('0')].append(r_['meeting_date'])
for i in fr:
    if (i['fr_doc'],i['app']) not in used_fr:
        try: D_=datetime.date.fromisoformat(i['meeting_date'])
        except: D_=None
        if D_ and i['app'] and any(abs((datetime.date.fromisoformat(x)-D_).days)<=3 for x in cov[i['app'].lstrip('0')] if x): continue
        gaps.append(dict(meeting_date=i['meeting_date'],committee=i['cab'],app=i['app'],fr_notice=i['fr_url'],fr_snippet=i['snippet'][:500],pre_2010=i['meeting_date']<'2010-01-01',reason='product meeting in Federal Register; no minutes document retrieved/matched'))
R=pd.DataFrame(rows); G=pd.DataFrame(gaps); X=pd.DataFrame(excluded)
R.to_pickle('rows_raw.pkl'); G.to_pickle('gaps.pkl'); X.to_pickle('excluded.pkl')
print(len(R),R['pivotal_question'].sum() if len(R) else 0,len(G),len(X))
