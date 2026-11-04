import re
N=r'(\d{1,2})'
PATS=[
 re.compile(r'Yes\s*[=:\-–]?\s*'+N+r'\s*[,;]?\s*No\s*[=:\-–]?\s*'+N+r'\s*[,;]?\s*(?:Abstain(?:ed|ing|ions?)?|Uncertain)\s*[=:\-–]?\s*'+N,re.I),
 re.compile(r'Yes\s*[=:\-–]?\s*'+N+r'\s*[,;]?\s*No\s*[=:\-–]?\s*'+N,re.I),
 re.compile(N+r'\s+(?:voted\s+)?Yes\s*[,;]?\s*(?:and\s+)?'+N+r'\s+(?:voted\s+)?No(?:\s*[,;]?\s*(?:and\s+)?'+N+r'\s+Abstain)?',re.I),
 re.compile(r'voted\s+'+N+r'\s*(?:to|-|–)\s*'+N+r'(?:\s*(?:with|,)\s*'+N+r'\s+abstent)?',re.I),
 re.compile(r'voted:?\s*'+N+r'\s*(?:for|in favor|yes)[,;]?\s*(?:and\s+)?'+N+r'\s*(?:against|opposed|no)(?:[,;]?\s*(?:and\s+)?'+N+r'\s*abst)?',re.I),
 re.compile(N+r'\s*(?:people|members?|persons?)?\s*voted\s+(?:for|yes|in favor)[^.]{0,60}?'+N+r'\s*(?:people|members?|persons?)?\s*voted\s+(?:against|no)(?:[^.]{0,40}?'+N+r'\s*abst)?',re.I),
]
def extract(t):
    t=re.sub(r'[ \t]+',' ',t); t=t.replace('\f','\n')
    flat=re.sub(r'\s+',' ',t)
    hits=[]; used=[]
    for p in PATS:
        for m in p.finditer(flat):
            if any(m.start()<e and m.end()>s for s,e in used): continue
            g=[int(x) if x else 0 for x in (m.groups()+(None,))[:3]]
            if g[0]+g[1]<3 or g[0]+g[1]+g[2]>40: continue
            used.append((m.start(),m.end())); hits.append((m.start(),m.end(),g))
    hits.sort()
    out=[];prev=0
    for s,e,g in hits:
        ctx=flat[max(prev,s-1800):s]
        qs=re.findall(r'((?:DISCUSSION|VOTE|Question|\b\d{1,2}\.)[^?]{10,900}\?)',ctx,re.I)
        q=qs[-1] if qs else ctx[-500:]
        out.append(dict(pos=s,yes=g[0],no=g[1],abstain=g[2],question=q.strip()[:900],raw=flat[s:e]))
        prev=e
    return out
