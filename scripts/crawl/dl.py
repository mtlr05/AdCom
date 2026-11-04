import json,re,os
from concurrent.futures import ThreadPoolExecutor as TP
from lib import *
import sys
L=[]
for fn in (sys.argv[1:] or ['minutes_links.json']): L+=json.load(open(fn))
seen=set();docs=[]
for x in L:
    if x.get('kind')=='calendar' or not x['url'] or x['url'] in seen: continue
    if not re.search(r'minutes|vote|voting',x['title'],re.I) or re.search(r'waiver|roster|federal register|draft',x['title'],re.I): continue
    seen.add(x['url']); docs.append(x)
print(len(docs),flush=True)
def norm(u):
    m=re.search(r'web\.archive\.org/web/(\d+)[a-z_]*/(.*)',u)
    if m and re.search(r'\.pdf$|/download$',m.group(2),re.I):
        orig=m.group(2)
        if '/media/' in orig: return 'https://www.fda.gov/media/'+re.search(r'/media/(\d+)',orig).group(1)+'/download'
        return f'https://web.archive.org/web/{m.group(1)}id_/'+orig
    return u
def f(x):
    u=norm(x['url']); x['fetch']=u
    t=getpdf(u)
    if len(t)<200 and 'fda.gov/media' in u:
        u2='https://web.archive.org/web/2026id_/'+u; t=getpdf(u2); x['fetch']=u2
    x['txt']='txt/'+hashlib.md5(x['fetch'].encode()).hexdigest()+'.txt'; x['txtlen']=len(t)
    return x
with TP(6) as ex: docs=list(ex.map(f,docs))
json.dump(docs,open('minutes_docs.json' if len(sys.argv)<2 else 'minutes_docs_fill.json','w'),indent=0)
print(len(docs),sum(1 for d in docs if d['txtlen']>200))
