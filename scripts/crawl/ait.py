import json,re,os,time,hashlib,subprocess,html as H
S=json.load(open('stage1.json'))
def curl(u,fn,t=90):
    for k in range(4):
        subprocess.run(['curl','-sL','-m',str(t),'-A','Mozilla','-o',fn,u])
        b=open(fn,'rb').read() if os.path.exists(fn) else b''
        if b and b'Rate limit' not in b[:3000] and b'Too Many Requests' not in b[:3000]: time.sleep(3); return b
        time.sleep(30*(k+1))
    return b''
docs=json.load(open('minutes_docs_ait.json')) if os.path.exists('minutes_docs_ait.json') else []
done=set(d['page'] for d in docs)|set(json.load(open('ait_pages_done.json')) if os.path.exists('ait_pages_done.json') else [])
pages=[]
for c,v in S.items():
    for u,y in v.get('years',{}).items():
        if y and '2016'<=str(y)<='2026':
            u=re.sub(r'^https?://web\.archive\.org/web/\d+(id_)?/','',u)
            pages.append((c,y,u))
for c,y,u in pages:
    if u in done: continue
    fn='html/ait_'+hashlib.md5(u.encode()).hexdigest()
    b=curl('https://wayback.archive-it.org/7993/2026/'+u,fn).decode('utf8','ignore')
    ls=re.findall(r'href="([^"]+)"[^>]*>([^<]{5,250})',b)
    n=0
    for a,t in ls:
        t=H.unescape(t).strip()
        if not re.search(r'minutes|transcript|vot',t,re.I) or not re.search(r'media/\d+|download|\.pdf',a,re.I): continue
        a=re.sub(r'^/7993/\d+/','',a)
        h=hashlib.md5(a.encode()).hexdigest(); pf='pdf/ait_'+h; tx='txt/ait_'+h+'.txt'
        if not os.path.exists(tx):
            live=curl(a,pf,60)
            if live[:5]!=b'%PDF-': live=curl('https://wayback.archive-it.org/7993/2026/'+a,pf,90)
            if live[:5]==b'%PDF-': subprocess.run(['pdftotext','-layout',pf,tx])
        L=os.path.getsize(tx) if os.path.exists(tx) else 0
        docs.append(dict(committee=c,era='new',page=u,url=a,fetch=a,title=t,txt=tx,txtlen=L,src='archive-it 7993 / fda.gov')); n+=1
    done.add(u); json.dump(sorted(done),open('ait_pages_done.json','w'))
    json.dump(docs,open('minutes_docs_ait.json','w'))
    print(c,y,len(b),n,flush=True)
