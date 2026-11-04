import json,re,sys
from concurrent.futures import ThreadPoolExecutor as TP
from lib import *
OLD={'ODAC':'Drugs/OncologicDrugsAdvisoryCommittee','PCNS':'Drugs/PeripheralandCentralNervousSystemDrugsAdvisoryCommittee','PDAC':'Drugs/PsychopharmacologicDrugsAdvisoryCommittee',
'CRDAC':'Drugs/CardiovascularandRenalDrugsAdvisoryCommittee','EMDAC':'Drugs/EndocrinologicandMetabolicDrugsAdvisoryCommittee','AMDAC':'Drugs/Anti-InfectiveDrugsAdvisoryCommittee',
'AVDAC':'Drugs/AntiviralDrugsAdvisoryCommittee','AAC':'Drugs/ArthritisAdvisoryCommittee','AADPAC':'Drugs/AnestheticAndAnalgesicDrugProductsAdvisoryCommittee',
'DODAC':'Drugs/DermatologicandOphthalmicDrugsAdvisoryCommittee','DSaRM':'Drugs/DrugSafetyandRiskManagementAdvisoryCommittee','GIDAC':'Drugs/GastrointestinalDrugsAdvisoryCommittee',
'MIDAC':'Drugs/MedicalImagingDrugsAdvisoryCommittee','NDAC':'Drugs/NonprescriptionDrugsAdvisoryCommittee','BRUDAC':'Drugs/ReproductiveHealthDrugsAdvisoryCommittee',
'PSCPAC':'Drugs/AdvisoryCommitteeforPharmaceuticalScienceandClinicalPharmacology','PADAC':'Drugs/Pulmonary-AllergyDrugsAdvisoryCommittee',
'CTGTAC':'BloodVaccinesandOtherBiologics/CellularTissueandGeneTherapiesAdvisoryCommittee','VRBPAC':'BloodVaccinesandOtherBiologics/VaccinesandRelatedBiologicalProductsAdvisoryCommittee',
'BPAC':'BloodVaccinesandOtherBiologics/BloodProductsAdvisoryCommittee','APAC':'BloodVaccinesandOtherBiologics/AllergenicProductsAdvisoryCommittee','PAC':'PediatricAdvisoryCommittee'}
NEW={'ODAC':['oncologic-drugs-advisory-committee'],'PCNS':['peripheral-and-central-nervous-system-drugs-advisory-committee'],'PDAC':['psychopharmacologic-drugs-advisory-committee'],
'CRDAC':['cardiovascular-and-renal-drugs-advisory-committee'],'EMDAC':['endocrinologic-and-metabolic-drugs-advisory-committee'],
'AMDAC':['antimicrobial-drugs-advisory-committee-formerly-known-anti-infective-drugs-advisory-committee','antimicrobial-drugs-advisory-committee'],'AVDAC':['antiviral-drugs-advisory-committee'],
'AAC':['arthritis-advisory-committee'],'AADPAC':['anesthetic-and-analgesic-drug-products-advisory-committee'],'DODAC':['dermatologic-and-ophthalmic-drugs-advisory-committee'],
'DSaRM':['drug-safety-and-risk-management-advisory-committee'],'GIDAC':['gastrointestinal-drugs-advisory-committee'],'GeMDAC':['genetic-metabolic-diseases-advisory-committee'],
'MIDAC':['medical-imaging-drugs-advisory-committee'],'NDAC':['nonprescription-drugs-advisory-committee'],
'BRUDAC':['obstetrics-reproductive-and-urologic-drugs-advisory-committee-formerly-bone-reproductive-and','bone-reproductive-and-urologic-drugs-advisory-committee-formerly-reproductive-health-drugs-advisory'],
'PSCPAC':['pharmaceutical-science-and-clinical-pharmacology-advisory-committee'],'PADAC':['pulmonary-allergy-drugs-advisory-committee'],
'CTGTAC':['cellular-tissue-and-gene-therapies-advisory-committee'],'VRBPAC':['vaccines-and-related-biological-products-advisory-committee'],'BPAC':['blood-products-advisory-committee'],
'APAC':['allergenic-products-advisory-committee']}
KEY=re.compile(r'minutes|voting|vote',re.I)
AI='https://web.archive.org/web/2017/https://www.fda.gov/AdvisoryCommittees/CommitteesMeetingMaterials/'
def old(c):
    root=AI+OLD[c]+'/default.htm'; seen=set(); out=[]; todo=[root]
    st=json.load(open('stage1.json')).get(c,{}).get('years',{})
    for yu in st:
        mm=re.search(r'(http://www.fda.gov/AdvisoryCommittees/.*ucm\d+\.htm)',yu)
        if mm: todo.append('https://web.archive.org/web/2017/'+mm.group(1))
    while todo:
        u=todo.pop(); 
        if u in seen: continue
        seen.add(u); h=get(u)
        for a,t in links(u,h):
            if re.search(r'^(19|20)\d\d Meeting Materials|^Meeting Materials',t) and 'archive' in a and a not in seen: todo.append(a)
            if KEY.search(t) and re.search(r'(download|\.pdf|ucm\d+\.htm)',a,re.I): out.append(dict(committee=c,era='old',page=u,url=a,title=t))
    return out
def new(c):
    out=[]
    for slug in NEW.get(c,[]):
        for y in range(2016,2027):
            p=f'https://www.fda.gov/advisory-committees/{slug}/{y}-meeting-materials-{slug}'
            h=get(p)
            if 'Page Not Found' in h[:3000] or len(h)<5000:
                p='https://web.archive.org/web/2026/'+p; h=get(p)
            for a,t in links(p,h):
                if KEY.search(t) and re.search(r'/media/\d+|download',a): out.append(dict(committee=c,era='new',year=y,page=p,url=a,title=t))
                elif re.search(r'advisory-committee-calendar/|meeting-announcement',a) and re.search(str(y),a+t):
                    out.append(dict(committee=c,era='new',year=y,page=p,url=a,title=t,kind='calendar'))
                    h2=get(a)
                    if len(h2)<5000 or 'Page Not Found' in h2[:3000]:
                        a='https://web.archive.org/web/2026/'+a.split('https://www.fda.gov',1)[-1].join(['https://www.fda.gov','']) if 'web.archive' not in a else a; h2=get(a)
                    for a2,t2 in links(a,h2):
                        if KEY.search(t2) and re.search(r'/media/\d+|download',a2): out.append(dict(committee=c,era='new',year=y,page=a,url=a2,title=t2,meeting=t))
    return out
res=[]
with TP(12) as ex:
    for r in ex.map(lambda c:(old(c) if c in OLD else [])+new(c), sorted(set(OLD)|set(NEW))):
        if r: print(r[0]['committee'],len(r),sum(1 for x in r if x.get('kind')!='calendar'),flush=True)
        res+=r
json.dump(res,open('minutes_links.json','w'),indent=0)
