import json,re,datetime
rows=json.load(open('fr_parsed.json'))
MON='(January|February|March|April|May|June|July|August|September|October|November|December)'
def d(s):
    try: return datetime.datetime.strptime(s.replace(',',''),'%B %d %Y').date().isoformat()
    except: return ''
APP=re.compile(r'(?:supplemental\s+)?(?:new drug applications?|biologics? licen[cs]e applications?|NDA|BLA|sNDA|sBLA)[^0-9]{0,40}?(\d{2,3}[-\s]?\d{3}(?:/[\dS-]+)?)',re.I)
items=[]
for r in rows:
    if not r['product_app']: continue
    m=re.search(MON+r'\s+(\d{1,2})(?:\s*(?:and|,|-)\s*\d{1,2})*,\s*(\d{4})',r['dates'])
    d0=d(f'{m.group(1)} {m.group(2)} {m.group(3)}') if m else ''
    yr=m.group(3) if m else r['pub'][:4]
    # split agenda by "On <date>"
    segs=re.split(r'(?=On\s+'+MON+r'\s+\d{1,2},?\s*(?:\d{4})?)',r['agenda'])
    cur=d0
    for s in segs:
        mm=re.match(r'On\s+'+MON+r'\s+(\d{1,2}),?\s*(\d{4})?',s)
        if mm: cur=d(f'{mm.group(1)} {mm.group(2)} {mm.group(3) or yr}') or cur
        apps=APP.findall(s)
        for a in dict.fromkeys(apps):
            i=s.find(a); items.append(dict(meeting_date=cur,committee=r['committee'],fr_doc=r['doc'],fr_url=r['url'],app=re.sub(r'[\s-]','',a.split('/')[0]),snippet=s[max(0,i-120):i+400]))
        if not apps and re.search(r'application',s,re.I): items.append(dict(meeting_date=cur,committee=r['committee'],fr_doc=r['doc'],fr_url=r['url'],app='',snippet=s[:500]))
# dedupe on date+app
seen={};
for it in items:
    k=(it['meeting_date'],it['app'] or it['snippet'][:60])
    seen.setdefault(k,it)
items=list(seen.values())
json.dump(items,open('fr_items.json','w'),indent=0)
import collections
print(len(items),collections.Counter(i['meeting_date'][:4] for i in items))
