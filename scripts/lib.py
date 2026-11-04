import re,subprocess,os,hashlib,html as H,time,threading
UA="Mozilla/5.0 (X11; Linux x86_64) Chrome/120"
_lock={'archive-it':threading.Semaphore(1),'web.archive.org':threading.Semaphore(4)}
_last={}
BAD=('Session Verification','Rate limit reached','Too Many Requests')
def fetch(u,fn):
    host=next((k for k in _lock if k in u),None)
    for tr in range(4):
        if host:
            with _lock[host]:
                w=(4.5 if host=='archive-it' else 0.3)-(time.time()-_last.get(host,0))
                if w>0: time.sleep(w)
                subprocess.run(['curl','-sL','-A','Mozilla' if host=='archive-it' else UA,'--max-time','90','-o',fn,u]); _last[host]=time.time()
        else: subprocess.run(['curl','-sL','-A',UA,'--max-time','90','-o',fn,u])
        if os.path.exists(fn):
            head=open(fn,'rb').read(600).decode('latin1')
            if any(b in head for b in BAD): os.remove(fn); time.sleep(30*(tr+1)); continue
        return
def get(u,d='html'):
    fn=d+'/'+hashlib.md5(u.encode()).hexdigest()
    if not os.path.exists(fn) or os.path.getsize(fn)<800: fetch(u,fn)
    if not os.path.exists(fn): return ''
    return open(fn,errors='ignore').read()
def getpdf(u):
    fn='pdf/'+hashlib.md5(u.encode()).hexdigest()
    if not os.path.exists(fn) or os.path.getsize(fn)<800: fetch(u,fn)
    tx='txt/'+hashlib.md5(u.encode()).hexdigest()+'.txt'
    if os.path.exists(fn) and not os.path.exists(tx):
        if open(fn,'rb').read(5)==b'%PDF-': subprocess.run(['pdftotext','-layout',fn,tx])
        else:
            s=re.sub(r'<[^>]+>',' ',open(fn,errors='ignore').read()); open(tx,'w').write(H.unescape(s))
    return open(tx,errors='ignore').read() if os.path.exists(tx) else ''
def absu(base,h):
    h=H.unescape(h).strip()
    if h.startswith('http'): return h
    if h.startswith('//'): return 'https:'+h
    if h.startswith('/web/') and 'web.archive.org' in base: return 'https://web.archive.org'+h
    if h.startswith('/7993/'): return 'https://wayback.archive-it.org'+h
    if h.startswith('/'):
        m=re.match(r'(https://web\.archive\.org/web/\d+(?:id_)?/)',base)
        return (m.group(1)+'https://www.fda.gov'+h) if m else 'https://www.fda.gov'+h
    return base.rsplit('/',1)[0]+'/'+h
def links(base,h):
    return [(absu(base,a),re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',H.unescape(t))).strip()) for a,t in re.findall(r'href="([^"#]+)"[^>]*>(.*?)</a>',h,re.S)]
