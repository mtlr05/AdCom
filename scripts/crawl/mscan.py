import subprocess,sys,concurrent.futures as cf,time,os,re
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
lo,hi=int(sys.argv[1]),int(sys.argv[2]); out=sys.argv[3]
done=set()
if os.path.exists(out):
    for l in open(out): done.add(int(l.split('\t')[0]))
def h(i):
    for k in range(4):
        r=subprocess.run(['curl','-sI','-m','20','-A',UA,f'https://www.fda.gov/media/{i}/download'],capture_output=True,text=True).stdout
        st=r.split(' ')[1] if r.startswith('HTTP') else '000'
        if st in ('429','403','000','503'): time.sleep(5*(k+1)); continue
        fn=re.search(r'filename="?([^"\r\n;]+)',r,re.I)
        return i,st,fn.group(1) if fn else ''
    return i,st,''
with open(out,'a') as f, cf.ThreadPoolExecutor(8) as ex:
    for i,st,fn in ex.map(h,[i for i in range(lo,hi) if i not in done]):
        f.write(f'{i}\t{st}\t{fn}\n'); f.flush()
