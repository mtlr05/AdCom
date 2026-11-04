import json,os,subprocess,glob,tempfile
from rapidocr_onnxruntime import RapidOCR
eng=RapidOCR()
for f in ['minutes_docs.json','minutes_docs_old.json','minutes_docs_new.json']:
    D=json.load(open(f)); ch=0
    for d in D:
        if d.get('txtlen',0)>=300: continue
        pdf='pdf/'+os.path.basename(d.get('txt') or '').replace('.txt','')
        if not (pdf and os.path.exists(pdf)): continue
        tmp=tempfile.mkdtemp(); subprocess.run(['pdftoppm','-r','150','-png',pdf,tmp+'/p'],timeout=300)
        out=[]
        for img in sorted(glob.glob(tmp+'/p*.png')):
            r,_=eng(img); out.append('\n'.join(x[1] for x in (r or [])))
        t='\n\f'.join(out)
        txt=d['txt']
        
        open(txt,'w').write(t); d['txt']=txt; d['txtlen']=len(t); d['ocr']=True; ch+=1
        print(f,pdf,len(t),flush=True)
        json.dump(D,open(f,'w'))
    print(f,'ocr',ch,flush=True)
