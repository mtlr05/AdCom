from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
ss=getSampleStyleSheet(); s=ss['BodyText']; s.fontSize=6.3; s.leading=7.4
f=ss['BodyText'].clone('f'); f.fontSize=5.8; f.leading=6.8
P=lambda t:Paragraph(t,s)
C='<font color="green"><b>Confirmed</b></font>'; X='<font color="red"><b>Corrected</b></font>'; N='<font color="orange"><b>Not found</b></font>'
H=['Therapy','(a) Date / committee','(b) Pivotal vote (question)','(c) FDA outcome / pathway','Rare disease (orphan, same indication)','(e) Review type','(f) Center']
R=[
['1. Kymriah (tisagenlecleucel)','2017-07-12, ODAC '+C,'10-0 favourable; recommended approval in r/r pediatric/young-adult B-ALL (6-K, press) '+C,'Approved 2017-08-30, traditional '+C,'Y: ALL, designated 2014-01-31 (OOPD) '+C,'Priority (Novartis PR) '+C,'CBER '+C],
['2. Luxturna (voretigene)','2017-10-12, CTGTAC '+C,'16-0 favourable, unanimous recommendation (press, FDA review) '+C,'Approved 2017-12-19, traditional '+C,'Y: biallelic RPE65 IRD, 2015-03-18 (OOPD) '+C,'Priority (Spark 8-K) '+C,'CBER '+C],
['3. Lantidra (donislecel)','2021-04-15, CTGTAC '+C,'12-4-1; "overall favorable benefit-risk profile for some patients with T1D" (FDA SBRA) '+C,'Approved 2023-06-28, traditional '+C,'Y: brittle T1D, 2017-02-01 (OOPD) '+C,'Standard (FDA memo) '+C,'CBER '+C],
['4. Skysona (eli-cel)','2022-06-09, CTGTAC '+C,'15-0, no abstention found; "Do the benefits outweigh the risks... any sub-population" '+C,'Approved 2022-09-16, accelerated (approval letter) '+C,'Y: adrenoleukodystrophy, 2012-04-19 (OOPD) '+C,'Priority (bluebird PR) '+C,'CBER '+C],
['5. Zynteglo (beti-cel)','2022-06-10, CTGTAC '+C,'13-0 favourable, unanimous (press) '+C,'Approved 2022-08-17, traditional '+C,'Y: beta-thalassemia, 2013-03-18 (OOPD) '+C,'Priority (bluebird 8-K) '+C,'CBER '+C],
['6. Elevidys','2023-05-12, CTGTAC '+C,'8-6 favourable, in favour of accelerated approval (FDA SBRA) '+C,'Approved 2023-06-22, accelerated '+C,'Y: DMD, 2018-06-21 (OOPD) '+C,'Priority (Sarepta PR) '+C,'CBER '+C],
['7. NurOwn (MSC-NTF)','2023-09-27, CTGTAC '+C,'1-17-1; vote on substantial evidence of EFFECTIVENESS, not benefit-risk (FDA minutes) '+C,'Not approved: BLA withdrawn 2023-11-03, status unchanged '+C,'<b>Y</b> (dataset N): "mesenchymal stromal cells secreting neurotrophic factors", ALS, 2011-02-04, BrainStorm (OOPD) '+X,'Not found '+N,'CBER '+C],
['8. Deramiocel (CAP-1002)','2026-07-29, CTGTAC '+C,'3-9-0; effectiveness for DMD cardiomyopathy only; no benefit-risk vote (8-K) '+C,'Pending: PDUFA 2026-11-22 after major amendment; indication refocused on upper-limb function. No decision as of 2026-11-04 '+C,'Y: DMD, 2015-04-21, Capricor (OOPD) '+C,'Original BLA priority; adcom reviewed Class 2 resubmission '+C,'CBER '+C],
['9. Tudriqev (RP1)','2026-07-30, CTGTAC '+C,'10-3; "Are the efficacy results from IGNYTE evaluable and clinically meaningful?" (efficacy, not benefit-risk) '+C,'Approved <b>2026-08-06</b>, accelerated (FDA letter, BL 125827) '+C,'N: no RP1/Replimune/melanoma-HSV-1 designation in OOPD '+C+' (absence only)','Original BLA (received 2024-11-21) priority; adcom reviewed the resubmission (complete response 2026-06-02) '+C,'CBER '+C],
]
fn='''<b>Sources.</b> [P] = FDA/SEC primary; [S] = press/company release.
1 Kymriah: [P] Novartis 6-K 2017-07-13 sec.gov/Archives/edgar/data/1114448/000117184317004057/f6k_071217.htm (ODAC unanimous 10-0); [S] ASH Clinical News "FDA Panel Recommends Approval of CAR T-Cell"; [P] OOPD row; [S] Novartis PR 2017-03-29 ("granted FDA Priority Review"). Approval date 2017-08-30 is from the dataset and the widely reported FDA announcement; the FDA page was not re-opened in this pass. Exact ODAC question wording not re-read.
2 Luxturna: [P] FDA Clinical Review 2017-12-16 fda.gov/files/vaccines,%20blood%20&%20biologics/published/Clinical-Review--December-16--2017---LUXTURNA.pdf; [S] fightingblindness.org ("unanimously recommends approval"); [P] FDA media briefing 2017-12-19 fda.gov/media/109952/download; [P] Spark 8-K (priority).
3 Lantidra: [P] SBRA fda.gov/media/170457/download ("Yes = 12; No = 4; Abstain = 1"); [P] Clinical memo fda.gov/media/170827/download ("Priority Review: No"); [P] OOPD donislecel-jujn.
4 Skysona: [S] Reuters 2022-06-09 ("All 15 committee members voted unanimously"); [S] BioProcess Insider (exact question); [P] approval letter fda.gov/media/161665/download (2022-09-16, accelerated). No source found showing an abstention.
5 Zynteglo: [S] Medscape 975467 and pharmaceutical-technology.com ("13-0"); [P] FDA bulletin content.govdelivery.com/accounts/USFDA/bulletins/3287e67 (approved 2022-08-17); [P] bluebird 8-K 2021-11-22 (priority).
6 Elevidys: [P] SBRA fda.gov/media/169746/download (8-6); [P] FDA press release (accelerated approval 2023-06-22); [S] Sarepta PR (priority).
7 NurOwn: [P] CTGTAC minutes fda.gov/media/177306/download (17 no, 1 yes, 1 abstain on effectiveness); [S] Endpoints (withdrawal); [P] BrainStorm ARS sec.gov/Archives/edgar/data/1137883/000110465924090306/tm2421739d1_ars.pdf (withdrawn 2023-11-03). [P] OOPD: "mesenchymal stromal cells secreting neurotrophic factors", Treatment of ALS, 2011-02-04, BrainStorm Cell Therapeutics. No source found for priority or standard review.
8 Deramiocel: [P] Capricor 8-K 2026-07-29 capricor.com/investors/sec-filings/all-sec-filings/content/0001104659-26-088667/capr-20260729x8k.htm ("3 for, 9 against, 0 abstain"); [S] Capricor PR 2026-08-24 (PDUFA 2026-11-22, major amendment); [S] Yahoo Finance 2026-11-01 (still pending); [S] Capricor PR 2025-03-04 (original BLA priority).
9 Tudriqev: [P] FDA approval letter fda.gov/media/194128/download ("ACCELERATED BLA APPROVAL AUGUST 6, 2026"; BLA received 2024-11-21; amendment 2026-06-02 answering the 2026-04-10 action letter); [P] FDA notice "FDA grants accelerated approval to vusolimogene oderparepvec-wtpg"; [S] Replimune PR 2026-07-30 (10-3, exact question); [S] Replimune PR Jan 2025 (priority). OOPD searched for RP1, vusolimogene, Replimune and HSV/oncolytic melanoma entries: none for Replimune.
OOPD = FDA orphan database export (oopd_all.csv). Center for all nine: CBER. Kymriah's ODAC is a CDER committee, but CBER reviewed the BLA.'''
doc=SimpleDocTemplate('cgt_validation_table.pdf',pagesize=landscape(letter),leftMargin=18,rightMargin=18,topMargin=16,bottomMargin=14)
t=Table([[P('<b>%s</b>'%h) for h in H]]+[[P(c) for c in r] for r in R],colWidths=[78,82,170,135,135,100,52],repeatRows=1)
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.3,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('VALIGN',(0,0),(-1,-1),'TOP')]))
doc.build([Paragraph('<b>CGT adcom rows: field-by-field validation (secondary sources), Nov 4 2026</b>',ss['Heading4']),t,Spacer(1,4)]+[Paragraph(x,f) for x in fn.split('\n')])
