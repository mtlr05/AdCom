import pandas as pd,re
O=pd.read_csv('oopd_all.csv',dtype=str).fillna('')
STOP=set('treatment patients with adult adults pediatric children years older prevention associated management chronic severe acute disease disorder therapy indicated use who have that this those from their under after least including other'.split())
def kw(t): return {w for w in re.findall(r'[a-z]{5,}',t.lower()) if w not in STOP}
def toks(s): return [w for w in re.findall(r'[a-z0-9\-]{5,}',s.lower()) if w not in STOP and w not in {'injection','tablets','capsules','hydrochloride','sodium','solution','extended','release','recombinant','human','oral','inhalation','powder','sulfate','acetate'}]
def run(M):
    res=[]
    for _,r in M.iterrows():
        names=set(toks(r.generic)+toks(r.brand)+toks(r.product_text[:120]))
        if not names: res.append(('unverified','no product name')); continue
        hit=O[O.apply(lambda o:any(n in (o['Generic Name']+' '+o['Trade Name']).lower() for n in names),axis=1)]
        hit=hit[pd.to_datetime(hit['Date Designated'],errors='coerce')<=pd.to_datetime(r.final_action_date[:10] if len(r.final_action_date)>=10 else r.meeting_date,errors='coerce')+pd.Timedelta(days=1)] if len(hit) else hit
        if not len(hit): res.append(('N','no OOPD designation for ingredient')); continue
        ind=kw(r.fr_snippet+' '+r.question_text+' '+r.final_action)
        best=max(((len(kw(h['Orphan Designation'])&ind),h['Orphan Designation']) for _,h in hit.iterrows()),key=lambda x:x[0])
        if best[0]>=2: res.append(('Y','indication match: '+best[1][:150]))
        elif best[0]==1: res.append(('review','weak (1-keyword) match: '+best[1][:150]))
        else: res.append(('N','designation(s) for other indication(s): '+hit['Orphan Designation'].iloc[0][:120]))
    return res
