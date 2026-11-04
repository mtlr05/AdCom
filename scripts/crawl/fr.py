import json,subprocess,urllib.parse,os
base='https://www.federalregister.gov/api/v1/documents.json'
allr={}
for y in range(2000,2027):
  for half in [('01-01','06-30'),('07-01','12-31')]:
    fn=f'fr/{y}_{half[0]}.json'
    if os.path.exists(fn): res=json.load(open(fn))
    else:
      res=[];page=1
      while True:
        q=[('conditions[agencies][]','food-and-drug-administration'),('conditions[type][]','NOTICE'),('conditions[term]','"advisory committee" notice of meeting'),
           ('conditions[publication_date][gte]',f'{y}-{half[0]}'),('conditions[publication_date][lte]',f'{y}-{half[1]}'),('per_page','100'),('page',str(page)),
           ('fields[]','title'),('fields[]','abstract'),('fields[]','publication_date'),('fields[]','document_number'),('fields[]','html_url'),('fields[]','raw_text_url'),('fields[]','dates')]
        u=base+'?'+urllib.parse.urlencode(q)
        d=json.loads(subprocess.run(['curl','-s','--max-time','60',u],capture_output=True,text=True).stdout or '{}')
        res+=d.get('results',[]) or []
        if not d.get('next_page_url'): break
        page+=1
      json.dump(res,open(fn,'w'))
    for r in res: allr[r['document_number']]=r
    print(y,half[0],len(res),flush=True)
json.dump(allr,open('fr_all.json','w'))
print(len(allr))
