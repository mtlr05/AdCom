"""Factor screen and AMT-130 probabilities from adcom_full_pivotal.csv.

Run from data/ with scripts/ on PYTHONPATH. Does not edit the pivotal CSV.

Fits every subset of the pre-meeting factors with an L2-penalized logistic
regression. R-squared is Nagelkerke pseudo-R-squared. Models used for the
prediction are the best few stable fits by AIC, plus the highest-R-squared
stable model if AIC did not already keep it. A fit whose unpenalized
coefficients run off (separation) is reported and is not used as a probability.
"""
import itertools, os
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit
from scipy.stats import beta as beta_dist

CHART = os.environ.get("CHART_DIR", "charts")
FACTORS = ["orphan", "priority", "CGT", "CNS", "cber", "initial"]
# AMT-130: orphan, priority, CGT, CBER, initial BLA. CNS is unknown.
AMT = dict(orphan=1, priority=1, CGT=1, CNS=0, cber=1, initial=1)


def cells(df):
    d = df[df.approved.notna()]
    def g(a, b):
        return int(((d.adcom == a) & (d.approved == b)).sum())
    return g("favourable", True), g("favourable", False), g("unfavourable", True), g("unfavourable", False), len(d)


def prepare(m):
    m = m.copy()
    m["replaced"] = m.replaced_by_later_meeting.map(lambda v: str(v) == "True")
    m["cgt"] = m.CGT.map(lambda v: str(v) == "True")
    m["cns"] = m.CNS.map(lambda v: str(v) == "True")
    fa = m.final_action.astype(str)
    pending = fa.str.lower().isin(["unverified", "nan", ""]) | fa.str.lower().str.startswith("pending")
    m["approved"] = fa.str.lower().str.startswith("approved").where(~pending)
    a1 = m.action_at_1yr.astype(str)
    m["index_ok"] = ~a1.isin(["unverified", "", "nan"]) & ~a1.str.startswith("pending")
    m["index_approved"] = (a1 == "approved").where(m.index_ok)
    m["fav"] = np.where(m.adcom == "favourable", 1.0, np.where(m.adcom == "unfavourable", 0.0, np.nan))
    m["orphan_y"] = np.where(m.orphan_for_indication.str.upper().str.startswith("Y"), 1.0,
                     np.where(m.orphan_for_indication.str.upper().str.startswith("N"), 0.0, np.nan))
    m["pri"] = np.where(m.review_priority.str.upper().str.startswith("PRI"), 1.0,
                np.where(m.review_priority.str.upper().str.startswith("STA"), 0.0, np.nan))
    m["cber_i"] = (m.center == "CBER").astype(float)
    m["init_i"] = m.meeting_type.str.startswith("initial").astype(float)
    yr = pd.to_datetime(m.meeting_date, errors="coerce").dt.year
    m["year_c"] = (yr - 2020).astype(float)
    return m


def gate(m, published):
    S = m[(~m.replaced) & (m.adcom != "tie")]
    fails = []
    def check(name, df):
        got = cells(df)
        row = published[(published.subset == name) & (published.outcome == "final")]
        if len(row) != 1:
            fails.append(name + " missing from two_by_two")
            return
        exp = tuple(int(row.iloc[0][c]) for c in ["FavApproved", "FavNotApproved", "UnfavApproved", "UnfavNotApproved"])
        if got[:4] != exp:
            fails.append(f"{name} recomputed {got[:4]} != published {exp}")
    check("All", S)
    check("Common (orphan N)", S[S.orphan_for_indication.str.upper().str.startswith("N")])
    check("Rare (orphan Y)", S[S.orphan_for_indication.str.upper().str.startswith("Y")])
    check("Rare + priority", S[S.orphan_for_indication.str.upper().str.startswith("Y") & S.review_priority.str.upper().str.startswith("PRI")])
    check("CGT (CTGTAC + CAR-T/MSC)", S[S.cgt])
    check("Approval-only: All", S[S.vote_type == "approval/benefit-risk"])
    if fails:
        raise SystemExit("validity gate failed:\n" + "\n".join(fails))
    print("validity gate: two_by_two cells match")


def design(df, cols, y):
    use = df.dropna(subset=cols + [y]).copy()
    X = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in cols])
    yy = use[y].to_numpy(float)
    return use, X, yy


