import json,re,os,time,hashlib,subprocess,html as H
S=json.load(open('stage1.json'))
def curl(u,fn,t=90):
    for k in range(4):
        subprocess.run(['curl','-sL','-m',str(t),'-A','Mozilla','-o',fn,u])
        b=open(fn,'rb').read() if os.path.exists(fn) else b''
        if b and b'Rate limit' not in b[:3000] and b'Too Many Requests' not in b[:3000]: time.sleep(3); return b
        time.sleep(30*(k+1))
    return b''
