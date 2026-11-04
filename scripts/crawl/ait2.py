import json,re,os,time,hashlib,subprocess,html as H,glob,datetime
from aitlib import curl
MON='january|february|march|april|may|june|july|august|september|october|november|december'
meet=set()
for f in glob.glob('html/ait_*'):
    b=open(f,errors='ignore').read()
    for a in re.findall(r'href="(?:/7993/\d+/)?(https://www\.fda\.gov/advisory-committees/[^"]+)"',b):
        if re.search(r'('+MON+r')-\d{1,2}(-\d{1,2})?-20(1[6-9]|2\d)',a) and 'meeting-materials' not in a: meet.add(a)
# gap calendar candidates too
import pandas as pd
G=pd.read_csv('gaps.csv'); G=G[G.meeting_date>='2016-11-04']
cal=[re.sub(r'^https?://(www\.)?fda\.gov(:80)?','https://www.fda.gov',l.strip().split('?')[0]) for l in open('cal_cdx.txt') if '%' not in l]
for d in G.meeting_date.dropna().unique():
    dd=datetime.date.fromisoformat(d)
    p=f"{dd.strftime('%B').lower()}-{dd.day}-"
    for c in cal:
        if p in c and str(dd.year) in c: meet.add(c)
print(len(meet),flush=True)
docs=json.load(open('minutes_docs_ait2.json')) if os.path.exists('minutes_docs_ait2.json') else []
done=set(json.load(open('ait2_done.json'))) if os.path.exists('ait2_done.json') else set()
for u in sorted(meet):
    if u in done: continue
    fn='html/m2_'+hashlib.md5(u.encode()).hexdigest()
    b=b''
    subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0 (X11; Linux x86_64) Chrome/120','-o',fn,u]); b=open(fn,'rb').read() if os.path.exists(fn) else b''
    src='live'
    if b'download' not in b or b'Page Not Found' in b[:3000]:
        b=curl('https://wayback.archive-it.org/7993/2026/'+u,fn); src='archive-it'
    b=b.decode('utf8','ignore')
    n=0
    for a,t in re.findall(r'href="([^"]+)"[^>]*>([^<]{5,250})',b):
        t=H.unescape(t).strip()
        if not re.search(r'minutes|transcript|vot',t,re.I) or not re.search(r'media/\d+|download|\.pdf',a,re.I): continue
        a=re.sub(r'^(https://wayback\.archive-it\.org)?/7993/\d+/','',a)
        if a.startswith('/'): a='https://www.fda.gov'+a
        h=hashlib.md5(a.encode()).hexdigest(); pf='pdf/ait_'+h; tx='txt/ait_'+h+'.txt'
        if not os.path.exists(tx):
            x=b''
            subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0 (X11; Linux x86_64) Chrome/120','-o',pf,a]); x=open(pf,'rb').read(5) if os.path.exists(pf) else b''
            if x!=b'%PDF-': x=curl('https://wayback.archive-it.org/7993/2026/'+a,pf,90)[:5]
            if x==b'%PDF-': subprocess.run(['pdftotext','-layout',pf,tx])
        L=os.path.getsize(tx) if os.path.exists(tx) else 0
        com=None
        docs.append(dict(committee='?',era='new',page=u,url=a,fetch=a,title=t,txt=tx,txtlen=L,src=src)); n+=1
    done.add(u); json.dump(sorted(done),open('ait2_done.json','w')); json.dump(docs,open('minutes_docs_ait2.json','w'))
    print(u[-90:],src,n,flush=True)
