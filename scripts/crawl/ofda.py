import json,os,subprocess,re
from concurrent.futures import ThreadPoolExecutor as TP
items=json.load(open('fr_items.json'))
apps=sorted(set(i['app'] for i in items if i['app']))
def f(a):
    fn=f'ofda/{a}.json'
    if os.path.exists(fn): return
    out={}
    for pre in (['NDA','BLA','ANDA'] ):
        u=f'https://api.fda.gov/drug/drugsfda.json?search=application_number:"{pre}{a.zfill(6)}"&limit=1'
        s=subprocess.run(['curl','-s','--max-time','60',u],capture_output=True,text=True).stdout
        try:
            d=json.loads(s)
            if d.get('results'): out=d['results'][0]; out['_q']=u; break
        except: pass
    json.dump(out,open(fn,'w'))
with TP(2) as ex: list(ex.map(f,apps))
print(len(apps),sum(1 for a in apps if os.path.getsize(f'ofda/{a}.json')>5))
