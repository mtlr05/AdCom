import json,os,sys,requests,pandas as pd,datetime as D
def ofda(app):
    a=app.lstrip('0').zfill(6); fn=f'ofda/{a}.json'
    if not os.path.exists(fn):
        for p in ['NDA','BLA','ANDA']:
            r=requests.get('https://api.fda.gov/drug/drugsfda.json',params={'search':f'application_number:"{p}{a}"'},timeout=30)
            if r.ok and r.json().get('results'): json.dump(r.json()['results'][0],open(fn,'w')); break
        else: json.dump({},open(fn,'w'))
    return json.load(open(fn))
def info(app,md,supp):
    d=ofda(app); out=[]
    for s in d.get('submissions',[]):
        dt=s.get('submission_status_date','');
        if not dt: continue
        dd=f'{dt[:4]}-{dt[4:6]}-{dt[6:]}'
        if s['submission_type']=='ORIG' or (dd>=md and dd<=str(int(md[:4])+3)+md[4:] and 'EFFIC' in s.get('submission_class_code','').upper()):
            docs=[x['url'] for x in s.get('application_docs',[]) if 'ltr' in x['url'].lower()]
            out.append((s['submission_type'],s['submission_number'],s['submission_status'],dd,s.get('review_priority',''),docs[:1]))
    return d.get('application_number',''),[p.get('brand_name') for p in d.get('products',[])[:1]],out
rows=pd.read_csv(sys.argv[1],dtype=str).fillna('')
for _,r in rows.iterrows():
    if not r.app: continue
    try: print(r.meeting_date,r.committee,r.app,r.get('meeting_type','')[:4],info(r.app,r.meeting_date,'supp' in r.get('meeting_type','')))
    except Exception as e: print(r.meeting_date,r.app,'ERR',e)