def fit_logit(X, y, penalize):
    p = X.shape[1]
    def objective(b):
        eta = np.clip(X @ b, -30, 30)
        ll = np.sum(y * eta - np.logaddexp(0, eta))
        if not penalize:
            return -ll
        pen = 0.5 * (b[0] / 2.5) ** 2 + 0.5 * np.sum((b[1:] / 1.0) ** 2)
        return -ll + pen
    res = minimize(objective, np.zeros(p), method="BFGS")
    b = res.x
    eta = np.clip(X @ b, -30, 30)
    ll = float(np.sum(y * eta - np.logaddexp(0, eta)))
    stable = bool(res.success) and np.all(np.abs(b) < 8)
    return b, ll, stable


def r2(ll, ll0, n):
    if n <= 0 or not np.isfinite(ll) or not np.isfinite(ll0) or ll0 == 0:
        return np.nan, np.nan
    mcf = 1 - (ll / ll0)
    cs = 1 - np.exp(2 / n * (ll0 - ll))
    denom = 1 - np.exp(2 / n * ll0)
    nag = cs / denom if denom > 0 else np.nan
    return float(nag), float(mcf)


def screen(df, y, with_vote):
    """Every subset of FACTORS. y column already 0/1."""
    rows = []
    # null, on the rows that have y (priority/orphan missingness depends on the subset)
    base_cols_needed = [y]
    for mask in itertools.product([0, 1], repeat=len(FACTORS)):
        cols = [f for f, k in zip(FACTORS, mask) if k]
        need = cols + ([ "fav" ] if with_vote else [])
        # map factor names to frame columns
        colmap = {"orphan": "orphan_y", "priority": "pri", "CGT": "cgt", "CNS": "cns", "cber": "cber_i", "initial": "init_i", "vote": "fav"}
        raw = [colmap[c] for c in cols] + (["fav"] if with_vote else [])
        use, X, yy = design(df, raw, y)
        if len(use) < 20 or yy.sum() in (0, len(yy)):
            rows.append(dict(factors="+".join(cols + (["vote"] if with_vote else [])) or "(intercept)",
                             n=len(use), nagelkerke=np.nan, mcfadden=np.nan, aic=np.nan, stable=False,
                             note="too few rows or no outcome variation"))
            continue
        b_p, ll_p, _ = fit_logit(X, yy, True)
        b_u, ll_u, stable = fit_logit(X, yy, False)
        # null on the same rows
        X0 = np.ones((len(yy), 1))
        _, ll0, _ = fit_logit(X0, yy, False)
        nag, mcf = r2(ll_u if stable else ll_p, ll0, len(yy))
        k = X.shape[1]
        aic = -2 * (ll_u if stable else ll_p) + 2 * k
        rows.append(dict(factors="+".join(cols + (["vote"] if with_vote else [])) or "(intercept)",
                         cols=cols, with_vote=with_vote, n=len(use), events=int(yy.sum()),
                         nagelkerke=nag, mcfadden=mcf, aic=aic, stable=stable,
                         ll=ll_u if stable else ll_p, b_pen=b_p, b_unpen=b_u,
                         raw=raw, note="" if stable else "unpenalized fit separated; R2 from penalized likelihood, not used for a probability"))
    return pd.DataFrame(rows)


def keep(sc, k=4):
    stable = sc[sc.stable == True].dropna(subset=["aic", "nagelkerke"])
    if not len(stable):
        return stable
    top = stable.sort_values(["aic", "nagelkerke"]).head(k)
    best_r = stable.sort_values("nagelkerke", ascending=False).head(1)
    out = pd.concat([top, best_r]).drop_duplicates(subset=["factors"])
    return out


def predict_row(b, cols, with_vote, cns, vote):
    colmap = {"orphan": "orphan", "priority": "priority", "CGT": "CGT", "CNS": "CNS", "cber": "cber", "initial": "initial"}
    x = [1.0]
    for c in cols:
        if c == "CNS":
            x.append(float(cns))
        else:
            x.append(float(AMT[colmap[c]]))
    if with_vote:
        x.append(float(vote))
    eta = float(np.clip(np.dot(b, x), -30, 30))
    return float(expit(eta))


