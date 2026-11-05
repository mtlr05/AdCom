"""One-at-a-time factor screen, then a joint model, on the approval questions.

Run from data/ with scripts/ on PYTHONPATH. Does not edit the pivotal CSV.

Each one-at-a-time fit drops a meeting only when that factor is unrecorded.
The joint model is orphan status plus cell and gene therapy, the candidate
named for this report, fit on the meetings that record both. A wider joint
model of every factor is written beside it so the comparison is visible.
Significance one at a time is Fisher's exact test. The effect size is the
penalized log-odds. The correlation is the phi coefficient.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy.stats import beta as beta_dist
from scipy.stats import chi2
from scipy.stats import fisher_exact

from amt130_predict import (
    boot_pred,
    fit_logit,
    gate,
    predict_row,
    prepare,
    r2,
    refit,
    stratum_beta,
)

CHART = os.environ.get("CHART_DIR", "charts")
B = 400
SEED = 130

# Display order. Column in the prepared frame, short key, axis label.
FACTORS = [
    ("orphan_y", "orphan", "Orphan status"),
    ("cgt", "CGT", "Cell and gene therapy"),
    ("pri", "priority", "Priority review"),
    ("cber_i", "cber", "Biologics center"),
    ("cns", "CNS", "Neurology committees"),
    ("init_i", "initial", "Initial application"),
]
JOINT = ["orphan", "CGT"]
COL = {key: col for col, key, _ in FACTORS}
LABEL = {key: lab for _, key, lab in FACTORS}


def fisher_row(x, y):
    """2x2 of factor (rows) by outcome (columns). Returns counts and Fisher p."""
    a = int(((x == 1) & (y == 1)).sum())
    b = int(((x == 1) & (y == 0)).sum())
    c = int(((x == 0) & (y == 1)).sum())
    d = int(((x == 0) & (y == 0)).sum())
    # Table columns are the outcome, so the odds ratio is the factor's.
    oddsratio, p = fisher_exact([[a, b], [c, d]], alternative="two-sided")
    return dict(yes_event=a, yes_n=a + b, no_event=c, no_n=c + d, odds_ratio=float(oddsratio), fisher_p=float(p))


def phi_of(x, y):
    if len(x) < 3 or len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def one(df, col, y):
    use = df.dropna(subset=[col, y]).copy()
    x = use[col].to_numpy(float)
    yy = use[y].to_numpy(float)
    counts = fisher_row(x, yy)
    X = np.column_stack([np.ones(len(use)), x])
    b_p, ll_p, _ = fit_logit(X, yy, True)
    b_u, ll_u, stable = fit_logit(X, yy, False)
    _, ll0, _ = fit_logit(np.ones((len(yy), 1)), yy, False)
    nag, mcf = r2(ll_u if stable else ll_p, ll0, len(yy))
    lr = 2 * (ll_u - ll0) if stable else float("nan")
    lr_p = float(chi2.sf(lr, 1)) if stable and lr == lr else float("nan")
    aic = (-2 * ll_u + 2 * 2) if stable else float("nan")
    aic0 = -2 * ll0 + 2 * 1
    return dict(
        n=int(len(use)), events=int(yy.sum()),
        phi=phi_of(x, yy),
        log_odds=float(b_p[1]), intercept=float(b_p[0]),
        log_odds_unpen=float(b_u[1]) if stable else float("nan"),
        stable=bool(stable), nagelkerke=float(nag), mcfadden=float(mcf),
        aic=float(aic) if aic == aic else float("nan"),
        aic_null=float(aic0), lr=float(lr) if lr == lr else float("nan"), lr_p=lr_p,
        **counts,
    )


def joint_fit(df, keys, y):
    cols = [COL[k] for k in keys]
    use = df.dropna(subset=cols + [y]).copy()
    X = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in cols])
    yy = use[y].to_numpy(float)
    b_p, ll_p, _ = fit_logit(X, yy, True)
    b_u, ll_u, stable = fit_logit(X, yy, False)
    _, ll0, _ = fit_logit(np.ones((len(yy), 1)), yy, False)
    nag, mcf = r2(ll_u if stable else ll_p, ll0, len(yy))
    k = X.shape[1]
    aic = -2 * (ll_u if stable else ll_p) + 2 * k
    out = dict(
        n=int(len(use)), events=int(yy.sum()), factors="+".join(keys),
        stable=bool(stable), nagelkerke=float(nag), mcfadden=float(mcf),
        aic=float(aic), ll=float(ll_u if stable else ll_p),
        intercept=float(b_p[0]),
        log_odds={key: float(b_p[i + 1]) for i, key in enumerate(keys)},
        log_odds_unpen={key: (float(b_u[i + 1]) if stable else float("nan")) for i, key in enumerate(keys)},
    )
    # Drop-one likelihood-ratio against the unpenalized fit, only when both fits are stable.
    drops = {}
    for i, key in enumerate(keys):
        keep = [c for j, c in enumerate(cols) if j != i]
        Xr = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in keep]) if keep else np.ones((len(use), 1))
        _, ll_r, stable_r = fit_logit(Xr, yy, False)
        if stable and stable_r:
            stat = 2 * (ll_u - ll_r)
            drops[key] = dict(lr=float(stat), p=float(chi2.sf(stat, 1)), stable=True)
        else:
            drops[key] = dict(lr=float("nan"), p=float("nan"), stable=False)
    out["drop"] = drops
    return out


def boot_coefs(df, keys, y, B=B):
    cols = [COL[k] for k in keys]
    use = df.dropna(subset=cols + [y])
    X = np.column_stack([np.ones(len(use))] + [use[c].to_numpy(float) for c in cols])
    yy = use[y].to_numpy(float)
    rng = np.random.default_rng(SEED)
    got = []
    n = len(yy)
    for _ in range(B):
        ix = rng.integers(0, n, n)
        if len(np.unique(yy[ix])) < 2:
            continue
        if X.shape[1] > 1 and any(len(np.unique(X[ix, j])) < 2 for j in range(1, X.shape[1])):
            continue
        b, _, _ = fit_logit(X[ix], yy[ix], True)
        got.append(b[1:])
    arr = np.array(got) if got else np.empty((0, len(keys)))
    lo = np.quantile(arr, 0.025, axis=0) if len(arr) >= 50 else [float("nan")] * len(keys)
    hi = np.quantile(arr, 0.975, axis=0) if len(arr) >= 50 else [float("nan")] * len(keys)
    return {key: (float(lo[i]), float(hi[i]), int(len(arr))) for i, key in enumerate(keys)}


def jeffreys(k, n):
    if n <= 0:
        return float("nan"), float("nan"), float("nan")
    lo, med, hi = beta_dist.ppf([0.025, 0.5, 0.975], 0.5 + k, 0.5 + n - k)
    return float(med), float(lo), float(hi)


def screen_frame(df, y):
    rows = []
    for col, key, lab in FACTORS:
        rec = one(df, col, y)
        rec.update(factor=key, label=lab, outcome=y)
        alone_ci = boot_coefs(df, [key], y)
        rec["boot_lo"], rec["boot_hi"], rec["boot_n"] = alone_ci[key]
        rows.append(rec)
    return rows


def conditional_fisher(df, y):
    """Exact tests that do not need a separated likelihood.

    Cell and gene therapy occurs inside the orphan rows, so its incremental
    test is Fisher among orphan products. Orphan status does not vary inside
    the cell-and-gene-therapy rows when those rows are all orphan, so its
    incremental test is Fisher among the other rows.
    """
    out = {}
    sub = df.dropna(subset=["orphan_y", "cgt", y])
    orphan = sub[sub.orphan_y == 1]
    rest = sub[sub.cgt == 0]
    out["cgt_among_orphan"] = fisher_row(orphan.cgt.to_numpy(float), orphan[y].to_numpy(float))
    out["cgt_among_orphan"]["n"] = int(len(orphan))
    out["orphan_among_non_cgt"] = fisher_row(rest.orphan_y.to_numpy(float), rest[y].to_numpy(float))
    out["orphan_among_non_cgt"]["n"] = int(len(rest))
    both = sub[(sub.orphan_y == 1) & (sub.cgt == 1)]
    out["both_n"] = int(len(both))
    out["both_events"] = int(both[y].sum()) if len(both) else 0
    out["cgt_not_orphan"] = int(((sub.cgt == 1) & (sub.orphan_y == 0)).sum())
    out["cgt_and_cber"] = int(((sub.cgt == 1) & (sub.cber_i == 1)).sum())
    out["cgt_and_cns"] = int(((sub.cgt == 1) & (sub.cns == 1)).sum())
    out["cgt_n"] = int((sub.cgt == 1).sum())
    return out


def prediction_block(df, y, keys):
    fit = refit(df, keys, y, False)
    lo, hi = boot_pred(df, keys, y, False, 0, None)
    n, k, med, blo, bhi = stratum_beta(df, keys, y, 0, None)
    p = predict_row(fit["b_pen"], keys, False, 0, None) if fit and fit["stable"] or (fit and np.all(np.abs(fit["b_pen"]) < 8)) else float("nan")
    # predict_row is the penalized probability even when the unpenalized fit separates.
    if fit is not None:
        p = predict_row(fit["b_pen"], keys, False, 0, None)
    return dict(p=p, boot_lo=lo, boot_hi=hi, stratum_n=n, stratum_k=k,
                stratum_med=med, stratum_lo=blo, stratum_hi=bhi,
                n=None if fit is None else fit["n"], r2=None if fit is None else fit["nagelkerke"],
                aic=None if fit is None else fit["aic"], stable=None if fit is None else fit["stable"])


def vote_conditional(df, y):
    """Approval given the vote, with and without the two factors."""
    rows = {}
    for keys in ([], ["orphan", "CGT"]):
        fit = refit(df, keys, y, True)
        if fit is None:
            continue
        rec = dict(n=fit["n"], r2=fit["nagelkerke"], aic=fit["aic"], stable=fit["stable"])
        for vote, name in ((1, "favourable"), (0, "unfavourable")):
            rec[name] = predict_row(fit["b_pen"], keys, True, 0, vote)
            lo, hi = boot_pred(df, keys, y, True, 0, vote)
            rec[name + "_lo"] = lo
            rec[name + "_hi"] = hi
            n, k, med, blo, bhi = stratum_beta(df, keys, y, 0, vote)
            rec[name + "_stratum"] = dict(n=n, k=k, med=med, lo=blo, hi=bhi)
        rows["+".join(keys) or "(vote only)"] = rec
    return rows


def main():
    m = prepare(pd.read_csv("adcom_full_pivotal.csv", dtype=str).fillna(""))
    gate(m, pd.read_csv("two_by_two.csv"))
    base = m[(~m.replaced) & m.fav.notna()].copy()
    appr = base[base.vote_type == "approval/benefit-risk"].copy()
    known = appr[appr.approved.notna()].copy()
    known["y_app"] = known.approved.astype(float)
    known["y_fav"] = known.fav

    payload = {}
    payload["n_approval"] = int(len(appr))
    payload["n_known"] = int(len(known))
    payload["vote_tiers"] = appr.vote_source_tier.value_counts().to_dict()
    payload["outcome_tiers"] = known.outcome_source_tier.value_counts().to_dict()
    payload["base_fav"] = dict(n=int(len(known)), k=int(known.y_fav.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(known.y_fav.sum()), int(len(known))))))
    payload["base_app"] = dict(n=int(len(known)), k=int(known.y_app.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(known.y_app.sum()), int(len(known))))))
    fav_yes = known[known.y_fav == 1]
    fav_no = known[known.y_fav == 0]
    payload["app_given_fav"] = dict(n=int(len(fav_yes)), k=int(fav_yes.y_app.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(fav_yes.y_app.sum()), int(len(fav_yes))))))
    payload["app_given_unfav"] = dict(n=int(len(fav_no)), k=int(fav_no.y_app.sum()), **dict(zip(
        ("med", "lo", "hi"), jeffreys(int(fav_no.y_app.sum()), int(len(fav_no))))))

    screens = {}
    joints = {}
    conds = {}
    boots = {}
    preds = {}
    for y, name in (("y_fav", "favourable"), ("y_app", "approval")):
        screens[name] = screen_frame(known, y)
        joints[name] = {
            "two": joint_fit(known, JOINT, y),
            "five": joint_fit(known, ["orphan", "CGT", "CNS", "cber", "initial"], y),
            "six": joint_fit(known, ["orphan", "priority", "CGT", "CNS", "cber", "initial"], y),
        }
        # One-at-a-time log-odds refit on the joint sample, so the comparison
        # of coefficients is not only a comparison of who was dropped.
        two_cols = [COL[k] for k in JOINT]
        same = known.dropna(subset=two_cols + [y])
        joints[name]["alone_on_joint_sample"] = {key: one(same, COL[key], y) for key in JOINT}
        conds[name] = conditional_fisher(known, y)
        boots[name] = boot_coefs(known, JOINT, y)
        preds[name] = {
            "orphan": prediction_block(known, y, ["orphan"]),
            "two": prediction_block(known, y, JOINT),
            "intercept": prediction_block(known, y, []),
        }
    payload["screens"] = screens
    payload["joints"] = joints
    payload["conditional"] = conds
    payload["joint_boot"] = boots
    payload["predictions"] = preds
    payload["vote_conditional"] = vote_conditional(known, "y_app")

    # One-year action, same two-factor model.
    idx = known[known.index_approved.notna()].copy()
    idx["y_idx"] = idx.index_approved.astype(float)
    payload["one_year"] = dict(
        n=int(len(idx)), k=int(idx.y_idx.sum()),
        screen=screen_frame(idx, "y_idx"),
        two=joint_fit(idx, JOINT, "y_idx"),
        pred_orphan=prediction_block(idx, "y_idx", ["orphan"]),
        pred_two=prediction_block(idx, "y_idx", JOINT),
        conditional=conditional_fisher(idx, "y_idx"),
    )
    both = known.dropna(subset=["index_approved"])
    payload["label_disagree"] = dict(
        n=int(len(both)),
        disagree=int((both.approved.astype(bool) != both.index_approved.astype(bool)).sum()),
    )

    # All pivotal votes, as a sensitivity. Same rule.
    piv = base[base.approved.notna()].copy()
    piv["y_app"] = piv.approved.astype(float)
    piv["y_fav"] = piv.fav
    payload["all_pivotal"] = {}
    for y, name in (("y_fav", "favourable"), ("y_app", "approval")):
        payload["all_pivotal"][name] = dict(
            n=int(len(piv.dropna(subset=[y]))),
            screen=screen_frame(piv, y),
            two=joint_fit(piv, JOINT, y),
            conditional=conditional_fisher(piv, y),
            pred_two=prediction_block(piv, y, JOINT),
        )

    # Year term on the two-factor model.
    year_notes = {}
    for y, name in (("y_fav", "favourable"), ("y_app", "approval")):
        base_fit = refit(known, JOINT, y, False)
        yr_fit = refit(known, JOINT, y, False, extra=("year_c",))
        year_notes[name] = dict(
            aic=None if base_fit is None else base_fit["aic"],
            aic_year=None if yr_fit is None else yr_fit["aic"],
            r2_year=None if yr_fit is None else yr_fit["nagelkerke"],
            stable=None if yr_fit is None else yr_fit["stable"],
        )
    payload["year"] = year_notes

    # Name the meetings in the orphan and cell-and-gene-therapy cell.
    cell = known.dropna(subset=["orphan_y", "cgt"])
    cell = cell[(cell.orphan_y == 1) & (cell.cgt == 1)]
    names = []
    for _, r in cell.sort_values("meeting_date").iterrows():
        label = r.brand or r.generic or r.product_text
        names.append(dict(
            date=r.meeting_date, committee=r.committee, app=r.app, name=label,
            vote=r.adcom, yes=r.vote_yes, no=r.vote_no, final=r.final_action,
            priority=r.review_priority, vote_tier=r.vote_source_tier, outcome_tier=r.outcome_source_tier,
        ))
    payload["cgt_orphan_rows"] = names

    # Priority missingness composition, for the discussion.
    miss = known[known.pri.isna()]
    payload["priority_missing"] = dict(
        n=int(len(miss)),
        favourable=int(miss.y_fav.sum()),
        approved=int(miss.y_app.sum()),
        orphan=int((miss.orphan_y == 1).sum()),
        orphan_recorded=int(miss.orphan_y.notna().sum()),
        cgt=int((miss.cgt == 1).sum()),
        cns=int((miss.cns == 1).sum()),
        cber=int((miss.cber_i == 1).sum()),
        initial=int((miss.init_i == 1).sum()),
    )

    def conv(o):
        if isinstance(o, dict):
            return {k: conv(v) for k, v in o.items()}
        if isinstance(o, list):
            return [conv(v) for v in o]
        if isinstance(o, (np.floating, float)):
            if o != o or np.isinf(o):
                return None
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return o

    clean = conv(payload)
    with open("amt130_factor_compare.json", "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)

    flat = []
    for name, rows in screens.items():
        for r in rows:
            flat.append(dict(outcome=name, **{k: r[k] for k in r if k != "outcome"}))
    pd.DataFrame(flat).to_csv("amt130_one_at_a_time.csv", index=False)

    draw(screens, joints, boots)
    print("wrote amt130_factor_compare.json")
    brief(clean)


def draw(screens, joints, boots):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    order = [key for _, key, _ in FACTORS]
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.15), sharey=True)
    titles = {"favourable": "Favourable vote", "approval": "FDA approval"}
    for ax, name in zip(axes, ("favourable", "approval")):
        by = {r["factor"]: r for r in screens[name]}
        joint = joints[name]["two"]["log_odds"]
        jboot = boots[name]
        ypos = np.arange(len(order))[::-1]
        ax.axvline(0, color="0.75", lw=0.8, zorder=0)
        for y, key in zip(ypos, order):
            r = by[key]
            ax.plot([r["boot_lo"], r["boot_hi"]], [y, y], color="0.45", lw=1.2, zorder=1)
            ax.plot(r["log_odds"], y, "o", color="0.1", ms=6, zorder=2)
            if key in joint:
                lo, hi, _ = jboot[key]
                ax.plot([lo, hi], [y - 0.18, y - 0.18], color="0.15", lw=1.2, zorder=1)
                ax.plot(joint[key], y - 0.18, "s", color="white", markeredgecolor="0.1",
                        markeredgewidth=1.1, ms=6, zorder=3)
        ax.set_yticks(ypos)
        ax.set_yticklabels([
            f"{LABEL[key]}  ({by[key]['n']})" for key in order
        ], fontsize=8)
        ax.set_xlabel("Penalized log-odds", fontsize=9)
        ax.set_title(titles[name], fontsize=11)
        ax.set_xlim(-1.6, 2.4)
        ax.tick_params(axis="x", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="0.1", markeredgecolor="0.1",
               ms=6, label="One factor at a time"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor="white", markeredgecolor="0.1",
               markeredgewidth=1.1, ms=6, label="In the two-factor model"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    os.makedirs(CHART, exist_ok=True)
    path = os.path.join(CHART, "amt130_factor_compare.png")
    fig.savefig(path, dpi=150)
    plt.close()
    print("wrote", path)


def brief(p):
    def f(x, nd=2):
        if x is None:
            return "NA"
        return f"{x:.{nd}f}"

    print("--- base", p["base_fav"]["k"], "/", p["base_fav"]["n"], p["base_app"]["k"], "/", p["base_app"]["n"])
    for name in ("favourable", "approval"):
        print("==", name)
        for r in p["screens"][name]:
            print(f"  {r['factor']:10} n={r['n']:3} yes {r['yes_event']}/{r['yes_n']} no {r['no_event']}/{r['no_n']} "
                  f"phi={f(r['phi'], 3)} b={f(r['log_odds'])} boot {f(r['boot_lo'])}-{f(r['boot_hi'])} "
                  f"fisher={f(r['fisher_p'], 4)} stable={r['stable']} lr_p={f(r['lr_p'], 4)} R2={f(r['nagelkerke'], 3)}")
        two = p["joints"][name]["two"]
        print("  JOINT", two["n"], "stable", two["stable"], "R2", f(two["nagelkerke"], 3), "AIC", f(two["aic"], 1),
              "b", {k: f(v) for k, v in two["log_odds"].items()}, "drop", two["drop"])
        five = p["joints"][name]["five"]
        print("  FIVE stable", five["stable"], "R2", f(five["nagelkerke"], 3), "b", {k: f(v) for k, v in five["log_odds"].items()})
        six = p["joints"][name]["six"]
        print("  SIX n", six["n"], "stable", six["stable"], "R2", f(six["nagelkerke"], 3),
              "b", {k: f(v) for k, v in six["log_odds"].items()})
        c = p["conditional"][name]
        print("  CGT|orphan", c["cgt_among_orphan"])
        print("  orphan|nonCGT", c["orphan_among_non_cgt"], "cgt_not_orphan", c["cgt_not_orphan"],
              "both", c["both_events"], "/", c["both_n"])
        pr = p["predictions"][name]
        print("  PRED orphan", {k: f(pr["orphan"][k]) if isinstance(pr["orphan"][k], float) else pr["orphan"][k] for k in ("p", "boot_lo", "boot_hi", "stratum_n", "stratum_k", "stratum_lo", "stratum_hi", "r2", "aic", "stable")})
        print("  PRED two", {k: f(pr["two"][k]) if isinstance(pr["two"][k], float) else pr["two"][k] for k in ("p", "boot_lo", "boot_hi", "stratum_n", "stratum_k", "stratum_lo", "stratum_hi", "r2", "aic", "stable")})
        same = p["joints"][name]["alone_on_joint_sample"]
        print("  ALONE on joint n", {k: (v["n"], f(v["log_odds"]), f(v["fisher_p"], 4)) for k, v in same.items()})
    print("vote conditional", json.dumps(p["vote_conditional"], default=str)[:2000])
    print("priority missing", p["priority_missing"])
    print("disagree", p["label_disagree"])
    print("year", p["year"])
    print("one year n", p["one_year"]["n"], p["one_year"]["k"], "two", p["one_year"]["two"]["log_odds"],
          "pred", p["one_year"]["pred_two"]["p"], p["one_year"]["pred_orphan"]["p"])
    print("tiers", p["vote_tiers"], p["outcome_tiers"])
    print("CGT rows:")
    for row in p["cgt_orphan_rows"]:
        print(" ", row)
    print("all pivotal fisher:")
    for name in ("favourable", "approval"):
        block = p["all_pivotal"][name]
        print(" ", name, "n", block["n"], "two", block["two"]["log_odds"], "stable", block["two"]["stable"],
              "pred", block["pred_two"]["p"], "cond", block["conditional"]["cgt_among_orphan"]["fisher_p"],
              block["conditional"]["orphan_among_non_cgt"]["fisher_p"])
        for r in block["screen"]:
            print(f"    {r['factor']:10} {r['yes_event']}/{r['yes_n']} vs {r['no_event']}/{r['no_n']} p={r['fisher_p']:.4f} b={r['log_odds']:.2f} phi={r['phi']:.3f}")


if __name__ == "__main__":
    main()
