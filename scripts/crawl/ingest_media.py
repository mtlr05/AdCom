import json,os,re,subprocess,requests
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36'}
AC=r'(ODAC|VRBPAC|BPAC|CTGTAC|PCNS|PDAC|AADPAC|AMDAC|AAC|EMDAC|CRDAC|DODAC|DSaRM|GIDAC|PADAC|NDAC|BRUDAC|MIDAC|PADAC|CDER|Advisory)'
out=[];old={d['fetch']:d for d in json.load(open('minutes_docs_media.json'))} if os.path.exists('minutes_docs_media.json') else {}
for l in open('media_index.tsv'):
    p=l.rstrip('\n').split('\t')
    if len(p)<3 or p[1]!='200': continue
    fn=p[2]
    if not re.search(r'minute|summary|vote|transcript',fn,re.I) or not re.search(AC,fn,re.I): continue
    if re.search(r'PDUFA|GDUFA|BsUFA|Stakeholder|Pediatric Advisory|roster',fn,re.I): continue
    url=f'https://www.fda.gov/media/{p[0]}/download'
    if url in old: out.append(old[url]); continue
    pdf=f'media_pdf/{p[0]}.pdf'; txt=pdf[:-4]+'.txt'
    try:
        if not os.path.exists(pdf):
            r=requests.get(url,headers=UA,timeout=60); open(pdf,'wb').write(r.content)
        subprocess.run(['pdftotext','-layout',pdf,txt],timeout=120)
        n=len(open(txt,errors='ignore').read()) if os.path.exists(txt) else 0
    except Exception as e: n=0
    out.append(dict(committee='?',page=fn,url=url,fetch=url,title=fn,txt=txt,txtlen=n,src='media-id scan'))
    json.dump(out,open('minutes_docs_media.json','w'))
json.dump(out,open('minutes_docs_media.json','w')); print(len(out))