def stratum_beta(df, cols, y, cns, vote=None):
    """Jeffreys interval on the rows that match AMT-130 on the factors in the model."""
    sub = df.dropna(subset=[y]).copy()
    spec = {"orphan": 1, "priority": 1, "CGT": 1, "CNS": cns, "cber": 1, "initial": 1}
    colmap = {"orphan": "orphan_y", "priority": "pri", "CGT": "cgt", "CNS": "cns", "cber": "cber_i", "initial": "init_i"}
    for c in cols:
        sub = sub[sub[colmap[c]] == spec[c]]
    if vote is not None:
        sub = sub[sub.fav == vote]
    sub = sub.dropna(subset=[y])
    k = int(sub[y].sum()) if len(sub) else 0
    n = len(sub)
    if n == 0:
        return n, k, np.nan, np.nan, np.nan
    lo, med, hi = beta_dist.ppf([0.025, 0.5, 0.975], 0.5 + k, 0.5 + n - k)
    return n, k, float(med), float(lo), float(hi)


COLMAP = {"orphan": "orphan_y", "priority": "pri", "CGT": "cgt", "CNS": "cns", "cber": "cber_i", "initial": "init_i"}


def raw_cols(cols, with_vote, extra=()):
    return [COLMAP[c] for c in cols] + (["fav"] if with_vote else []) + list(extra)


def refit(df, cols, y, with_vote, extra=()):
    """Penalized and unpenalized fit. Returns None if the rows cannot support it."""
    use, X, yy = design(df, raw_cols(cols, with_vote, extra), y)
    if len(use) < 20 or yy.sum() in (0, len(yy)):
        return None
    b_p, ll_p, _ = fit_logit(X, yy, True)
    b_u, ll_u, stable = fit_logit(X, yy, False)
    _, ll0, _ = fit_logit(np.ones((len(yy), 1)), yy, False)
    nag, mcf = r2(ll_u if stable else ll_p, ll0, len(yy))
    aic = -2 * (ll_u if stable else ll_p) + 2 * X.shape[1]
    return dict(n=len(use), events=int(yy.sum()), nagelkerke=nag, mcfadden=mcf, aic=aic,
                stable=stable, b_pen=b_p, note="" if stable else "separated; not used as a probability")


def boot_pred(df, cols, y, with_vote, cns, vote, B=400):
    colmap = {"orphan": "orphan_y", "priority": "pri", "CGT": "cgt", "CNS": "cns", "cber": "cber_i", "initial": "init_i"}
    raw = [colmap[c] for c in cols] + (["fav"] if with_vote else [])
    use, X, yy = design(df, raw, y)
    rng = np.random.default_rng(130)
    preds = []
    n = len(yy)
    for _ in range(B):
        ix = rng.integers(0, n, n)
        if len(np.unique(yy[ix])) < 2:
            continue
        b, _, _ = fit_logit(X[ix], yy[ix], True)
        preds.append(predict_row(b, cols, with_vote, cns, vote))
    if len(preds) < 50:
        return np.nan, np.nan
    return float(np.quantile(preds, 0.025)), float(np.quantile(preds, 0.975))


