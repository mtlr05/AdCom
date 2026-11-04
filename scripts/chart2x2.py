"""Shared 2x2 chart builder. Reads adcom_full_pivotal.csv; writes into $CHART_DIR (default ./charts)."""
import os, pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
OUT=os.environ.get('CHART_DIR','charts')
def load(cgt=False,approval_only=False):
    M=pd.read_csv('adcom_full_pivotal.csv',dtype=str).fillna('')
    M['rep']=M.replaced_by_later_meeting.str.lower().eq('true')
    S=M[(~M.rep)&(M.adcom.isin(['favourable','unfavourable']))].copy()
    if cgt: S=S[S.CGT.str.lower()=='true']
    if approval_only: S=S[S.vote_type=='approval/benefit-risk']
    fa=S.final_action.str.lower()
    ok=~S.final_action.isin(['unverified','nan',''])&~fa.str.startswith('pending')
    S['out']=None; S.loc[ok&fa.str.startswith('approved'),'out']='A'; S.loc[ok&~fa.str.startswith('approved'),'out']='R'
    return M,S
def tables(S):
    o=S.orphan_for_indication.str.upper(); p=S.review_priority.str.upper()
    subs={'1) Common diseases (not orphan)':S[o.str.startswith('N')],'2) Rare diseases (orphan)':S[o.str.startswith('Y')],
          '3) Rare and priority review':S[o.str.startswith('Y')&p.str.startswith('PRI')],'4) Aggregate (all)':S}
    res={}
    for k,d in subs.items():
        unv=int(d.out.isna().sum()); d=d[d.out.notna()]; r=dict(unv=unv,cen={})
        for a,oo,l in [('favourable','A','AA'),('favourable','R','AR'),('unfavourable','A','RA'),('unfavourable','R','RR')]:
            x=d[(d.adcom==a)&(d.out==oo)]; r[l]=len(x); vc=x.center.value_counts()
            r['cen'][l]=' / '.join(f'{c} {vc[c]}' for c in ['CDER','CBER'] if c in vc) or '-'
        r['n']=r['AA']+r['AR']+r['RA']+r['RR']; res[k]=r
    return res
def draw(res,title,foot,fn,pct):
    fig,axs=plt.subplots(2,2,figsize=(12,8.5))
    for ax,(k,r) in zip(axs.flat,res.items()):
        ax.set_xlim(0,2);ax.set_ylim(0,2);ax.axis('off'); t=r['n'] or 1
        raw={l:100*r[l]/t for l in ['AA','AR','RA','RR']}; fl={l:int(raw[l]) for l in raw}
        if r['n']:
            for l in sorted(raw,key=lambda l:-(raw[l]-fl[l]))[:100-sum(fl.values())]: fl[l]+=1
        for x,y,l,c in [(0,1,'AA','#cfe8cf'),(1,1,'AR','#f6dcb0'),(0,0,'RA','#f6dcb0'),(1,0,'RR','#cfe8cf')]:
            ax.add_patch(Rectangle((x*0.95+0.05,y*0.9+0.05),0.9,0.85,fc=c,ec='#444'))
            big=f"{l}\n{fl[l]}%" if pct else f"{l}\n{r[l]}"
            ax.text(x*0.95+0.5,y*0.9+0.58,big,ha='center',va='center',fontsize=18,weight='bold')
            ax.text(x*0.95+0.5,y*0.9+0.27,f"n={r[l]}",ha='center',va='center',fontsize=9)
            ax.text(x*0.95+0.5,y*0.9+0.14,r['cen'][l],ha='center',va='center',fontsize=8,color='#333')
        ax.set_title(f"{k}\nn={r['n']}; {r['unv']} unverified/pending outcome(s) left out",fontsize=10,weight='bold',loc='left')
        ax.text(0.5,0,"FDA approved",ha='center',fontsize=8);ax.text(1.45,0,"FDA not approved",ha='center',fontsize=8)
        ax.text(0.03,1.4,"Adcom\nfav.",ha='right',va='center',fontsize=8);ax.text(0.03,0.5,"Adcom\nunfav.",ha='right',va='center',fontsize=8)
    import textwrap; fig.suptitle('\n'.join(textwrap.wrap(title,140)),fontsize=9); import textwrap; fig.text(0.5,0.005,'\n'.join(textwrap.wrap(foot,170)),ha='center',fontsize=7.5)
    plt.tight_layout(rect=(0,0.04,1,0.94)); os.makedirs(OUT,exist_ok=True); plt.savefig(os.path.join(OUT,fn),dpi=150); plt.close(fig)
    return res
def make(kind,pct,approval_only,fn):
    M,S=load(cgt=(kind=='cgt'),approval_only=approval_only); res=tables(S)
    ex_tie=int((M.adcom=='tie').sum()); ex_oth=int((~M.adcom.isin(['favourable','unfavourable','tie'])).sum())
    scope='Cell and gene therapies only (CTGTAC + Kymriah, Ryoncil, Carvykti, Abecma)' if kind=='cgt' else 'FDA adcom pivotal vote vs FDA final decision'
    vt='; approval/benefit-risk votes only' if approval_only else '; all pivotal votes'
    title=f"{scope}{vt}, 2016-11-04 to 2026 (A = approved/favourable, R = rejected/unfavourable; first letter = adcom, second = FDA)"
    foot=f"Excludes {ex_tie} tied votes, {ex_oth} non-binary-coded vote(s) (Lynparza 2023 restricted) and superseded meetings. Outcome = FDA final decision; later approvals count as approved. Rare = OOPD orphan designation for the indication. Centre counts under n."
    draw(res,title,foot,fn,pct); print(fn,{k:(r['AA'],r['AR'],r['RA'],r['RR'],r['unv']) for k,r in res.items()}); return res
