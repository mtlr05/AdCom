"""Data-driven CGT tables built from adcom_full_pivotal.csv (CGT==True)."""
import os,re,pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
OUT=os.environ.get('CHART_DIR','charts'); os.makedirs(OUT,exist_ok=True)
M=pd.read_csv('adcom_full_pivotal.csv',dtype=str).fillna('')
G=M[M.CGT.str.lower()=='true'].sort_values('meeting_date')
ss=getSampleStyleSheet(); s=ss['BodyText']; s.fontSize=6.3; s.leading=7.4
esc=lambda t:str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def link(t): return re.sub(r'(https?://\S+)',lambda m:f'<link href="{m.group(1)}" color="blue">{m.group(1)}</link>',esc(t))
P=lambda t:Paragraph(link(t),s)
def build(fn,title,H,rows,widths):
    doc=SimpleDocTemplate(os.path.join(OUT,fn),pagesize=landscape(letter),leftMargin=18,rightMargin=18,topMargin=16,bottomMargin=14)
    t=Table([[Paragraph('<b>'+h+'</b>',s) for h in H]]+[[P(c) for c in r] for r in rows],colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.3,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8e8e8')),('VALIGN',(0,0),(-1,-1),'TOP')]))
    doc.build([Paragraph('<b>'+title+'</b>',ss['Heading4']),Spacer(1,4),t,Spacer(1,4),Paragraph('Generated from adcom_full_pivotal.csv (CGT = CTGTAC rows + Kymriah, Ryoncil, Carvykti, Abecma). Values are exactly those in the dataset; see AGENTS.md corrections log 2026-11-04.',s)])
name=lambda r:(r.brand or r.generic or r.product_text)[:40]
rows=[[name(r),f'{r.meeting_date} {r.committee}',f'{r.vote_yes}-{r.vote_no}-{r.vote_abstain} {r.adcom}',r.vote_type+' ('+r.vote_type_basis+')',f'{r.final_action} {r.final_action_date}',r.orphan_for_indication+': '+r.orphan_indication_basis,r.review_priority,r.center+' ('+r.center_basis+')'] for r in G.itertuples()]
build('cgt_validation_table_v5.pdf','CGT adcom rows: field values in the dataset (2026-11-04)',['Therapy','Date / committee','Vote (Y-N-A) / coding','Vote type','FDA outcome','Orphan for indication','Review priority','Center'],rows,[70,60,70,120,110,150,50,110])
rows=[[name(r),r.meeting_date,r.review_priority,r.priority_basis] for r in G.itertuples()]
build('cgt_priority_review_table_v5.pdf','CGT review priority and source (2026-11-04)',['Therapy','Meeting','Review priority','Basis / source URL'],rows,[100,70,70,500])
print('cgt tables',len(G))
