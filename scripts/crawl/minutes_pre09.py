import json,re
from lib import *
Y={'2009':'09acdocs.html','2008':'08acdocs.htm','2007':'07acdocs.htm','2006':'06acdocs.htm','2005':'05acdocs.htm','2004':'04acdocs.htm','2003':'03acdocs.htm','2002':'02acdocs.htm','2001':'01docsbc.htm','2000':'00mtbc.htm'}
out=[]
PAGES=[(str(y),f'{c}{str(y)[2:]}.htm') for y in range(2000,2009) for c in ('cder','cber')]
for y,f in PAGES:
    u='https://web.archive.org/web/2015/http://www.fda.gov/ohrms/dockets/ac/'+f
    h=get(u)
    h=re.sub(r'<a\s+name="([^"]+)"[^>]*>',lambda m:' [[SECTION '+m.group(1)+']] ',h)
    # walk sequentially remembering the latest committee heading / date text
    toks=re.split(r'(<a\s[^>]*href="[^"]+"[^>]*>.*?</a>)',h,flags=re.S)
    ctx=''
    for tk in toks:
        m=re.match(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>',tk,re.S)
        if not m:
            txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',tk)).strip()
            if len(txt)>15: ctx=txt[-300:]
            continue
        a=absu(u,m.group(1)); t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',m.group(2))).strip()
        if re.search(r'minutes|vote',t,re.I): out.append(dict(era='pre09',year=y,page=u,url=a,title=t,context=ctx))
    print(f,len(h),sum(1 for o in out if o['year']==y),flush=True)
json.dump(out,open('minutes_pre09.json','w'),indent=0)
