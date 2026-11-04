import json,re,collections
k=json.load(open('fr_kept.json'))
M='(January|February|March|April|May|June|July|August|September|October|November|December)'
rows=[]
for r in k:
    try: t=open('frtxt/'+r['document_number']+'.txt',errors='ignore').read()
    except: continue
    t=re.sub(r'<[^>]+>','',t); t=re.sub(r'\s+',' ',t)
    dm=re.search(r'Date and Time:\s*(.{0,250})',t,re.I) or re.search(r'DATES:\s*(.{0,250})',t)
    ag=re.search(r'Agenda:\s*(.{0,2500}?)(?:FDA intends|Procedure:|Persons attending|Background material|$)',t,re.I)
    agenda=ag.group(1) if ag else ''
    prod=bool(re.search(r'\b(s?NDA|s?BLA|PMA|new drug application|biologics? license application|supplemental)\b',agenda,re.I))
    comm=re.match(r'(.*?Committee)',r['title']).group(1) if 'Committee' in r['title'] else r['title']
    rows.append(dict(doc=r['document_number'],pub=r['publication_date'],committee=comm,title=r['title'],url=r['html_url'],dates=dm.group(1)[:250] if dm else '',agenda=agenda,product_app=prod,
      apps=';'.join(sorted(set(re.findall(r'(?:s?NDA|s?BLA|BLA STN|PMA)\s*\(?\s*(?:STN\s*)?[\d\-/,.]+\)?',agenda)))) ))
json.dump(rows,open('fr_parsed.json','w'),indent=0)
print(len(rows),sum(r['product_app'] for r in rows), sum(1 for r in rows if not r['agenda']))