def main():
    m = prepare(pd.read_csv("adcom_full_pivotal.csv", dtype=str).fillna(""))
    published = pd.read_csv("two_by_two.csv")
    gate(m, published)
    base = m[(~m.replaced) & m.fav.notna()].copy()
    appr = base[base.vote_type == "approval/benefit-risk"].copy()
    known = appr[appr.approved.notna()].copy()
    known["y_app"] = known.approved.astype(float)
    appr["y_fav"] = appr.fav
    # tiers
    print("approval-question rows", len(appr), "with a final outcome", len(known))
    print("vote tiers", appr.vote_source_tier.value_counts().to_dict())
    print("outcome tiers", known.outcome_source_tier.value_counts().to_dict())
    print("priority still unverified", int((m.review_priority == "unverified").sum()), "orphan review", int((m.orphan_for_indication == "review").sum()))
    both = known.dropna(subset=["index_approved"])
    disagree = int((both.approved.astype(bool) != both.index_approved.astype(bool)).sum())
    print("final vs 1-year disagreements among rows with both labels", disagree, "of", len(both))

    fav_sc = screen(appr, "fav", False)
    app_sc = screen(known, "y_app", False)
    app_v = screen(known, "y_app", True)
    fav_keep = keep(fav_sc)
    app_keep = keep(app_sc)
    appv_keep = keep(app_v)

    # All pivotal votes are a sensitivity. Same factor grid, wider vote-type set.
    piv = base.copy()
    piv_known = piv[piv.approved.notna()].copy()
    piv_known["y_app"] = piv_known.approved.astype(float)
    piv_fav_sc = screen(piv, "fav", False)
    piv_app_sc = screen(piv_known, "y_app", False)
    piv_appv_sc = screen(piv_known, "y_app", True)

    pred_rows = []
    def p_fav(fav_screen, cols, cns):
        key = "+".join(cols) or "(intercept)"
        hit = fav_screen[fav_screen.factors == key]
        if not len(hit) or not bool(hit.iloc[0].stable):
            return np.nan
        return predict_row(hit.iloc[0].b_pen, list(hit.iloc[0].cols), False, cns, None)

    def add_preds(label, kept, frame, y, with_vote, fav_screen, bootstrap=True):
        for _, r in kept.iterrows():
            cols = list(r.cols)
            for cns in (0, 1):
                vote_for_boot = 1 if with_vote else None
                lo, hi = boot_pred(frame, cols, y, with_vote, cns, vote_for_boot) if bootstrap else (np.nan, np.nan)
                nb, kb, med, blo, bhi = stratum_beta(frame, cols, y, cns, vote_for_boot)
                pf = predict_row(r.b_pen, cols, True, cns, 1) if with_vote else np.nan
                pu = predict_row(r.b_pen, cols, True, cns, 0) if with_vote else np.nan
                pfav = p_fav(fav_screen, cols, cns) if with_vote else np.nan
                marg = pfav * pf + (1 - pfav) * pu if pfav == pfav else np.nan
                pred_rows.append(dict(screen=label, factors=r.factors, cns=cns, n=r.n, events=r.events,
                                      nagelkerke=r.nagelkerke, mcfadden=r.mcfadden, aic=r.aic, stable=bool(r.stable),
                                      p=predict_row(r.b_pen, cols, with_vote, cns, vote_for_boot),
                                      p_if_favourable=pf, p_if_unfavourable=pu, p_marginal=marg,
                                      boot_lo=lo, boot_hi=hi,
                                      stratum_n=nb, stratum_events=kb, stratum_median=med, stratum_lo=blo, stratum_hi=bhi))

    add_preds("P(favourable) approval-question votes", fav_keep, appr, "fav", False, fav_sc)
    add_preds("P(FDA final approval)", app_keep, known, "y_app", False, fav_sc)
    add_preds("P(FDA final approval | vote)", appv_keep, known, "y_app", True, fav_sc)
    add_preds("sensitivity all-pivotal P(favourable)", keep(piv_fav_sc), piv, "fav", False, piv_fav_sc, bootstrap=False)
    add_preds("sensitivity all-pivotal P(FDA final approval)", keep(piv_app_sc), piv_known, "y_app", False, piv_fav_sc, bootstrap=False)
    add_preds("sensitivity all-pivotal P(FDA final approval | vote)", keep(piv_appv_sc), piv_known, "y_app", True, piv_fav_sc, bootstrap=False)

    # 1-year action: refit the winning approval-question models. Not a new search.
    idx = known[known.index_approved.notna()].copy()
    idx["y_idx"] = idx.index_approved.astype(float)
    for label, kept, with_vote in [
        ("sensitivity 1-year approval", app_keep, False),
        ("sensitivity 1-year approval | vote", appv_keep, True),
    ]:
        for _, r in kept.iterrows():
            cols = list(r.cols)
            fit = refit(idx, cols, "y_idx", with_vote)
            if fit is None or not fit["stable"]:
                pred_rows.append(dict(screen=label, factors=r.factors, cns=0, n=0 if fit is None else fit["n"],
                                      events=0 if fit is None else fit["events"], nagelkerke=np.nan, mcfadden=np.nan,
                                      aic=np.nan, stable=False, p=np.nan, p_if_favourable=np.nan, p_if_unfavourable=np.nan,
                                      p_marginal=np.nan, boot_lo=np.nan, boot_hi=np.nan, stratum_n=0, stratum_events=0,
                                      stratum_median=np.nan, stratum_lo=np.nan, stratum_hi=np.nan))
                continue
            for cns in (0, 1):
                vote_for = 1 if with_vote else None
                pf = predict_row(fit["b_pen"], cols, True, cns, 1) if with_vote else np.nan
                pu = predict_row(fit["b_pen"], cols, True, cns, 0) if with_vote else np.nan
                nb, kb, med, blo, bhi = stratum_beta(idx, cols, "y_idx", cns, vote_for)
                pred_rows.append(dict(screen=label, factors=r.factors, cns=cns, n=fit["n"], events=fit["events"],
                                      nagelkerke=fit["nagelkerke"], mcfadden=fit["mcfadden"], aic=fit["aic"], stable=True,
                                      p=predict_row(fit["b_pen"], cols, with_vote, cns, vote_for),
                                      p_if_favourable=pf, p_if_unfavourable=pu, p_marginal=np.nan,
                                      boot_lo=np.nan, boot_hi=np.nan,
                                      stratum_n=nb, stratum_events=kb, stratum_median=med, stratum_lo=blo, stratum_hi=bhi))

    # Year, linear and centered at 2020, only on the kept subsets.
    year_notes = []
    for label, kept, frame, y, with_vote in [
        ("P(favourable)", fav_keep, appr, "fav", False),
        ("P(FDA final approval)", app_keep, known, "y_app", False),
    ]:
        for _, r in kept.iterrows():
            cols = list(r.cols)
            base_fit = refit(frame, cols, y, with_vote)
            yr_fit = refit(frame, cols, y, with_vote, extra=("year_c",))
            if base_fit is None or yr_fit is None:
                continue
            year_notes.append((label, r.factors, base_fit["aic"], yr_fit["aic"], yr_fit["nagelkerke"], yr_fit["stable"]))
            if yr_fit["stable"] and yr_fit["aic"] + 0.01 < base_fit["aic"]:
                # Meeting year 2026 is year_c = 6. The year term is the last column.
                b = yr_fit["b_pen"]
                for cns in (0, 1):
                    x = [1.0] + [float(cns if c == "CNS" else AMT[c]) for c in cols] + [6.0]
                    p = float(expit(np.clip(np.dot(b, x), -30, 30)))
                    pred_rows.append(dict(screen="sensitivity year " + label, factors=r.factors + "+year", cns=cns,
                                          n=yr_fit["n"], events=yr_fit["events"], nagelkerke=yr_fit["nagelkerke"],
                                          mcfadden=yr_fit["mcfadden"], aic=yr_fit["aic"], stable=True, p=p,
                                          p_if_favourable=np.nan, p_if_unfavourable=np.nan, p_marginal=np.nan,
                                          boot_lo=np.nan, boot_hi=np.nan, stratum_n=0, stratum_events=0,
                                          stratum_median=np.nan, stratum_lo=np.nan, stratum_hi=np.nan))

    pred = pd.DataFrame(pred_rows)
    pred.to_csv("amt130_prediction.csv", index=False)
    primary = pred[~pred.screen.str.startswith("sensitivity")].copy()

    # forest plot of the main CNS-off predictions
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    # The unfiltered intercept sits above the priority-conditioned rows. The
    # criterion is not comparable across those two sample sizes.
    intercept_rows = []
    for sname, frame, y in [
        ("P(favourable) approval-question votes", appr, "fav"),
        ("P(FDA final approval)", known, "y_app"),
    ]:
        fit = refit(frame, [], y, False)
        lo, hi = boot_pred(frame, [], y, False, 0, None)
        intercept_rows.append(dict(screen=sname, factors="(intercept)", cns=0,
                                    p=predict_row(fit["b_pen"], [], False, 0, None),
                                    boot_lo=lo, boot_hi=hi))
    show = pd.concat([pd.DataFrame(intercept_rows), primary[primary.cns == 0]], ignore_index=True)
    def lab(screen):
        return (screen.replace("P(favourable) approval-question votes", "Favourable vote")
                      .replace("P(FDA final approval | vote)", "Approval given the vote")
                      .replace("P(FDA final approval)", "FDA approval"))
    def factors_plain(text):
        if str(text) == "(intercept)":
            return "no factors, all meetings"
        names = {"priority": "priority", "initial": "initial application", "orphan": "orphan",
                 "CGT": "cell/gene therapy", "cber": "biologics center", "CNS": "neurology committee",
                 "vote": "vote", "year": "year"}
        return " + ".join(names.get(p, p) for p in str(text).split("+"))
    show["label"] = show.screen.map(lab) + " | " + show.factors.map(factors_plain)
    show = show.iloc[::-1]
    fig, ax = plt.subplots(figsize=(11, max(3.2, 0.42 * len(show))))
    ypos = np.arange(len(show))
    ax.hlines(ypos, show.boot_lo, show.boot_hi, color="0.5")
    ax.plot(show.p, ypos, "o", color="0.15")
    ax.set_yticks(ypos)
    ax.set_yticklabels(show.label, fontsize=7)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Predicted probability (penalized logistic; line is bootstrap 95%)")
    ax.set_title("Top points use every meeting. A priority row sets priority review to yes.")
    fig.tight_layout()
    os.makedirs(CHART, exist_ok=True)
    fig.savefig(os.path.join(CHART, "amt130_prediction_forest.png"), dpi=140)
    plt.close()

    def fmt(p):
        return "n/a" if p != p else f"{p:.2f}"
    def fmt3(p):
        return "n/a" if p != p else f"{p:.3f}"
    def fmt1(p):
        return "n/a" if p != p else f"{p:.1f}"

    lines = []
    lines.append("# AMT-130: favourable adcom and FDA approval")
    lines.append("")
    lines.append("Historical rates among products that already had a product-approval vote. The model does not see the external-control analysis, the 48-month cUHDRS result, or accelerated approval. A small R-squared means the pre-meeting labels explain little of the vote.")
    lines.append("")
    lines.append("AMT-130 vector: orphan Y (OOPD 525216, 27 Sep 2017, AAV5 microRNA to huntingtin, uniQure), priority review (uniQure, 2 and 4 Nov 2026, company release), CGT, CBER, initial BLA. CNS is predicted both ways because the committee is not set. CNS in this table means the committee was PCNS or PDAC.")
    lines.append("")
    lines.append(f"Validity: recomputed 2x2 cells match `two_by_two.csv`. Approval-question rows: {len(appr)}. With a final outcome: {len(known)}. Vote source among approval-question rows: {appr.vote_source_tier.value_counts().to_dict()}. Outcome source: {known.outcome_source_tier.value_counts().to_dict()}. Priority still unverified: {int((m.review_priority=='unverified').sum())}. Orphan still `review`: {int((m.orphan_for_indication=='review').sum())} (dropped from models that use orphan). Final vs 1-year label disagreements: {disagree} of {len(both)} rows that have both.")
    lines.append("")
    lines.append("R-squared is Nagelkerke pseudo-R-squared. AIC keeps the smaller model when extra factors do not help. The intercept prior is Normal(0, 2.5); other coefficients Normal(0, 1). Unpenalized fits with a coefficient past 8 are marked separated and are not used as a probability.")
    lines.append("")
    lines.append("## Kept models, CNS off")
    lines.append("")
    lines.append("| Screen | Factors | n | Nagelkerke R2 | AIC | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |")
    lines.append("|---|---|---:|---:|---:|---:|---|---:|---|")
    for _, r in primary[primary.cns == 0].iterrows():
        lines.append(f"| {r.screen} | {r.factors} | {int(r.n)} | {fmt3(r.nagelkerke)} | {fmt1(r.aic)} | {fmt(r.p)} | {fmt(r.boot_lo)}–{fmt(r.boot_hi)} | {int(r.stratum_n)} ({int(r.stratum_events)}) | {fmt(r.stratum_median)} ({fmt(r.stratum_lo)}–{fmt(r.stratum_hi)}) |")
    lines.append("")
    lines.append("## Same models, CNS on (joint PCNS)")
    lines.append("")
    lines.append("| Screen | Factors | P | Bootstrap 95% | Stratum n (events) | Stratum median (95% CrI) |")
    lines.append("|---|---|---:|---|---:|---|")
    for _, r in primary[primary.cns == 1].iterrows():
        lines.append(f"| {r.screen} | {r.factors} | {fmt(r.p)} | {fmt(r.boot_lo)}–{fmt(r.boot_hi)} | {int(r.stratum_n)} ({int(r.stratum_events)}) | {fmt(r.stratum_median)} ({fmt(r.stratum_lo)}–{fmt(r.stratum_hi)}) |")
    lines.append("")
    def rng(screen):
        s = primary[(primary.screen == screen) & (primary.cns == 0)]
        if not len(s):
            return np.nan, np.nan
        return float(s.p.min()), float(s.p.max())
    a, b = rng("P(favourable) approval-question votes")
    c, d = rng("P(FDA final approval)")
    lines.append(f"CNS off, the kept models give P(favourable) from {fmt(a)} to {fmt(b)} and P(FDA final approval), not conditioning on the vote, from {fmt(c)} to {fmt(d)}.")
    lines.append("")
    cond = primary[(primary.screen == "P(FDA final approval | vote)") & (primary.cns == 0)]
    if len(cond):
        lines.append(f"Conditioning on the vote, P(approve | favourable) runs from {cond.p_if_favourable.min():.2f} to {cond.p_if_favourable.max():.2f}, and P(approve | unfavourable) from {cond.p_if_unfavourable.min():.2f} to {cond.p_if_unfavourable.max():.2f}.")
        marg = cond.p_marginal.dropna()
        if len(marg):
            lines.append(f"The marginal, each model's P(favourable) times P(approve | favourable) plus the unfavourable term, runs from {marg.min():.2f} to {marg.max():.2f}. The low end is a vote model whose paired stage-1 model does not include priority or CGT, so that end is not the AMT-130 covariate profile.")
        lines.append("")
    best = fav_sc[fav_sc.stable == True].sort_values("nagelkerke", ascending=False).head(1)
    if len(best):
        lines.append(f"Best stable pre-meeting model for a favourable vote: {best.iloc[0].factors}, Nagelkerke R2 {best.iloc[0].nagelkerke:.3f}. That is a small share of the variation. Most of the association in this table is between the vote and the later FDA action, and the covariates are regulatory labels, not the data package.")
    lines.append("")
    lines.append("Stratum column: Jeffreys beta-binomial on the rows that match AMT-130 on the factors in that model. A stratum under about 8 rows is a count, not a forecast. `final` counts a later approval as approved.")
    lines.append("")
    lines.append("## Sensitivities")
    lines.append("")
    lines.append("All pivotal votes (not only approval/benefit-risk questions), the 1-year FDA action on the same kept factor sets, and a linear meeting-year term on those sets. Year is centered at 2020 and predicted at 2026. These rows are not in the range above.")
    lines.append("")
    lines.append("| Screen | Factors | CNS | n | Nagelkerke R2 | AIC | P |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    sens = pred[pred.screen.str.startswith("sensitivity")]
    for _, r in sens.iterrows():
        lines.append(f"| {r.screen} | {r.factors} | {int(r.cns)} | {int(r.n)} | {fmt3(r.nagelkerke)} | {fmt1(r.aic)} | {fmt(r.p)} |")
    lines.append("")
    if year_notes:
        lines.append("Year term versus the same model without it (AIC; lower is better):")
        lines.append("")
        for label, factors, aic0, aic1, nag, stable in year_notes:
            lines.append(f"- {label}, {factors}: AIC {aic0:.1f} without year, {aic1:.1f} with year (Nagelkerke {nag:.3f}, stable={stable}).")
        lines.append("")
    lines.append("Sources for the AMT-130 vector: orphan, OOPD 525216 in `oopd_all.csv`; priority review, uniQure releases of 2 Nov 2026 and 4 Nov 2026 (company, secondary) until an FDA letter is in hand.")
    open(os.path.join("amt130_prediction.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    drop_cols = ("b_pen", "b_unpen", "cols", "raw", "ll")
    for name, sc in [
        ("amt130_screen_favourable.csv", fav_sc),
        ("amt130_screen_approval.csv", app_sc),
        ("amt130_screen_approval_given_vote.csv", app_v),
        ("amt130_screen_allpivotal_favourable.csv", piv_fav_sc),
        ("amt130_screen_allpivotal_approval.csv", piv_app_sc),
    ]:
        sc.drop(columns=[c for c in sc.columns if c in drop_cols], errors="ignore").to_csv(name, index=False)
    print("wrote amt130_prediction.md")
    print(pred[pred.cns == 0][["screen", "factors", "nagelkerke", "p", "stratum_n"]].to_string(index=False))


if __name__ == "__main__":
    main()
